from api.rotateAPI import * # Rotate Utilities

from client.audio import play_random_sound  # Sound Utilities
from client.config import *  # Configuration
from client.client import OpenAPI  # Client Interface
from client.config import LABEL_THRESHOLD, MAC_MODE  # Configuration

from labels.config import handler as config_handler  # Configuration Specifications

import time
from typing import Any  # Type Annotations


def recognize(api: OpenAPI, message: str) -> bool:
    desc: str     = 'Any command involving moving or rotating.'
    example1: str = 'Move forward X feet.'
    example2: str = 'Raise your strong/weak arm X degrees.'
    example3: str = 'Rotate your head X degrees.'
    example4: str = 'Look left/right/around.'

    matches: list[str] = [desc, example1, example2, example3, example4]
    _, score = api.categorize(message, matches)
    if (DEBUG): print(f"Movement: {score}")
    return score > LABEL_THRESHOLD


def handler(api: OpenAPI, message: str, client: Any) -> str:
    subtask1: str = 'Move body forward/backward/left/right.'
    subtask2: str = 'Move strong arm up/down/left/right.'
    subtask3: str = 'Move precise arm up/down/left/right.'
    subtask4: str = 'Make head rotate left/right.'

    subtasks: list[str] = [subtask1, subtask2, subtask3, subtask4]
    label, _ = api.categorize(message, subtasks)

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
    if client is None:
        print('Make head rotate left/right.')
        return
    delay: float = 2.0

    if 'left' in message or 'around' in message:
        client.communicate('put', f'xbox_put: {left_rotate()}')
        time.sleep(delay)
        client.communicate('put', f'xbox_put: {zero_rotate()}')
        time.sleep(delay)
        if (not MAC_MODE): play_random_sound()

    if 'right' in message or 'around' in message:
        client.communicate('put', f'xbox_put: {right_rotate()}')
        time.sleep(delay)
        client.communicate('put', f'xbox_put: {zero_rotate()}')
        time.sleep(delay)
        if (not MAC_MODE): play_random_sound()

    if 'around' in message:
        client.communicate('put', f'xbox_put: {right_rotate()}')
        time.sleep(delay)
        client.communicate('put', f'xbox_put: {zero_rotate()}')
        time.sleep(delay)
        client.communicate('put', f'xbox_put: {left_rotate()}')
        time.sleep(delay)
        client.communicate('put', f'xbox_put: {zero_rotate()}')
        time.sleep(delay)
        if (not MAC_MODE): play_random_sound()
