import os

class Config:
    BASE_URL = os.getenv("YUNO_API_URL", "https://api-sandbox.y.uno/v1")
    PUBLIC_API_KEY = os.getenv("PUBLIC_API_KEY", "to_complete")
    PRIVATE_SECRET_KEY = os.getenv("PRIVATE_SECRET_KEY", "to_complete")
    ACCOUNT_ID = os.getenv("ACCOUNT_ID", "to_complete")
 