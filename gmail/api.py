import streamlit as st
import base64
import re
from email.utils import parseaddr
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


def get_gmail_service(credentials: Credentials):
    """Build Gmail API service."""
    return build("gmail", "v1", credentials=credentials)


def get_user_info(credentials: Credentials) -> dict:
    """Fetch user profile information."""
    service = build("oauth2", "v2", credentials=credentials)
    return service.userinfo().get().execute()


def fetch_emails(credentials: Credentials, max_results: int = 20) -> list[dict]:
    """Fetch latest emails from inbox."""

    st.write("✅ Creating Gmail service...")
    service = get_gmail_service(credentials)

    st.write("✅ Fetching message list...")

    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX"],
        maxResults=max_results,
    ).execute()

    st.write("📦 Raw Gmail Response:")
    st.write(results)

    messages = results.get("messages", [])

    st.write(f"📧 Messages found: {len(messages)}")

    emails = []

    for msg in messages:
        try:
            st.write(f"🔍 Processing message: {msg['id']}")

            email_data = get_email_details(service, msg["id"])

            if email_data:
                emails.append(email_data)

        except Exception as e:
            st.error(f"Error processing {msg['id']} : {e}")

    st.write(f"✅ Final emails collected: {len(emails)}")

    return emails


def get_email_details(service, message_id: str) -> dict | None:
    """Extract email details from message ID."""

    try:
        message = service.users().messages().get(
            userId="me",
            id=message_id,
            format="full",
        ).execute()

        headers = message.get("payload", {}).get("headers", [])

        sender = ""
        sender_email = ""
        subject = "(No Subject)"

        for header in headers:
            name = header.get("name", "").lower()
            value = header.get("value", "")

            if name == "from":
                sender = value
                _, sender_email = parseaddr(value)

            elif name == "subject":
                subject = value if value else "(No Subject)"

        body = extract_body(message.get("payload", {}))

        return {
            "id": message_id,
            "sender": sender,
            "sender_email": sender_email,
            "subject": subject,
            "body": body,
            "snippet": message.get("snippet", ""),
        }

    except Exception as e:
        st.error(f"❌ Error fetching email {message_id}: {e}")
        return None


def extract_body(payload: dict) -> str:
    body = ""

    if "body" in payload and payload["body"].get("data"):
        body = decode_base64(payload["body"]["data"])

    if "parts" in payload:
        for part in payload["parts"]:
            mime_type = part.get("mimeType", "")

            if mime_type == "text/plain":
                if part.get("body", {}).get("data"):
                    body = decode_base64(part["body"]["data"])
                    break

            elif mime_type == "text/html" and not body:
                if part.get("body", {}).get("data"):
                    body = decode_base64(part["body"]["data"])
                    body = strip_html(body)

            elif "parts" in part:
                body = extract_body(part)
                if body:
                    break

    return body.strip()


def decode_base64(data: str) -> str:
    try:
        return base64.urlsafe_b64decode(data).decode(
            "utf-8",
            errors="ignore"
        )
    except Exception:
        return ""


def strip_html(html: str) -> str:
    clean = re.sub(r"<[^>]+>", " ", html)
    clean = re.sub(r"\s+", " ", clean)
    return clean.strip()