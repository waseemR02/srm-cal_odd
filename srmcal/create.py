from __future__ import print_function

import datetime
import os.path
import pickle
import sys

import srmcal.dayorder as do

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/calendar.events']

calendar_name = "6Sem_Theory"

def create_calendar(service, calendar_name):
    calendar = {
        'summary': calendar_name,
        'timeZone': 'Asia/Kolkata'
    }
    created_calendar = service.calendars().insert(body=calendar).execute()
    return created_calendar
def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('calendar', 'v3', credentials=creds)
        calendar = create_calendar(service, calendar_name)
        with open(sys.argv[1], 'rb') as f:
            dayorders, courses = pickle.load(f)
        do_sched = {
            do.DayOrder.One: do.DayOrderSched(do.DayOrder.One, courses),
            do.DayOrder.Two: do.DayOrderSched(do.DayOrder.Two, courses),
            do.DayOrder.Three: do.DayOrderSched(do.DayOrder.Three, courses),
            do.DayOrder.Four: do.DayOrderSched(do.DayOrder.Four, courses),
            do.DayOrder.Five: do.DayOrderSched(do.DayOrder.Five, courses)
        }
        # breakpoint()
        for day in dayorders.keys():
            order = dayorders[day]
            events = do_sched[order].add_events(day.astimezone())
            print(f"Generating {day}")
            for event in events:
                service.events().insert(calendarId=calendar['id'],
                                        body=event).execute()
    except HttpError as error:
        print('An error occurred: %s' % error)
  
if __name__ == '__main__':
    main()

