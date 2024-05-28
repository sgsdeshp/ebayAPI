import datetime
import os
import sys
import json
from urllib.parse import unquote
import requests
from config import (
    FBB_EBAY_API_KEY,
    FBB_EBAY_APP_ID,
    FBB_EBAY_DEV_ID,
    FBB_EBAY_REDIRECT_URI,
    FBB_EBAY_CERT_ID,
    TOKEN,
)
import base64


API_KEY = FBB_EBAY_API_KEY


def main():
    production_login_endpoint = "https://auth.ebay.com/oauth2/authorize"
    client_id = os.getenv("FBB_EBAY_APP_ID")
    client_secret = os.getenv("FBB_EBAY_CERT_ID")
    redirect_uri = os.getenv("FBB_EBAY_REDIRECT_URI")
    scope = "https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/sell.inventory https://api.ebay.com/oauth/api_scope/sell.marketing.readonly"
    url = f"{production_login_endpoint}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}"
    print(url)
    code = input("Enter the code: ")
    code = unquote(code)
    exchange_end_point = "https://api.ebay.com/identity/v1/oauth2/token"
    ci_cs = f"{client_id}:{client_secret}"
    encoded_ci_cs = ci_cs.encode()
    b64_encoded_ci_cs = base64.b64encode(encoded_ci_cs).decode()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic " + b64_encoded_ci_cs,
    }
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
    }
    response = requests.post(exchange_end_point, headers=headers, data=data, timeout=30)
    print(response.json())


if __name__ == "__main__":
    main()
