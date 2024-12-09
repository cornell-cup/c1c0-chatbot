from client.config import * # Configuration
from client.client import OpenAPI # Client Interface

from labels.config import handler as config_handler # Configuration Specifications
from client.audio import text_to_speech

from typing import Any # Type Hinting


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


subtask1: str = 'Return a greeting/welcome.'
subtask2: str = 'How are you doing today.'

def handler(api: OpenAPI, message: str, client: Any) -> None:
    subtasks: list[str] = [subtask1, subtask2]
    label, score = api.categorize(message, subtasks)

    if label == subtask1 and score > SPECIFIC_THRESHOLD:
        return subtask1_handler(api, message, client)
    if label == subtask2 and score > SPECIFIC_THRESHOLD:
        return subtask1_handler(api, message, client)

    context: str = "You are C1C0, a helpful and polite lab assisstant."
    return api.response(message, context=context)


def subtask1_handler(api: OpenAPI, message: str, client: Any) -> str:
    context = "Return a greeting introducing yourself, how you are feeling, and offering assistance."
    return api.response(message, context=context)
