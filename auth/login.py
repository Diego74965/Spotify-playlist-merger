import requests, base64, json, urllib.parse
from flask import Flask, request, redirect
import json
import time

with open('config.json', 'r') as f:
    config = json.load(f)

CLIENT_ID = config['client_id']
CLIENT_SECRET = config['client_secret']
REDIRECT_URI = config['redirect_uri']
SCOPE = config['scope']


auth_url = config['auth_url']
token_url = config['token_url']

app = Flask(__name__)

@app.route('/')
def login():
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPE
    }
    url = f"{auth_url}?{urllib.parse.urlencode(params)}"
    return redirect(url)


@app.route('/callback')
def callback():
    code = request.args.get('code')
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }

    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(token_url, data=payload, headers=headers)
    token_info = response.json()
    token_info['expires_at'] = int(time.time()) + token_info['expires_in']

    with open('auth.json', 'w') as f:
        json.dump(token_info, f, indent=2)
    return "Login successful! You can close this window."


if __name__ == '__main__':
    app.run(port=8888)