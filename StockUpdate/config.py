"""# Configuration file for the ebay API."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API and database configuration
FBB_EBAY_API_KEY = os.environ.get("FBB_EBAY_API_KEY")
FBB_EBAY_APP_ID = os.environ.get("FBB_EBAY_APP_ID")
FBB_EBAY_DEV_ID = os.environ.get("FBB_EBAY_DEV_ID")
FBB_EBAY_REDIRECT_URI = os.environ.get("FBB_EBAY_REDIRECT_URI")
FBB_EBAY_CERT_ID = os.environ.get("FBB_EBAY_CERT_ID")
TOKEN = os.environ.get("TOKEN")
REFRESH_TOKEN = os.environ.get("REFRESH_TOKEN")

# Google Sheets credentials
GOOGLE_SHEETS_CREDENTIALS = os.environ.get("PMGCPKEY")
