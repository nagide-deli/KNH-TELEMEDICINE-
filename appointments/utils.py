import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def create_google_meet(request, appointment):
    # 1. Retrieve stored OAuth2 credentials from session
    data = request.session.get('credentials')
    stored = request.user.google_credentials

    if not data:
        raise RuntimeError("No Google credentials found in session. Please connect your account at /googleauth/login/")

    # 2. Construct a Credentials object directly from that data
    creds = Credentials(
        token=stored.token,
        refresh_token=stored.refresh_token,
        token_uri=stored.token_uri,
        client_id=stored.client_id,
        client_secret=stored.client_secret,
        scopes=stored.get_scopes()
    )

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        # persist new access token
        stored.token = creds.token
        stored.save(update_fields=['token', 'updated_at'])

    # 3. Build the Calendar service
    service = build('calendar', 'v3', credentials=creds)

    # 4. Prepare event times
    start = datetime.datetime.combine(appointment.date, appointment.time)
    end = start + datetime.timedelta(minutes=30)

    # 5. Create the event with a Google Meet link
    event = {
      'summary': 'Telemedicine Appointment',
      'description': f'Appointment with Dr. {appointment.doctor.get_full_name()}',
      'start': {'dateTime': start.isoformat(), 'timeZone': 'Africa/Nairobi'},
      'end':   {'dateTime': end.isoformat(),   'timeZone': 'Africa/Nairobi'},
      'conferenceData': {
        'createRequest': {
          'requestId': f"meet-{appointment.id}",
          'conferenceSolutionKey': {'type': 'hangoutsMeet'}
        }
      },
      'attendees': [
        {'email': appointment.doctor.email},
        {'email': appointment.patient.email}
      ],
    }

    try:
        created = service.events().insert(
            calendarId='primary',
            body=event,
            conferenceDataVersion=1
        ).execute()
    except Exception as e:
        print("Google Calendar API error:", e)
        raise

    print("Event returned:", created)  
    link = created.get('hangoutLink')
    print("hangoutLink:", link)  
    return link

   