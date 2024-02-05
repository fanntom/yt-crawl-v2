import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re
from utils import load_api_key
api_key = load_api_key()
def load_channel_list(filename='channel-list.json'):
    try:
        with open(filename, 'r', encoding='utf-16') as f:
            channels = json.load(f)
        return channels
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON from the channel list file.")
        return []


def save_channel_list(channels, filename='channel-list.json'):
    with open(filename, 'w', encoding='utf-16') as f:
        json.dump(channels, f, ensure_ascii=False, indent=4)


def extract_channel_id(url, youtube):
    match = re.search(r'youtube\.com/@([^/?&]+)', url)
    username = match.group(1)
    youtube = build("youtube", "v3", developerKey=api_key)
    if "@" in url:
        try:
            request = youtube.search().list(
                q=username,
                type='channel',
                part='snippet',
                maxResults=1
            ).execute()

            if request["items"]:
                channel_id = request['items'][0]['snippet']['channelId']
                channel_name = request['items'][0]['snippet']['title']
                return channel_id, channel_name
        except HttpError as e:
            print(f"An error occurred: {e}")
    else:
        match = re.search(r'channel/([a-zA-Z0-9_-]+)', url)
        if match:
            channel_id = match.group(1)
            request = youtube.channels().list(id=channel_id, part='snippet')
            response = request.execute()
            if response['items']:
                channel_name = response['items'][0]['snippet']['title']
                return channel_id, channel_name
    return None, None

def modify_channel_list(channels):
    print("Current channels:")
    for idx, channel in enumerate(channels, start=1):
        print(f"{idx}. {channel['name']}")
    removals = input("Enter the numbers of channels to remove (comma separated): ")
    for idx in removals.split(","):
        try:
            idx = int(idx.strip()) - 1
            if 0 <= idx < len(channels):
                channels.pop(idx)
        except ValueError:
            continue
    return channels
