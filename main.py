import utils
from datetime import datetime


if __name__ == "__main__":
    print("Starting playlist creation...")
    config = utils.load_config()

    playlists = config.get("playlist_urls", [])
    all_tracks = []
    for playlist_url in playlists:
        playlist_id = playlist_url.split("playlist/")[1].split("?")[0]
        tracks = utils.get_tracks_from_playlist(playlist_id)
        tracks.reverse()  # Get latest songs first
        all_tracks.extend(tracks)

    # Remove duplicates and filter valid track URIs
    all_tracks = list(dict.fromkeys(all_tracks))
    all_tracks = [track for track in all_tracks if track.startswith("spotify:track")]
    print(f"Total unique tracks: {len(all_tracks)}")

    datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_id = utils.get_user_id()
    playlist_name = config.get('playlist_name', 'New Playlist')
    playlist_description = config.get('playlist_description', '')

    if config.get('add_last_update_to_description', False):
        playlist_description = f"{playlist_description} Last updated: {datetime_now}"

    playlist_image = config.get('playlist_image')
    utils.create_playlist(user_id, playlist_name, playlist_description, all_tracks, playlist_image)
    