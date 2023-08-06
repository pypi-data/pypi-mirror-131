"""Stream type classes for tap-googlesheet."""
from pathlib import Path
from typing import Optional, Iterable

import singer
from singer_sdk.streams import Stream


LOGGER = singer.get_logger()

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class SheetStream(Stream):
    """Dynamic stream for creating a sheet stream based on the number of sheets available."""

    def __init__(self, tap, stream_data, request):
        self.stream = stream_data
        self.request = request
        super().__init__(tap)
        self.range_values = self.config.get("sheet_ranges")
        self.primary_keys = self.stream["primary_keys"]
    replication_method = "FULL_TABLE"

    @property
    def schema(self):
        '''
        Get the sheetstream property schema
        '''
        return self.stream["schema"]

    @property
    def name(self):
        '''
        Get the property name
        '''
        return self.stream["name"]

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        """Return a generator of row-type dictionary objects.

        The optional `context` argument is used to identify a specific slice of the
        stream if partitioning is required for the stream. Most implementations do not
        require partitioning and should ignore the `context` argument.
        """
        rows = []
        ranges = f'{self.name}!A1:Z100'

        if self.range_values is not None:
            for sheet_range in self.range_values:
                sheet_name = sheet_range.split("!")[0]
                if sheet_name.lower() == self.name.lower():
                    ranges = sheet_range

        get_columns_and_values = self.request(
            self.config, "sheets", ranges=ranges, valueRenderOption="UNFORMATTED_VALUE",
            dateRenderOption="FORMATTED_STRING").get("valueRanges")[0]

        values = get_columns_and_values["values"]

        if len(values) == 1:
            data_keys = [values[0][0]]
            data_values = [values[0][1:]]
        else:
            data_keys = values[0]
            data_values = values[1:]

        for row in data_values:
            value = dict(zip(data_keys, row))
            rows.append(value)
        for row in rows:
            yield row


class SheetMetaDataStream(Stream):
    '''
     Stream for Meta data resulting from calling google sheet api
    '''

    def __init__(self, tap, request) -> None:
        self.request = request
        super().__init__(tap)
    name = "SheetMetadata"
    primary_keys = ["spreadsheetId", "sheetId"]
    replication_method = "FULL_TABLE"
    schema_filepath = SCHEMAS_DIR / "schema_metadata.json"

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        """Return a generator of row-type dictionary objects.

        The optional `context` argument is used to identify a specific slice of the
        stream if partitioning is required for the stream. Most implementations do not
        require partitioning and should ignore the `context` argument.
        """
        rows = []
        get_columns_and_values = self.request(
            self.config, "sheets_metadata",ranges=None, includeOption=False)
        for sheet in get_columns_and_values.get('sheets'):
            properties = sheet.get("properties")
            rows.append({
                "spreadsheetId": get_columns_and_values["spreadsheetId"],
                "spreadsheetUrl": get_columns_and_values["spreadsheetUrl"],
                "sheet": {
                    "sheetId": properties["sheetId"],
                    "title": properties["title"],
                    "index": properties["index"],
                    "sheetType": properties["sheetType"]
                }
            })
        for row in rows:
            yield row
