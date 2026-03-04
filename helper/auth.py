from db import db
from passlib.hash import argon2

DEFAULT_GLOBAL_PERSONA = "You are a helpful assistant."


def _hash_password(password:str):
    """
    Hash the password using bcrypt
    """
    return argon2.hash(password)

def _verify_password(password, hash):
    """
    Verify the password using bcrypt
    """
    return argon2.verify(password, hash)

def _get_user(email):
    """
    Get the user from the database using the email
    """
    query = "SELECT * FROM users WHERE email = ?"
    params = (email,)
    result = db.query(query, params)

    return dict(result[0]) if result else None

def _create_user(email, hashed_password):
    """
    Create a new user in the database using the email and hashed_password
    """
    query = "INSERT INTO users (email, password_hash, global_persona) VALUES (?, ?, ?)"
    params = (email, hashed_password, DEFAULT_GLOBAL_PERSONA)
    return db.execute(query, params)



def authenticate_user(email, password):
    """
    Authenticate the user using the email and password
    """
    db_user = _get_user(email)
    if not db_user:
        return "No such user found"
    else:
        if _verify_password(password, db_user['password_hash']):
            return dict(db_user)
        else:            
            return "Invalid password"
        
def register_user(email:str, password:str):
    """
    Register a new user using the email and password
    """
    print("the password: ",password)
    hashed_password = _hash_password(password)
    print(hashed_password)
    _create_user(email, hashed_password)
    return 1
