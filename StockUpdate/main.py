import base64
from token_gen import refresh_access_token

import requests
from config import (
    FBB_EBAY_API_KEY,
    FBB_EBAY_APP_ID,
    FBB_EBAY_CERT_ID,
    FBB_EBAY_DEV_ID,
    REFRESH_TOKEN,
    TOKEN,
)
from ebaysdk.trading import Connection as Trading

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
    print(f"Requesting page {params['PageNumber']}...")
    response = trading_api.execute("GetSellerList", params).dict()
    print("Response:", response)

    if "ItemArray" in response and response["ItemArray"] is not None:
        items = response["ItemArray"].get("Item", [])
        print("Items:", items)
        all_items.extend(items)
    else:
        print("'ItemArray' key not found or is None in response")

    if "PaginationResult" in response:
        total_pages = int(response["PaginationResult"].get("TotalNumberOfPages", 1))
        current_page = int(
            response["PaginationResult"].get("PageNumber", params["PageNumber"])
        )

        print(f"Current page: {current_page}, Total pages: {total_pages}")

        if current_page >= total_pages:
            break
    else:
        print("No pagination information in response, assuming only one page.")
        break

    # Move to the next page
    params["PageNumber"] += 1
    params["Pagination"]["PageNumber"] += 1

# Print the listings
for item in all_items:
    title = item.get("Title", "N/A")
    item_id = item.get("ItemID", "N/A")
    start_price = item.get("StartPrice", {}).get("_value_", "N/A")
    current_price = item.get("CurrentPrice", {}).get("_value_", "N/A")
    hit_count = item.get("HitCount", "N/A")
    condition = item.get("ConditionDisplayName", "N/A")

    print(f"Title: {title}")
    print(f"Item ID: {item_id}")
    print(f"Start Price: {start_price}")
    print(f"Current Price: {current_price}")
    print(f"Hits: {hit_count}")
    print(f"Condition: {condition}")
    print("=" * 30)
