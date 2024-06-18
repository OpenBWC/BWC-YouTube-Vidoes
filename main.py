import os


from dotenv import load_dotenv
from pprint import PrettyPrinter
from googleapiclient.discovery import build

# Load my api key that is stored as an environment variable into this environment
load_dotenv()
YT_CREDENTIALS = os.getenv("YOUTUBE_API_KEY")

#add the youtube id to the end of this preamble
yt_preamble = "https://www.youtube.com/watch?v="

# PoliceActivity channel id
Police_Activity_id = "UCXMYxKMh3prxnM_4kYZuB3g"

def main(): 
    
    youtube = build('youtube','v3', developerKey=YT_CREDENTIALS)
    print(type(youtube))


    request = youtube.search().list(part='snippet',channelId=Police_Activity_id, type='video',maxResults=50)
    print(type(request))
    
    res = request.execute()
    pp = PrettyPrinter()
    pp.pprint(res)

if __name__ == "__main__":


    main()