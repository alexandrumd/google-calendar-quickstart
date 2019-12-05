from __future__ import print_function
import datetime
import pickle
import os.path
import argparse
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# quickstart snippet from https://developers.google.com/calendar/quickstart/python
# you need to have a credentials.json file in the same folder with the correpsonding OAuth info

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    # parse timeMin/ timeMax if provided as args
    parser = argparse.ArgumentParser(description='Get busy calendar time by providing min/ max time values in the form e.g. 2019-12-04T00:00:00+02:00')
    parser.add_argument('--timeMin', '-min', type=str, 
                        help='min time to start search, in the form YYYY-MM-DDTHH:mm:ss+02:00 where +02:00 represents UTC zone')
    parser.add_argument('--timeMax', '-max', type=str, 
                        help='min time to start search, in the form YYYY-MM-DDTHH:mm:ss+02:00 where +02:00 represents UTC zone')
    args = parser.parse_args()

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

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
    
    # Get free/ busy info (it returns the busy times in a time range from a specific calendar)
    # docs - https://developers.google.com/calendar/v3/reference/freebusy/query
    print ('\n=== Now for the free/ busy part ===\n')
    calendar_id = 'primary'
    if not args.timeMin and not args.timeMax:
        # some hardcoded values in case they're not suplied as args
        timeMin = '2019-12-04T00:00:00+02:00'
        timeMax = '2019-12-04T23:59:00+02:00'
    else:
        timeMin = args.timeMin
        timeMax = args.timeMax
    body = {
        "timeMin": timeMin,
        "timeMax": timeMax,
        "timeZone": 'UTC',
        "items": [{"id": calendar_id}]
    }

    freebusy_result = service.freebusy().query(body=body).execute()
    slots = freebusy_result.get('calendars', {}).get(calendar_id, [])

    if not slots:
        # every slot in the timeframe is free
        print('No busy slots in the specified timeframe.')
    print (f'Busy slot(s) in the interval {timeMin} - {timeMax}: {slots}')


if __name__ == '__main__':
    main()