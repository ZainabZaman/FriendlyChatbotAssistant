# FriendlyChatbotAssistant

This Python script implements an enhanced chatbot using the OpenAI gpt-3.5-turbo model. The chatbot features user management, context storage, keyword detection, fetching results from google search, multiple roles interaction and response modifications for a more engaging conversation.

## Features

- **User Class**: Manages user contexts, creates new users, saves/loads existing conversation contexts and history, and handles token limits.
- **Multiple Roles**: The uer can select from multiple roles that include `friend`, `mentor`, `sister` and a few others which make the chatbot interact in a way that particular role would interact.
- **Context Storage**: Utilizes pickle for saving and loading conversation contexts.
- **Token Management**: Tracks the number of tokens and if the number of tokens exceede 15500 the context and history for that particular ID is reset and the chatbot suggests the user to continue the conversation later.
- **Keyword Detection**: Identifies specific keywords to trigger actions like `people_also_ask` to get search results directly from google.
- **Response Modifications**: Adjusts responses based on triggers for a more interactive conversation.
- **Error Handling**: Addresses cases with empty responses or no matches to predefined patterns.

## Usage

1. **Set Up OpenAI API Key**: Replace `'YOUR_OPENAI_API_KEY'` with your actual OpenAI GPT-3.5 Turbo API key.
2. **Run the Script**: Execute the script and interact with the chatbot by providing the user_ID, chatbot name you want to set, chatbot role you want to set and message.

## Dependencies

- `openai`: OpenAI Python library for API integration.
- `tiktoken`: Python library for counting tokens in a text string.
- `people_also_ask`: External API for fetching results from the people also ask section from google search results.
- `nltk`: Natural Language Toolkit for tokenization.
- `datetime`: Python module for working with dates and times.
- `pickle`: Python module for object serialization.

## Example
Below are a few examples of the chatbot interacting as a friend!

[//]: # (![Description of Screenshot 1](screenshots/screenshot1.png))

![alt text](https://github.com/ZainabZaman/FriendlyChatbotAssistant/blob/c2e2f22301740e4179df4156aaa3ab186770fa86/result_images/friend.JPG?raw=true)
```python
python chatbot.py
