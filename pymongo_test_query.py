from pprint import PrettyPrinter as pp
from pandas import DataFrame

# Get the database using the method we defined in pymongo_test_insert file
from pymongo_get_database import get_database
dbname = get_database()
 
# Retrieve a collection named "user_1_items" from database
collection_name = dbname["user_1_items"]
 
item_details = collection_name.find()
# convert the dictionary objects to dataframe
items_df = DataFrame(item_details)

# see the magic
print(items_df)