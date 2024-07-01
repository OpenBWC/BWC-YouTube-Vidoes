import os
import pymongo
from bson.objectid import ObjectId
import MongoConnection
from icecream import ic
import project_main as PM
from pprint import PrettyPrinter
from googleapiclient.discovery import build



def setup_yt_query():
    """This function creates the youtube model / object. Only run once.
    
    returns the youtube model object
    """

    youtube = build('youtube','v3', developerKey=PM.YT_CREDENTIALS)

    return youtube

def create_request(youtube_object, input_pageToken):
    """
    This function constructs the youtube request based on the previously created
    youtube_object AND the input_pageToken which gets results from different pages.
    
    returns the request that was created
    """

    request = youtube_object.playlistItems().list(part="snippet,contentDetails",
                                                  maxResults = 50,
                                                  pageToken=input_pageToken,
                                                  playlistId=PM.PA_PLAYLIST_ID)

    return request


def execute_request(created_request):
    """Executes the request that was created from the create_request function
    
    returns the response JSON object / type dictionary
    """
    response = created_request.execute()

    return response



# this function will use the 'nextPageToken' to iterate through the 
def iterate_through_pages():
        

    return False

def main(): 
    
    return False
   
if __name__ == "__main__":
    main()