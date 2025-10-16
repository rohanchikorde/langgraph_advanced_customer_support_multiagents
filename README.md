# Customer Service Workflow with LangGraph

This project implements a cyclical multi-agent customer service workflow using LangGraph. The system uses a state machine architecture to handle customer queries through various stages including classification, sentiment analysis, specialized handling, dynamic collaboration, and escalation.

## Project Structure

```
essay-multi-agent/
├── src/
│   ├── __init__.py
│   ├── config.py          # LLM configuration and initialization
│   ├── graph.py           # Graph construction and routing logic
│   ├── memory.py          # Agent memory and learning system
│   ├── nodes.py           # All node functions for processing stages
│   └── state.py           # CustomerServiceState TypedDict definition
├── data/
│   └── agent_memory.json  # Persistent memory storage
├── main.py                # Entry point to run the workflow
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

3. Run the workflow:
   ```bash
   python main.py
   ```

4. Run tests:
   ```bash
   python test_memory.py
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