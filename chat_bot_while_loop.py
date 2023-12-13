import os
import openai
import tiktoken
import datetime
import numpy as np
import pickle
from openai import OpenAI


# openai.api_key  = 'YOUR_OPENAI_API_KEY'
today = datetime.datetime.now()
day = datetime.datetime.now().strftime('%A')
tokens = 0

tokens = 0
import tiktoken

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
    # constructor function    
    def __init__(self, id, chatbot_name):
        self.id = id
        self.chatbot_name = chatbot_name
        self.context = [
                {'role': 'system', 'content': 'Today is ' + str(today) + ' and the day is ' + day + '. You are chatting with a best friend. Enjoy the conversation.'},
                {'role': 'assistant', 'content': f'My name is {self.chatbot_name}'},
                {'role': 'user', 'content': 'Tell me about your day, buddy.'},
                {'role': 'assistant', 'content': 'My day has been exciting. How did you survive your day without me? Hehehe.'}
                ]
        self.user_dict = {}
        
    def create_user(self):
        user_ids = self.user_dict.values()
        if self.id not in user_ids:
            self.user_dict[self.id] = self.context
            return print("User created sucessfuly!")
        else:
            return print("User ID already exits!")
    
    def get_user_dict(self):
       return self.user_dict
    
    def get_user_context(self):
       if self.id in self.user_dict.keys():
        return self.user_dict[self.id]
       else: 
          return print('User not found!')
       
    def save_context(self, context):
        path = './'
        with open(path +self.id +'.pkl', 'wb') as fp:
            pickle.dump(context, fp)
            print('It was great talking to you! See ya later!')

        return print(context, path)

    def load_saved_dict(self):
        if os.path.exists(self.id + '.pkl'):
           with open(self.id +'.pkl', 'rb') as fp:
            dict = pickle.load(fp)
            self.user_dict = dict
            return dict
        else:
            return print('User not found!')
    
    def is_user(self):
        if os.path.exists('./' + self.id + '.pkl'):
            return self.load_saved_dict()
        else:
            return 0
        
    def delete_previous_context(self):
        context = self.context
        return context
    
id = input('Enter user id: ')
name = input('chatbot name: ')
client = user(id, name)
is_user = client.is_user()
if is_user == 0:
    print('New User')
    client.create_user()
    context = client.get_user_context()
    prompt = 'hello'
    prompt = input()
    while prompt != 'exit':
        context.append({'role':'user', 'content':f"{prompt}"})

        for i in context:
            for j in i.values():
                count = num_tokens_from_string(j,'cl100k_base')
                tokens = tokens + count
        if tokens >= 15500:
            context = client.delete_previous_context()
            print('i\'m a little tired, how about we continue our conversation later!')

        print(tokens)
        response = get_completion_from_messages(context)
        context.append({'role':'assistant', 'content':f"{response}"})
        print('Assistant:', response)
        prompt = input()

        if prompt == 'exit':
            client.save_context(context)
            client.load_saved_dict()
else:
    print('Existing User')
    context = client.load_saved_dict()
    prompt = 'hello'
    prompt = input()
    while prompt != 'exit':
        context.append({'role':'user', 'content':f"{prompt}"})
    
        for i in context:
            for j in i.values():
                count = num_tokens_from_string(j,'cl100k_base')
                tokens = tokens + count
        if tokens >= 15500:
            context = client.delete_previous_context()
            print('i\'m a little tired, how about we continue our conversation later!')
            break

        print(tokens)
        response = get_completion_from_messages(context)
        context.append({'role':'assistant', 'content':f"{response}"})
        print('Assistant:', response)
        prompt = input()

        if prompt == 'exit':
            client.save_context(context)
            client.load_saved_dict()
