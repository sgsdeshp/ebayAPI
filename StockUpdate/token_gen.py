import base64
import requests
from config import (
    FBB_EBAY_APP_ID,
    FBB_EBAY_CERT_ID,
    REFRESH_TOKEN,
)


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
