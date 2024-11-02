from client.config import * # Configuration
from client.client import OpenAPI # Client Interface

from labels.config import handler as config_handler # Configuration Specifications

from typing import Any # Type Hinting


def recognize(api: OpenAPI, message: str) -> bool:
    desc: str     = 'Any request for general knowledge or information.'
    example1: str = 'What is Cornell Cup Robotics?'
    example2: str = 'What is today\'s date?'
    example3: str = 'Tell me a joke.'

    matches: list[str] = [desc, example1, example2, example3]
    _, score = api.categorize(message, matches)
    if (DEBUG): print(f"General: {score}")
    return score > LABEL_THRESHOLD


def handler(api: OpenAPI, message: str, client: Any) -> None:
    subtask1: str = 'Answer a general knowledge question.'
    subtask2: str = 'Answer a Cornell Cup Robotics question.'
    subtasks: list[str] = [subtask1, subtask2]
    label, score = api.categorize(message, subtasks)

    thresholds = {subtask1: SPECIFIC_THRESHOLD, subtask2: GENERAL_THRESHOLD}
    if label == subtask1 and score > thresholds[subtask1]: return subtask1_handler(api, message, client)
    if label == subtask2 and score > thresholds[subtask2]: return subtask2_handler(api, message, client)
    return config_handler(api, message, client)


def subtask1_handler(api: OpenAPI, message: str, client: Any) -> None:
    print(api.response(message))


def subtask2_handler(api: OpenAPI, message: str, client: Any) -> None:
    print(api.response(message))
