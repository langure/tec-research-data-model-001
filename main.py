from helpers import *

if __name__ == '__main__':
    try:
        validate_env_vars()
        yt_comments = get_youtube_comments_from_video_id('QwievZ1Tx-8')
        db_driver = DatabaseDriver(username=env_variables['DB_USER'], 
                                   password=env_variables['DB_PASSWORD'],
                                   host=env_variables['DB_HOST'],
                                   port=env_variables['DB_PORT'],
                                   database=env_variables['DB_NAME'])
        db_driver.initialize_database()
        for comment in yt_comments:
            db_driver.save_youtube_comment(comment)
    except Exception as e:
        print(e)