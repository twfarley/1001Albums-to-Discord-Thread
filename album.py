import os
import requests
import json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

GROUP = os.getenv("GROUP_SLUG")
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def get_group_info(group_slug):
    url = f"https://1001albumsgenerator.com/api/v1/groups/{group_slug}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def post_to_discord(content):
    resp = requests.post(WEBHOOK_URL, json={"content": content})
    if resp.status_code != 204: # Discord webhook returns 204 on success
        print(f"Failed to post to Discord. Status code: {resp.status_code}")
        print("Response body:", resp.text)
    else:
        print("Successfully posted to Discord.")

def format_album_post(data):
    if data is None: # Handle case where get_group_info failed
        return "Could not retrieve album information."

    current_album = data.get("currentAlbum")
    if not current_album:
        return "No current album available for the group."

    date_str = datetime.now().strftime("%B%d").replace("-0", "-")
    title = current_album.get("name", "Unknown Title")
    artist = current_album.get("artist", "Unknown Artist")
    year = current_album.get("releaseDate", "Unknown Year")
    spotify_id = current_album.get("spotifyId")
    spotify_url = f"https://open.spotify.com/album/{spotify_id}" if spotify_id else "No Spotify link available"
    return f"{date_str} - **{title}** by **{artist} ({year})**\n{spotify_url}"

def run():
    try:
        print(f"Fetching group info for: {GROUP}")
        group_data = get_group_info(GROUP)
        if group_data: # Only proceed if data was fetched successfully
            message = format_album_post(group_data)
            post_to_discord(message)
        else:
            print("Failed to get group data, skipping post.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    run()