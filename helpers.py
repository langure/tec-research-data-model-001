from dotenv import dotenv_values
from googleapiclient.discovery import build
import pandas as pd

from entities import *

REQUIRED_ENV_VARS = ['GOOGLE_API_KEY', 'MAX_RESULTS', "DB_HOST", "DB_NAME", "DB_USER", "DB_PASSWORD", "DB_PORT", "YT_CHANNELS_FILE"]

env_variables = dotenv_values('.env')

def validate_env_vars():
    for var in REQUIRED_ENV_VARS:
        value = env_variables.get(var)
        if value is None or value.strip() == "":
            raise Exception(f'{var} is not set or has an empty value in the .env file')

def get_youtube_channel_data_from_seed_file(channel_id):
    seed_file = env_variables['YT_CHANNELS_FILE']
    seed_contents = pd.read_excel(seed_file, sheet_name="run")
    channel_data = seed_contents[seed_contents['id'] == channel_id]
    
    return channel_data.to_dict(orient='records')[0] if not channel_data.empty else None
    
        
def get_youtube_data_from_seed_file():
    seed_file = env_variables['YT_CHANNELS_FILE']
    seed_contents = pd.read_excel(seed_file, sheet_name="run")
    return seed_contents.to_dict(orient='records')
    

def get_youtube_channel_info_from_id(channel_id):
    api_key = env_variables['GOOGLE_API_KEY']
    resource = build('youtube', 'v3', developerKey=api_key)
    response = resource.channels().list(
        part='snippet,statistics',
        id=channel_id
    ).execute()
    
    if 'items' in response:
        channel = response['items'][0]
        return YouTubeChannel(
            you_tube_id = channel['id'],
            title = channel['snippet']['title'],
            description = channel['snippet']['description'],
            subscribers = channel['statistics']['subscriberCount'],
            views = channel['statistics']['viewCount'],
            videos = channel['statistics']['videoCount'])
    else:
        return None

def get_youtube_comments_from_video_id(video_id):
    api_key = env_variables['GOOGLE_API_KEY']
    max_results = int(env_variables['MAX_RESULTS'])
    resource = build('youtube', 'v3', developerKey=api_key)

    all_comments = []
    total_results = 0

    # Initial request
    response = resource.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=min(max_results, 100),
        order='orderUnspecified').execute()

    # Process initial response
    all_comments.extend(response['items'])
    total_results += len(response['items'])

    # Paginate through remaining comments
    while 'nextPageToken' in response and total_results < max_results:
        response = resource.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=min(max_results - total_results, 100),
            order='orderUnspecified',
            pageToken=response['nextPageToken']).execute()

        all_comments.extend(response['items'])
        total_results += len(response['items'])

    yt_comments = []

    for comment in all_comments:
        snippet = comment['snippet']['topLevelComment']['snippet']
        yt_comments.append(YouTubeComment(
            youtube_id=comment['id'],
            channel_youtube_id=video_id,
            author=snippet['authorDisplayName'],
            text=snippet['textDisplay'],
            likes=snippet['likeCount'],
            date=snippet['publishedAt']))

    return yt_comments

