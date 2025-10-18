# Customer Service Workflow with LangGraph

This project implements a cyclical multi-agent customer service workflow using LangGraph. The system uses a state machine architecture to handle customer queries through various stages including classification, sentiment analysis, specialized handling, dynamic collaboration, and escalation.

## Project Structure

```
essay-multi-agent/
├── src/
│   ├── __init__.py
│   ├── api.py             # FastAPI application and endpoints
│   ├── config.py          # LLM configuration and initialization
│   ├── graph.py           # Graph construction and routing logic
│   ├── memory.py          # Agent memory and learning system
│   ├── nodes.py           # All node functions for processing stages
│   └── state.py           # CustomerServiceState TypedDict definition
├── frontend/
│   ├── index.html         # Main chat interface
│   ├── styles.css         # Modern UI styling
│   └── script.js          # Frontend logic and API calls
├── data/
│   └── agent_memory.json  # Persistent memory storage
├── api_server.py         # API server startup script
├── main.py                # Entry point for CLI usage
├── frontend_server.py    # Frontend HTTP server
├── run_servers.py         # Combined server starter
├── test_integration.py    # End-to-end testing
├── test_memory.py         # Memory system test suite
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── .env                   # Environment variables (API keys)
```

## Features

- **Classification Node**: Analyzes incoming queries to determine intent and category (technical, billing, returns, general).
- **Sentiment Analysis**: Assesses emotional tone to set priority and route accordingly.
- **Dynamic Agent Collaboration**: Enables agents to form teams based on query complexity, combining multiple specialized handlers for hybrid issues using consensus algorithms.
- **Agent Memory & Learning**: Persistent memory system that stores user interaction history, tracks successful patterns, and automatically updates a knowledge base from resolved issues.
- **Specialized Handlers**: Domain-specific agents for different query types with memory-enhanced responses.
- **Cyclical Logic**: Includes validation loops and refinement cycles for quality assurance (up to 3 attempts before escalation).
- **Conversation History**: Maintains full conversation context for richer responses.
- **Automated Resolution**: Attempts autonomous handling before escalating to human agents.
- **Escalation**: Routes cases to human agents only after multiple failed attempts.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables in `.env`:
   ```
   OPENROUTER_API_KEY=your_openrouter_api_key
   ```

3. Run the workflow (CLI):
   ```bash
   python main.py
   ```

4. Run tests:
   ```bash
   python test_memory.py
   python test_api.py  # Requires API server running
   ```

5. Start the complete system (frontend + backend):
   ```bash
   python run_servers.py
   ```
   This starts both the backend API and frontend servers.
   - Frontend: http://localhost:3000
   - Backend API: http://127.0.0.1:8000
   - API Docs: http://127.0.0.1:8000/docs

6. Alternative: Run servers separately:
   ```bash
   # Terminal 1: Start backend
   python api_server.py

   # Terminal 2: Start frontend
   python frontend_server.py
   ```

7. Run integration tests:
   ```bash
   python test_integration.py
   ```

## API Integration

The system includes a FastAPI-based REST API for seamless frontend integration.

### Endpoints

#### Process Customer Query
```http
POST /api/v1/support/query
```

**Request Body:**
```json
{
  "query": "I have a billing issue with order 12345",
  "user_id": "optional_user_id",
  "metadata": {}
}
```

**Response:**
```json
{
  "conversation_id": "conv_abc123",
  "user_id": "user_xyz",
  "query": "I have a billing issue with order 12345",
  "response": "I've checked your order...",
  "categories": ["billing", "technical"],
  "satisfactory": true,
  "escalation_needed": false,
  "processing_time": 2.34,
  "timestamp": "2025-10-17T12:00:00"
}
```

#### Get Conversation History
```http
GET /api/v1/support/history/{user_id}?limit=10
```

#### Get System Statistics
```http
GET /api/v1/support/stats
```

#### Submit Feedback
```http
POST /api/v1/support/feedback
```

**Request Body:**
```json
{
  "conversation_id": "conv_abc123",
  "user_id": "user_xyz",
  "rating": 5,
  "feedback": "Great response!"
}
```

#### Health Check
```http
GET /health
```

### Frontend Integration Example

```javascript
// Submit a customer query
const response = await fetch('http://localhost:8000/api/v1/support/query', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    query: "I have a billing issue with order 12345",
    user_id: "user123"
  })
});

const result = await response.json();
console.log(result.response);
```

### CORS Configuration

The API includes CORS middleware configured to allow all origins for development. In production, specify your frontend domains:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Web Frontend

The project includes a modern, responsive web interface for interacting with the customer support system.

### Frontend Features

- **Real-time Chat**: Send messages and receive responses instantly
- **Conversation History**: Persistent chat history using local storage
- **Responsive Design**: Works on desktop and mobile devices
- **Connection Status**: Visual indicators for backend connectivity
- **Typing Indicators**: Shows when the AI is processing responses
- **Error Handling**: Graceful error messages and retry logic
- **System Statistics**: Live dashboard showing conversation metrics
- **Export Functionality**: Download chat history as text files

### Usage Instructions

1. **Start the System**:
   ```bash
   python run_servers.py
   ```

2. **Open Browser**:
   - Navigate to `http://localhost:3000`
   - Start chatting with the AI support system

3. **API Access**:
   - Backend API: `http://127.0.0.1:8000`
   - Interactive docs: `http://127.0.0.1:8000/docs`

### System Architecture

```
Frontend (localhost:3000)
    ↓ HTTP Requests
Backend API (127.0.0.1:8000)
    ↓ LangGraph Processing
Multi-Agent System
    ↓ Persistent Storage
Memory System (data/agent_memory.json)
```

### File Structure

```
├── frontend/
│   ├── index.html          # Main chat interface
│   ├── styles.css          # Modern UI styling
│   └── script.js           # Frontend logic and API calls
├── frontend_server.py     # Simple HTTP server for frontend
├── run_servers.py          # Combined server starter
├── test_integration.py     # End-to-end testing
└── api_server.py          # FastAPI backend server
```

## Architecture

The graph consists of nodes connected by conditional and cyclical edges, allowing for dynamic routing and iterative refinement of responses. The system includes a Collaboration Node that spawns parallel executions for multi-category queries, enabling dynamic team formation. A persistent memory system stores user profiles, conversation history, and successful resolution patterns to continuously improve responses. Memory nodes load user context at the start and save conversations after resolution. It tries to resolve queries autonomously through multiple cycles before escalating.

## Data Persistence

The system includes a persistent memory layer that stores:
- **User Profiles**: Individual user interaction history and preferences
- **Successful Patterns**: Learned resolution strategies for common issues
- **Knowledge Base**: Automatically updated FAQ entries from resolved cases
- **Performance Metrics**: System statistics and agent effectiveness tracking

Memory data is stored in JSON format in the `data/` directory for easy inspection and backup. **Note**: The `data/` directory is gitignored to protect user privacy and memory data.
- **Node Logic**: Separated processing functions
- **Graph Construction**: Isolated graph building and routing