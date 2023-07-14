from dotenv import dotenv_values
from googleapiclient.discovery import build
from entities import *

REQUIRED_ENV_VARS = ['GOOGLE_API_KEY', 'MAX_RESULTS', "DB_HOST", "DB_NAME", "DB_USER", "DB_PASSWORD", "DB_PORT"]

env_variables = dotenv_values('.env')

def validate_env_vars():
    for var in REQUIRED_ENV_VARS:
        value = env_variables.get(var)
        if value is None or value.strip() == "":
            raise Exception(f'{var} is not set or has an empty value in the .env file')

        

def get_youtube_video_info_from_id(video_id):
    api_key = env_variables['GOOGLE_API_KEY']
    resource = build('youtube', 'v3', developerKey=api_key)
    response = resource.channels().list(
        part='snippet,statistics',
        id=video_id
    ).execute()

def get_youtube_comments_from_video_id(video_id):
    api_key = env_variables['GOOGLE_API_KEY']
    resource = build('youtube', 'v3', developerKey=api_key)
    response = resource.commentThreads().list(
        part='snippet',
        videoId = video_id,
        maxResults=env_variables['MAX_RESULTS'],
        order='orderUnspecified').execute()    
    
    comments = response['items']
    
    yt_comments = []
    
    for comment in comments:
        snippet = comment['snippet']['topLevelComment']['snippet']
        yt_comments.append(YouTubeComment(
            youtube_id = comment['id'],
            author = snippet['authorDisplayName'],
            text = snippet['textDisplay'],
            likes = snippet['likeCount'],
            date = snippet['publishedAt']))
    
    return yt_comments