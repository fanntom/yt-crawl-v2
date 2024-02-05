from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re

def get_channel_id_from_api(url, api_key):
    match = re.search(r'youtube\.com/@([^/?&]+)', url)
    if not match:
        print("URL does not contain a valid @username format.")
        return None
    
    username = match.group(1)
    youtube = build("youtube", "v3", developerKey=api_key)

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
    
    return None

# Example usage
api_key = "AIzaSyCdOjQ0b6zaskxwTlPO8hNniaXaBKLedjg"  # Replace with your actual API key
url = "https://www.youtube.com/@ow_esports_kr"
channel_id = get_channel_id_from_api(url, api_key)
if channel_id:
    print(f"Found Channel ID: {channel_id}")
else:
    print("No channel found or an error occurred.")
