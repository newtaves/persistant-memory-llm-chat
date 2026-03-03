import sqlite3
import sqlite_vec


DB_PATH = "college_project.db"

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        
        self.conn.enable_load_extension(True)
        sqlite_vec.load(self.conn)
        self.conn.enable_load_extension(False)
        
        self.conn.execute("PRAGMA foreign_keys = ON;")
        
        self._create_tables()

    def _create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    email TEXT UNIQUE,
                    password_hash TEXT,
                    global_persona TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""")
            
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    conversation_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    metadata JSON,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )""")

            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    message_id TEXT PRIMARY KEY,
                    conversation_id TEXT,
                    role TEXT,
                    content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id)
                )""")

            self.conn.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS message_embeddings USING vec0(
                    message_id_ref INTEGER PRIMARY KEY, 
                    embedding FLOAT[768]
                )""")

    def execute(self, query, params=()):
        with self.conn:
            return self.conn.execute(query, params)

    def query(self, query, params=()):
        cursor = self.conn.execute(query, params)
        return cursor.fetchall()

db = Database()