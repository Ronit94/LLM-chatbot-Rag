from dotenv import load_dotenv
import os

load_dotenv()
google_client_id = os.getenv("GOOGLE_CLIENT_ID")
google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
redirect_url = os.getenv("REDIRECT_URI")
token_url = os.getenv("TOKEN_URL")
auth_url = os.getenv("AUTH_URL")
user_info_url = os.getenv("USER_INFO_URL")
database_url = os.getenv("DATABASE_URL")
pin_cone_api_key = os.getenv("PINCONE_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")
index_name = os.getenv("PINECONE_INDEX_NAME")