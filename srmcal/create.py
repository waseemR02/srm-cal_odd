from __future__ import print_function

import os.path
import pickle
import argparse

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


def create_calendar(service, calendar_name):
    calendar = {"summary": calendar_name, "timeZone": "Asia/Kolkata"}
    created_calendar = service.calendars().insert(body=calendar).execute()
    return created_calendar


def main(batch: str, pkl: str):
    creds = None
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
        calendar = create_calendar(service, calendar_name)
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
        for day in dayorders.keys():
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
