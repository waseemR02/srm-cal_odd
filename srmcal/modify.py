from __future__ import print_function

import os.path
import pickle
import argparse
from datetime import datetime
from dateutil import tz

import srmcal.dayorder as do

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar.events",
]

calendar_name = "6Sem_Theory"

def delete_calendar(service, calendar_id, time_min, time_max):
    calendar = service.calendars().get(calendarId=calendar_id).execute()
    print(calendar["summary"])
    page_token = None
    while True:
        events = service.events().list(calendarId=calendar_id, timeMin=time_min.astimezone().isoformat(),
                                       timeMax=time_max.astimezone().isoformat(), pageToken=page_token).execute()
        for e in events["items"]:
            print(f"Deleting event id: {e['id']} at time {e['start']['dateTime']}")
            service.events().delete(calendarId=calendar_id, eventId=e["id"]).execute()
        page_token = events.get("nextPageToken")
        if not page_token:
            break
    return calendar

def main(batch: str, pkl: str):
    creds = None
    # time_min = datetime(2024, 3, 25).replace(tzinfo=tz.gettz("Asia/Kolkata"))
    # time_max = datetime(2024, 6, 1).replace(tzinfo=tz.gettz("Asia/Kolkata"))
    time_min = datetime(2024, 3, 25)
    time_max = datetime(2024, 6, 1)
    calendar_id = "1add9d7b0a6ec8495f54c4fec31ecc9779faad5ebf57fdbb1c35bddba9c43cc4@group.calendar.google.com"
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    try:
        service = build("calendar", "v3", credentials=creds)
        calendar = delete_calendar(service, calendar_id, time_min, time_max)
        with open(pkl, "rb") as f:
            dayorders, courses = pickle.load(f)
        do_sched = {
            do.DayOrder.One: do.DayOrderSched(do.DayOrder.One, courses, batch),
            do.DayOrder.Two: do.DayOrderSched(do.DayOrder.Two, courses, batch),
            do.DayOrder.Three: do.DayOrderSched(do.DayOrder.Three, courses, batch),
            do.DayOrder.Four: do.DayOrderSched(do.DayOrder.Four, courses, batch),
            do.DayOrder.Five: do.DayOrderSched(do.DayOrder.Five, courses, batch),
        }
        # breakpoint()
        for day in filter(lambda x: x >= time_min and x < time_max, dayorders.keys()):
            order = dayorders[day]
            events = do_sched[order].add_events(day.astimezone())
            print(f"Generating {day}")
            for event in events:
                service.events().insert(calendarId=calendar["id"], body=event).execute()
    except HttpError as error:
        print("An error occurred: %s" % error)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Create a calendar for the semester's schedule"
    )
    ap.add_argument("batch", type=str, help="batch: odd or even")
    ap.add_argument(
        "pickle", help="path to pickle file containing dayorders and courses"
    )
    args = vars(ap.parse_args())

    main(args["batch"], args["pickle"])
