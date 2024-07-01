import os
from dotenv import load_dotenv

'''
Project Global Variables

YT_Credentials --> api key for youtube api access
POLICE_ACTIVITY_ID --> id of the police activity youtube channel
PA_PLAYLIST_ID --> id of the playlist of all uploads from the police activity
youtube channel
'''
load_dotenv()
YT_CREDENTIALS = os.getenv("YOUTUBE_API_KEY")
POLICE_ACTIVITY_ID = "UCXMYxKMh3prxnM_4kYZuB3g"
PA_PLAYLIST_ID = "PL7csYbrPKf-zz09U1uVvt0ew00Myy4gIP"