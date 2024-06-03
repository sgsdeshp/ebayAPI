import base64
import requests
from config import (
    FBB_EBAY_APP_ID,
    FBB_EBAY_CERT_ID,
    REFRESH_TOKEN,
)
import pandas as pd
from utils.ftp_utils import get_file
import csv


def refresh_access_token():
    url = "https://api.ebay.com/identity/v1/oauth2/token"
    client_id_secret = f"{FBB_EBAY_APP_ID}:{FBB_EBAY_CERT_ID}"
    encoded_client_id_secret = base64.b64encode(client_id_secret.encode()).decode()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_client_id_secret}",
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "scope": "https://api.ebay.com/oauth/api_scope/sell.inventory",
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()["access_token"]


def update_inventory(api_token, items_list, stock_dict):
    url = "https://api.ebay.com/sell/inventory/v1/inventory_item/{sku}/availability"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }
    for item in items_list:
        sku = item["SKU"]
        if sku in stock_dict:
            quantity = stock_dict[sku]
            payload = {"shipToLocationAvailability": {"quantity": quantity}}
            response = requests.put(url.format(sku=sku), headers=headers, json=payload)
            if response.status_code == 200:
                print(f"Inventory updated for SKU {sku}.")
            else:
                print(
                    f"Failed to update inventory for SKU {sku}. Error: {response.text}"
                )
        else:
            print(f"No stock information found for SKU {sku}. Skipping.")


# Main script
api_token = refresh_access_token()

# Get stock data from FTP server
stock_data = get_file("https://www.picbox.uk/ow-exports/Puig-Free-Stock-Export.xlsx")

# Convert stock data to a dictionary
stock_dict = dict(stock_data.values)

# Read items list from CSV file
items_list = []
with open(
    "c:\\Users\\hello\\Desktop\\PM Projects\\ebayAPI\\StockUpdate\\test.csv", "r"
) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        items_list.append(row)

# Group items by SKU to update inventory for each unique SKU
items_by_sku = {}
for item in items_list:
    sku = item["SKU"]
    items_by_sku.setdefault(sku, []).append(item)

# Update inventory for each unique SKU
for sku, items in items_by_sku.items():
    update_inventory(api_token, items, stock_dict)
