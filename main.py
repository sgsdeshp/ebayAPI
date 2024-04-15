from dotenv import load_dotenv
import os

load_dotenv()
API_KEY=os.getenv('api_key')
print(API_KEY)