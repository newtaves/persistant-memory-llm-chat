from db import db

def messages():
    query = ("""
        SELECT content
        FROM messages
    """)
    return db.query(query)

def keyword_popularity(word:str):
    """
    Get the poplularity/frequency of the word in the entire database
    """

    query = ("""
        SELECT SUM(CASE WHEN LOWER(word) = %s THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS poplularity
        FROM messages m,
        LATERAL regexp_split_to_table(m.content, '\s+') AS word;
    """)
    params = [word,]

    return db.query(query,params)

def top_users(word:str):
    """
    Get the user which has used that word
    """
    query= """
        SELECT 
            c.user_id, 
            COUNT(*) AS word_count
        FROM messages m
        JOIN conversations c ON m.conversation_id = c.conversation_id
        CROSS JOIN LATERAL regexp_split_to_table(m.content, '[^a-zA-Z]+') AS t(word)
        WHERE LOWER(t.word) = %s
        GROUP BY c.user_id
        ORDER BY word_count DESC;
    """

    params= [word,]

    return db.query(query,params)

def top_time(word:str):
    """
    Get the topframe in which the word is used
    """
    query = """
        SELECT hour, COUNT(*) AS occurrences
        FROM (
            SELECT date_trunc('hour', m.created_at AT TIME ZONE 'Asia/Kolkata') AS hour,LOWER(word) AS word
            FROM messages m,
            LATERAL regexp_split_to_table(m.content, '[^a-zA-Z]+') AS t(word)
        )
        WHERE word = %s
        GROUP BY hour
        ORDER BY occurrences DESC;
    """

    params = [word,]

    return db.query(query,params)

def vocabulary(user_id:str):
    """
    Get the vocabulary of the user
    """
    query = """
    SELECT word, COUNT(*) AS occurrences
    FROM messages m
    JOIN conversations c on m.conversation_id = c.conversation_id
    JOIN users u on c.user_id = u.user_id    
    CROSS JOIN LATERAL regexp_split_to_table(m.content, '[^a-zA-Z]+') AS t(word)
    WHERE u.user_id = %s
    GROUP BY word
    """

    params = [user_id,]

    return db.query(query,params)

def active_time(user_id:str):
    """
    Get the freequency of the hour at which the user has messaged
    """
    query = """
    WITH hours AS (
    SELECT generate_series(0, 23) AS hour
    ),
    user_activity AS (
        SELECT 
            EXTRACT(HOUR FROM m.created_at AT TIME ZONE 'Asia/Kolkata') AS hour,
            COUNT(*) AS occurrences
        FROM messages m
        JOIN conversations c 
            ON m.conversation_id = c.conversation_id
        WHERE c.user_id = %s
        GROUP BY hour
    )
    SELECT 
        h.hour,
        COALESCE(u.occurrences, 0) AS occurrences
    FROM hours h
    LEFT JOIN user_activity u 
        ON h.hour = u.hour
    ORDER BY h.hour DESC;
    """
    
    params = [user_id,]

    return db.query(query,params)

def convo_by_users(keyword:str):
    """
    Get the users that have used that keyword in the 
    conversation and the occurence of that word
    """
    query = """
    SELECT 
    c.user_id,
    COUNT(*) AS occurrences
    FROM messages m
    JOIN conversations c 
        ON m.conversation_id = c.conversation_id
    CROSS JOIN LATERAL regexp_split_to_table(m.content, '[^a-zA-Z]+') AS word
    WHERE LOWER(word) = %s
    GROUP BY c.user_id
    ORDER BY occurrences DESC;    
    """

    params = [keyword,]

    return db.query(query,params)