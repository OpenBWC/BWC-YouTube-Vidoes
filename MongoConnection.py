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
    """
    This function places takes the fields from the dictionary responses from Police Activity Scraper and inputs them into a mongoDB database
    according to the correct fields.

    DB outline: 

    Collection: yt-force-used-vids
    """

def append_UOF_COLLECTION(dict_response):
    

# def main():

#     client = create_client_connection()

#     confirm_connection(client)

# if __name__ == "__main__":
#     main()

# for db_name in MONGO_CLIENT.list_database_names():
#     pp.pprint(db)


