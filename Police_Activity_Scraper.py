import os
import pymongo
from bson.objectid import ObjectId
import MongoConnection
from icecream import ic
import project_main as PM
from pprint import PrettyPrinter as pp
from googleapiclient.discovery import build
import re
import string
import MongoConnection as MC

"""
This py file gets use of force videos and puts them into a database.
"""

"""
Global Variables 
"""
COUNT = 0
TOKENS_DICTIONARY = {}
PAGE_TOKENS_LIST = []

def setup_yt_query():
    """This function creates the youtube model / object. Only run once.
    
    returns the youtube model object
    """

    youtube_object = build('youtube','v3', developerKey=PM.YT_CREDENTIALS)

    return youtube_object

def create_request(youtube_object, input_pageToken=""):
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
    global COUNT
    """Executes the request that was created from the create_request function
    
    returns the response JSON object / type dictionary
    """
    response = created_request.execute()

    print("Executed request number: " +str( COUNT))

    return response


    
    

def tokenize_vid_title(video_title_string):
    """This function takes the video title field returned from the YouTube api
    and it converts it into a list of words with punctuation removed
    
    This function will be used for building the keyword list for use of force / violent videos
    """

    string_list =  [re.sub('^[{0}]+|[{0}]+$'.format(string.punctuation), '', w) for w in video_title_string.split()]

    return string_list

def write_tokens_to_dict(token_list):
    """
    This func adds all the tokens from the video title and adds it to a dictionary. Each key
    is a unique word. The value will be how many time that word appears in all 2,000 videos from Police Activity
    """
    for token in token_list:
        if token in TOKENS_DICTIONARY:
           TOKENS_DICTIONARY[token] +=1
        else:
            TOKENS_DICTIONARY[token] = 1

def get_timestamps(vid_description):

    """
    This fuction tries to find a "Timestamps:" section of the video. If there isn't one, it returns false.
    If there is a timestamps section of the video it return that timestamps section.
    """
    # Find the starting index of "Timestamps:"
    start_index = vid_description.find("Timestamps:")
    
    if start_index == -1:
        # If "Timestamps:" is not found, return an empty string or handle as needed
        return ""
    
    # Extract the text from "Timestamps:" to the end
    timestamps_section = vid_description[start_index:]
    
    # If there's a delimiter (e.g., '\n\n'), find its index and slice up to it
    end_index = timestamps_section.find('\n\n')
    if end_index != -1:
        timestamps_section = timestamps_section[:end_index]
    
    return timestamps_section.strip()

def clean_description(vid_description):
    """
    Clean Description func removes all the patreon supporter information and uncessary emojis from the
    video description.

    Used chatgpt to generate most of the code found below.Slighty edited to code to get information that I wanted.
    """

    # get the timestamp if it exists, else input no video timestamps
    desired_text = get_timestamps(vid_description)
    if desired_text == "":
        desired_text = "No video Timestamps"

    # Define the pattern to search for cleaning
    pattern = r'Special thanks to Shout-Out Supporters on Patreon:'

    # Find the position where the pattern appears
    match = re.search(pattern, vid_description)

    if match:
        # Extract the vid_description before the match
        desired_text += vid_description[:match.start()].strip()
    else:
        # If pattern is not found, consider handling the case (e.g., read until end)
        desired_text += vid_description

    pattern2 = r'⭐⭐⭐⭐⭐'

    match2 = re.search(pattern2, vid_description)
    if match2:
        # Extract the vid_description before the match
        desired_text += vid_description[:match2.start()].strip()
    else:
        # If pattern is not found, consider handling the case (e.g., read until end)
        desired_text += vid_description

    return desired_text

def process_api_response(response):


    """
    This function sifts through the JSON object reponse and gets the data from the following fields: 


    channelID: check to make sure that this video is coming from the Police Activity YT channel --> mongoDB
    playlistID: check to make sure that the video is coming from the correct playlist

    video title: title of the youtube video --> mongoDB & pandas df
    videoId: unique id of the youtube video --> mongoDB 
    
    description: description of the YouTube video **remove bogus info from description like Patreon supporters --> mongoDB
    
    nextPageToken: token to get the search results from the next page --> return value

    dict_response --> Then a new dictionary is created with the above fields as key value pairs in preparation for inputting
    the data into mongoDB. 

    returns nextPageToken for subsequent calls to pages and the dictionary
    
    """
    
    
    channel_ID = response['items'][0]['snippet']['channelId']
    playlist_ID = response['items'][0]['snippet']['playlistId']

    
    
    if channel_ID != PM.POLICE_ACTIVITY_ID:
        return "Mistake, the channel Id is not correct for this video id: " + video_ID
    if playlist_ID != PM.PA_PLAYLIST_ID:
        return "Mistake: the playlist ID is not correct for this video id: " + video_ID


    video_title = response['items'][0]['snippet']['title']
    video_ID = response['items'][0]['contentDetails']['videoId']
    raw_description = response['items'][0]['snippet']['description']

    video_description = clean_description(raw_description)

    nextPageToken = response['nextPageToken']
    PAGE_TOKENS_LIST.append(nextPageToken) # --> I can slighty adjust the code if something breaks without using api calls

    dict_response = {}

    dict_response['video_title'] = video_title
    dict_response['video_ID'] = video_ID
    dict_response['channel_ID'] = channel_ID
    dict_response['playlist_ID'] = playlist_ID
    dict_response['video_description'] = video_description

    write_tokens_to_dict(tokenize_vid_title(video_title))
    


    return nextPageToken, dict_response

# this function will use the 'nextPageToken' to iterate through the 
def iterate_through_pages():
    global COUNT
    if COUNT == 0:
        youtube_object = setup_yt_query()
        youtube_request = create_request(youtube_object)
        response = execute_request(youtube_request)
        pp.pprint(response)

        nextPageToken, dict_response = process_api_response(response)
        COUNT+=1
    else:

        while nextPageToken != "":
            
            iterate_through_pages()
            MC.append_UOF_COLLECTION(dict_response)
            COUNT+=1


    

def main(): 
    iterate_through_pages()


    print(COUNT)
    print(TOKENS_DICTIONARY)
    
    MC.confirm_connection(MC.MONGO_CLIENT)
   
   
if __name__ == "__main__":
    main()