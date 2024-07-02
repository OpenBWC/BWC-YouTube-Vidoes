from pymongo import MongoClient
from pymongo.server_api import ServerApi
import MongoConnection as MC
def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = MC.uri
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING,server_api=ServerApi('1'))
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['yt-database']
  
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
  
   # Get the database
   dbname = get_database()