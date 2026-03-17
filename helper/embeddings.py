#Contains helper functions to create and manage embeddings for the documents and chat sessions.
#
#
from db import db
from sentence_transformers import SentenceTransformer
import re
import os
_model = None

def get_model():
    global _model
    if _model is None:
        model_path = '.\\models'
        # Fallback to download if local path doesn't exist
        if os.path.exists(model_path):
            _model = SentenceTransformer(model_path)
        else:
            _model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
    return _model


def get_embeddings(texts):
    model = get_model()
    return model.encode(texts)

def get_context(query):
    """
    `query` breaks down the long message into shorter for the context search

    example:
        message = "The sun set slowly over the mountains, casting long shadows across the valley.
        A cool breeze rustled the leaves, signaling the end of a hot summer day. 
        Birds began their evening songs, while lights twinkled on in the distant town. 
        It was a moment of peaceful calm"
        message_list = list(map(lambda x :x.strip(), re.split(r'[,;|.]',message)))
        print(*message_list, sep="\n")
        >>> The sun set slowly over the mountains
        casting long shadows across the valley
        A cool breeze rustled the leaves
        signaling the end of a hot summer day
        Birds began their evening songs
        while lights twinkled on in the distant town
        It was a moment of peaceful calm
    """

    message = "The sun set slowly over the mountains, casting long shadows across the valley. A cool breeze rustled the leaves, signaling the end of a hot summer day. Birds began their evening songs, while lights twinkled on in the distant town. It was a moment of peaceful calm"
    message_list = list(map(lambda x :x.strip(), re.split(r'[,;|.]',message)))

    return message_list

