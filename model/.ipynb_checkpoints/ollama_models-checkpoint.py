# Import librraies
from typing import List, Dict
import json
import ollama



# Ollama model class to invoke toll call
class OllamaModel:
    def __init__(self, model_name: str) -> None:
        self.model_name = model_name

    def __call__(self, messages: List[Dict], tools: List[Dict]=[]) -> str:
        completion = ollama.chat(
            model=self.model_name,
            messages=messages,
            tools=tools,
            # stream=True
        )
        if completion.message.tool_calls is not None:
            tools = []
            for tool in completion.message.tool_calls:
                tools.append({
                    'function_name': tool.function.name,
                    'function_args': tool.function.arguments
                })
            return tools
        else:
            return completion.message.content
        # for chunk in completion:
        #     if chunk.message.tool_calls is None and not tool_calls:
        #         return chunk.message.content
        #     else:
        #         if chunk.message.tool_calls is not None:
        #             tools = []
        #             for tool in chunk.message.tool_calls:
        #                 tools.append({
        #                     'function_name': tool.function.name,
        #                     'function_args': tool.function.arguments
        #                 })
        #             return tools
                    
                    
                

