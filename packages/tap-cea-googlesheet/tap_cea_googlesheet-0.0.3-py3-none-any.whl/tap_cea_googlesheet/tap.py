"""googlesheet tap class."""
from typing import List
from singer_sdk import Tap, Stream
from singer_sdk import typing as th
# JSON schema typing helpers
from tap_cea_googlesheet.client import request, generate_streams_data
from tap_cea_googlesheet.streams import (
    SheetStream, SheetMetaDataStream
)

NoneType = type(None)


class Tapgooglesheet(Tap):
    """googlesheet tap class."""
    name = "tap-googlesheet"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "client_id",
            th.StringType,
            required=True,
            description="The client id generated from credentials"
        ),
        th.Property(
            "client_secret",
            th.StringType,
            required=True,
            description="The client secret from google auth"
        ),
        th.Property(
            "spreadsheet_id",
            th.StringType,
            required=True,
            description="The id of the spreadsheet to read"
        ),
        th.Property(
            "scopes",
            th.ArrayType(
                th.StringType
            ),
            description="Default scopes defined",
            default=[
                'https://www.googleapis.com/auth/drive.readonly',
                'https://www.googleapis.com/auth/drive.metadata.readonly',
                'https://www.googleapis.com/auth/drive.file',
                'https://www.googleapis.com/auth/spreadsheets.readonly']
        ),
        th.Property(
            "sheet_ranges",
            th.ArrayType(
                th.StringType
            ),
            description='''Specific ranges to be read in the format
            SHEETNAME!A1:B2 where A1:B2 is the range choice''',
        ),
        th.Property(
            "auth_uri",
            th.StringType,
            description="google authorization url",
            default="https://accounts.google.com/o/oauth2/auth"
        ),
        th.Property(
            "token_uri",
            th.StringType,
            description="google token generation url",
            default="https://oauth2.googleapis.com/token"
        ),
        th.Property(
            "auth_provider",
            th.StringType,
            default="https://www.googleapis.com/oauth2/v1/certs"
        )

    ).to_dict()
    
    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        streams_data = generate_streams_data(self.config)
        dynamic_streams = [SheetStream(
            tap=self, stream_data=stream_data, request=request) for stream_data in streams_data]
        return [*dynamic_streams, SheetMetaDataStream(tap=self, request=request)]

