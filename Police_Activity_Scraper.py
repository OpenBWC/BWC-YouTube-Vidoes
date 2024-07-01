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

    title: title of the youtube video --> mongoDB & pandas df
    videoId: unique id of the youtube video --> mongoDB 
    channelID: check to make sure that this video is coming from the Police Activity YT channel --> mongoDB
    playlistID: check to make sure that the video is coming from the correct playlist
    description: description of the YouTube video **remove bogus info from description like Patreon supporters --> mongoDB
    
    nextPageToken: token to get the search results from the next page --> return value

    dict_response --> Then a new dictionary is created with the above fields as key value pairs in preparation for inputting
    the data into mongoDB. 

    returns nextPageToken for subsequent calls to pages and the dictionary
    
    """

    video_title = response['items'][0]['snippet']['title']
    video_ID = response['items'][0]['contentDetails']['videoId']
    channel_ID = response['items'][0]['snippet']['channelId']
    playlist_ID = response['items'][0]['snippet']['playlistId']
    
    if ['items'][0]['snippet']['channelId'] != PM.POLICE_ACTIVITY_ID:
        return "Mistake, the channel Id is not correct for this video id: " + video_ID
    elif ['items'][0]['snippet']['playlistId'] != PM.PA_PLAYLIST_ID:
        return "Mistake: the playlist ID is not correct for this video id: " + video_ID
    else:
        dict_response = {}

        dict_response['video title'] = video_title
        dict_response['video ID'] = video_ID
        dict_response['channel ID'] = channel_ID
        dict_response['playlist ID'] = playlist_ID

    


    return nextPageToken, dict_reponse

# this function will use the 'nextPageToken' to iterate through the 
def iterate_through_pages():
        

    return False

def main(): 
    
    return False
   
if __name__ == "__main__":
    main()