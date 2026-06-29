import os
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
import streamlit as st
from urllib.parse import parse_qs, urlparse

# Configure page
st.set_page_config(
    page_title="Inbox Intel",
    page_icon="📬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Import modules
from auth.google_oauth import (
    get_authorization_url,
    exchange_code_for_credentials,
    store_credentials,
    get_valid_credentials,
    clear_credentials,
    is_authenticated,
)
from gmail.api import fetch_emails, get_user_info
from ml.predict import SpamPredictor
from ui.dashboard import (
    render_header,
    render_login_page,
    render_email_table,
    render_sidebar,
    render_error,
)


def handle_oauth_callback() -> bool:
    """Handle OAuth callback and exchange code for credentials."""
    query_params = st.query_params
    
    if "code" in query_params:
        try:
            code = query_params["code"]
            credentials = exchange_code_for_credentials(code)
            store_credentials(credentials)
            
            # Clear query params
            st.query_params.clear()
            return True
        except Exception as e:
            render_error(f"Authentication failed: {str(e)}")
            st.query_params.clear()
            return False
    
    return False


def refresh_emails(credentials, max_emails: int) -> None:
    st.session_state["loading"] = True

    try:
        # Fetch emails only once
        emails = fetch_emails(credentials, max_results=max_emails)

        predictor = SpamPredictor()
        analyzed_emails = predictor.predict_batch(emails)

        st.session_state["emails"] = analyzed_emails
        st.session_state["loading"] = False

        st.rerun()

    except FileNotFoundError as e:
        render_error(str(e))
        st.session_state["loading"] = False

    except Exception as e:
        render_error(f"Error fetching emails: {str(e)}")
        st.session_state["loading"] = False


def main():
    """Main application entry point."""
    
    # Initialize session state
    if "emails" not in st.session_state:
        st.session_state["emails"] = []
    if "loading" not in st.session_state:
        st.session_state["loading"] = False
    
    # Handle OAuth callback
    if not is_authenticated():
        handle_oauth_callback()
    
    # Check authentication
    credentials = get_valid_credentials()
    
    if credentials:
        # Authenticated view
        try:
            user_info = get_user_info(credentials)
            st.session_state["user_info"] = user_info
        except Exception:
            user_info = st.session_state.get("user_info", {})
        
        render_header(user_info)
        
        # Sidebar with controls
        max_emails = render_sidebar(
            on_refresh=lambda: refresh_emails(
                credentials,
                st.session_state.get("max_emails", 20)
            ),
            on_logout=clear_credentials,
        )          

        st.session_state["max_emails"] = max_emails
        
        # Auto-fetch on first load
        if not st.session_state["emails"] and not st.session_state["loading"]:
            refresh_emails(credentials, max_emails)
        
        # Display emails
        if st.session_state["loading"]:
            with st.spinner("Fetching and analyzing emails..."):
                st.empty()
        else:
            render_email_table(st.session_state["emails"])
    
    else:
        # Login view
        render_header()
        auth_url = get_authorization_url()
        render_login_page(auth_url)


if __name__ == "__main__":
    main()
