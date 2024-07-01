import os
from dotenv import load_dotenv

'''
Project Global Variables
'''
load_dotenv()
YT_CREDENTIALS = os.getenv("YOUTUBE_API_KEY")

# PoliceActivity channel id
POLICE_ACTIVITY_ID = "UCXMYxKMh3prxnM_4kYZuB3g"
# Main PoliceActvity Playlist id
PA_PLAYLIST_ID = "PL7csYbrPKf-zz09U1uVvt0ew00Myy4gIP"