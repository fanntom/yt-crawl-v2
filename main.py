from googleapiclient.discovery import build
from utils import load_api_key, get_current_timestamp
from channel_manager import load_channel_list, save_channel_list, extract_channel_id, modify_channel_list
from broadcast_fetcher import fetch_broadcasts, save_broadcasts_to_csv
import os

def main():
    api_key = load_api_key()
    youtube = build('youtube', 'v3', developerKey=api_key)
    channels = load_channel_list()
    modify = 'no'

    if channels:
        print("Currently saved channels:")
        for idx, channel in enumerate(channels, start=1):
            print(f"{idx}. {channel['name']} ({channel['id']})")
        
        modify = input("Do you want to modify the channel list? (yes/no): ").lower()
        if modify == 'yes':
            channels = modify_channel_list(channels)
            save_channel_list(channels)  # Make sure to save any modifications
    else:
        print("No channels are currently saved.")
        response = input("Would you like to add channels now? (yes/no): ").strip().lower()
        if response == 'yes':
            modify = 'yes'
    
    if modify == 'yes':
        while True:
            url = input("Enter a YouTube channel URL (or 'no' to finish): ")
            if url.lower() == 'no':
                break
            channel_id, channel_name = extract_channel_id(url, youtube)
            if channel_id and channel_name:
                channels.append({"id": channel_id, "name": channel_name})
                print(f"Added channel: {channel_name}")
            else:
                print("Failed to add channel.")
        save_channel_list(channels)

    if channels:
        year = input("Enter a year to fetch broadcasts from: ")
        all_broadcasts = []
        for channel in channels:
            broadcasts = fetch_broadcasts(youtube, channel['id'], year)
            broadcasts_with_names = [(channel['name'],) + broadcast[1:] for broadcast in broadcasts]
            all_broadcasts.extend(broadcasts_with_names)
        
        if all_broadcasts:
            filename = f"{get_current_timestamp()}.csv"
            save_broadcasts_to_csv(all_broadcasts, filename)
            print(f"Broadcasts saved to {filename}")
        else:
            print("No broadcasts found for the given year.")

if __name__ == "__main__":
    main()
