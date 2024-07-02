from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from icecream import ic
from pprint import PrettyPrinter as pp
import Police_Activity_Scraper as PAS

"""
Global Variables
"""
COUNT = 0

load_dotenv()
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

uri = "mongodb+srv://" + MONGO_USERNAME +":" + MONGO_PASSWORD + "@cluster0.jxpmcwi.mongodb.net/?appName=Cluster0"
MONGO_CLIENT = MongoClient(uri, server_api=ServerApi('1'))
# yt-database is the database that I'll be storing the information from the yt-vids in
DATABASE = MONGO_CLIENT['yt-database']
UOF_COLLECTION = DATABASE['yt-force-used-vids'] # use of force
NUOF_COLLECTION = DATABASE['yt-no-force-vids'] # non-use of force

def confirm_connection(client):

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    for db_name in client.list_database_names():
        print(db_name)



def append_UOF_COLLECTION(dict_response):
    global COUNT
    """
    This function places takes the fields from the dictionary responses from Police Activity Scraper and inputs them into a mongoDB database
    according to the correct fields.

    DB outline: 

    Collection: yt-force-used-vids


        
    mandatory fields: 
    'fileNumber':COUNT,
    'video_title':"",
    'UOF_YT':True,
    'UOF_Decision_Tree':False,
    'YT_video_ID':"",
    'YT_channel_ID':"",
    'Video_Description':"",
    

    optional fields: 
    'YT_Playlist_ID':"",


    optional fields for machine learning part of processs
    'Objects_Detected':[]
    **Objects_detected as their own individual fields

    """
    document_dict = {
        'fileNumber':COUNT,
        'video_title':"",
        'UOF_YT':True,
        'UOF_Decision_Tree':False,
        'YT_video_ID':"",
        'YT_channel_ID':"",
        'Video_Description':"",
        
        }
    
    for key in dict_response:
        match key:
            # for every case it should match the field from the dict response and correlate it with the doc dict equivalent
            case "video_title":
                document_dict['video_title'] = dict_response['video_title']
            case "video_ID":
                document_dict['YT_video_ID'] = dict_response['video_ID']
            case "channel_ID":
                document_dict['YT_channel_ID'] = dict_response['channel_ID']
            case "video_description":
                document_dict['Video_Description'] = dict_response['video_description']
            case "playlist_ID": #will only create this field if the video is coming from a playlist
                document_dict['YT_Playlist_ID'] = dict_response['playlist_ID']
            case _:
                document_dict[key] = dict_response[key]




    UOF_COLLECTION.insert_one(document_dict)
    
    COUNT+=1

def append_UOF_COLLECTION(dict_response):

    return False
# def main():

#     client = create_client_connection()

#     confirm_connection(client)

# if __name__ == "__main__":
#     main()

# for db_name in MONGO_CLIENT.list_database_names():
#     pp.pprint(db)

