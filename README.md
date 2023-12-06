# FriendlyChatbotAssistant

# Enhanced Chatbot with OpenAI GPT-3.5 Turbo

This Python script implements an enhanced chatbot using the OpenAI GPT-3.5 Turbo model. The chatbot features user management, context storage, keyword detection, external API usage, and response modifications for a more engaging conversation.

## Features

- **User Class**: Manages user contexts, including creating new users, saving/loading conversation contexts, and handling token limits.
- **Context Storage**: Utilizes pickle for saving and loading conversation contexts.
- **Token Management**: Tracks the number of tokens and suggests continuing later if it exceeds a limit.
- **Keyword Detection**: Identifies specific keywords, triggering actions like using `people_also_ask` API.
- **Response Modifications**: Adjusts responses based on triggers for a more interactive conversation.
- **Error Handling**: Addresses cases with empty responses or no matches to predefined patterns.

## Usage

1. **Set Up OpenAI API Key**: Replace `'YOUR_OPENAI_API_KEY'` with your actual OpenAI GPT-3.5 Turbo API key.
2. **Run the Script**: Execute the script and interact with the chatbot by providing the user ID and a message.

## Dependencies

- `openai`: OpenAI Python library for API integration.
- `tiktoken`: Python library for counting tokens in a text string.
- `people_also_ask`: External API for fetching additional information.
- `nltk`: Natural Language Toolkit for tokenization.
- `datetime`: Python module for working with dates and times.
- `pickle`: Python module for object serialization.

## Example

```python
python chatbot.py
