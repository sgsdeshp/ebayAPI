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

# Set the parameters for the GetMyeBaySelling API call
params = {
    "DetailLevel": "ReturnAll",
    "IncludeVariations": True,
    "GranularityLevel": "Fine",
    "ActiveList": {
        "Include": True,
        "Pagination": {
            "EntriesPerPage": 200,
            "PageNumber": 1,
        },
    },
    "UnsoldList": {
        "Include": True,
        "Pagination": {
            "EntriesPerPage": 200,
            "PageNumber": 1,
        },
    },
}

all_items = []


# Function to fetch listings
def fetch_listings(list_type):
    while True:
        print(
            f"Requesting {list_type} listings page {params[list_type]['Pagination']['PageNumber']}..."
        )
        response = trading_api.execute("GetMyeBaySelling", params).dict()
        print("Response:", response)

        if list_type in response and response[list_type] is not None:
            items = response[list_type].get("ItemArray", {}).get("Item", [])
            print(f"{list_type} items:", items)
            all_items.extend(items)
        else:
            print(f"'{list_type}' key not found or is None in response")

        if "PaginationResult" in response.get(list_type, {}):
            total_pages = int(
                response[list_type]["PaginationResult"].get("TotalNumberOfPages", 1)
            )
            current_page = int(
                response[list_type]["PaginationResult"].get(
                    "PageNumber", params[list_type]["Pagination"]["PageNumber"]
                )
            )

            print(f"Current page: {current_page}, Total pages: {total_pages}")

            if current_page >= total_pages:
                break
        else:
            print("No pagination information in response, assuming only one page.")
            break

        # Move to the next page
        params[list_type]["Pagination"]["PageNumber"] += 1


# Fetch active listings
fetch_listings("ActiveList")

# Reset pagination for unsold items
params["UnsoldList"]["Pagination"]["PageNumber"] = 1

# Fetch unsold listings
fetch_listings("UnsoldList")

# Print the listings
for item in all_items:
    title = item.get("Title", "N/A")
    item_id = item.get("ItemID", "N/A")
    start_price = item.get("StartPrice", {}).get("_value_", "N/A")
    current_price = (
        item.get("SellingStatus", {}).get("CurrentPrice", {}).get("_value_", "N/A")
    )
    hit_count = item.get("HitCount", "N/A")
    condition = item.get("ConditionDisplayName", "N/A")
    quantity_available = item.get("QuantityAvailable", "N/A")
    sku = item.get("SKU", "N/A")

    print(f"Title: {title}")
    print(f"Item ID: {item_id}")
    print(f"Start Price: {start_price}")
    print(f"Current Price: {current_price}")
    print(f"Hits: {hit_count}")
    print(f"Condition: {condition}")
    print(f"Quantity Available: {quantity_available}")
    print(f"SKU: {sku}")

    if "Variations" in item:
        variations = item["Variations"].get("Variation", [])
        if isinstance(variations, dict):
            variations = [variations]
        for variation in variations:
            if isinstance(variation, dict):
                variation_sku = variation.get("SKU", "N/A")
                variation_quantity = variation.get("Quantity", "N/A")
                variation_price = variation.get("StartPrice", {}).get("_value_", "N/A")

                print(f"  Variation SKU: {variation_sku}")
                print(f"  Variation Quantity: {variation_quantity}")
                print(f"  Variation Price: {variation_price}")

    print("=" * 30)
