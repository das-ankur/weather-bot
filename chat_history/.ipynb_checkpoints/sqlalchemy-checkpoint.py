# Import libraries
from typing import List, Tuple, Dict
import json
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from llama_token_counter import LlamaTokenCounter
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.messages.base import message_to_dict
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.messages import trim_messages




# Class to maintain chat_history
class ChatHistory:
    def __init__(self, max_conversation: int, max_token: int):
        self.db_path = 'sqlite:///chat_history.db'
        self.engine = create_engine(self.db_path)
        self.chat_history = SQLChatMessageHistory(session_id="weather-bot", connection=self.engine)
        self.max_conversation = max_conversation
        self.max_token = max_token
        self.token_counter = LlamaTokenCounter()
        
    def add(self, message: Dict) -> None:
        if message['role'] == 'user':
            message = HumanMessage(content=message['content'])
        elif message['role'] == 'assistant':
            message = AIMessage(content=message['content'])
        else:
            message = ToolMessage(tool_call_id=message['name'], content=message['content'])
        self.chat_history.add_message(message)
        
    def get_last_k_messages(self, k: int) -> List[Tuple]:
        Session = sessionmaker(bind=self.engine)
        session = Session()
        query = text(f"SELECT * FROM (SELECT * FROM message_store ORDER BY id DESC LIMIT {k}) ORDER BY id ASC;")
        result = session.execute(query).fetchall()
        session.close()
        return result
    
    def count_tokens(self, messages: List[Dict]) -> int:
        token_count = 0
        for message in messages:
            token_count += self.token_counter.count_tokens_sync(f"{message['role']}: {message['content']}")
        return token_count
        
    def get(self) -> List[Dict]:
        messages = self.get_last_k_messages(2*self.max_conversation)
        messages = [json.loads(message[2]) for message in messages]
        processed_messages = []
        for message in messages:
            if message['type'] == 'human':
                processed_messages.append(
                    {
                        'role': 'user',
                        'content': message['data']['content']
                    }
                )
            elif message['type'] == 'ai':
                processed_messages.append(
                    {
                        'role': 'assistant',
                        'content': message['data']['content']
                    }
                )
            else:
                processed_messages.append(
                    {
                        'role': 'tool',
                        'name': message['data']['tool_call_id'],
                        'content': message['data']['content']
                    }
                )
        while self.count_tokens(processed_messages) > self.max_token - 1000:
            try:
                processed_messages = processed_messages[2:]
            except Exception:
                processed_messages = processed_messages[1:]
        return processed_messages
        