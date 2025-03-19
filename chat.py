# Import libraries
import os
from dotenv import load_dotenv
load_dotenv()
# os.environ['WEATHER_API_KEY'] = ""
import json
import yaml
from custom_tools.weather import *
from chat_history.sqlalchemy import ChatHistory
from model.ollama_models import OllamaModel
# Load configs
with open("configs.yaml", "r") as fp:
    configs = yaml.safe_load(fp)
# Load tools
with open(configs["tool_schema"], "r") as fp:
    tools = json.load(fp)
# Initialize Ollama model
llm = OllamaModel(model_name=configs["model"])
# Initialize datbase
chat_db = ChatHistory(max_conversation=configs['max_conversation'], max_token=configs['max_token'])
# Define system promt
system_prompt = {
    "role": "system",
    "content": "You are an helpful AI assitant. To answer the user's query first decide that any tool needs to be invoked or not. If any tool needs to be invoked then do that otherwise just answer the user's query through chat completion. You are provided a function to get weather of a city. If user want to know weather of a city first check if the name of the city is correct or not and exists in real life. If the city is correct then try to find the country for the city by yourself. If multiple cities have the same name in different countries then ask the user to manually enter the country for th city and show the user all the name of the countries where the city exists."
}




# Function to chat
def chat(message: str) -> str:
    previous_chats = chat_db.get()
    messages = [system_prompt] + previous_chats + [{"role": "user", "content": message}]
    chat_db.add({"role": "user", "content": message})
    resp = llm(messages, tools)
    if isinstance(resp, list):
        for func_schema in resp:
            function_output = get_weather(**func_schema['function_args'])
            messages.append({'role': 'tool', 'content': str(function_output), 'name': func_schema['function_name']})
            chat_db.add({'role': 'tool', 'content': str(function_output), 'name': func_schema['function_name']})
        resp = llm(messages, tools)
        chat_db.add({"role": "user", "content": resp})
        return resp
    else:
        chat_db.add({"role": "user", "content": resp})
        return resp
