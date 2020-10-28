"""
Name: Dhaval Shrishrimal
Description: This file uses google api to download the Nicholas Cage image 
from google drive.
PRE_REQ: must have credentials.json
File: 'get_image.py'
"""

import os.path
import pickle
import sys
import io
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from oauth2client import file, client, tools

# API Scopes
SCOPES = ['https://www.googleapis.com/auth/drive']

def build_service():
    """
    This function builds the google api service.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    return service

def download_nick(service, fileId, location):
    """
    using the service and file id, the file downloads the file
    onto the given location
    """
    request = service.files().get_media(fileId=fileId)
    fh = io.FileIO(location, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()

