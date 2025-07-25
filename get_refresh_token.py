import os
import subprocess
import requests
import webbrowser
from termcolor import colored as c
from urllib.parse import urlencode
from get_user_info import get_reddit_credentials

(
  client_id, 
  client_secret, 
  user_agent, 
  refresh_token
) = get_reddit_credentials()

CLIENT_ID = client_id
CLIENT_SECRET = client_secret
REDIRECT_URI = 'http://localhost:8080/callback'
DURATION = 'permanent'
SCOPE = 'identity read submit history edit'

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

def write_to_clipboard(output: str):
	process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
	process.communicate(output.encode('utf-8'))
 
response_json = res.json()
refresh_token = response_json['refresh_token']
print(f"\n{c('Your refresh token is', 'blue')}: {refresh_token}")

write_to_clipboard(refresh_token)
print(c('\nYour refresh token has been copied to clipboard! Keep it somewhere safe!', 'green'))
