from .mongodb_connection import connect_to_mongodb,messages_collection
from datetime import datetime

def store_message_from_db(email, message_content, is_user, title=None):
    """
    Store a message in the database.
    
    Args:
        email (str): The email identifier for the user
        message_content (str): The message text
        is_user (bool): Whether the message is from the user (True) or system (False)
        title (str, optional): The title for the chat session
        
    Returns:
        bool: True if successful, False otherwise
    """
    if messages_collection is not None:
        print("Database connection not established")
        return False
    
    if not title:
        print("Title is required")
        return False
    existing_doc = messages_collection.find_one({"email": email, "title": title})
    
    current_time = datetime.now().strftime("%I:%M:%S %p")  
    
    new_message = {
        "isUser": is_user,
        "message": message_content,
        "date": current_time
    }
    
    if existing_doc:
        result = messages_collection.update_one(
            {"email": email, "title": title},
            {"$push": {"messages": new_message}}
        )
        return result.modified_count > 0
    else:
        new_doc = {
            "email": email,
            "title": title,
            "messages": [new_message],
            "created_at": datetime.now()
        }
        result = messages_collection.insert_one(new_doc)
        return result.inserted_id is not None

def get_messages_from_db(email, title):
    """
    Retrieve all messages for a specific email and title.
    
    Args:
        email (str): The email of the user
        title (str): The title of the conversation
        
    Returns:
        list: List of message objects or empty list if none found
    """
    if messages_collection is not None:
        print("Database connection not established")
        return []
    
    doc = messages_collection.find_one({"email": email, "title": title})
    if doc and "messages" in doc:
        return doc["messages"]
    return []

def get_titles_for_email(email):
    """
    Retrieve all conversation titles for a specific email.
    
    Args:
        email (str): The email to retrieve titles for
        
    Returns:
        list: List of titles for the email
    """
    if messages_collection is not None:
        print("Database connection not established")
        return []
    results = messages_collection.find({"email": email}, {"title": 1, "_id": 0})
    
    titles = [doc["title"] for doc in results if "title" in doc]
    return titles

def delete_conversations(email):
    """
    Delete a conversation by email.
    
    Args:
        email (str): The email identifier for the user
        
    Returns:
        bool: True if successful, False otherwise
    """
    if messages_collection is not None:
        print("Database connection not established")
        return False
    
    result = messages_collection.delete_many({"email": email})
    return result.deleted_count > 0

def get_all_conversations_for_email(email):
    """
    Retrieve all conversations for a specific email.
    
    Args:
        email (str): The email to retrieve conversations for
        
    Returns:
        list: List of conversations (each with title and message count)
    """
    if messages_collection is not None:
        print("Database connection not established")
        return []
    
    pipeline = [
        {"$match": {"email": email}},
        {"$project": {
            "title": 1,
            "message_count": {"$size": "$messages"},
            "last_updated": {"$arrayElemAt": ["$messages.date", -1]},
            "_id": 0
        }}
    ]
    
    results = messages_collection.aggregate(pipeline)
    return list(results)

def get_all_conversations():
    """
    Retrieve all conversations across all emails.
    
    Returns:
        list: List of conversations with email, title, and message count
    """
    if messages_collection is not None:
        print("Database connection not established")
        return []
    
    pipeline = [
        {"$project": {
            "email": 1,
            "title": 1,
            "message_count": {"$size": "$messages"},
            "last_updated": {"$arrayElemAt": ["$messages.date", -1]},
            "_id": 0
        }}
    ]
    
    results = messages_collection.aggregate(pipeline)
    return list(results)