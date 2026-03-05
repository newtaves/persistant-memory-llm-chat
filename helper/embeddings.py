#Contains helper functions to create and manage embeddings for the documents and chat sessions.
#
#
from db import db
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-mpnet-base-v2")

def get_context(query, top_k):
    """
    Search `query` in the vector database and return the top `top_k` most relevant documents as context for the chat session.
    args:
        query: The query to search in the vector database.
        top_k: The number of most relevant documents to return as context.
    returns:
        A list of the top `top_k` most relevant documents as context for the chat session.

    example:
        context = get_context("What is the capital of France?", 5)
        print(context)
        >>> ["The capital of France is Paris.", "Paris is the capital city of France.", 
        "France's capital is Paris.", "The city of Paris is the capital of France.", 
        "Paris, the capital of France, is known for its art and culture."]
    """

    query_embeddings = model.encode(query)
    query = "SELECT messages.content FROM message_embeddings JOIN messages ON messages.message_id = message_embeddings.message_id_ref  ORDER BY embedding <-> ? LIMIT ?;"
    params = (query_embeddings, top_k,)

    return db.execute(query,params)

