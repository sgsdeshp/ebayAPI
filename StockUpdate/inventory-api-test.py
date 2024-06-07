import requests
from token_gen import refresh_access_token
from config import (
    FBB_EBAY_API_KEY,
    FBB_EBAY_APP_ID,
    FBB_EBAY_CERT_ID,
    FBB_EBAY_DEV_ID,
    REFRESH_TOKEN,
    TOKEN,
)

token = refresh_access_token()
# Define your API credentials
app_id = FBB_EBAY_APP_ID
cert_id = FBB_EBAY_CERT_ID
oauth_token = token

# Define the base URL for the eBay Inventory API
base_url = "https://api.ebay.com/sell/inventory/v1"

# Retrieve all inventory items
inventory_items = []
offset = 0
limit = 100  # Number of items to retrieve per request

while True:
    # Retrieve a batch of inventory items
    response = requests.get(
        f"{base_url}/inventory_item",
        params={"offset": offset, "limit": limit},
        headers={
            "Authorization": f"Bearer {oauth_token}",
            "X-EBAY-C-MARKETPLACE-ID": "EBAY_GB",
        },
    )

    # Check the response status code
    if response.status_code == 200:
        batch_data = response.json()
        # print(batch_data)
        # print("-" * 50)
        if "inventoryItems" in batch_data:
            inventory_items.extend(batch_data["inventoryItems"])
            if len(batch_data["inventoryItems"]) < limit:
                break  # All items retrieved
            offset += limit
        else:
            print("Unexpected response format. 'inventoryItems' key not found.")
            break
    else:
        print(f"Error: {response.status_code} - {response.text}")
        break

# Print the retrieved inventory items
for item in inventory_items:
    print(item)
    # print(f"SKU: {item.get('sku')}, Inventory Item ID: {item.get('inventoryItemId')}")
    # Process the inventory item data as needed
