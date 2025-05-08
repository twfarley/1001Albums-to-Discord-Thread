import os
import requests
import json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

GROUP = os.getenv("GROUP_SLUG")
WEBHOOK_URL = os.getenv(" ")

def get_group_info(group_slug):
    url = f"https://1001albumsgenerator.com/api/v1/groups/{group_slug}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()
    response = requests.get(url)
    data = response.json()
    print(json.dumps(data, indent=2))

def post_to_discord(content):
    resp = requests.post(WEBHOOK_URL, json={"content": content})
    if resp.status_code != 204:
        print("Failed to post:", resp.text)

def format_album_post(data):
    current_album = data.get("currentAlbum")
    if not current_album:
        return "No current album available."

    date_str = datetime.now().strftime("%B%d")
    title = current_album.get("name")
    artist = current_album.get("artist")
    year = current_album.get("year")
    url = current_album.get("url") or "https://1001albumsgenerator.com"
    return f"{date_str} - {title} by {artist} ({year})\n{url}"

def run():
    while True:
        try:
            group_data = get_group_info(GROUP)
            message = format_album_post(group_data)
            post_to_discord(message)
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    run()