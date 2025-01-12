import os
import requests
import webbrowser
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:8080/callback'
DURATION = 'permanent'
SCOPE = 'identity read'

creds = {
	'client_id': CLIENT_ID,
	'response_type': 'code',
	'state': 'random_string',
	'redirect_uri': REDIRECT_URI,
	'duration': DURATION,
	'scope': SCOPE
}

auth_url = f"https://www.reddit.com/api/v1/authorize?{urlencode(creds)}"

print(f"Go to the following URL to authorize your bot: {auth_url}")
webbrowser.open(auth_url)

auth_code = input("Enter the authorization code: ")

auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)

data = {
	'grant_type': 'authorization_code',
	'code': auth_code,
	'redirect_uri': REDIRECT_URI
}

headers = {'User-Agent': 'MyBot/0.0.1'}

res = requests.post('https://www.reddit.com/api/v1/access_token',
					 auth=auth, data=data, headers=headers)

response_json = res.json()
refresh_token = response_json['refresh_token']
print(f"\033[94mYour refresh token is\033[0m: {refresh_token}")