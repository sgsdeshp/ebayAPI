"""A class for interacting with Google Sheets."""

import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from typing import List, Dict, Union

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
        """(Private method)Get the worksheet object for the specified sheet name."""
        workbook = client.open_by_key(self.sheet_id)
        return workbook.worksheet(worksheet)

    def update_cell(self, worksheet: str, cell: str, value: str | int | float) -> None:
        """
        Update a cell in the specified worksheet with the given value.

        Args:
            worksheet (str): The name of the worksheet to update.
            cell (str): The address of the cell to update. Eg.: A1.
            value (Any): The new value to set in the cell.

        Returns:
            None
        """
        worksheet = self._get_worksheet(worksheet)  # type: ignore
        worksheet.update_acell(cell, value)  # type: ignore

    def update_sheet_with_df(self, worksheet: str, df: pd.DataFrame) -> None:
        """
        Update a Google Sheets worksheet with a DataFrame.

        Args:
            worksheet (str): The name of the worksheet to update.
            df (pd.DataFrame): The DataFrame to write to the worksheet.

        Returns:
            None: This function does not return anything.
        """
        worksheet = self._get_worksheet(worksheet)  # type: ignore
        worksheet.clear()  # type: ignore
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())  # type: ignore

    def get_cell(self, worksheet: str, cell: str) -> str | int | float:
        """
        Get the value of a cell in the specified worksheet.

        Args:
            worksheet (str): The name of the worksheet.
            cell (str): The address of the cell. Eg.: A1.

        Returns:
            str | int | float: The value of the cell.
        """
        worksheet = self._get_worksheet(worksheet)  # type: ignore
        return worksheet.acell(cell).value  # type: ignore

    def get_row(self, worksheet: str, row: int) -> List[Union[str, int, float]]:
        """
        Get the values of a row in the specified worksheet.

        Args:
            worksheet (str): The name of the worksheet.
            row (int): The index of the row to retrieve.

        Returns:
            List[Union[str, int, float]]: The values of the row.
        """
        worksheet = self._get_worksheet(worksheet)  # type: ignore
        return worksheet.row_values(row)  # type: ignore

    def get_col(self, worksheet: str, row: int) -> List[Union[str, int, float]]:
        """
        Get the values of a column in the specified worksheet.

        Args:
            worksheet (str): The name of the worksheet.
            row (int): The index of the column to retrieve.

        Returns:
            List[Union[str, int, float]]: The values of the column.
        """
        worksheet = self._get_worksheet(worksheet)  # type: ignore
        return worksheet.col_values(row)  # type: ignore

    def get_all_as_list(self, worksheet: str) -> List[List[Union[str, int, float]]]:
        """
        Get all values in the specified worksheet as a list of lists.

        Args:
            worksheet (str): The name of the worksheet.

        Returns:
            List[List[Union[str, int, float]]]: The values in the worksheet.
        """
        worksheet = self._get_worksheet(worksheet)  # type: ignore
        return worksheet.get_all_values()  # type: ignore

    def get_all_as_dict(
        self, worksheet: str
    ) -> List[Dict[str, Union[str, int, float]]]:
        """
        Get all values in the specified worksheet as a list of dictionaries.

        Args:
            worksheet (str): The name of the worksheet.

        Returns:
            List[Dict[str, Union[str, int, float]]]: The values in the worksheet.
        """
        worksheet = self._get_worksheet(worksheet)  # type: ignore
        return worksheet.get_all_records()  # type: ignore

    def get_as_df(self, worksheet: str) -> pd.DataFrame:
        """
        Get all values in the specified worksheet as a DataFrame.

        Args:
            worksheet (str): The name of the worksheet.

        Returns:
            pd.DataFrame: The values in the worksheet.
        """
        worksheet = self._get_worksheet(worksheet)  # type: ignore
        return pd.DataFrame(worksheet.get_all_values())  # type: ignore
