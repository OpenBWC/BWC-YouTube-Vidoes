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

def place_in_mongoDB():
    """
    This function 
    """

def process_api_response(response):


    """
    This function sifts through the JSON object reponse and gets the data from the following fields: 

    videoId: unique id of the youtube video --> mongoDB 
    channelID: check to make sure that this video is coming from the Police Activity YT channel --> mongoDB
    description: description of the YouTube video **remove bogus info from description like Patreon supporters --> mongoDB
    playlistID: check to make sure that the video is coming from the correct playlist
    title: title of the youtube video --> mongoDB & pandas df
    nextPageToken: token to get the search results from the next page --> return value

    Then a new dictionary is created with the above fields as key value pairs in preparation for inputting
    the data into mongoDB. 

    returns nextPageToken for subsequent calls to pages and the dictionary
    
    """

    dict_response = {}

    dict_response['video title'] = response['items'][0]['snippet']['title']



    return nextPageToken, dict_reponse

# this function will use the 'nextPageToken' to iterate through the 
def iterate_through_pages():
        

    return False

def main(): 
    
    return False
   
if __name__ == "__main__":
    main()