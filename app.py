import os
import base64
import random
import time
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Constants
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
TOKEN_FILE = "token.json"
CREDENTIALS_FILE = "credentials.json"
SENDER_EMAIL = "birth.of.kira.2k17@gmail.com"
REDIRECT_URI = "http://localhost:8080"
MIN_INTERVAL = 45  # Minimum interval between replies in seconds
MAX_INTERVAL = 120  # Maximum interval between replies in seconds
#REPLIED_LABEL = "Replied"

# Function to send an auto-response email
def send_auto_response(service, sender_email):
    auto_response = """
    <html>
        <body>
            <p>Thank you for your email. I am currently on vacation and will reply to your message after my return.</p>
            <p>Best regards,<br>Mohan N</p>
        </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Auto-response: On Vacation"
    msg["From"] = SENDER_EMAIL
    msg["To"] = sender_email

    html_part = MIMEText(auto_response, "html")
    msg.attach(html_part)

    raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
    body = {"raw": raw_message}

    service.users().messages().send(userId="me", body=body).execute()

# Function to check for unread emails and send auto-responses
def check_emails(service):
    results = service.users().messages().list(userId="me", q="is:unread label:inbox").execute()
    messages = results.get("messages", [])

    if messages:
        for message in messages:
            msg = service.users().messages().get(userId="me", id=message["id"], format="metadata").execute()
            labels = msg["labelIds"]
            sender_email = next(h["value"] for h in msg["payload"]["headers"] if h["name"] == "From")
            replied = 'Label_1' in labels
            if not replied:
                # Send auto-response
                send_auto_response(service, sender_email)

                # Mark the processed email as "read"
                #service.users().messages().modify(userId="me", id=message["id"], body={"removeLabelIds": ["UNREAD"]}).execute()

                # Add label to the replied email
                service.users().messages().modify(userId="me", id=message["id"], body={"addLabelIds": ["Label_1"]}).execute()

# Main function
def main():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            flow.redirect_uri = REDIRECT_URI
            creds = flow.run_local_server(port=8080, authorization_prompt_message="")

        # Save the credentials for the next run
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)

    while True:
        check_emails(service)
        interval = random.randint(MIN_INTERVAL, MAX_INTERVAL)
        time.sleep(interval)

if __name__ == "__main__":
    main()
