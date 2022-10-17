from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import dotenv_values

env = dotenv_values()


class GCal:
    TOKEN_FILE = 'token.json'
    CREDS_FILE = 'credentials.json'
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

    def __init__(self, max_results=10):
        self.max_results = max_results
        self.__creds = GCal.__auth()
        self.__service = build('calendar', 'v3', credentials=self.__creds)

    def get_next_events(self):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        try:
            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            print('Getting the upcoming 10 events')
            events_result = self.__service.events().list(calendarId=env['CALENDAR_ID'], timeMin=now,
                                                         maxResults=self.max_results,
                                                         singleEvents=True,
                                                         orderBy='startTime').execute()
            return events_result.get('items', [])

        except HttpError as error:
            print('An error occurred: %s' % error)
            return []

    @staticmethod
    def __auth() -> Credentials:
        _creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(GCal.TOKEN_FILE):
            _creds = Credentials.from_authorized_user_file(GCal.TOKEN_FILE, GCal.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not _creds or not _creds.valid:
            if _creds and _creds.expired and _creds.refresh_token:
                _creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    GCal.CREDS_FILE, GCal.SCOPES)
                _creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(GCal.TOKEN_FILE, 'w') as token:
                token.write(_creds.to_json())
        return _creds


if __name__ == '__main__':
    gcal = GCal()
    events = gcal.get_next_events()

    if not events:
        print('No upcoming events found.')

    # Prints the start and name of the next 10 events
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
