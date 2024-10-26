from client.config import * # Configuration
from client.client import OpenAPI # Client Interface


def recognize(api: OpenAPI, message: str) -> bool:
    desc: str     = 'General: Any task related to requesting general knowledge or information.'
    example1: str = 'Hey C1C0, what is Cornell Cup Robotics?'
    example2: str = 'Hey C1C0, what it today\'s date?'
    example3: str = 'Hey C1C0, tell me a joke.'

    matches: list[str] = [desc, example1, example2, example3]
    _, score = api.categorize(message, matches)
    return score > LABEL_THRESHOLD


def handler(api: OpenAPI, message: str) -> str:
    # subtask1: str = 'Move the robot\'s body forward/backward/left/right.'
    # subtask2: str = 'Move the robot\'s strong arm up/down/left/right.'
    # subtask3: str = 'Move the robot\'s precise arm up/down/left/right.'
    # subtask4: str = 'Make the robot\'s head rotate left/right/reset.'

    # subtasks: list[str] = [subtask1, subtask2, subtask3, subtask4]
    # label, _ = api.categorize(message, subtasks)

    # print("Movement Handler: ", message, label)
    # if label == subtask1: return subtask1_handler(api, message)
    # if label == subtask2: return subtask2_handler(api, message)
    # if label == subtask3: return subtask3_handler(api, message)
    # if label == subtask4: return subtask4_handler(api, message)
    # return config_handler(api, message)
    print('General Handler Not Implemented Yet')
