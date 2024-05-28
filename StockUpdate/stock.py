import base64
import json
import openpyxl
import pandas as pd
import requests
from ebaysdk.trading import Connection as Trading
from config import (
    FBB_EBAY_APP_ID,
    FBB_EBAY_DEV_ID,
    FBB_EBAY_CERT_ID,
    TOKEN,
    REFRESH_TOKEN,
    FBB_EBAY_API_KEY,  # Assuming this is your Base64 encoded client_id:client_secret
)


# Function to refresh the access token using the refresh token
def refresh_access_token():
    url = "https://api.ebay.com/identity/v1/oauth2/token"

    # Combine client_id and client_secret
    client_id_secret = f"{FBB_EBAY_APP_ID}:{FBB_EBAY_CERT_ID}"
    encoded_client_id_secret = base64.b64encode(client_id_secret.encode()).decode()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_client_id_secret}",
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "scope": "https://api.ebay.com/oauth/api_scope",
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()["access_token"]


# Get a new access token
token = refresh_access_token()

# Create a Trading API connection
trading_api = Trading(
    config_file=None,
    appid=FBB_EBAY_APP_ID,
    devid=FBB_EBAY_DEV_ID,
    certid=FBB_EBAY_CERT_ID,
    token=token,
    warnings=True,
)

# Set the parameters for the GetSellerList API call
params = {
    "DetailLevel": "ReturnAll",
    "EndTimeFrom": "2024-04-01T00:00:00.000Z",
    "EndTimeTo": "2024-06-01T00:00:00.000Z",
    "EntriesPerPage": 200,  # Set the desired number of results per page
    "PageNumber": 1,  # Start with the first page
    "Pagination": {  # Add the Pagination container
        "EntriesPerPage": 200,  # Set the desired number of results per page
        "PageNumber": 1,  # Start with the first page
    },
}

all_items = []

while True:
    # Call the GetSellerList API
    response = trading_api.execute("GetSellerList", params).dict()
    # print("Response:", response)
    # Check if the "ItemArray" key exists and is not None
    if "ItemArray" in response and response["ItemArray"] is not None:
        items = response["ItemArray"].get("Item", [])
        # print("Items:", items)
        all_items.extend(items)
    else:
        print("'ItemArray' key not found or is None in response")

    # Check if there are more pages
    if (
        "PaginationResult" in response
        and "TotalNumberOfPages" in response["PaginationResult"]
    ):
        total_pages = int(response["PaginationResult"]["TotalNumberOfPages"])
        if "PageNumber" in response["PaginationResult"]:
            current_page = int(response["PaginationResult"]["PageNumber"])
        else:
            current_page = 1  # Assume current_page is 1 if "PageNumber" is not present
    else:
        total_pages = 1  # Assume only one page if "PaginationResult" or "TotalNumberOfPages" is not present
        current_page = 1

    if current_page >= total_pages:
        break

    # Move to the next page
    params["PageNumber"] += 1
    params["Pagination"]["PageNumber"] += 1


# Print the listings
for item in all_items:
    print(f"Title: {item['Title']}")
    print(f"Item ID: {item['ItemID']}")
    print(f"Start Price: {item['StartPrice']['_value_']}")
    print(f"Current Price: {item['CurrentPrice']['_value_']}")
    print(f"Hits: {item['HitCount']}")
    print(f"Condition: {item['ConditionDisplayName']}")
    print("=" * 30)
