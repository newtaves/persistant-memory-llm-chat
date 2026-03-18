import os
import psycopg2
from psycopg2.extras import RealDictCursor
from pgvector.psycopg2 import register_vector
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL")
        self.conn = None
        self.connect()
        self._create_tables()

    def connect(self):
        """Establishes connection and executes a wake-up query."""
        try:
            # Connect to Neon
            self.conn = psycopg2.connect(self.db_url)
            self.conn.autocommit = True
            
            # Wake-up query to initialize compute if suspended
            with self.conn.cursor() as cur:
                cur.execute("SELECT 1;") 
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                register_vector(self.conn)
        except Exception as e:
            print(f"Database connection failed: {e}")
            raise

    def ensure_connection(self):
        """Checks if connection is alive; reconnects if necessary."""
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT 1;")
        except (psycopg2.OperationalError, AttributeError):
            self.connect()

    def _create_tables(self):
        sql_path = os.path.join('db', 'database.sql')
        if os.path.exists(sql_path):
            with open(sql_path, 'r') as f:
                sql = f.read()
            self.execute(sql)

    def execute(self, query, params=()):
        self.ensure_connection()
        with self.conn.cursor() as cur:
            cur.execute(query, params)
            return cur

    def query(self, query, params=()):
        self.ensure_connection()
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            return cur.fetchall()

db = Database()