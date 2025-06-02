import streamlit as st
from authlib.integrations.requests_client import OAuth2Session
from pymongo import MongoClient
from config import redirect_url, google_client_id, google_client_secret, auth_url, token_url, user_info_url, \
    database_url
import time
import logging
from app.chatbot import streamlit_chat_interface
import asyncio
import os

os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

# Your credentials from Google Cloud Console
GOOGLE_CLIENT_ID = google_client_id
GOOGLE_CLIENT_SECRET = google_client_secret
REDIRECT_URI = redirect_url

# --- Setup MongoDB ---
client_mongo = MongoClient(database_url)
db = client_mongo["sample_mflix"]
session_col = db["sessions"]

st.set_page_config(page_title="LLM Chatbot with RAG System", layout="centered")
st.title("🔐 LLM Chatbot with RAG System with Google OAuth")



def get_saved_session(email):
    return session_col.find_one({"email": email})


def save_session(email, token, user_info):
    print(email)
    session = session_col.find_one({"email": email})
    print(session)
    if session:
        session_col.update_one(
            {"email": email},
            {
                "$set": {
                    "user_id": email,
                    "token": token,
                    "expires_at": token.get("expires_at", 0),
                    "user_info": user_info
                }
            },
            upsert=True
        )
    else:
        print("=======================")
        session_col.insert_one({
            "user_id": email,
            "email": email,
            "expires_at": token.get("expires_at", 0),
            "user_info": user_info,
            "token": token
        })


# Create an OAuth2 session
client = OAuth2Session(
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="openid email profile"
)


async def main():
    # --- Check Streamlit Session ---
    logging.debug("session", st.session_state)
    if "user_email" in st.session_state:
        saved = get_saved_session(st.session_state["user_email"])
        logging.debug("saved===================", saved)
        if saved and time.time() < saved["expires_at"]:
            user_info = saved["user_info"]
            st.success(f"👋 Welcome back, {user_info['name']}!")
            st.image(user_info["picture"], width=100)
            st.write("**Email:**", user_info["email"])

            if st.button("🚪 Logout"):
                del st.session_state["user_email"]
                del st.session_state["code"]
                st.query_params.clear()
                st.session_state.clear()
                st.rerun()

            await streamlit_chat_interface(user_info)


        else:
            st.warning("Session expired. Please log in again.")
            del st.session_state["user_email"]
            st.rerun()

    else:
        # Check OAuth redirect
        # query_params = st.experimental_get_query_params()
        query_params = st.query_params
        # code = query_params.get("code", [None])[0]
        code = query_params.get("code", None)

        logging.debug("code==================>", code)
        st.session_state["code"] = code

        if code and "token" not in st.session_state:
            # Exchange code for token
            token = client.fetch_token(
                token_url,
                code=code
            )
            token["expires_at"] = time.time() + token.get("expires_in", 3600)
            client.token = token
            user_info = client.get(user_info_url).json()

            # Save session to MongoDB
            save_session(user_info["email"], token, user_info)

            # Set session
            st.session_state["user_email"] = user_info["email"]
            st.session_state["token"] = token
            st.rerun()

        else:
            # No session yet — show login
            auth_url2, _ = client.create_authorization_url(auth_url)
            st.markdown("Login using your Google Account:")
            st.markdown(f"[🔑 Login with Google]({auth_url2})")


if __name__ == "__main__":
    asyncio.run(main())
    # asyncio.run(load_llm_model())
