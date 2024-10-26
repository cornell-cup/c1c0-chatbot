from client.config import *  # Configuration
from client.client import OpenAPI  # Client Interface
from client.config import LABEL_THRESHOLD  # Configuration

from labels.config import handler as config_handler  # Configuration Specifications

from typing import Any  # Type Annotations


def recognize(api: OpenAPI, message: str) -> bool:
    desc: str     = 'Movement: Any command involving moving or rotating the robot\'s body or arms.'
    example1: str = 'Hey C1C0, move forward X feet.'
    example2: str = 'Hey C1C0, raise your strong/weak arm X degrees.'
    example3: str = 'Hey C1C0, rotate your head X degrees.'

    matches: list[str] = [desc, example1, example2, example3]
    _, score = api.categorize(message, matches)
    return score > LABEL_THRESHOLD


def handler(api: OpenAPI, message: str, client: Any) -> str:
    subtask1: str = 'Move the robot\'s body forward/backward/left/right.'
    subtask2: str = 'Move the robot\'s strong arm up/down/left/right.'
    subtask3: str = 'Move the robot\'s precise arm up/down/left/right.'
    subtask4: str = 'Make the robot\'s head rotate left/right/reset.'

    subtasks: list[str] = [subtask1, subtask2, subtask3, subtask4]
    label, _ = api.categorize(message, subtasks)

    if client is None:
        print('Movement: ', label)
        return

    if label == subtask1: return subtask1_handler(api, message, client)
    if label == subtask2: return subtask2_handler(api, message, client)
    if label == subtask3: return subtask3_handler(api, message, client)
    if label == subtask4: return subtask4_handler(api, message, client)
    return config_handler(api, message)


def subtask1_handler(api: OpenAPI, message: str, client: Any) -> str:
    print('movement_put: locomotion')


def subtask2_handler(api: OpenAPI, message: str, client: Any) -> str:
    print('movement_put: strong_arm')


def subtask3_handler(api: OpenAPI, message: str, client: Any) -> str:
    print('movement_put: precise_arm')


def subtask4_handler(api: OpenAPI, message: str, client: Any) -> str:
    print('movement_put: rotate')
