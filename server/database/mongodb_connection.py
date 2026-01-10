import pymongo
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

def connect_to_mongodb():
  
    connection_string = os.environ['MONGODB_URI']
    
    try:
        client = pymongo.MongoClient(connection_string)
        
        client.admin.command('ping')
        print("Connected successfully to MongoDB Atlas!")
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB Atlas: {e}")
        return None

client = connect_to_mongodb()
db = client["gc_tech_project_database"] if client is not None else None
messages_collection = db["chat_history"] if db is not None else None

