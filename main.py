import requests
import base64  # Import the base64 module

# Replace with your eBay Sandbox credentials
app_id = 'id'
dev_id = 'id'
cert_id = 'id'

# Define the Sandbox API endpoint URL
base_url = "https://api.sandbox.ebay.com/sell/inventory/v1/listing"

# Authorization header generation using base64 encoding
auth_str = f"{app_id}:{cert_id}"
encoded_auth = base64.b64encode(bytes(auth_str, 'utf-8')).decode('utf-8')
headers = {"Authorization": f"Basic {encoded_auth}"}

# Define the store ID to retrieve listings from
store_id = "YOUR_STORE_ID"


# Function to retrieve paginated listings data
def get_listings(offset=0, limit=20):
    url = f"{base_url}?offset={offset}&limit={limit}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error retrieving listings: {response.status_code}")
        return None


# Get the first page of listings data
listings_data = get_listings()


# Process retrieved listings data (loop through pages if needed)
if listings_data:
    total_entries = listings_data.get("total", 0)
    current_offset = 0

    while listings_data["listings"] and current_offset < total_entries:
        for listing in listings_data["listings"]:
            # Access product details from each listing object here
            print(f"Listing ID: {listing['listingId']}")
            print(f"Title: {listing['title']}")
            print(f"Description: {listing.get('description', 'N/A')}")
            # ... access other product details as needed ...

        # Check if there are more pages to retrieve
        if listings_data.get("next"):
            current_offset += listings_data.get("limit")
            listings_data = get_listings(offset=current_offset)
        else:
            break

else:
    print("No listings found for the specified store ID.")


