#CRUD operations for chat sessions
from db import db
from .embeddings import get_embeddings
import uuid

def create_conversation(user_id, title, metadata="{}"):
    conversation_id = str(uuid.uuid4())

    db.execute("""
        INSERT INTO conversations(conversation_id, user_id, title, metadata)
        VALUES (?, ?, ?, ?)
    """, (conversation_id, user_id, title, metadata))

    return conversation_id

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

def list_conversations(user_id:int):
    """
    List all the chat sessions from the database
    """
    query = "SELECT conversation_id, title FROM conversations WHERE user_id=?"
    params = (user_id,)
    return db.query(query, params)

def add_message(conversation_id, role, content):
    message_id = str(uuid.uuid4())

    db.execute("""
        INSERT INTO messages(message_id, conversation_id, role, content)
        VALUES (?, ?, ?, ?)
    """, (message_id, conversation_id, role, content))

    # update conversation timestamp
    db.execute("""
        UPDATE conversations
        SET updated_at = CURRENT_TIMESTAMP
        WHERE conversation_id = ?
    """, (conversation_id,))

    return message_id

def get_messages(conversation_id):
    rows = db.query("""
        SELECT role, content
        FROM messages
        WHERE conversation_id = ?
        ORDER BY created_at
    """, (conversation_id,))

    return [{"role": r["role"], "content": r["content"]} for r in rows]

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

def save_message_n_message_embeddings(conversation_id, role, content):

    message_id = str(uuid.uuid4())

    # save message
    db.execute("""
        INSERT INTO messages(message_id, conversation_id, role, content)
        VALUES (?, ?, ?, ?)
    """, (message_id, conversation_id, role, content))

    # create embedding
    embedding = get_embeddings(content)

    db.execute("""
        INSERT INTO message_embeddings(message_id_ref, embedding)
        VALUES (?, ?)
    """, (message_id, embedding.tobytes()))

    return message_id

def retrieve_context(message: str, top_k: int = 5):

    query_embedding = get_embeddings(message)

    rows = db.query("""
        SELECT messages.content
        FROM message_embeddings
        JOIN messages
        ON messages.message_id = message_embeddings.message_id_ref
        WHERE message_embeddings.embedding MATCH ?
        AND k = ?
        ORDER BY distance
    """, (query_embedding.tobytes(), top_k))

    return [r["content"] for r in rows]
