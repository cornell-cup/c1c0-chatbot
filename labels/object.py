from client.config import * # Configuration
from client.client import OpenAPI # Client Interface

from labels.config import handler as config_handler # Configuration Specifications

import time
from typing import Any, List # Type Hinting


def recognize(api: OpenAPI, message: str) -> float:
    desc: str     = 'Any task involving object detection.'
    example1: str = 'What is the most prominent object in front of you?'
    example2: str = "How many objects are in front of you?"
    example3: str = "Name every object in front of you."

    matches: List[str] = [desc, example1, example2, example3]
    _, score = api.categorize(message, matches)
    if (DEBUG): print(f"Object Detection: {score}")
    return score


subtask1: str = 'Recognize the singular item in front of you.'
subtask2: str = 'How many items are directly in front of you.'
subtask3: str = 'Look around and recognize every object.'


def handler(api: OpenAPI, message: str, client: Any) -> None:
    subtasks: List[str] = [subtask1, subtask2, subtask3]
    label, _ = api.categorize(message, subtasks)

    if label == subtask1: return subtask1_handler(api, message, client)
    if label == subtask2: return subtask2_handler(api, message, client)
    if label == subtask3: return subtask3_handler(api, message, client)
    return config_handler(api, message)


def subtask1_handler(api: OpenAPI, message: str, client: Any) -> None:
    if client is None:
        print(f'Attempted "{subtask1}" without a client')
        return
    
    _ = client.communicate('put', f'object_get: main')
    response = client.communicate('get', 'object_put: null')

    while (response.data == 'null'):
        time.sleep(1)
        response = client.communicate('get', 'object_put: null')
    
    print("Most prominent object detected")


def subtask2_handler(api: OpenAPI, message: str, client: Any) -> None:
    if client is None:
        print(f'Attempted "{subtask2}" without a client')
        return
    
    _ = client.communicate('put', f'object_get: count')
    response = client.communicate('get', 'object_put: null')

    while (response.data == 'null'):
        time.sleep(1)
        response = client.communicate('get', 'object_put: null')
    
    print("Objects Counted")  


def subtask3_handler(api: OpenAPI, message : str, client: Any) -> None:
    if client is None:
        print(f'Attempted "{subtask3}" without a client')
        return
    
    _ = client.communicate('put', f'object_get: all')
    response = client.communicate('get', 'object_put: null')

    while (response.data == 'null'):
        time.sleep(1)
        response = client.communicate('get', 'object_put: null')
    
    print("Objects counted")