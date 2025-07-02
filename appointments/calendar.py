import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def get_credentials():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    creds = None

    token_path = os.path.join(BASE_DIR, 'secrets', 'token.pickle')
    creds_path = os.path.join(BASE_DIR, 'secrets', 'credentials.json')

    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
    #         creds = flow.run_local_server(port=0)

        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds
