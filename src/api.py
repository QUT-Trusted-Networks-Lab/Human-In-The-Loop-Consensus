#! python3
# api.py
# Manages the API calls for Gmail to facilitate the P.O.C application.

import os, re

from .message import Response

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from base64 import urlsafe_b64decode
from bs4 import BeautifulSoup

# ---------- Object class definition ---------- #
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GmailAPI:
    '''
    Arguments:
        credentialsDir -- Location where token.json and/or credentials.json
                          files are located.
    '''
    def __init__(self, credentialsDir="."):
        self.creds = self.login(credentialsDir)

    def login(self, credentialsDir):
        '''
        Handle the login and authorisation of GMail account reading. For
        a new authorisation, a token.json file will be created. This will be read
        back on future program launches until it expires and a fresh one will 
        be obtained again.

        Returns:
            creds -- Google API object containing user credentials to authorise
                    access to the GMail account.
        '''
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(os.path.join(credentialsDir, 'token.json')):
            creds = Credentials.from_authorized_user_file(os.path.join(credentialsDir, 'token.json'), SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.path.join(credentialsDir, 'credentials.json'), SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(os.path.join(credentialsDir, 'token.json'), 'w') as token:
                token.write(creds.to_json())
        
        return creds
    
    def search(self, query):
        '''
        Search the user's Gmail inbox for messages that match the provided query string.

        Arguments:
            query -- String to use for searching for emails by their title.
        Returns:
            messages -- A python list containing sublists consisting of
                        [subject, sender, date, messageID]. Date is in the format
                        "dd MMM YYYY"; messageID corresponds to the Gmail email ID.


        Credit to: https://www.thepythoncode.com/article/use-gmail-api-in-python#Searching_for_Emails
        '''

        messageIDs = []
        messages = []

        with build('gmail', 'v1', credentials=self.creds) as service:
            # Find our messages based on the query term
            result = service.users().messages().list(userId='me',q=query).execute()
            if 'messages' in result:
                messageIDs.extend(result['messages'])
            while 'nextPageToken' in result:
                page_token = result['nextPageToken']
                result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
                if 'messages' in result:
                    messageIDs.extend(result['messages'])
        
            # Extract relevant details from the messages
            for message in messageIDs:
                msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()

                payload = msg['payload']
                headers = payload.get("headers")
                for header in headers:
                    name = header.get("name")
                    value = header.get("value")
                    if name.lower() == "date":
                        regexSearch = re.search(r"^\w+?, (\d{1,2}) (\w+?) (\d{4})", value)
                        date = "{0} {1} {2}".format(regexSearch[1], regexSearch[2], regexSearch[3])
                    if name.lower() == "from":
                        sender = value
                    if name.lower() == "subject":
                        subject = value
                    if name.lower() == "to":
                        to = value.split(", ") # Potential bug location if space isn't present
                
                messages.append([subject, sender, date, message['id'], to])
        
        return messages

    def read(self, messageID):
        '''
        Using an email's ID, read the email's contents and return this as text.

        Arguments:
            messageID -- String identifying a Gmail email.
        Returns:
            text -- A string containing the email's contents.

        Credit to https://www.geeksforgeeks.org/how-to-read-emails-from-gmail-using-gmail-api-in-python/
        '''

        # Get the message text
        with build('gmail', 'v1', credentials=self.creds) as service:
            msg = service.users().messages().get(userId='me', id=messageID, format='full').execute()
            
            # Extract relevant details from the messages
            payload = msg['payload']
            mimeType = payload.get("mimeType")
            
            # If relevant, find our part's payload
            if mimeType == "multipart/alternative":
                parts = payload.get("parts")
                for part in parts:
                    mimeType = part.get("mimeType")
                    if mimeType == "text/plain": # This is preferential
                        payload = part
                        break
                    elif mimeType == "text/html":
                        payload = part # In the absence of our preference, take this part

            # For non 'parts' MIME types
            data = payload['body']['data']
            decoded_data = urlsafe_b64decode(data)
            if mimeType == "text/html":
                soup = BeautifulSoup(decoded_data, "lxml")
                body = soup.body()
                text = str(body)
            elif mimeType == "text/plain":
                text = decoded_data.decode()
            else:
                raise NotImplementedError("Unknown MIME type")
        
        return text
