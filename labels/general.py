from client.config import * # Configuration
from client.client import OpenAPI # Client Interface

from labels.config import handler as config_handler # Configuration Specifications
from labels.config import IDKhandler
from client.audio import text_to_speech

from typing import Any # Type Hinting


#recognizes if message is a request or question, examples are just certain instances that belong to subtasks
#example1 belongs to subtask2, example2 belongs to subtask1, etc 
def recognize(api: OpenAPI, message: str) -> bool:
    desc: str     = 'Anything.'
    example1: str = 'Where is France?'
    example2: str = 'What happened in 1970?'
    example3: str = 'Give me examples of animals.'
    example4: str = 'What is computer science?'
    example5: str = 'Hello.'

    matches: list[str] = [desc, example1, example2, example3, example4, example5]
    _, score = api.categorize(message, matches)
    if (DEBUG): print(f"General: {score}")
    return score

def handler(api: OpenAPI, message: str, client: Any) -> None:
    # context = """"You are answering a question or request."""
    if (DEBUG): print("4: This is related to GENERAL TASKS")  
    _, helloscore = api.categorize(message, ['Hello', "Hi", "What's going", "What's good", "What's up"])   
    print(helloscore) 
    if helloscore>=0.7:
        text_to_speech("Hello, I am C1C0. How can I assist you today?")  
        return 
    # print(api.response(message, context))
    context = """You are C1C0, a helpful and polite lab assistant."""
    return api.response(message, context=context)

