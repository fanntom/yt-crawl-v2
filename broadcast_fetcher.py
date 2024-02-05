from googleapiclient.discovery import build
import csv
import os

def fetch_broadcasts(youtube, channel_id, year):
    broadcasts = []
    next_page_token = None
    
    print(f"Fetching completed live broadcasts for channel ID {channel_id} for the year {year}...")
    while True:
        search_request = youtube.search().list(
            channelId=channel_id,
            part="id,snippet",
            type="video",
            eventType="completed",
            videoType="any",
            publishedAfter=f"{year}-01-01T00:00:00Z",
            publishedBefore=f"{year}-12-31T23:59:59Z",
            maxResults=50,
            pageToken=next_page_token
        )
        search_response = search_request.execute()
        
        video_ids = [item['id']['videoId'] for item in search_response['items']]
        if video_ids:
            video_request = youtube.videos().list(
                part='snippet,statistics',
                id=','.join(video_ids)
            ).execute()
            
            for video_item in video_request['items']:
                title = video_item['snippet']['title']
                published_at = video_item['snippet']['publishedAt']
                broadcast_day = published_at.split("T")[0]
                view_count = video_item['statistics'].get('viewCount', '0')
                like_count = video_item['statistics'].get('likeCount', '0')
                comment_count = video_item['statistics'].get('commentCount', '0')
                broadcasts.append((channel_id, title, "https://www.youtube.com/watch?v="+video_item['id'], broadcast_day, view_count, like_count, comment_count))

        next_page_token = search_response.get('nextPageToken')
        if not next_page_token:
            break
    
    return broadcasts


def save_broadcasts_to_csv(broadcasts, filename):
    data_directory = "data"
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)
    
    # Adjust the file path to include the data directory
    file_path = os.path.join(data_directory, filename)
    with open(file_path, 'w', encoding='utf-16') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['Channel Name', 'Broadcast Title', 'Video ID', 'Broadcast Day', 'View Count', 'Like Count', 'Comment Count'])
        writer.writerows(broadcasts)
