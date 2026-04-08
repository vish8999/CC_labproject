import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
# We are defaulting to 127.0.0.1 since you are running this locally (without Docker)
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="URL Shortener", page_icon="🔗")

st.title("🔗 URL Shortener")



long_url = st.text_input("Enter a long URL")

if st.button("Shorten URL"):
    if not long_url:
        st.error("Please enter a URL")
    else:
        response = requests.post(
            f"{API_URL}/shorten",
            json={"long_url": long_url}
        )

        if response.status_code == 200:
            short_url = response.json()["short_url"]
            st.success("Short URL created!")
            st.code(short_url)
        else:
            st.error("Failed to shorten URL")
