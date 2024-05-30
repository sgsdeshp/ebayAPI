import requests
import json
from token_gen import refresh_access_token
from test import get_stock_data, convert_to_csv
from config import (
    FBB_EBAY_API_KEY,
    FBB_EBAY_APP_ID,
    FBB_EBAY_CERT_ID,
    FBB_EBAY_DEV_ID,
    REFRESH_TOKEN,
    TOKEN,
)

# Get a new access token
token = refresh_access_token()

# Sample data
inventory_status_list = [{"ItemID": "276170086545", "SKU": "20702H", "Quantity": 0}]

sku_stock_dict = get_stock_data()


# Function to create or update inventory item
def create_inventory_item(sku, quantity):
    url = f"https://api.ebay.com/sell/inventory/v1/inventory_item/{sku}"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    payload = {
        "availability": {"shipToLocationAvailability": {"quantity": quantity}},
        "product": {
            "title": "Your Product Title",
            "description": "Your Product Description",
            "aspects": {"Brand": ["Your Brand"]},
        },
    }
    response = requests.put(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 204:
        print(f"Inventory item for SKU {sku} created/updated successfully.")
    else:
        print(
            f"Error creating/updating inventory item for SKU {sku}: {response.status_code}, {response.text}"
        )


# Function to create offer
def create_offer(sku, listing_id):
    url = "https://api.ebay.com/sell/inventory/v1/offer"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    payload = {
        "sku": sku,
        "marketplaceId": "EBAY_US",
        "format": "FIXED_PRICE",
        "listingDescription": "Your listing description",
        "availableQuantity": sku_stock_dict[sku],
        "categoryId": "Your Category ID",
        "listingPolicies": {
            "fulfillmentPolicyId": "Your Fulfillment Policy ID",
            "paymentPolicyId": "Your Payment Policy ID",
            "returnPolicyId": "Your Return Policy ID",
        },
        "pricingSummary": {"price": {"value": "Your Price", "currency": "USD"}},
        "listingId": listing_id,
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 201:
        offer_id = response.json()["offerId"]
        print(f"Offer created for SKU {sku} with offer ID {offer_id}.")
        return offer_id
    else:
        print(
            f"Error creating offer for SKU {sku}: {response.status_code}, {response.text}"
        )
        return None


# Function to bulk update inventory
def bulk_update_inventory(inventory_status_list, sku_stock_dict):
    sku_to_offer_id = {}

    # Create inventory items and offers
    for item in inventory_status_list:
        sku = item["SKU"]
        listing_id = item["ItemID"]
        quantity = item["Quantity"]

        # Create inventory item
        create_inventory_item(sku, quantity)

        # Create offer
        offer_id = create_offer(sku, listing_id)
        if offer_id:
            sku_to_offer_id[sku] = offer_id

    # Prepare the bulk update payload
    requests_payload = []
    for sku, offer_id in sku_to_offer_id.items():
        requests_payload.append(
            {"offerId": offer_id, "availableQuantity": sku_stock_dict[sku]}
        )

    # Perform bulk update
    url = "https://api.ebay.com/sell/inventory/v1/bulk_update_price_quantity"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    payload = {"requests": requests_payload}

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("Inventory updated successfully:", response.json())
    else:
        print(f"Error updating inventory: {response.status_code}, {response.text}")


# Execute bulk update
bulk_update_inventory(inventory_status_list, sku_stock_dict)

print("Stock update completed.")
