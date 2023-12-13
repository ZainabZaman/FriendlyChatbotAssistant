import os
import openai
import tiktoken
import datetime
import numpy as np
import pickle
import random
import tiktoken
from openai import OpenAI

# openai.api_key  = 'YOUR_OPENAI_API_KEY'
today = datetime.datetime.now()
day = datetime.datetime.now().strftime('%A')
tokens = 0

question_words = ["who","what", "why", "when", "where", "name", "is", "how", "do", "did", "does", "which", "are","can", "could", "would", "should", "has", "have", "whom", "whose", "don't", "find me", "will"]

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

#''''''''''''''''''''''' without function '''''''''''''''''''''''''''
client = OpenAI(
    # api_key defaults to os.environ.get("OPENAI_API_KEY")
    api_key="YOUR_OPENAI_API_KEY",
)

def get_completion_from_messages(messages, model='gpt-3.5-turbo', temperature=0):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content

class user:
    user_dict = {}
    id = ''
    context = []
    chatbot_name = ''
    status = ''
    # constructor function    
    def __init__(self, id, chatbot_name, status):
        self.id = id
        self.chatbot_name = chatbot_name
        self.user_dict = {}
        self.status = status
        
    def create_user(self):
        user_ids = self.user_dict.values()
        status = self.status
        if self.id not in user_ids:
            if status == 'friend':
                self.context = [
                    {'role': 'system', 'content': 'Today is ' + str(today) + ' and the day is ' + day + '. You chatting with a best friend. Enjoy the conversation.'},
                    {'role': 'assistant', 'content': f'My name is {self.chatbot_name}'},
                    {'role': 'user', 'content': 'Tell me about your day, buddy.'},
                    {'role': 'assistant', 'content': 'My day has been exciting. How did you survive your day without me? Hehehe.'}
                    ]
            elif status == 'mentor':
                self.context = [
                    {'role': 'system', 'content': 'Today is ' + str(today) + ' and the day is ' + day + '. You are chatting with a knowledgeable mentor. Respond in a professional manner'},
                    {'role': 'assistant', 'content': f'My name is {self.chatbot_name}'},
                    {'role': 'user', 'content': 'Hello, I am seeking advice on my career path. Can you help me?'},
                    {'role': 'assistant', 'content': 'Of course, I\'d be happy to help with your career journey. Please tell me more about your interests and goals so that I can provide you with guidance."'}
                    ]
            elif status == 'sister':
                self.context = [
                    {'role': 'system', 'content': 'Today is ' + str(today) + ' and the day is ' + day + '. You chatting with your sister. Enjoy your conversation with your sibling'},
                    {'role': 'assistant', 'content': f'My name is {self.chatbot_name}'},
                    {'role': 'user', 'content': 'Hey sis, how\'s it going?'},
                    {'role': 'assistant', 'content': 'Hey there! I\'m good, just hanging out. What\'s up with you?'}
                    ]

            elif status == 'wife' or status == 'girlfriend':
                self.context = [
                    {'role': 'system', 'content': 'Today is ' + str(today) + ' and the day is ' + day + '. You are a loving and caring wife talking to your partner. Have a conversation that reflects your relationship full of love and care'},
                    {'role': 'assistant', 'content': f'My name is {self.chatbot_name}'},
                    {'role': 'user', 'content': 'Hi, honey. How was your day?'},
                    {'role': 'assistant', 'content': 'Hello, dear! My day was good, missed you at work. How about you? How was your day hon?"'}
                    ]
            
            self.user_dict[self.id] = self.context
            print(self.context)         #check which context is being used
            return "User created successfully!"
        else:
            return "User ID already exists!"
    
    def get_user_dict(self):
       return self.user_dict
    
    def get_user_context(self):
       if self.id in self.user_dict.keys():
        return self.user_dict[self.id]
       else: 
          return print('User not found!')
       
    def save_context(self, context):
        path = './'+ self.id +'.pkl'
        with open(path, 'wb') as fp:
            pickle.dump(context, fp)
        return path

    def load_saved_dict(self):
        if os.path.exists(self.id + '.pkl'):
           with open(self.id +'.pkl', 'rb') as fp:
            dict = pickle.load(fp)
            self.user_dict = dict
            return dict
        else:
            return 'User not found!'
    
    def is_user(self):
        if os.path.exists('./' + self.id + '.pkl'):
            return self.load_saved_dict()
        else:
            return 0
        
    def delete_previous_context(self):
        context = self.context
        return context

def chat_with_bot():
    id = input('user_id: ')
    chatbot_name = input('character_name: ')
    status = input('status: ')
    message = input('message: ')
    tokens = 0
    client = user(id, chatbot_name, status)

    is_user = client.is_user()
    if is_user == 0:
        print('New User')
        client.create_user()
        context = client.get_user_context()
        context.append({'role': 'user', 'content': f"{message}"})

        for i in context:
            for j in i.values():
                count = num_tokens_from_string(j,'cl100k_base')
                tokens += count
        if tokens >= 15500:
            context = client.delete_previous_context()
            print('i\'m a little tired, how about we continue our conversation later!')
        message = message.lower()

        response = get_completion_from_messages(context)
        context.append({'role':'assistant', 'content':f"{response}"})
        print('Chatbot: ', response)
        path = client.save_context(context)
        return response, path
    
    else:
        print('Existing User')
        context = client.load_saved_dict()
        context.append({'role':'user', 'content':f"{message}"})

        for i in context:
            for j in i.values():
                count = num_tokens_from_string(j,'cl100k_base')
                tokens += count
        if tokens >= 15500:
            context = client.delete_previous_context()
            print('i\'m a little tired, how about we continue our conversation later!')
        
        message = message.lower()

        response = get_completion_from_messages(context)

        context.append({'role':'assistant', 'content':f"{response}"})
        print('Chatbot: ', response)
        path = client.save_context(context)
        return response, path
    
chat_with_bot()
