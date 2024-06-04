import base64
from token_gen import refresh_access_token
from test import get_stock_data, convert_to_csv
from utils.notifications import send_email
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

# Example dictionary with SKU and stock values
sku_stock_dict = get_stock_data()

# Prepare the inventory status update
inventory_status_list = []

for item in all_items:
    item_id = item.get("ItemID", "N/A")
    if "Variations" in item:
        variations = item["Variations"].get("Variation", [])
        if isinstance(variations, dict):
            variations = [variations]
        for variation in variations:
            if isinstance(variation, dict):
                variation_sku = variation.get("SKU", "N/A")
                if variation_sku in sku_stock_dict:
                    inventory_status_list.append(
                        {
                            "ItemID": item_id,
                            "SKU": variation_sku,
                            "Quantity": sku_stock_dict[variation_sku],
                        }
                    )

# Call ReviseInventoryStatus for each batch of SKUs
batch_size = 4
for i in range(0, len(inventory_status_list), batch_size):
    batch = inventory_status_list[i : i + batch_size]
    print(f"Updating batch: {batch}")
    try:
        response = trading_api.execute(
            "ReviseInventoryStatus", {"InventoryStatus": batch}
        ).dict()
        print("Update response:", response)
    except Exception as e:
        print(f"Error updating batch: {batch} - {e}")
        pass

print("Stock update completed.")

# Send email notification
send_email("support@puremoto.co.uk", "Ebay Stock.", "Stock update completed.")
