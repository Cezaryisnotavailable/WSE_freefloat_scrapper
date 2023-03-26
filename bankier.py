"""A script that scrapes free float data for a list of tickers from bankier.pl"""

import os
import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook
from tickers import tickers_list

lista = tickers_list()
location = os.getenv("TICKERS_PATH")
print(location)

workbook = load_workbook(filename=location)
sheet_1 = workbook['Freefloat']


def run_example():
    """Scrapes free float data for a list of tickers from bankier.pl"""

    max_tries = 3
    row_number = 1

    for ticker in lista:
        url = "https://www.bankier.pl/gielda/notowania/new-connect/" + ticker + "/akcjonariat"
        print(url)
        print(ticker)
        tries = 0
        while tries < max_tries:

            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                break  # breaks out of the while loop if successful
            except requests.RequestException as error:
                tries += 1
                print(f"Connection error: {error}. Trying again ({tries}/{max_tries})...")

        else:
            # If all tries failed
            print(f"Request failed after {max_tries} attempts. Skipping {ticker}.")
            continue

        text = response.text
        soup = BeautifulSoup(text, "html.parser")

        # Find the "Free float:" in the table
        free_float_row = soup.find("td", string="Free float:").parent

        # Extract the value from the fourth column
        free_float_value = free_float_row.find_all("td")[3].get_text(strip=True)

        # saving data to the Excel workbook
        sheet_1.cell(row=row_number, column=1, value=ticker)
        sheet_1.cell(row=row_number, column=2, value=free_float_value)
        sheet_1.cell(row=row_number, column=3, value=url)
        row_number += 1

        input()
    workbook.save(location)


if __name__ == "__main__":
    run_example()
