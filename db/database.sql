CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    email VARCHAR(256) UNIQUE,
    password_hash VARCHAR(512),
    global_persona TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE conversations (
    conversation_id VARCHAR(256) PRIMARY KEY,
    user_id INTEGER,
    title TEXT,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE messages (
    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id VARCHAR(256),
    role VARCHAR(50),
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id) ON DELETE CASCADE
);


CREATE VIRTUAL TABLE message_embeddings USING vec0(
    message_id_ref INTEGER PRIMARY KEY, 
    embedding FLOAT[768]
);

CREATE TRIGGER update_conv_timestamp AFTER INSERT ON messages 
AFTER INSERT ON messages
BEGIN
    UPDATE conversations 
    SET updated_at = CURRENT_TIMESTAMP 
    WHERE conversation_id = NEW.conversation_id;
END;

CREATE TRIGGER delete_embedding_when_message_deleted
AFTER DELETE ON messages
BEGIN
    DELETE FROM message_embeddings
    WHERE message_id_ref = OLD.message_id;
END;