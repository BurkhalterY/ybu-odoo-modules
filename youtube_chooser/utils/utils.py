import re

import requests


def iso8601_to_minutes(duration):
    if not duration:
        return 0
    pattern = re.compile(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?")
    match = pattern.match(duration)
    if not match:
        return 0

    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    seconds = int(match.group(3)) if match.group(3) else 0

    total_minutes = hours * 60 + minutes + seconds / 60
    return total_minutes


def get_channel_id(channel_name, api_key):
    api_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": channel_name,
        "type": "channel",
        "key": api_key,
    }
    response = requests.get(api_url, params=params)
    if response.status_code != 200:
        return
    data = response.json()
    if "items" in data and len(data["items"]) > 0:
        return data["items"][0]["id"]["channelId"]
