import requests
import os
from requests_oauthlib import OAuth1Session
from oauthlib.oauth1 import SIGNATURE_RSA

# Replace these values with your actual credentials
app_id = os.getenv("FBB_EBAY_APP_ID")
cert_id = os.getenv("FBB_EBAY_CERT_ID")
dev_id = os.getenv("FBB_EBAY_DEV_ID")
redirect_uri = os.getenv("FBB_EBAY_REDIRECT_URI")

# Set up the authentication
oauth = OAuth1Session(
    client_key=app_id,
    client_secret=cert_id,
    resource_owner_key=dev_id,
    resource_owner_secret="",
    signature_method=SIGNATURE_RSA,
    rsa_key=open("YOUR_PRIVATE_KEY_FILE.pem", "r").read(),
    signature_type="auth_header",
)

# Define the request parameters
url = "https://auth.ebay.com/oauth2/token"
headers = {"Content-Type": "application/x-www-form-urlencoded"}
body = {
    "grant_type": "client_credentials",
    "redirect_uri": redirect_uri,
    "scope": "https://api.ebay.com/oauth/api_scope",
}

# Send the request to obtain the access token and refresh token
response = oauth.post(url, headers=headers, data=body)
tokens = response.json()

access_token = tokens["access_token"]
refresh_token = tokens["refresh_token"]
