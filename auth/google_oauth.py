"""Google OAuth 2.0 authentication module."""

import streamlit as st
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import json

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

def get_oauth_config() -> dict:
    return {
        "web": {
            "client_id": st.secrets["google"]["client_id"],
            "client_secret": st.secrets["google"]["client_secret"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [st.secrets["google"]["redirect_uri"]],
        }
    }


def create_auth_flow() -> Flow:
    config = get_oauth_config()

    flow = Flow.from_client_config(
        config,
        scopes=SCOPES,
        redirect_uri=st.secrets["google"]["redirect_uri"],
        autogenerate_code_verifier=False,
    )

    return flow


def get_authorization_url():
    flow = create_auth_flow()

    auth_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )

    st.session_state["oauth_flow"] = flow
    st.session_state["oauth_state"] = state

    return auth_url

def exchange_code_for_credentials(code):
    flow = create_auth_flow()
    flow.fetch_token(code=code)
    return flow.credentials


def refresh_credentials(credentials: Credentials) -> Credentials:
    """Refresh expired credentials."""
    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    return credentials


def get_valid_credentials() -> Credentials | None:
    """Retrieve and validate stored credentials."""
    if "credentials" not in st.session_state:
        return None

    creds_data = st.session_state["credentials"]
    credentials = Credentials(
        token=creds_data["token"],
        refresh_token=creds_data.get("refresh_token"),
        token_uri=creds_data["token_uri"],
        client_id=creds_data["client_id"],
        client_secret=creds_data["client_secret"],
        scopes=creds_data["scopes"],
    )

    if credentials.expired:
        try:
            credentials = refresh_credentials(credentials)
            store_credentials(credentials)
        except Exception:
            clear_credentials()
            return None

    return credentials


def store_credentials(credentials: Credentials) -> None:
    """Store credentials in session state."""
    st.session_state["credentials"] = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }


def clear_credentials() -> None:
    """Clear stored credentials."""
    if "credentials" in st.session_state:
        del st.session_state["credentials"]
    if "user_info" in st.session_state:
        del st.session_state["user_info"]


def is_authenticated() -> bool:
    """Check if user is authenticated."""
    return get_valid_credentials() is not None
