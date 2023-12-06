import os
import openai
import tiktoken
import datetime
import numpy as np
import pickle
import random
import people_also_ask
# import nltk
# nltk.download('punkt')
from nltk.tokenize import word_tokenize
import time
from openai import OpenAI

openai.api_key  = 'YOUR_OPENAI_API_KEY'
today = datetime.datetime.now()
day = datetime.datetime.now().strftime('%A')
tokens = 0

keywords = ['covid-19 pandemic','vaccines', 'omicron variant', 'travel restrictions', 'lockdowns', 'vaccination campaigns', 'booster shots', 'working from home', 'remote learning', 
            'online meetings', 'virtual events', 'social distancing', 'mask mandates', 'quarantine', 'global', 'supply chain', 'disruptions', 'inflation', 'cryptocurrency', 'nfts', 
            'non-fungible tokens', 'stock market', 'gamestop stock surge', 'spacex', 'mars', 'climate change', 'cop26', 'united nations', 'conference', 'weather events', 'wildfires', 
            'droughts', 'hurricanes', 'flooding', 'environmental', 'renewable energy', 'electric vehicles', 'green initiatives', 'plastic pollution', 'cybersecurity', 'ransomware', 
            'attacks', 'data breaches', 'artificial intelligence', 'machine learning', 'automation', '5g', '4g', 'remote work cybersecurity', 'social media', 'controversies', 'disinformation', 
            'privacy concerns', 'mental health', 'online therapy', 'self-care', 'wellness trends', 'fitness apps', 'streaming services', 'netflix', 'disney+', 'spotify', 'tiktok', 'youtube', 
            'influencers', 'celebrity', 'royal family', 'sports highlights', 'olympics', 'world cup', 'super bowl', 'uefa', 'champions league', 'nba', 'wimbledon', 'tour de france', 'fashion trends', 
            'met gala', 'red carpet fashion', 'collaborations', 'pop culture', 'releases', 'award shows', 'music festivals', 'concert tours', 'new music releases', 'viral challenges', 'art exhibitions', 
            'virtual reality experiences', 'space tourism', 'medical breakthroughs', 'gene editing technology', 'crispr', 'artificial organs', 'cancer treatments', 'sustainable fashion', 'ethical consumerism', 
            'ethical', 'fair trade movement', 'food trends', 'plant-based diets', 'veganism', 'food delivery services', 'restaurant', 'supply chain', 'remote learning tools', 'edtech advancements', 'e-commerce growth',
            'employee well-being programs', 'diversity and inclusion', 'social justice', 'women rights', 'lgbtq+', 'indigenous', 'elections', 'policies', 'immigration', 'humanitarian', 'crises', 'refugee', 'peace', 
            'historical anniversary', 'celebrations', 'collaborations', 'philanthropy', 'community support', 'fundraisers', 'activism movements', 'education reforms', 'disaster response', 'space exploration', 
            'tech industry', 'electric vehicle', 'gaming industry', 'competitions', 'trends', 'entertainment', 'breakthroughs', 'movements', 'conservation', 'humanitarian aid', 'healthcare', 'entrepreneurship', 'initiatives'
            , 'support services', 'gender equality', 'urban development', 'disaster', 'campaigns', 'renewable energy', 'digital transformation', 'clean energy', 'architecture', 'water conservation', 'war', 'world bank', 
            'who', 'world health', 'russia', 'ukrain', 'china', 'usa', 'uk', 'india', 'pakistan', 'iran', 'prime minister', 'queen', 'assassination', 'asteroid', 'ocean gate', 'king', 'clerical ', 'killing', 'murder',  '2022', '2023']

question_words = ["who","what", "why", "when", "where", "name", "is", "how", "do", "does", "which", "are", "could", "would", "should", "has", "have", "whom", "whose", "don't", "find me"]

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

#''''''''''''''''''''''' without function '''''''''''''''''''''''''''
client = OpenAI(
    # api_key defaults to os.environ.get("OPENAI_API_KEY")
    api_key="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",
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
    # constructor function    
    def __init__(self, id):
        self.id = id
        self.context = [
                {'role': 'system', 'content': 'Today is ' + str(today) + ' and the day is ' + day + '. You are chatting with a best friend. Enjoy the conversation.'},
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
        path = './'+ self.id +'.pkl'
        with open(path, 'wb') as fp:
            pickle.dump(context, fp)
        return print(path)

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

def chat_with_bot(id, message):
    tokens = 0
    client = user(id)
    is_user = client.is_user()
    if is_user == 0:
        print('New User')
        client.create_user()
        context = client.get_user_context()
        context.append({'role':'user', 'content':f"{message}"})

        message = message.lower()
        token_prompt = word_tokenize(message)

        for i in context:
            for j in i.values():
                count = num_tokens_from_string(j,'cl100k_base')
                tokens += count
        if tokens >= 15500:
            context = client.delete_previous_context()
            print('i\'m a little tired, how about we continue our conversation later!')

        response = get_completion_from_messages(context)

        if any(x in token_prompt[0] for x in question_words):
            if any(substring in message for substring in keywords):
                time.sleep(1)
                response = people_also_ask.get_simple_answer(message)
                time.sleep(1)

        if response == '':
            response = 'I\'m sorry I could not understand your request, kidly rephrase or ask a different queation.'
        if any(word in response.lower() for word in ['i\'m an AI', 'as an ai', 'i am an ai language model']):
            response = 'I haven\'t decided on it yet, Thanks for asking though!'
        if any(word in message.lower() for word in ['how are you', 'how\'s your day', 'how\'s it going']):
            # Randomly select a response from a list of possible mood variations
            moods = ['I\'m doing well, thank you for asking! How are you feeling today?', 'Feeling great today! What about you pal?', 'I\'m having a fantastic day! Hope you are having an awesome day too!', 'Just like any other day, I am doing very well. What about you?']
            response = random.choice(moods)
        if any(word in response.lower() for word in ['do you have feeling', 'your feelings','feelings']):
            # Modify the response to sound more human-like
            response = "I have feelings although I am unlike as you but I'm here to talk to you. You can share anything. I am always there for you!"

        context.append({'role':'assistant', 'content':f"{response}"})
        print('Chatbot: ', response)
        path = client.save_context(context)
        return response, path
    
    else:
        print('Existing User')
        context = client.load_saved_dict()
        context.append({'role':'user', 'content':f"{message}"})

        message = message.lower()
        token_prompt = word_tokenize(message)

        for i in context:
            for j in i.values():
                count = num_tokens_from_string(j,'cl100k_base')
                tokens += count
        if tokens >= 15500:
            context = client.delete_previous_context()
            print('i\'m a little tired, how about we continue our conversation later!')

        response = get_completion_from_messages(context)
        if any(x in token_prompt[0] for x in question_words):
            if any(substring in message for substring in keywords):
                time.sleep(1)
                response = people_also_ask.get_simple_answer(message)
                time.sleep(1)

        if response == '':
            response = 'I\'m sorry I could not understand your request, kidly rephrase or ask a different queation.'
        if any(word in response.lower() for word in ['i\'m an AI', 'as an ai', 'i am an ai language model']):
            response = 'I haven\'t decided on it yet, Thanks for asking though!'
        if any(word in message.lower() for word in ['how are you', 'how\'s your day', 'how\'s it going']):
            # Randomly select a response from a list of possible mood variations
            moods = ['I\'m doing well, thank you for asking! How are you feeling today?', 'Feeling great today! What about you pal?', 'I\'m having a fantastic day! Hope you are having an awesome day too!', 'Just like any other day, I am doing very well. What about you?']
            response = random.choice(moods)
        if any(word in response.lower() for word in ['do you have feeling', 'your feelings','feelings']):
            # Modify the response to sound more human-like
            response = "I have feelings although I am unlike as you but I'm here to talk to you. You can share anything. I am always there for you!"

        context.append({'role':'assistant', 'content':f"{response}"})
        print('Chatbot: ', response)
        path = client.save_context(context)
        return response, path
    
chat_with_bot('9965', 'what was the iran masha amini headscarves issue?')