#CRUD operations for chat sessions
from db import db
from .embeddings import get_embeddings
import uuid

def create_conversation(user_id, title, metadata="{}"):
    conversation_id = str(uuid.uuid4())

    db.execute("""
        INSERT INTO conversations(conversation_id, user_id, title, metadata)
        VALUES (%s, %s, %s, %s)
    """, (conversation_id, user_id, title, metadata))

    return conversation_id

def load_session(conversation_id:str):
    """
    Load the chat session from the database using the conversation_id
    """
    query = "SELECT role, content FROM messages WHERE conversation_id = %s ORDER BY created_at ASC;"
    params = (conversation_id,)
    return db.query(query, params)

def delete_session(conversation_id):
    """
    Delete the chat session from the database using the conversation_id
    """
    #Delete embeddings
    query = """
            DELETE FROM message_embeddings
            WHERE message_id_ref IN (
                SELECT message_id FROM messages
                WHERE conversation_id = %s
            )
        """
    params = (conversation_id,)
    db.execute(query,params)

    #delete conversation
    query = "DELETE FROM conversations WHERE conversation_id = %s"
    return db.execute(query, params)


def list_conversations(user_id:int):
    """
    List all the chat sessions from the database
    """
    query = "SELECT conversation_id, title FROM conversations WHERE user_id=%s ORDER by created_at DESC"
    params = (user_id,)
    return db.query(query, params)

def add_message(conversation_id, role, content):
    message_id = str(uuid.uuid4())

    db.execute("""
        INSERT INTO messages(message_id, conversation_id, role, content)
        VALUES (%s, %s, %s, %s)
    """, (message_id, conversation_id, role, content))

    # update conversation timestamp
    db.execute("""
        UPDATE conversations
        SET updated_at = CURRENT_TIMESTAMP
        WHERE conversation_id = %s
    """, (conversation_id,))

    return message_id

def get_messages(conversation_id):
    rows = db.query("""
        SELECT role, content
        FROM messages
        WHERE conversation_id = %s
        ORDER BY created_at
    """, (conversation_id,))

    return [{"role": r["role"], "content": r["content"]} for r in rows]

def load_global_persona(user_id:int):
    """
    Load the global persona for the user from the database using the user_id
    """
    query = "SELECT global_persona FROM users WHERE user_id=%s"
    params = (user_id,)
    return db.query(query, params)[0]

def save_global_persona(user_id, persona):
    """
    Save the global persona for the user to the database using the user_id and persona
    """
    query = "UPDATE users SET global_persona=%s WHERE user_id=%s"
    params = (persona, user_id,)
    return db.execute(query, params)

def save_message_n_message_embeddings(conversation_id, role, content):

    message_id = str(uuid.uuid4())

    # save message
    db.execute("""
        INSERT INTO messages(message_id, conversation_id, role, content)
        VALUES (%s, %s, %s, %s)
    """, (message_id, conversation_id, role, content))

    # create embedding
    embedding = get_embeddings(content)

    db.execute("""
        INSERT INTO message_embeddings(message_id_ref, embedding)
        VALUES (%s, %s)
    """, (message_id, embedding))

    return message_id

def retrieve_context(message: str, user_id: int, top_k: int = 5):
    # Ensure query_embedding is a list or vector object, 
    # as pgvector-python handles the conversion to Postgres format.
    query_embedding = get_embeddings(message)

    # Use the <=> operator for cosine distance (smaller is closer)
    # Use <-> for Euclidean distance
    rows = db.query("""
        SELECT m.content
        FROM message_embeddings me
        JOIN messages m ON m.message_id = me.message_id_ref
        JOIN conversations c ON c.conversation_id = m.conversation_id
        Where c.user_id = %s
        ORDER BY me.embedding <=> %s
        LIMIT %s
    """, (user_id, query_embedding, top_k))

    return [r["content"] for r in rows]