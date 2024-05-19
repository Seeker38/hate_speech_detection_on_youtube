from Google import Create_Service

API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

CLIENT_SECRETS_FILE = "D:/final/client_secret.json"
SCOPES = [
        'https://www.googleapis.com/auth/youtube.force-ssl',
        'https://www.googleapis.com/auth/youtube',
        'https://www.googleapis.com/auth/youtubepartner',
]
service = Create_Service(CLIENT_SECRETS_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)