import os.path
import pickle
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_google_calendar_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)

def create_calendar_event(interview):
    service = get_google_calendar_service()

    # Prepare attendees list including interviewers and the candidate
    attendees = [{'email': interviewer.user.email} for interviewer in interview.interviewers.all()]
    attendees.append({'email': interview.candidat.email})

    event = {
        'summary': interview.title,
        'location': interview.location,
        'description': interview.description,
        'start': {
            'dateTime': interview.start_datetime.isoformat(),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': interview.end_datetime.isoformat(),
            'timeZone': 'UTC',
        },
        'conferenceData': {
            'createRequest': {
                'requestId': datetime.utcnow().isoformat(),
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet'
                }
            }
        },
        'attendees': attendees,  # Use the combined list of interviewers and candidate
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    created_event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1, sendUpdates='all').execute()
    return created_event['id'], created_event['hangoutLink']

def update_calendar_event(interview):
    service = get_google_calendar_service()

    # Prepare attendees list including interviewers and the candidate
    attendees = [{'email': interviewer.user.email} for interviewer in interview.interviewers.all()]
    attendees.append({'email': interview.candidat.email})

    event = {
        'summary': interview.title,
        'location': interview.location,
        'description': interview.description,
        'start': {
            'dateTime': interview.start_datetime.isoformat(),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': interview.end_datetime.isoformat(),
            'timeZone': 'UTC',
        },
        'attendees': attendees,  # Use the combined list of interviewers and candidate
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    updated_event = service.events().update(calendarId='primary', eventId=interview.id_event, body=event, sendUpdates='all').execute()
    return updated_event['hangoutLink']

def delete_calendar_event(interview):
    service = get_google_calendar_service()
    service.events().delete(calendarId='primary', eventId=interview.id_event, sendUpdates='all').execute()
