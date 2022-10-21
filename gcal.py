from __future__ import print_function

import datetime
import os.path
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import dotenv_values

env = dotenv_values()


def is_match(text, pattern=r'^[A-Za-z_][0-9A-Za-z_]*$'):
    """Check if variable has proper naming convention"""
    return bool(re.compile(pattern).search(text))


class GCal:
    SCOPES = env['GCAL_SCOPES'].split(',')

    def __init__(self, max_results=10):
        self.max_results = max_results
        self.__creds = GCal.__auth()
        self.__service = build('calendar', 'v3', credentials=self.__creds)

    def get_next_events(self):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        def get_event_args(event: dict):
            args = {}
            lines = event.get('description', '').split('\n')
            for line in lines:
                parts = line.split('=')
                if len(parts) == 2 and is_match(parts[0]):
                    args[parts[0]] = parts[1]
            return args

        try:
            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            print('Getting the upcoming 10 events')
            events_result = self.__service.events().list(calendarId=env['GCAL_ID'], timeMin=now,
                                                         maxResults=self.max_results,
                                                         singleEvents=True,
                                                         orderBy='startTime').execute()
            events = events_result.get('items', [])
            for event in events:
                event['args'] = get_event_args(event)
            return events

        except HttpError as error:
            print('An error occurred: %s' % error)
            return []

    @staticmethod
    def __auth() -> Credentials:
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(env['GCAL_TOKEN_FILE']):
            creds = Credentials.from_authorized_user_file(env['GCAL_TOKEN_FILE'], GCal.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    env['GCAL_CREDS_FILE'], GCal.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(env['GCAL_TOKEN_FILE'], 'w') as token:
                token.write(creds.to_json())
        return creds


if __name__ == '__main__':
    gcal = GCal()
    events = gcal.get_next_events()

    if not events:
        print('No upcoming events found.')

    # Prints the start and name of the next 10 events
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
