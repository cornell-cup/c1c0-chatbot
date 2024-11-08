from client.config import * # Configuration
from client.client import OpenAPI # Client Interface

from typing import Any # Type Hinting


def recognize(api: OpenAPI, message: str) -> bool:
    desc: str = 'Any task related to settings or error handling.'
    example1: str = 'Turn off voice recognition.'

    matches: list[str] = [desc, example1]
    _, score = api.categorize(message, matches)
    # if (DEBUG): print(f"Configuration: {score}")
    return score > LABEL_THRESHOLD


def handler(api: OpenAPI, message: str, client: Any) -> None:
    subtask1: str = 'Turn off voice recognition feature of C1C0.'
    subtask2: str = 'Could not understand the audio message.'

    subtasks = [subtask1, subtask2]
    label, _ = api.categorize(message, subtasks)

    if label == subtask1: return subtask1_handler(api, message, client)
    if label == subtask2: return subtask2_handler(api, message, client)


def subtask1_handler(api: OpenAPI, message: str, client: Any) -> None:
    print("Ending Chatbot Voice Recognition")
    exit(0)


def subtask2_handler(api: OpenAPI, message: str, client: Any) -> None:
    print("No Audio Parsed")
