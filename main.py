import argparse
import colorama
from colorama import Back, Fore, Style
from helpers import *

# Initialize colorama
colorama.init()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--initializeDB', action='store_true')
    args = parser.parse_args()

    try:
        validate_env_vars()        
        db_driver = DatabaseDriver(username=env_variables['DB_USER'], 
                                   password=env_variables['DB_PASSWORD'],
                                   host=env_variables['DB_HOST'],
                                   port=env_variables['DB_PORT'],
                                   database=env_variables['DB_NAME'])
        
        if args.initializeDB:
            print(Back.RED + Fore.WHITE + Style.BRIGHT + "Are you sure you want to erase and re-create the database? (Yes/No): " + Style.RESET_ALL, end='')
            confirmation = input()
            if confirmation.lower() == 'yes':
                db_driver.initialize_database()
                print("Database initialized.")
            else:
                print("Operation canceled.")
        else:
            # Get the data from the seed file
            youtube_seed_data = get_youtube_data_from_seed_file()
            youtube_channels_seed_data = set()
            for video in youtube_seed_data:
                print(f"Retrieving comments from video {video['video_id']} of channel {video['id']}")                
                yt_comments = get_youtube_comments_from_video_id(video['video_id'])
                youtube_channels_seed_data.add(video['id'])            
                for comment in yt_comments:
                    db_driver.save_youtube_comment(comment)
            
            for channel_id in youtube_channels_seed_data:
                channel_info = get_youtube_channel_data_from_seed_file(channel_id)
                yt_channel = get_youtube_channel_info_from_id(channel_id)
                yt_channel.audience_gender = channel_info['audience_gender']
                yt_channel.audience_avg_age = channel_info['audience_avg_age']
                yt_channel.topic = channel_info['topic']
                yt_channel.country = channel_info['country']
                yt_channel.language = channel_info['language']
                db_driver.save_youtube_channel(yt_channel)
    except Exception as e:
        print(e)

# Deinitialize colorama
colorama.deinit()