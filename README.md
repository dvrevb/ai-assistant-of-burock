# Burock Portfolio AI Assistant

> **⚠️ Note**: Burock Software Consultancy is a fictional company created for demonstration purposes. This project showcases AI assistant capabilities using simulated portfolio data.

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green)
![License](https://img.shields.io/badge/license-MIT-blue)

An AI-powered FastAPI backend for exploring **Burock Software Consultancy's** project portfolio through intelligent conversation and retrieval-augmented generation (RAG).

---

## 🚀 Quick Start

```bash
# Clone and navigate
git clone <your-repo-url>.git
cd "AI Assistant"

# Setup environment
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Configure API key
echo "OPENAI_API_KEY=your-key-here" > .env

# Populate vector store (first time only)
python scripts/ingest_portfolio.py

# Run the server
python main.py
```

Visit `http://localhost:9000/docs` for interactive API documentation.

---

## ✨ Features

- **🤖 Dual AI Modes**: Choose between stateless OpenAI Responses API or stateful LangChain RAG
- **💬 Conversation Memory**: Maintains context across multiple messages
- **🔍 Vector Search**: Semantic search through Burock's portfolio using Chroma DB
- **🎯 Grounded Responses**: Answers strictly based on portfolio data—no hallucinations
- **🔌 API-First Design**: Easy integration with web apps, CLIs, or mobile clients
- **📊 Observability**: Optional LangSmith integration for tracing and monitoring

---

## 📁 Project Structure

```
AI Assistant/
├── main.py                          # FastAPI application entrypoint
├── openai_responses/
│   ├── api_openai_responses.py      # Stateless chatbot (Responses API)
│   └── testing_responses_chatbot.py # CLI test client
├── langchain_agent/
│   ├── langchain_agent.py           # RAG pipeline with memory
│   ├── prompts.py                   # Prompt templates
│   └── vector_store.py              # Chroma vector store configuration
├── utils/
│   └── vector-store/                # Persistent Chroma DB (auto-generated)
├── scripts/
│   └── ingest_portfolio.py          # Vector store population script
├── data/
│   └── portfolio/                   # Source portfolio documents
├── requirements.txt
└── .env                             # Environment variables (create this)
```

---

## 📋 Requirements

- **Python**: 3.10+ (recommended 3.11)
- **OpenAI API key** with access to:
  - `gpt-4o-mini` (for Responses API)
  - `gpt-4` (for LangChain agent)
  - `text-embedding-ada-002` (for embeddings)
- **(Optional)** Virtual environment (recommended)

All Python dependencies are listed in `requirements.txt`.

---

## 🔧 Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>.git
cd "AI Assistant"
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```bash
# Required
OPENAI_API_KEY=sk-your-openai-api-key-here

# Optional – for LangSmith tracing/monitoring
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=lsv2_pt_your-langsmith-key-here
LANGSMITH_PROJECT=ai-assistant
```

⚠️ **Security**: Keep this file **private** and **never commit** real keys to version control. The `.env` file is already in `.gitignore`.

### 5. Prepare the vector store (IMPORTANT - First Time Setup)

The LangChain pipeline requires a populated Chroma vector database.

---

## 🏃 Running the API

### Option 1: Using Python directly

```bash
python main.py
```

Server starts at `http://0.0.0.0:9000`

### Option 2: Using Uvicorn (with auto-reload for development)

```bash
uvicorn main:app --host 0.0.0.0 --port 9000 --reload
```

### Verify it's running

Visit `http://localhost:9000/docs` for Swagger UI documentation.

---

## 📡 API Endpoints

### 1. OpenAI Responses API Chatbot (Stateless)

#### `GET /start_conversation`
Initiates a new conversation session.

**Response**:
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### `POST /chat`
Send a message and receive a portfolio-grounded response.

**Request**:
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "What projects has Burock completed in fintech?"
}
```

**Response**:
```json
{
  "response": "Burock has completed several fintech projects including..."
}
```

**Example cURL**:
```bash
# Start conversation
curl -X GET http://localhost:9000/start_conversation

# Send message
curl -X POST http://localhost:9000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
    "message": "What technologies does Burock specialize in?"
  }'
```

---

### 2. LangChain RAG Assistant (with Vector Search)

#### `POST /chain`
Query the portfolio using RAG with conversation memory.

**Request**:
```json
{
  "question": "Tell me about projects using React and AWS",
  "conversation_id": "user-session-123"
}
```

**Response**:
```json
{
  "output": "Based on Burock's portfolio, we've completed 3 major projects using React and AWS..."
}
```

**Example cURL**:
```bash
curl -X POST http://localhost:9000/chain \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are your most recent healthcare projects?",
    "conversation_id": "user-session-123"
  }'
```

**Notes**:
- Maintains conversation history per `conversation_id`
- Retrieves relevant context from vector store before answering

---

## 🧪 Testing with CLI Client

A simple terminal interface is included for quick testing.

### Run the CLI client

```bash
python openai_responses/testing_responses_chatbot.py
```

### Usage

```
Starting new conversation...
Conversation started with ID: 550e8400-e29b-41d4-a716-446655440000

You: What projects has Burock worked on?
Bot: Burock has worked on several notable projects including...

You: Tell me more about the e-commerce ones
Bot: Regarding e-commerce projects...

You: exit
Goodbye!
```

**Commands**:
- Type your questions naturally
- Type `exit` or `quit` to stop

---

## 💡 Example Questions

Here are some questions that work well with the system:

**General Portfolio Queries**:
- "What types of projects does Burock specialize in?"
- "Show me projects completed in the last year"
- "What industries has Burock worked with?"

**Technology-Specific**:
- "Which projects used React and Node.js?"
- "Do you have experience with AWS cloud services?"
- "Tell me about your mobile app development projects"

**Client/Industry Focus**:
- "What healthcare projects have you completed?"
- "Do you have fintech experience?"
- "Show me enterprise-level projects"

**Outcome-Oriented**:
- "What were the key achievements in your recent projects?"
- "Which projects resulted in measurable performance improvements?"

---

## 🔍 Troubleshooting

### "Vector store not found" error

**Problem**: The LangChain `/chain` endpoint fails with a Chroma error.

**Solution**:
```bash
# Verify the directory was created
ls utils/vector-store/
```

### "OpenAI API key not found"

**Problem**: Getting authentication errors.

**Solution**:
```bash
# Check your .env file exists and contains the key
cat .env

# Make sure it's in the project root directory
# Restart the server after adding the key
```

### Empty or irrelevant responses

**Problem**: The AI gives generic answers or says "I don't know".

**Solution**:
- Ensure your portfolio documents are properly formatted
- Verify documents contain enough detail
- Try rephrasing your question more specifically

### Conversation memory not working

**Problem**: The chatbot doesn't remember previous messages.

**Solution**:
- Ensure you're using the same `conversation_id` across requests
- Note that memory is **in-process only** and resets when server restarts

---

## 🏗️ Architecture Overview

```
┌─────────────┐
│   Client    │
│  (Web/CLI)  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│         FastAPI Backend             │
│  ┌─────────────┐  ┌──────────────┐ │
│  │  Responses  │  │  LangChain   │ │
│  │     API     │  │     RAG      │ │
│  └──────┬──────┘  └──────┬───────┘ │
└─────────┼─────────────────┼─────────┘
          │                 │
          │           ┌─────┴─────┐
          │           ▼           ▼
          │    ┌────────────┐ ┌────────────┐
          │    │   Chroma   │ │   OpenAI   │
          │    │   Vector   │ │   GPT-4    │
          │    │   Store    │ │            │
          │    └────────────┘ └────────────┘
          ▼
   ┌────────────┐
   │   OpenAI   │
   │ gpt-4o-mini│
   └────────────┘
```

---

## 🚀 Development Notes

### Adding New Portfolio Documents

1. Add files to `data/portfolio/`
2. Run ingestion: `python scripts/ingest_portfolio.py`
3. Restart the server

### Extending the System

**Custom Prompts**:
- Edit `langchain_agent/prompts.py` to adjust response style
- Modify system messages in `api_openai_responses.py`

**Different Embeddings**:
- Update `vector_store.py` to use other embedding models
- Re-run ingestion after changes

**Persistent Memory**:
```python
# Example: Using Redis for conversation storage
from redis import Redis
redis_client = Redis(host='localhost', port=6379)

# Store conversation history
redis_client.setex(
    f"conversation:{conversation_id}",
    3600,  # 1 hour TTL
    json.dumps(messages)
)
```

---

## 📊 Performance Considerations

- **Rate Limits**: OpenAI API has rate limits; implement request throttling for production
- **Vector Store Size**: Large portfolios (>1000 documents) may need chunking optimization
- **Memory Usage**: In-memory stores scale poorly; use Redis/PostgreSQL for production
- **Response Time**: RAG endpoint typically takes 2-5 seconds depending on context size

---