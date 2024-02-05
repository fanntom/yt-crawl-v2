import json
from datetime import datetime

def load_api_key(filename='api-key.json'):
    try:
        with open(filename) as f:
            data = json.load(f)
            return data['youtube_api_key']
    except FileNotFoundError:
        print("API key file not found.")
        return None

def get_current_timestamp():
    return datetime.now().strftime("%Y%m%d-%H%M%S")
