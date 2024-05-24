import gspread
from google.oauth2.service_account import Credentials

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)  # type: ignore


class GoogleSheet:

    def __init__(self, sheet_id):
        self.sheet_id = sheet_id

    def _get_worksheet(self, worksheet):
        """Get the worksheet object for the specified sheet name."""
        workbook = client.open_by_key(self.sheet_id)
        return workbook.worksheet(worksheet)

    def update_cell(self, worksheet: str, cell: str, value: str) -> None:
        """
        Update a cell in the specified worksheet with the given value.

        Args:
            worksheet (str): The name of the worksheet to update.
            cell (str): The address of the cell to update.
            value (str): The new value to set in the cell.

        Returns:
            None
        """
        worksheet = self._get_worksheet(worksheet)  # type: ignore
        worksheet.update_acell(cell, value)  # type: ignore

    """
    def update_cell(self, worksheet, cell, value) -> None:
        workbook = client.open_by_key(self.sheet_id)
        worksheet = workbook.worksheet(worksheet)
        worksheet.update_acell(cell, value)
    """

    def get_cell(self, worksheet, cell):
        workbook = client.open_by_key(self.sheet_id)
        worksheet = workbook.worksheet(worksheet)
        return worksheet.acell(cell).value

    def get_row(self, worksheet, row):
        workbook = client.open_by_key(self.sheet_id)
        worksheet = workbook.worksheet(worksheet)
        return worksheet.row_values(row)

    def get_col(self, worksheet, row):
        workbook = client.open_by_key(self.sheet_id)
        worksheet = workbook.worksheet(worksheet)
        return worksheet.col_values(row)

    def get_all_as_list(self, worksheet):
        workbook = client.open_by_key(self.sheet_id)
        worksheet = workbook.worksheet(worksheet)
        return worksheet.get_all_values()

    def get_all_as_dict(self, worksheet):
        workbook = client.open_by_key(self.sheet_id)
        worksheet = workbook.worksheet(worksheet)
        return worksheet.get_all_records()


if __name__ == "__main__":
    sheet = GoogleSheet("1kSu1qAPryfFvxp7znMQHTvP0R83ZWqTd9mpJQOjFUQg")
    sheet.update_cell("data", "A1", "Hello")
