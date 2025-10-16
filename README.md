# Essay Multi-Agent System

A multi-agent system using LangGraph for collaborative essay writing and critiquing.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your OpenRouter API key:
   ```
   OPENROUTER_API_KEY=your_api_key_here
   ```

3. Run the system:
   ```bash
   python main.py
   ```

## Description

This system consists of two agents:
- **Essay Agent**: Writes essays on given topics.
- **Critique Agent**: Reviews essays and provides feedback.

The process iterates until the critique approves the essay or reaches 5 iterations max. Memory is included for conversation history.

Uses OpenRouter API with z-ai/glm-4.5-air:free model.