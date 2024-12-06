from api.rotateAPI import * # Rotate Utilities

from client.config import * # Configuration
from client.client import OpenAPI # Client Interface

from labels.config import handler as config_handler # Configuration Specifications

import ast, time, spacy
from typing import Any, List # Type Hinting

nlp = spacy.load("en_core_web_sm")


def recognize(api: OpenAPI, message: str) -> float:
    desc: str     = 'Any task involving facial recognition.'
    example1: str = 'Who do you recognize around you?'
    example2: str = "Who am I? What's my name?"
    example2: str = 'Learn my face/name, I am X.'

    matches: List[str] = [desc, example1, example2]
    _, score = api.categorize(message, matches)
    if (DEBUG): print(f"Facial Recognition: {score}")
    return score


subtask1: str = 'Recognize a singular face or person.'
subtask2: str = 'Look around and recognize every face or person.'
subtask3: str = 'Learn/remember a face, person, or name.'


def handler(api: OpenAPI, message: str, client: Any) -> None:
    subtasks: List[str] = [subtask1, subtask2, subtask3]
    label, _ = api.categorize(message, subtasks)

    if label == subtask1: return subtask1_handler(api, message, client)
    if label == subtask2: return subtask2_handler(api, message, client)
    if label == subtask3: return subtask3_handler(api, message, client)
    return config_handler(api, message)


def get_facial_names(api: OpenAPI, client: Any) -> List[str]:
    _ = client.communicate('put', 'facial_get: attendance')
    response = client.communicate('get', 'facial_put: null')

    while (response.data == 'null'):
        time.sleep(1)
        response = client.communicate('get', 'facial_put: null')

    names: list = ast.literal_eval(response.data)
    return names


def subtask1_handler(api: OpenAPI, message: str, client: Any) -> None:
    if client is None:
        print(f'Attempted "{subtask1}" without a client.')
        return

    names: List[str] = get_facial_names(api, client)
    if len(names) == 0: return "I don't recognize anyone."
    else: return f"I recognize {names[0]}."


def subtask2_handler(api: OpenAPI, message: str, client: Any) -> None:
    if client is None:
        print(f'Attempted "{subtask2}" without a client.')
        return

    delay: float = 2.0
    names = get_facial_names(api, client)

    client.communicate('put', f'xbox_put: {left_rotate()}')
    time.sleep(delay)
    client.communicate('put', f'xbox_put: {zero_rotate()}')
    names = names + get_facial_names(api, client)

    client.communicate('put', f'xbox_put: {right_rotate()}')
    time.sleep(2*delay)
    client.communicate('put', f'xbox_put: {zero_rotate()}')
    names = names + get_facial_names(api, client)

    names = list(set(names))
    if len(names) == 0: return "I don't recognize anyone."
    else: return f"I recognize {', '.join(names)}."


def extract_name(message: str) -> str:
    doc = nlp(message)
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

    if len(names) == 0: return None
    return max(names, key=len)


def subtask3_handler(api: OpenAPI, message: str, client: Any) -> None:
    if client is None:
        print(f'Attempted "{subtask3}" without a client.')
        return

    name = extract_name(message) or 'Unknown'
    _ = client.communicate('put', f'facial_get: learn {name}')
    response = client.communicate('get', 'facial_put: null')

    while (response.data == 'null'):
        time.sleep(1)
        response = client.communicate('get', 'facial_put: null')

    print(f"I have learned the face of {name}.")
