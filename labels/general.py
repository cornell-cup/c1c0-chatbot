from client.config import * # Configuration
from client.client import OpenAPI # Client Interface

from labels.config import handler as config_handler # Configuration Specifications
from labels.config import IDKhandler

from typing import Any # Type Hinting


#recognizes if message is a request or question, examples are just certain instances that belong to subtasks
#example1 belongs to subtask2, example2 belongs to subtask1, etc 
def recognize(api: OpenAPI, message: str) -> bool:
    desc: str     = 'A question or request.'
    example1: str = 'Where is France?'
    example2: str = 'What happened in 1970?'
    example3: str = 'Give me examples of animals.'
    example4: str = 'What is computer science?'

    matches: list[str] = [desc, example1, example2, example3]
    _, score = api.categorize(message, matches)
    if (DEBUG): print(f"General: {score}")
    return score

def handler(api: OpenAPI, message: str, client: Any) -> None:
    # context = """"You are answering a question or request."""
    if (DEBUG): print("4: This is related to GENERAL TASKS")
    # print(api.response(message, context))
    return api.response(message)