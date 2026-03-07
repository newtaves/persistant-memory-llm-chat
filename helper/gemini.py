# all the helper function of gemini will be here
from google.genai import types
from google.genai import errors
from google import genai
import os

def get_gemini_response(prompt:str, system_instructions:str="")->dict:
    """
    use google.genai to send the prompt and system instructions to get the response from gemini
    args:
        prompt: The prompt to send to gemini.
        system_instructions: The system instructions to send to gemini.
    returns:
        {
        'status':"success"/"error",
        response: ""
        }
    """
    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
            system_instruction=system_instructions),
            contents=prompt,
            
        )
        return {"status":"success", "response":response.text}
        
    except errors.ClientError as e:
        return {"status":"error", "response":e.message}
    except errors.ServerError as e:
        return {"status":"error", "response":e.message}
    except errors.APIError as e:
        return {"status":"error", "response":e.message}

def create_session_name(session_chat:str)->dict:
    """
    use gemini to create a title for the given session chat
    call this function 
    after gemini's first response. -> call this function -> save the conversation with the title given by this function 
    
    args:
        session_chat: The chat history of the session to create a session name for.
    returns:
        {
        'status':"success"/"error",
        response: " "
    """
    system_instructions="""
    "Your task is to generate only one 3-6 word title for the given chats and nothing else. 
    the title should not be poetic and should reflect only the content of the chats."
    """
    response = get_gemini_response(session_chat, system_instructions)
    return response

def create_embeddings(chunks:str, dimentions:int=768)->dict:
    """
    use gemini embeddings model to create embeddings for the given chunk of text and return the embeddings
    use 768 dimensions
    """
    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        result = client.models.embed_content(
        model="gemini-embedding-001",
        contents="What is the meaning of life?",
        config=types.EmbedContentConfig(output_dimensionality=dimentions)
    )
        embedding_obj = result.embeddings[0].values
        return {"status":"success", "response":embedding_obj}
        
    except errors.ClientError as e:
        return {"status":"error", "response":e.message}
    except errors.ServerError as e:
        return {"status":"error", "response":e.message}
    except errors.APIError as e:
        return {"status":"error", "response":e.message}
