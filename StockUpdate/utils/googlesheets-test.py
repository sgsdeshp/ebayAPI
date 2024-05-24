"""A class for interacting with Google Sheets."""

from typing import Any, Dict, List, Union

import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)  # type: ignore


class GoogleSheet:
    def __init__(self, sheet_id: str):
        self.sheet_id = sheet_id

    def _get_worksheet(self, worksheet: str) -> Union[gspread.models.Worksheet, None]:
        """(Private method) Get the worksheet object for the specified sheet name."""
        try:
            workbook = client.open_by_key(self.sheet_id)
            return workbook.worksheet(worksheet)
        except gspread.exceptions.WorksheetNotFound:
            print(f"Worksheet {worksheet} not found.")
            return None

    def update_cell(self, worksheet: str, cell: str, value: Any) -> None:
        """
        Update a cell in the specified worksheet with the given value.

        Args:
            worksheet (str): The name of the worksheet to update.
            cell (str): The address of the cell to update. Eg.: A1.
            value (Any): The new value to set in the cell.

        Returns:
            None
        """
        worksheet_obj = self._get_worksheet(worksheet)
        if worksheet_obj:
            worksheet_obj.update_acell(cell, value)

    def update_sheet_with_df(self, worksheet: str, df: pd.DataFrame) -> None:
        """
        Update a Google Sheets worksheet with a DataFrame.

        Args:
            worksheet (str): The name of the worksheet to update.
            df (pd.DataFrame): The DataFrame to write to the worksheet.

        Returns:
            None: This function does not return anything.
        """
        worksheet_obj = self._get_worksheet(worksheet)
        if worksheet_obj:
            worksheet_obj.clear()
            worksheet_obj.update([df.columns.values.tolist()] + df.values.tolist())

    def get_cell(self, worksheet: str, cell: str) -> Any:
        """
        Get the value of a specific cell in the specified worksheet.

        Args:
            worksheet (str): The name of the worksheet.
            cell (str): The address of the cell to retrieve. Eg.: A1.

        Returns:
            Any: The value of the cell.
        """
        worksheet_obj = self._get_worksheet(worksheet)
        if worksheet_obj:
            return worksheet_obj.acell(cell).value

    def get_row(self, worksheet: str, row: int) -> List[Any]:
        """
        Get the values of a row in the specified worksheet.

        Args:
            worksheet (str): The name of the worksheet.
            row (int): The index of the row to retrieve.

        Returns:
            List[Any]: The values of the row.
        """
        worksheet_obj = self._get_worksheet(worksheet)
        if worksheet_obj:
            return worksheet_obj.row_values(row)

    def get_col(self, worksheet: str, col: int) -> List[Any]:
        """
        Get the values of a column in the specified worksheet.

        Args:
            worksheet (str): The name of the worksheet.
            col (int): The index of the column to retrieve.

        Returns:
            List[Any]: The values of the column.
        """
        worksheet_obj = self._get_worksheet(worksheet)
        if worksheet_obj:
            return worksheet_obj.col_values(col)

    def get_all_as_list(self, worksheet: str) -> List[List[Any]]:
        """
        Get all values in the specified worksheet as a list of lists.

        Args:
            worksheet (str): The name of the worksheet.

        Returns:
            List[List[Any]]: The values in the worksheet.
        """
        worksheet_obj = self._get_worksheet(worksheet)
        if worksheet_obj:
            return worksheet_obj.get_all_values()

    def get_all_as_dict(self, worksheet: str) -> List[Dict[str, Any]]:
        """
        Get all values in the specified worksheet as a list of dictionaries.

        Args:
            worksheet (str): The name of the worksheet.

        Returns:
            List[Dict[str, Any]]: The values in the worksheet.
        """
        worksheet_obj = self._get_worksheet(worksheet)
        if worksheet_obj:
            return worksheet_obj.get_all_records()

    def get_as_df(self, worksheet: str) -> pd.DataFrame:
        """
        Get all values in the specified worksheet as a DataFrame.

        Args:
            worksheet (str): The name of the worksheet.

        Returns:
            pd.DataFrame: The values in the worksheet.
        """
        worksheet_obj = self._get_worksheet(worksheet)
        if worksheet_obj:
            return pd.DataFrame(worksheet_obj.get_all_values())
