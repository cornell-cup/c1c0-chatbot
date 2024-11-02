from client.config import * # Configuration
from client.client import OpenAPI # Client Interface


def recognize(api: OpenAPI, message: str) -> bool:
    # desc: str     = 'General: Any task related to requesting general knowledge or information.'
    # example1: str = 'Hey C1C0, what is Cornell Cup Robotics?'
    # example2: str = 'Hey C1C0, what it today\'s date?'
    # example3: str = 'Hey C1C0, tell me a joke.'

    example1: str = 'Question or request about Cornell Cup Robotics project team'
    example2: str = 'Questions or requests about current or famous events'
    example3: str = 'Requests on anything funny.'

    # questions to ask
    #   what is today's date

    matchThresh: dict[str] = {example1: SPECIFIC_THRESHOLD, example2: GENERAL_THRESHOLD, example3: GENERAL_THRESHOLD} 
    #associate each example or category with its own threshhold 

    # print(matches)
    matches: list[str] = list(matchThresh.keys())
    # print(matches)
    matchlabel, score = api.categorize(message, matches)
    print(matchlabel, score)
    if score>matchThresh[matchlabel]:
        return True

    genEx: str    = 'Any request or question'
    _, genScore = api.categorize(message, [genEx])
    print(genScore)
    return True if genScore>VERY_GENERAL_THRESHOLD else False 
        



def handler(api: OpenAPI, message: str) -> str:
    # print(message)
    print(api.response(message))
 
    # print('General Handler Not Implemented Yet')


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
