from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from django.shortcuts import redirect
from django.http import HttpResponse
from google_auth_oauthlib.flow import Flow

from googleauth.models import GoogleCredentials

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, 'telehealth', 'secrets', 'credentials.json')
SCOPES = ['https://www.googleapis.com/auth/calendar.events']
REDIRECT_URI = 'http://127.0.0.1:8000/googleauth/oauth2callback/'

@login_required
def google_login(request):
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE,
                                         scopes=SCOPES,
                                         redirect_uri=REDIRECT_URI,
                                         )

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )

    request.session['state'] = state
    return redirect(authorization_url)
@login_required
def oauth2callback(request):
    state = request.session['state']
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri=REDIRECT_URI,
    )
    flow.fetch_token(authorization_response=request.build_absolute_uri())

    credentials = flow.credentials


    GoogleCredentials.objects.update_or_create(
        user=request.user,
        defaults={
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes

        }
    )

    return HttpResponse("Google account successfully connected!")


# Create your views here.
