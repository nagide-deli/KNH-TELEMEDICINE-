from datetime import datetime

from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from django.shortcuts import redirect
import os


def google_calendar_redirect(request):
    flow = Flow.from_client_secrets_file(
        'client_secrets.json', scopes=['https://www.googleapis.com/auth/calendar'],
        redirect_uri= ''
    )

    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials


    service = build('calendar', 'v3', credentials=credentials)

    event = {
        'summary': 'Appointment with doctor',
        'description': 'Appointment with doctor',
        'start': {
            'dateTime': str(datetime.datetime.now()),
            'timeZone': 'Africa/Nairobi',
        },

        'end': {
            'dateTime': str(datetime.datetime.now()),
            'timeZone': 'Africa/Nairobi',

        },
        'conferenceData': {
            'createRequest': {
                'requestId': 'sample123',  # Use UUID
                'conferenceSolutionKey': {'type': 'hangoutsMeet'},
            },

            },



    }
    created_event = service.events().insert(
        calendarId='primary',
        body=event,
        conferenceDataVersion=1
    ).execute()

    meet_link = created_event['hangoutLink']
    # Save meet_link to your appointment model

    return redirect('/')  # or any response you prefer

# Create your views here.
