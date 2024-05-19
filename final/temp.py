import os
import json
import os.path
import google.oauth2.credentials
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():

  if os.path.isfile("credentials.json"):
    with open("credentials.json", 'r') as f:
      creds_data = json.load(f)
    creds = Credentials(creds_data['token'])

  else:
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    creds = flow.run_console()
    creds_data = {
          'token': creds.token,
          'refresh_token': creds.refresh_token,
          'token_uri': creds.token_uri,
          'client_id': creds.client_id,
          'client_secret': creds.client_secret,
          'scopes': creds.scopes
      }
    print(creds_data)
    with open("credentials.json", 'w') as outfile:
      json.dump(creds_data, outfile)
  return build(API_SERVICE_NAME, API_VERSION, credentials = creds)

def channels_list(service, **kwargs):
  results = service.channels().list(**kwargs).execute()
  print('This channel\'s ID is %s. Its title is %s, and it has %s views.' %
       (results['items'][0]['id'],
        results['items'][0]['snippet']['title'],
        results['items'][0]['statistics']['viewCount']))
   
if __name__ == '__main__':
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
  service = get_authenticated_service()

  channels_list(service, part='snippet,contentDetails,statistics', forUsername='GoogleDevelopers')
  # or if the above doesn't work
  channels_list(service, part='snippet,contentDetails,statistics', id='YOUR_YOUTUBE_CHANNEL_ID')