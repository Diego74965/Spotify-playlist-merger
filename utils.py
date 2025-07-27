import json
import base64
import requests
import time

CONFIG_FILE = 'config.json'
AUTH_FILE = 'auth.json'
def load_config():
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

# Load configuration from config.json
config = load_config()
CLIENT_ID = config['client_id']
CLIENT_SECRET = config['client_secret']
REDIRECT_URI = config['redirect_uri']

def load_auth():
    with open(AUTH_FILE, 'r') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def save_auth(auth):
    with open(AUTH_FILE, 'w') as f:
        json.dump(auth, f, indent=2)


def refresh_access_token(refresh_token):
    token_url = 'https://accounts.spotify.com/api/token'
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }

    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(token_url, data=payload, headers=headers)
    data = response.json()

    if 'access_token' in data:
        config = load_config()
        config['access_token'] = data['access_token']
        config['expires_at'] = int(time.time()) + data['expires_in']
        return data['access_token']
    else:
        raise Exception(f"Failed to refresh token: {data}")


def get_access_token():
    auth = load_auth()
    now = int(time.time())

    if now >= auth.get('expires_at', 0):
        print("🔄 Access token expired. Refreshing...")
        return refresh_access_token(auth['refresh_token'])

    return auth['access_token']


def get_headers():
    token = get_access_token()
    return {
        'Authorization': f'Bearer {token}'
    }


def get_user_id():
    headers = get_headers()
    url = "https://api.spotify.com/v1/me"
    response = requests.get(url, headers=headers)
    data = response.json()
    return data['id']


def get_tracks_from_playlist(playlist_id):
    headers = get_headers()
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    all_tracks = []
    print(f"Fetching tracks from playlist: {playlist_id}")
    while url:
        response = requests.get(url=url, headers=headers)
        data = response.json()
        all_tracks.extend([
            item['track']['uri']
            for item in data.get('items', [])
            if item.get('track') is not None
        ])
        url = data.get('next')
    return all_tracks


def create_playlist(user_id, name, description, track_uris, playlist_image=None):
    print(f"Creating playlist '{name}' for user '{user_id}'...")

    headers = get_headers()
    headers['Content-Type'] = 'application/json'
    print(f"Headers: {headers}")
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    data = {
        "name": name,
        "description": description,
        "public": True
    }
    response = requests.post(url=url, headers=headers, json=data)
    response.raise_for_status()
    playlist_id = response.json()['id']

    # Add image to the playlist if provided
    if playlist_image:
        print(f"Uploading image for playlist '{name}'...")
        upload_playlist_image(playlist_id, playlist_image)

    # Add songs to the playlist in batches of 100
    print(f"Adding {len(track_uris)} tracks to playlist '{name}'...")
    for i in range(0, len(track_uris), 100):
        print(f"Adding tracks {i + 1} to {min(i + 100, len(track_uris))}...")
        chunk = track_uris[i:i + 100]
        add_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        res = requests.post(url=add_url, headers=headers, json={"uris": chunk})
        if res.status_code != 201:
            print(f"Error adding tracks: {res.status_code} - {res.text}")
            print(f"Request body: {{'uris': {chunk}}}")

    print(f"Playlist '{name}' created at: https://open.spotify.com/playlist/{playlist_id}")
    return playlist_id


def upload_playlist_image(playlist_id, image_path):
    headers = get_headers()
    headers['Content-Type'] = 'image/jpeg'
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/images"

    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()

    image_b64 = base64.b64encode(image_data)

    if len(image_b64) > 262144:
        print(f"Error: Base64-encoded image exceeds 256KB (actual size: {len(image_b64)} bytes). Upload aborted.")
        return

    response = requests.put(url=url, headers=headers, data=image_b64)    
    response.raise_for_status()
    print(f"Image uploaded successfully for playlist '{playlist_id}'")