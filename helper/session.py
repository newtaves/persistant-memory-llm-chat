#CRUD operations for chat sessions
from db import db

def save_session(user_id:int, conversation_id:str, metadata:dict):
    """
    Save the chat session to the database
    """
    query = "INSERT INTO conversations(conversation_id, user_id, metadata) VALUES (?,?,?);"
    params = (conversation_id, user_id, metadata)
    return db.execute(query, params)

def load_session(conversation_id:str):
    """
    Load the chat session from the database using the session_id
    """
    query = "SELECT m.role, m.content FROM messages WHERE conversation_id = ? ORDER BY created_at ASC;"
    params = (conversation_id,)
    return db.query(query, params)

def delete_session(session_id):
    """
    Delete the chat session from the database using the session_id
    """
    return 1

def list_sessions(user_id:int):
    """
    List all the chat sessions from the database
    """
    query = "SELECT conversation_id, title FROM conversations WHERE user_id=?"
    params = (user_id,)
    return db.query(query, params)

def save_message(session_id, message):
    """
    Save a message to the chat session in the database using the session_id and message
    """
    return 1

def load_messages(session_id):
    """
    Load all the messages from the chat session in the database using the session_id
    """
    return 1



def load_global_persona(user_id:int):
    """
    Load the global persona for the user from the database using the user_id
    """
    query = "SELECT global_persona FROM users WHERE user_id=?"
    params = (user_id,)
    return db.query(query, params)[0]

def save_global_persona(user_id, persona):
    """
    Save the global persona for the user to the database using the user_id and persona
    """
    query = "UPDATE users SET global_persona=? WHERE user_id=?"
    params = (persona, user_id,)
    print(params)
    return db.execute(query, params)