# Spotify Playlist Merger

Easily merge multiple Spotify playlists into a single playlist on your account, with support for custom images, deduplication, and automatic updates.

## Features
- Merge tracks from multiple Spotify playlists into one
- Remove duplicate tracks automatically
- Add a custom image to your playlist
- Automatically update playlist description with the last update date
- Simple configuration via JSON

## Requirements
- Python 3.8+ (I used Python 3.13)
- A Spotify account
- Spotify Developer credentials (Client ID and Client Secret)

## Installation

1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd Spotify
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # Or on Unix/macOS:
   # source .venv/bin/activate
   ```

3. **Install the requirements:**
   ```sh
   pip install -r requirements.txt
   ```

## Spotify App Setup

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) and create a new app.
2. Note your **Client ID** and **Client Secret**.
3. In your app settings, add `http://127.0.0.1:8888/callback` to the Redirect URIs.

## Configuration

1. **Edit `config-test.json`:**
   - Edit config-test.json and rename it config.json
   - Fill in your `client_id` and `client_secret` from the Spotify Developer Dashboard.
   - Set your desired playlist name, description, and the list of playlist URLs to merge.
   - Optionally, set `playlist_image` to the path of a local image (JPEG, max 256KB) to use as the playlist cover.

## Authentication

1. **Run the login server to authenticate your account:**
   ```sh
   python auth/login.py
   ```
   - This will open a browser window for you to log in and authorize the app.
   - After successful login, an `auth.json` file will be created with your tokens.

## Usage

1. **Run the main script:**
   ```sh
   python main.py
   ```
   - The script will fetch tracks from all playlists listed in `config.json`, remove duplicates, and create a new playlist in your account.
   - If `playlist_image` is set, it will upload the image as the playlist cover.
   - The playlist description will include the last update date if enabled.

## Troubleshooting

- **Token expired or invalid?**
  - Delete `auth.json` and re-run `python auth/login.py` to re-authenticate.
- **Image upload fails?**
  - Ensure the image is JPEG and less than 256KB after base64 encoding.
- **Missing dependencies?**
  - Re-run `pip install -r requirements.txt`.
- **API errors?**
  - Check your `client_id`, `client_secret`, and playlist URLs in `config.json`.

## File Overview

- `main.py` — Main script to merge playlists
- `utils.py` — Helper functions for Spotify API
- `auth/login.py` — Handles Spotify OAuth login
- `config.json` — Main configuration file
- `auth.json` — Stores your access and refresh tokens (auto-generated)
- `requirements.txt` — Python dependencies
- `meowth.jpg` — Example playlist image (replaceable)

