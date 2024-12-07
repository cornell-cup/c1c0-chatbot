from client.config import * # Configuration
from client.client import OpenAPI # Client Interface
from client.audio import text_to_speech
from typing import Any # Type Hinting


def recognize(api: OpenAPI, message: str) -> float:
    desc: str = 'Any task related to settings or error handling.'
    example1: str = 'Turn off voice recognition.'
    example2: str = 'Power off'

    matches: list[str] = [desc, example1, example2]
    _, score = api.categorize(message, matches)
    if (DEBUG): print(f"Configuration: {score}")
    return score


def handler(api: OpenAPI, message: str, client: Any) -> None:
    subtask1: str = 'Turn off voice recognition feature.'

    subtasks = [subtask1]
    label, _ = api.categorize(message, subtasks)

    if label == subtask1: return subtask1_handler(api, message, client)


def subtask1_handler(api: OpenAPI, message: str, client: Any) -> None:
    print("Ending Chatbot Voice Recognition")
    print(f"Embedding Token Usage: {api.embed_tokens}")
    print(f"Chat Token Usage: {api.chat_tokens}")
    exit(0)
