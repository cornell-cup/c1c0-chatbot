from client.config import * # Configuration
from client.client import OpenAPI # Client Interface

from typing import Any # Type Hinting


def recognize(api: OpenAPI, message: str) -> bool:
    desc: str = 'Configuration: Any task related to turning on or off C1C0\'s settings or error handling.'
    example1: str = 'Hey C1C0, turn off voice recognition.'

    matches: list[str] = [desc, example1]
    _, score = api.categorize(message, matches)
    return score > LABEL_THRESHOLD


def handler(api: OpenAPI, message: str, client: Any) -> None:
    subtask1: str = 'Turn off voice recognition feature of C1C0.'
    subtask2: str = 'Could not understand the audio message.'

    subtasks = [subtask1, subtask2]
    label: str = api.categorize(message, subtasks)

    if client is None:
        print('Configuration: ', label)
        return

    if label == subtask1: return subtask1_handler(api, message)
    if label == subtask2: return subtask2_handler(api, message)


def subtask1_handler(api: OpenAPI, message: str) -> None:
    print("Ending Chatbot Loop")
    exit(0)


def subtask2_handler(api: OpenAPI, message: str) -> None:
    print("No Audio Parsed")
