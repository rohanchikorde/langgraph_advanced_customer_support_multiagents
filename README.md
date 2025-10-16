# Customer Service Workflow with LangGraph

This project implements a cyclical multi-agent customer service workflow using LangGraph. The system uses a state machine architecture to handle customer queries through various stages including classification, sentiment analysis, specialized handling, dynamic collaboration, and escalation.

## Project Structure

- `main.py`: Entry point to run the workflow
- `state.py`: Defines the CustomerServiceState TypedDict
- `config.py`: LLM configuration and initialization
- `nodes.py`: All node functions for processing stages
- `graph.py`: Graph construction and routing logic
- `requirements.txt`: Python dependencies
- `.env`: Environment variables (API keys)

## Features

- **Classification Node**: Analyzes incoming queries to determine intent and category (technical, billing, returns, general).
- **Sentiment Analysis**: Assesses emotional tone to set priority and route accordingly.
- **Dynamic Agent Collaboration**: Enables agents to form teams based on query complexity, combining multiple specialized handlers for hybrid issues using consensus algorithms.
- **Specialized Handlers**: Domain-specific agents for different query types.
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

## Architecture

The graph consists of nodes connected by conditional and cyclical edges, allowing for dynamic routing and iterative refinement of responses. The system includes a Collaboration Node that spawns parallel executions for multi-category queries, enabling dynamic team formation. It tries to resolve queries autonomously through multiple cycles before escalating.

## Modular Design

The codebase is organized into modules for maintainability:
- **State Management**: Centralized state definition
- **Configuration**: LLM setup and API configuration
- **Node Logic**: Separated processing functions
- **Graph Construction**: Isolated graph building and routing