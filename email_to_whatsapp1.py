import os
import pickle
import base64
import email
import time
import requests
from email.header import decode_header
import imaplib
from twilio.rest import Client
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv
import httplib2

# Load environment variables
load_dotenv()

# Set up environment variables
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')
PERSONAL_WHATSAPP_NUMBER = os.getenv('PERSONAL_WHATSAPP_NUMBER')

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    if os.path.exists('token.json'):
        with open('token.json', 'rb') as token:
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'wb') as token:
            token.write(creds.to_json().encode())
    service = build('gmail', 'v1', credentials=creds)
    return service

def parse_email_parts(parts):
    """Parse the parts of an email to extract the body content."""
    body = ""
    for part in parts:
        if part['mimeType'] == 'text/plain':
            body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
            break
        elif 'parts' in part:
            body = parse_email_parts(part['parts'])
            if body:
                break
    return body

def read_latest_email():
    service = get_gmail_service()
    max_retries = 5
    for attempt in range(max_retries):
        try:
            results = service.users().messages().list(userId='me', maxResults=1).execute()
            message_id = results['messages'][0]['id']
            message = service.users().messages().get(userId='me', id=message_id).execute()
            break
        except (requests.ConnectionError, requests.Timeout, httplib2.ServerNotFoundError) as e:
            print(f"Network error occurred: {e}. Retrying ({attempt+1}/{max_retries})...")
            time.sleep(5)
        except Exception as e:
            print(f"An error occurred: {e}")
            raise
    else:
        raise Exception("Failed to connect to Gmail API after several attempts.")

    payload = message['payload']
    headers = payload.get('headers', [])
    subject = next((header['value'] for header in headers if header['name'] == 'Subject'), None)
    if 'parts' in payload:
        body = parse_email_parts(payload['parts'])
    else:
        body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
    return subject, body

def send_whatsapp_message(to, body):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=body,
        from_=TWILIO_WHATSAPP_NUMBER,
        to=to
    )
    return message.sid

if __name__ == '__main__':
    subject, body = read_latest_email()
    print(f"Subject: {subject}")
    print(f"Body: {body}")
    
    message_sid = send_whatsapp_message(PERSONAL_WHATSAPP_NUMBER, body)
    print(f"Message SID: {message_sid}")
