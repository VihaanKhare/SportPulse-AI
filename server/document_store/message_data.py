import pathway as pw
from datetime import datetime

# Defines schema for message
class MessageSchema(pw.Schema):
    user_id: str
    timestamp: datetime
    message_text: str

# Creates an empty table to store messages (can be extended with persistence)
message_store = pw.Table.empty(schema=MessageSchema)

# Function to add a message to the store
def store_user_message(user_id: str, message_text: str):
    global message_store 
    new_row = {
        "user_id": user_id,
        "timestamp": datetime.utcnow(),
        "message_text": message_text
    }
    message_store += pw.Table.from_rows([new_row], schema=MessageSchema)
