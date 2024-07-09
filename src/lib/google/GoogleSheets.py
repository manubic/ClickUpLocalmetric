from googleapiclient.discovery import build



class Sheets:
    def __init__(self, _id: str, creds) -> None:
        self.__sample_spreadsheet_id: str = _id
        self.creds = creds
        self.__service = build("sheets", "v4", credentials = creds)

    def getAllRows(self, sheet_name: str) -> list[list[str]]:
        sheet = self.__service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=self.__sample_spreadsheet_id, range=f'{sheet_name}!A:ZZ')
            .execute()
        )
        values: list[str|int] = result.get("values", [])
        return values

    def getSheets(self, resFormat = list) -> set[str] | list[str]:
        service = build("sheets", "v4", credentials=self.creds)
        sheets = service.spreadsheets().get(spreadsheetId=self.__sample_spreadsheet_id).execute().get('sheets', '')
        return resFormat(sheet['properties']['title'] for sheet in sheets)