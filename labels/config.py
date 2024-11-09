from client.config import * # Configuration
from client.client import OpenAPI # Client Interface

from typing import Any # Type Hinting


def recognize(api: OpenAPI, message: str) -> float:
    desc: str = 'Any task related to settings or error handling.'
    example1: str = 'Turn off voice recognition.'

    matches: list[str] = [desc, example1]
    _, score = api.categorize(message, matches)
    if (DEBUG): print(f"Configuration: {score}")
    return score



#turn off handler 
def handler(api: OpenAPI, message: str, client: Any) -> None:
    subtask1: str = 'Turn off voice recognition feature.'

    subtasks = [subtask1]
    label, _ = api.categorize(message, subtasks)

    if label == subtask1: return subtask1_handler(api, message, client)

#IDK handler
def IDKhandler(api: OpenAPI, message: str, client: Any) -> None:
    print("I did not understand the message. Please repeat it again.")


def subtask1_handler(api: OpenAPI, message: str, client: Any) -> None:
    print("Ending Chatbot Voice Recognition")
    print(f"Embedding Token Usage: {api.embed_tokens}")
    print(f"Chat Token Usage: {api.chat_tokens}")
    exit(0)
