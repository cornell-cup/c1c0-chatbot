from api.locomotionAPI import * # Locomotion Utilities
from api.rotateAPI import * # Head Rotation Utilities
from api.strongAPI import * # Strong Arm Utilities

from client.audio import play_random_sound  # Sound Utilities
from client.config import *  # Configuration
from client.client import OpenAPI  # Client Interface
from client.config import LABEL_THRESHOLD, MAC_MODE  # Configuration

from labels.config import handler as config_handler  # Configuration Specifications

import time
from typing import Any  # Type Annotations


def recognize(api: OpenAPI, message: str) -> float:
    desc: str     = 'Any command involving moving or rotating.'
    example1: str = 'Move forward X feet.'
    example2: str = 'Raise your strong/weak arm X degrees.'
    example3: str = 'Rotate your head X degrees.'
    example4: str = 'Look left/right/around.'

    matches: list[str] = [desc, example1, example2, example3, example4]
    _, score = api.categorize(message, matches)
    if (DEBUG): print(f"Movement: {score}")
    return score


subtask1: str = 'Move body forward/backward/left/right.'
subtask2: str = 'Move strong arm up/down to grab object.'
subtask3: str = 'Move precise arm up/down to grab object.'
subtask4: str = 'Make head rotate left/right to look around.'


def handler(api: OpenAPI, message: str, client: Any) -> str:
    subtasks: list[str] = [subtask1, subtask2, subtask3, subtask4]
    label, _ = api.categorize(message, subtasks)

    if label == subtask1: return subtask1_handler(api, message, client)
    if label == subtask2: return subtask2_handler(api, message, client)
    if label == subtask3: return subtask3_handler(api, message, client)
    if label == subtask4: return subtask4_handler(api, message, client)
    return config_handler(api, message)


def subtask1_handler(api: OpenAPI, message: str, client: Any) -> str:
    if client is None:
        print(f'Attempted "{subtask1}" without client.')
        return

    delay: float = 1.0
    if 'forward' in message or 'around' in message:
        client.communicate('put', f'xbox_put: {get_locomotion(0, 1)}')
        time.sleep(delay)
        client.communicate('put', f'xbox_put: {zero_locomotion()}')
        if (not MAC_MODE): play_random_sound()

    if 'right' in message or 'around' in message:
        client.communicate('put', f'xbox_put: {get_locomotion(1, 0)}')
        time.sleep(delay)
        client.communicate('put', f'xbox_put: {zero_locomotion()}')
        if (not MAC_MODE): play_random_sound()

    if 'backward' in message or 'around' in message:
        client.communicate('put', f'xbox_put: {get_locomotion(0, -1)}')
        time.sleep(delay)
        client.communicate('put', f'xbox_put: {zero_locomotion()}')
        if (not MAC_MODE): play_random_sound()

    if 'left' in message or 'around' in message:
        client.communicate('put', f'xbox_put: {get_locomotion(-1, 0)}')
        time.sleep(delay)
        client.communicate('put', f'xbox_put: {zero_locomotion()}')
        if (not MAC_MODE): play_random_sound()


def subtask2_handler(api: OpenAPI, message: str, client: Any) -> str:
    if client is None:
        print(f'Attempted "{subtask2}" without client.')
        return

    delay: float = 1.0
    if 'up' in message or 'around' in message:
        client.communicate('put', f'xbox_put: {move_shoulder(1)}')
        time.sleep(delay)
        client.communicate('put', f'xbox_put: {move_shoulder(0)}')

        client.communicate('put', f'xbox_put: {move_elbow(2)}')
        time.sleep(delay)
        client.communicate('put', f'xbox_put: {move_elbow(0)}')

        client.communicate('put', f'xbox_put: {move_hand(2)}')
        time.sleep(delay)
        client.communicate('put', f'xbox_put: {move_hand(0)}')

        client.communicate('put', f'xbox_put: {move_spin(1)}')
        time.sleep(delay)
        client.communicate('put', f'xbox_put: {move_spin(0)}')
        if (not MAC_MODE): play_random_sound()

    if 'down' in message or 'around' in message:
        client.communicate('put', f'xbox_put: {move_shoulder(2)}')
        time.sleep(delay)
        client.communicate('put', f'xbox_put: {move_shoulder(0)}')

        client.communicate('put', f'xbox_put: {move_elbow(1)}')
        time.sleep(delay)
        client.communicate('put', f'xbox_put: {move_elbow(0)}')

        client.communicate('put', f'xbox_put: {move_hand(1)}')
        time.sleep(delay)
        client.communicate('put', f'xbox_put: {move_hand(0)}')

        client.communicate('put', f'xbox_put: {move_spin(2)}')
        time.sleep(delay)
        client.communicate('put', f'xbox_put: {move_spin(0)}')
        if (not MAC_MODE): play_random_sound()


def subtask3_handler(api: OpenAPI, message: str, client: Any) -> str:
    print(f'Attempted {subtask3}')


def subtask4_handler(api: OpenAPI, message: str, client: Any) -> str:
    if client is None:
        print(f'Attempted "{subtask4}" without client.')
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
