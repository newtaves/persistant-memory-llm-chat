# Persistent Memory LLM Chat with RAG

A Streamlit-based chat application featuring **Retrieval-Augmented Generation (RAG)** with persistent memory management. This project demonstrates how to build an AI-powered chat interface that maintains conversation history and uses vector embeddings to get context from past chats.

## Demonstration Urls
   [Live demonstration](https://persistant-memory-llm-chat.streamlit.app/)
   The website may go to sleep mode due to inactivity. So opening may take some time.

   [Github url](https://github.com/newtaves/persistant-memory-llm-chat)

## Features

- **User Authentication**: Secure login system with password hashing
- **Persistent Conversations**: All chat history stored in postgres database
- **RAG Implementation**: Context-aware responses using vector similarity search
- **Multi-page Interface**: Clean Streamlit UI with dashboard and chat pages
- **Google Gemini Integration**: Powered by Google's Gemini AI model
- **Vector Embeddings**: Uses sentence transformers for semantic search

## Technologies Used

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: Neon postgres with pgvector(for embeddings)
- **AI/ML**: Google Gemini API, Sentence Transformers

## Project Structure
```
persistant-memory-llm-chat/
├── .streamlit/
├── db/
│   ├── __init__.py
│   ├── database.sql       #Contains schema
│   └── db.py              #Contains helper function to initalize and connect the database
│   
├── helper/
│   ├── __init__.py
│   ├── auth.py            # Authentication query and logic 
│   ├── embeddings.py
│   ├── gemini.py
│   └── session.py         #Contains sql queries
│   
├── models/
│   ├── 1_Pooling/
│   │   └── config.json
│   ├── config.json
│   ├── config_sentence_transformers.json
│   ├── model.safetensors
│   ├── modules.json
│   ├── README.md
│   ├── sentence_bert_config.json
│   ├── tokenizer.json
│   └── tokenizer_config.json
├── pages/
│   ├── __init__.py
│   ├── auth.py
│   ├── chat.py
│   └── dashboard.py
├── .env
├── .gitignore
├── college_project.db   # The database but later switched to neon postgres database
├── README.md
├── requirements.txt
└── streamlit_app.py
```

## Local Setup

### Prerequisites

- Python 3.8+
- Google Gemini API key
- Neon Postgres authentication key or local postgres server

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/newtaves/persistant-memory-llm-chat
   cd persistant-memory-llm-chat
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Environment Variables**

   Create a `.env` file in the root directory:
   ```
   GEMINI_API_KEY=your-gemini-api-key-here
   DATABASE_URL=your-postgres-database-url
   ```

5. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

## Usage

1. **Login/Register**: Create an account or log in with existing credentials. Use 'test' for demonstration purpose. No password required
2. **Dashboard**: View your account information
3. **Chat**: Start new conversations or continue previous ones
4. **Context Retrieval**: The app automatically retrieves relevant past messages for context-aware responses

## ER Diagram
![er diagram](https://github.com/user-attachments/assets/4909ac29-2b13-4510-a60c-b1ca190b236e)


## Database Schema

The application uses Postgres database with vector extensions for efficient storage and retrieval of chat data. The schema includes the following tables:

### Tables

#### `users`
Stores user account information and authentication data.
- `user_id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique identifier for each user
- `email` (VARCHAR(256), UNIQUE): User's email address for login
- `password_hash` (VARCHAR(512)): Hashed password using Argon2
- `global_persona` (TEXT): Optional user persona/customization data
- `created_at` (TIMESTAMP): Account creation timestamp

#### `conversations`
Manages chat sessions for each user.
- `conversation_id` (VARCHAR(256), PRIMARY KEY): Unique conversation identifier
- `user_id` (INTEGER): Reference to the user who owns the conversation (FOREIGN KEY)
- `title` (TEXT): Optional conversation title
- `metadata` (JSON): Additional conversation metadata
- `created_at` (TIMESTAMP): Conversation creation timestamp
- `updated_at` (TIMESTAMP): Last modification timestamp

#### `messages`
Stores individual chat messages within conversations.
- `message_id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique message identifier
- `conversation_id` (VARCHAR(256)): Reference to the parent conversation (FOREIGN KEY)
- `role` (VARCHAR(50)): Message role (e.g., 'user', 'assistant')
- `content` (TEXT): The actual message content
- `created_at` (TIMESTAMP): Message creation timestamp

#### `message_embeddings`
Vector embeddings table for RAG functionality using pgvector.
- `message_id_ref` (INTEGER, PRIMARY KEY): Reference to message_id in messages table
- `embedding` (FLOAT[384]): 384-dimensional vector embedding for semantic search


### Relationships

- **users** → **conversations**: One-to-many (one user can have multiple conversations)
- **conversations** → **messages**: One-to-many (one conversation can have multiple messages)
- **messages** → **message_embeddings**: One-to-one (each message has one embedding)

The schema uses foreign key constraints with CASCADE deletion to maintain referential integrity.

## RAG Implementation

The application implements **Retrieval-Augmented Generation (RAG)** to provide context-aware responses by retrieving relevant information from previous conversations.

### Embedding Model
- **Model**: `paraphrase-MiniLM-L6-v2` from Sentence Transformers
- **Dimensions**: 384-dimensional vector embeddings
- **Purpose**: Converts text messages into numerical vectors for semantic similarity search

### Vector Storage
- **Database**: postgres with `pgvector` extension for efficient vector operations
- **Table**: `message_embeddings` stores embeddings as byte arrays
- **Indexing**: Uses vector indexing for fast similarity searches


## Screenshots

![Application Interface](https://github.com/user-attachments/assets/bb1c1262-4e4a-4e9f-8807-89b709e7c0f9)

The application can recall and utilize previous conversations when needed, providing context-aware responses through its RAG implementation.
![streamlit-streamlit_app-2026-03-17-22-20-43](https://github.com/user-attachments/assets/ed46d9c5-dce0-4e71-a9b7-c396b9adc331)

