import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from defs import *
import crawl
import pytz


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]
creds = None


# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first time.
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
        token.write(creds.to_json())

try:
    service = build("calendar", "v3", credentials=creds)
except HttpError as error:
        print(f"An error occurred: {error}")



def process_date(date):
    timezone = pytz.timezone('Asia/Taipei')  
    dt = datetime.datetime(*(int(i) for i in date.split('-')), tzinfo=timezone)
    timestamp = dt.isoformat()
    return timestamp
    

def get_events(service, start_day):
    start_day = process_date(start_day)
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=start_day,
            maxResults=3000,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
        print("No upcoming events found.")
        return
        
    return events


def create_events(service, previous_events):
    for date, todo_list in crawled_data.items():
        for course_name, assignment in todo_list:
            event_details = {
                "summary": assignment,
                "description": course_name,
                "start": {
                    'date': date,
                    "timeZone": TIMEZONE,
                },
                "end": {
                    'date': date,
                    "timeZone": TIMEZONE,
                },
                "reminders": {
                    "useDefault": False,
                    "overrides": [
                        {"method": "email", "minutes": EMAIL_NOTIFICATION * 60},
                        {"method": "popup", "minutes": POPUP_NOTIFICATION * 60},
                    ],
                },
            }

            flag = False
            try:
                for pre_event in previous_events:
                    if event_details['summary'] == pre_event.get('summary', 0) and \
                    event_details['description'] == pre_event.get('description', 0) and \
                    event_details['start']['date'] == pre_event.get('start', {}).get('date', 0):
                        print(f"{event_details['summary']} is duplicated !")
                        flag = True
                        break
            except TypeError:
                pass

            if flag:
                continue

            event = service.events().insert(calendarId="primary", body=event_details).execute()
            print(f"Event created {event_details['summary']} {event_details['description']} {event_details['start']['date']}")


if __name__ == "__main__":
    try:
        crawled_data = crawl.main()
        previous_events = get_events(service, list(crawled_data.items())[0][0])
        create_events(service, previous_events)
        input('--- Task Completes, Press Enter to Close ---')
    except:    
        input('! Task Terminated \nPlease Makesure You Setup Correct Usernames and Password in defs.py \nPress Enter to Close')
    quit()

