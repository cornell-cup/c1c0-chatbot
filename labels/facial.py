from client.config import * # Configuration
from client.client import OpenAPI # Client Interface

from labels.config import handler as config_handler # Configuration Specifications



def recognize(api: OpenAPI, message: str) -> bool:
    desc: str     = 'Facial Recognition: Any task involving C1C0 identifying/learning a person\'s face.'
    example1: str = 'Hey C1C0, who am I?'
    example2: str = 'Hey C1C0, remember my face, I am X.'
    example3: str = 'Hey C1C0, forget my face, I am X.'

    matches: list[str] = [desc, example1, example2, example3]
    _, score = api.categorize(message, matches)
    return score > LABEL_THRESHOLD


def handler(api: OpenAPI, message: str) -> str:
    subtask1: str = 'Recognize a person\'s face and say their name.'
    subtask2: str = 'Learn a person\'s face and save their name.'

    subtasks: list[str] = [subtask1, subtask2]
    label: str = api.categorize(message, subtasks)

    print("Facial Handler: ", message, label)
    if label == subtask1: return subtask1_handler(api, message)
    if label == subtask2: return subtask2_handler(api, message)
    return config_handler(api, message)


def subtask1_handler(api: OpenAPI, message: str) -> str:
    print('facial_get: attendance')


def subtask2_handler(api: OpenAPI, message: str) -> str:
    print('facial_put: learn')
