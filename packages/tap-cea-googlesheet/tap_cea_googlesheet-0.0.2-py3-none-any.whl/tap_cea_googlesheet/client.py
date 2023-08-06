"""Custom client handling, including googlesheetStream base class."""
from collections import OrderedDict
from typing import List, Union
import os
import singer
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

NoneType = type(None)
LOGGER = singer.get_logger()


def request(config, stream_name, **kwargs) -> dict:
    """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
    """
    creds = None
    client_id = config["client_id"]
    client_secret = config['client_secret']
    credentials = {
        "scopes": config["scopes"],
            "spreadsheet_id": config["spreadsheet_id"],
            "installed": {
                "client_id": client_id,
                "project_id": "",
                "auth_uri": config["auth_uri"],
                "token_uri": config["token_uri"],
                "auth_provider_x509_cert_url": config["auth_provider"],
                "client_secret": client_secret}
        }

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json", credentials["scopes"])

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(
                credentials, credentials["scopes"])
            creds = flow.run_local_server(port=0,authorization_prompt_message="")
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    drive_service = build('drive', 'v3', credentials=creds)
    spreadsheet = drive_service.files().copy(fileId=credentials["spreadsheet_id"], body={
        'mimeType': "application/vnd.google-apps.spreadsheet"}).execute()
    service = build('sheets', 'v4', credentials=creds)
    # Call the Sheets API
    sheet = service.spreadsheets()
    if stream_name =="sheets":
        requested = service.spreadsheets().values().batchGet(
                spreadsheetId=spreadsheet["id"],
                ranges=kwargs["ranges"],
                valueRenderOption=kwargs["valueRenderOption"],
                dateTimeRenderOption=kwargs["dateRenderOption"]
            )
    else:
        requested = sheet.get(
            spreadsheetId=spreadsheet["id"],
            ranges=kwargs["ranges"],
            includeGridData=kwargs["includeOption"]
        )
    response = requested.execute()
    return response


def generate_streams_data(config) -> List[dict] :
    '''
    generates the various stream data used to dynamically
    create streams for each sheet
    '''
    stream_data = []
    range_value = config.get("sheet_ranges")
    spreadsheet_metadata = request(
        config, "sheets_metadata", ranges=range_value,
        includeOption=True)
    sheets = spreadsheet_metadata.get('sheets')
    if sheets:
        for sheet in sheets:
            sheet_title = sheet.get('properties', {}).get('title')
            LOGGER.info('sheet_title = {}'.format(sheet_title))
            try:
                result = get_sheet_schema(sheet, sheet_title)
                if result is not None:
                    schema = {"type": "object", "properties": dict(result)}
                    data = {"schema": schema, "name": sheet_title,
                            "primary_keys": list(result.keys())[0] }
                    stream_data.append(data)
            except NotImplementedError  as error:
                LOGGER.warning('{}'.format(error))
                LOGGER.warning('SKIPPING Malformed sheet: {}'.format(sheet_title))
    return stream_data


def get_sheet_schema(sheet, sheet_title) -> Union[dict, NoneType]:
    '''
     Get the schema for each sheet
    '''
    data = next(iter(sheet.get('data', [])), {})
    row_data = data.get('rowData', [])
    # if the row is empty, or if there is either no header or no initial value
    # when length is 1 we cant determine either the column name or the columnType
    if row_data == [] or row_data[0] == {}:
        LOGGER.info(
            "Skipping sheet, unable to generate sheet schema:{}".format(sheet_title))
        return None

    if len(row_data) == 1:
        # if there is only one row, invert the row to column
        row_data.append({"values": row_data[0]["values"][1:]})
        row_data[0]["values"] = [row_data[0]["values"][0]]

    sheet_schema = OrderedDict()
    # Used To determine schema based on column name

    headers = row_data[0].get('values', [])
    # Used To determine type of data
    first_values = row_data[1].get('values', [])
    headers_list = []

    for i, header in enumerate(headers):
        header_val = header.get('formattedValue')
        if header_val:
            try:
                column_name = str(header_val)
                # Having the same name for two different columns affects the schema creation.
                if column_name in headers_list:
                    column_name = '{}_{}'.format(column_name, i)
                headers_list.append(column_name)
                column_property = evaluate_type(
                    first_values[i], sheet_title, column_name)
            except IndexError as error:
                LOGGER.warning('NO VALUE IN 2ND ROW FOR HEADER. SHEET: {}, COL: {}, {}'.format(
                    sheet_title, column_name, error))
                first_values.append({})
        else:
            LOGGER.info('WARNING: SKIPPED COLUMN; NO COLUMN HEADER. SHEET: {}, COL: {} '.format(
                sheet_title, i))
        sheet_schema[column_name] = column_property
    return sheet_schema


def evaluate_type(value, sheet_title, column_name) -> dict:
    '''
        Evaluates the data type for each sheet property and
        returns the types to get_sheet_schema
    '''
    col_property = None
    column_effective_val = value.get('effectiveValue', {})
    if column_effective_val == {}:
        column_effective_type = 'stringValue'
    else:
        column_effective_type = list(column_effective_val.keys())[0]
    if column_effective_type in ("errorType", 'formulaType'):
        raise TypeError("Error in dataType of second row value; SHEET:{}, COL:{}, Type:{}".format(
            sheet_title, column_name, column_effective_type
        ))
    if column_effective_type == "numberValue":
        number_format = value.get("effectiveFormat", {}).get(
            "numberFormat", {}).get('type')
        if number_format in ("DATE_TIME", "DATE", "TIME"):
            col_property = {
                'type': 'string',
                'format': number_format.lower()
            }
        elif number_format == 'TEXT':
            col_property = {'type': 'string'}

        else:
            col_property = {'type': 'number', 'multipleOf': 1e-15}
    else:
        col_property = {'type': 'string'}
    return col_property
