"""Streamlit UI components for the dashboard."""

import streamlit as st
import pandas as pd


def render_header(user_info: dict | None = None) -> None:
    """Render the app header."""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.title("📬 Inbox Intel")
        st.caption("AI-powered spam detection for your Gmail inbox")
    
    with col2:
        if user_info:
            st.write(f"👤 {user_info.get('name', 'User')}")
            st.caption(user_info.get("email", ""))


def render_login_page(auth_url: str) -> None:
    """Render the login page."""
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(
            """
            ### Welcome to Inbox Intel
            
            Securely analyze your Gmail inbox for spam using AI.
            
            **Features:**
            - 🔒 Secure Google OAuth authentication
            - 📧 Fetch and analyze your latest emails
            - 🤖 ML-powered spam detection
            - 📊 Visual spam probability indicators
            
            **Your data is safe:**
            - No passwords stored
            - Read-only Gmail access
            - Processing done locally
            """
        )
        
        st.markdown("---")
        
        st.link_button(
            "🔐 Sign in with Google",
            auth_url,
            use_container_width=True,
            type="primary",
        )


def render_email_table(emails: list[dict]) -> None:
    """Render the email analysis table."""
    if not emails:
        st.info("No emails found in your inbox.")
        return
    
    st.markdown("### 📊 Email Analysis Results")
    st.caption(f"Showing {len(emails)} emails from your inbox")
    
    # Summary stats
    spam_count = sum(1 for e in emails if e.get("prediction") == "Spam")
    ham_count = len(emails) - spam_count
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Emails", len(emails))
    col2.metric("🟢 Ham", ham_count)
    col3.metric("🔴 Spam", spam_count)
    
    st.markdown("---")
    
    # Render each email as a card
    for idx, email in enumerate(emails):
        render_email_card(email, idx)


def render_email_card(email: dict, index: int) -> None:
    """Render a single email card with prediction styling."""
    is_spam = email.get("prediction") == "Spam"
    probability = email.get("probability", 0)
    
    # Color coding
    border_color = "#ff4b4b" if is_spam else "#21c354"
    bg_color = "#ffebee" if is_spam else "#e8f5e9"
    badge_color = "🔴" if is_spam else "🟢"
    
    # Truncate long values
    sender = email.get("sender", "Unknown")[:60]
    subject = email.get("subject", "(No Subject)")[:80]
    
    with st.container():
        st.markdown(
            f"""
            <div style="
                border-left: 4px solid {border_color};
                background-color: {bg_color};
                padding: 12px 16px;
                margin-bottom: 12px;
                border-radius: 4px;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="color: #333;">From:</strong> {sender}<br>
                        <strong style="color: #333;">Subject:</strong> {subject}
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 1.2em;">{badge_color} {email.get('prediction', 'Unknown')}</span><br>
                        <span style="color: #666; font-size: 0.9em;">
                            Spam probability: {probability:.1%}
                        </span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_sidebar(on_refresh: callable, on_logout: callable) -> int:
    """Render the sidebar with controls."""
    with st.sidebar:
        st.markdown("### ⚙️ Controls")
        
        max_emails = st.slider(
            "Emails to fetch",
            min_value=5,
            max_value=50,
            value=20,
            step=5,
        )
        
        st.markdown("---")
        
        if st.button("🔄 Refresh Inbox", use_container_width=True, type="primary"):
            on_refresh()
            st.rerun()
        
        st.markdown("---")
        
        if st.button("🚪 Sign Out", use_container_width=True):
            on_logout()
            st.rerun()
        
        st.markdown("---")
        st.caption("Inbox Intel v1.0")
        st.caption("Powered by ML spam detection")
        
        return max_emails


def render_error(message: str) -> None:
    """Render an error message."""
    st.error(f"⚠️ {message}")


def render_loading() -> None:
    """Render loading state."""
    with st.spinner("Fetching and analyzing emails..."):
        pass
