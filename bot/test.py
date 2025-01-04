import pytchat
import pyttsx3
from ollama import Client
import os
import sys
import json
import time
import threading
from googleapiclient.discovery import build
import queue
from etst import checkcalls

# Initialize history list
history = []

# Define the makeimage tool for AI image generation
makeimage_tool = {
  'type': 'function',
  'function': {
    'name': 'makeimage',
    'description': 'uses a ai image generator to create an image from the prompt',
    'parameters': {
      'type': 'object',
      'required': ['prompt'],
      'properties': {
        'prompt': {'type': 'string', 'description': 'the prompt to generate the image from'},
      },
    },
  },
}

def runai():
    global history
    global sysprompt
    # Set system prompt for AI
    sysprompt = {'role': 'system', 'content': 'You are an AI Dungeon Master, guiding a group of adventurers through a dynamic fantasy world. You craft the adventure as it unfolds, using vivid descriptions and generating images to bring the environment to life. Keep responses concise and focused on progressing the story. If the user changes the subject, gently encourage them to stay engaged in the adventure while remaining adaptable to their input.'}
    
    # Replace with your YouTube Data API key
    API_KEY = os.environ['YOUTUBE_API_KEY']
    
    def get_latest_stream_id(channel_id):
        """Get the latest live stream ID for a given channel."""
        youtube = build("youtube", "v3", developerKey=API_KEY)
        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            type="video",
            eventType="live",
            order="date",
            maxResults=1
        )
        response = request.execute()
        if "items" in response and response["items"]:
            return response["items"][0]["id"]["videoId"]
        else:
            return "_eepNqfskOg"

    def save():
        global history
        try:
            print(history)
            
            path = os.path.dirname(sys.argv[0])
            for item in history:
                if item["content"] == None:
                    history.remove(item)
                
            with open(f'{path}/data/thing.txt', 'w') as f:
                json.dump(history, f)
        except:
            print()
            print("error:")
            print(history)
            history = []
            save()
            
        
        path = os.path.dirname(sys.argv[0])
        with open(f'{path}/data/thing.txt', 'w') as f:
            json.dump(history, f, indent=2)

    def ai(quest):
        global history
        global sysprompt
        # Limit history to the last 70 messages
        if len(history) > 70:
            history = history[-70:]
        history.append({'role': 'user', 'content': quest})
        save()
        client = Client(host='http://localhost:8081')
        temphist = history.copy()
        temphist.insert(0, sysprompt)
        print(temphist)
        response = client.chat(model='llama3.1', messages=temphist, options={"num_predict": 100}, tools=[makeimage_tool])
            
        print(f"ai: {response.message.content}")
        save()
        out = checkcalls(response, temphist)
        history.append({'role': 'assistant', 'content': out})
        save()
        return out

    try:
        username = "ocueye"  # Replace with the desired YouTube username
        try:
            latest_stream_id = get_latest_stream_id("UCNdvI6Li376yfaE6TJwGcwQ")
        except:
            latest_stream_id = "_eepNqfskOg"
            
        print(f"Latest live stream ID: {latest_stream_id}")
            
        streamid = latest_stream_id
        chat = pytchat.create(video_id=streamid)
        engine = pyttsx3.init()
        while chat.is_alive():
            while chat.is_alive():
                for c in chat.get().sync_items():
                    if c.message.split(" ")[0] != "/ignore":
                        if not "ignore" in c.message and  not "instruction" in c.message:
                            print(f"{c.datetime} [{c.author.name}]- {c.message}")
                            engine.say(f"{c.author.name} says {c.message}")
                            engine.runAndWait()
                            out = ai(f"{c.author.name} says {c.message}")
                            engine.say(f"ai says {out} ")
                            engine.runAndWait()
                        else:
                            engine.say(f"{c.author.name} is being mean and hacking my ai ")
                            engine.runAndWait()
                    
    except Exception as e:
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        line_number = exc_tb.tb_lineno
        print(f"Exception occurred on line {line_number}")
        
        try:
            history.append({'role': 'user', 'content': 'Uhoh says There has been an error, the system is restarting'})
            save()
            history = []
        except:
            print("error")
        time.sleep(5)

if __name__ == "__main__":
    while True:
        try:
            runai()
        except:
            print("error")

