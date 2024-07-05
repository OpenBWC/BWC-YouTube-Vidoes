from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from pprint import PrettyPrinter as pp
import Police_Activity_Scraper as PAS

"""
Global Variables
"""
COUNT = 0
MONGO_USERNAME = ""
MONGO_PASSWORD = ""






def get_mongo_creds():
    global MONGO_USERNAME
    global MONGO_PASSWORD

    load_dotenv()
    MONGO_USERNAME = os.getenv("MONGO_USERNAME")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

def construct_mongo_connection():
    uri = "mongodb+srv://" + MONGO_USERNAME +":" + MONGO_PASSWORD + "@cluster0.jxpmcwi.mongodb.net/?appName=Cluster0"
    mongo_client = MongoClient(uri, server_api=ServerApi('1'))
    

    test_mongo_connection(mongo_client)

def create_establish_yt_database():
    global YT_DATABASE

    if 'yt-database' in MONGO_CLIENT.list_database_names():
        YT_DATABASE = MONGO_CLIENT['yt-database']
    else:
        print("yt-database does not exist")

def instantiate_UOF_collection():
    global UOF_COLLECTION
    
    UOF_COLLECTION = YT_DATABASE['yt-force-used-vids']
def instantiate_NUOF_database():
    global NUOF_COLLECTION

    NUOF_COLLECTION = YT_DATABASE['yt-no-force-vids']

def test_mongo_connection(mongo_client):

    # Send a ping to confirm a successful connection
    try:
        mongo_client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    for db_name in mongo_client.list_database_names():
        print(db_name)

def append_UOF_COLLECTION(dict_response):
    global COUNT
    global UOF_COLLECTION
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
    
    query = {'YT_video_ID': dict_response['video_ID']}
    results =  UOF_COLLECTION.count_documents(query)

    if results == 0:
        return False
    
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


def main():
    get_mongo_creds()
    

    construct_mongo_connection()

    #create_establish_yt_database()

    #instantiate_UOF_collection()





if __name__ == "__main__":
    main()

