from client.config import * # Configuration
from client.client import OpenAPI # Client Interface

from labels.config import handler as config_handler # Configuration Specifications

from typing import Any # Type Hinting


#recognizes if message is a request or question, examples are just certain instances that belong to subtasks
#example1 belongs to subtask2, example2 belongs to subtask1, etc 
def recognize(api: OpenAPI, message: str) -> bool:
    desc: str     = 'Any request for general knowledge or information.'
    example1: str = 'What is Cornell Cup Robotics?'
    example2: str = 'What about the laboratory?'
    example3: str = 'What is C1C0?'
    example4: str = 'Questions about you.'
    # example2: str = 'What is today\'s date?'
    # example3: str = 'Tell me a joke.'

    matches: list[str] = [desc, example1, example2, example3]
    _, score = api.categorize(message, matches)
    if (DEBUG): print(f"General: {score}")
    return score > GENERAL_THRESHOLD


def handler(api: OpenAPI, message: str, client: Any) -> None:
    subtask1: str = 'Answer a Cornell Cup Robotics question.'
    subtask2: str = 'Answer a lab-related or experiment question.'
    subtask3: str = 'Answer a question or request about C1C0.'
    subtask4: str = 'Answer a question or request about you.'


    subtasks: list[str] = [subtask1, subtask2, subtask3, subtask4]
    label, score = api.categorize(message, subtasks)

    thresholds = {subtask1: SPECIFIC_THRESHOLD, subtask2: SPECIFIC_THRESHOLD, subtask3: SPECIFIC_THRESHOLD, subtask4: SPECIFIC_THRESHOLD}
    if label == subtask1 and score > thresholds[subtask1]: 
        return subtask1_handler(api, message, client)
    if label == subtask2 and score > thresholds[subtask2]: 
        return subtask2_handler(api, message, client)
    if (label == subtask3 and score > thresholds[subtask3]) or (label == subtask4 and score > thresholds[subtask4]): 
        return subtask3_handler(api, message, client)
    return config_handler(api, message, client)


#handles requests and questions related to cornell cup robotics
def subtask1_handler(api: OpenAPI, message: str, client: Any) -> None:
    context = """You are helping to answer a question or request related to Cornell Cup Robotics. 
    Cornell Cup Robotics is a student run organization at Cornell University that designs, manufactures, 
    and creates innovative robotics oriented projects. Over 70 Cornell students work to create dynamic 
    projects that bolster the ingenuity of embedded technologies. Since 2010, our projects have been 
    showcased at many conferences and we have received support from numerous robotics and technology 
    companies.
    """
    print(api.response(message, context))

#handles requests and questions related to lab
def subtask2_handler(api: OpenAPI, message: str, client: Any) -> None:
    context = """You are helping to answer a question or request related lab. This can include questions 
    about measurements, laboratory instruments, experiments, chemical recipes, and experimental design.
    """
    print(api.response(message, context))

#handles requests and questions related to C1C0
def subtask3_handler(api: OpenAPI, message: str, client: Any) -> None:
    context = """You are helping to answer a question or request about yourself. C1C0 (which is you) 
    is an original R2D2 project focused upon creating a semi-autonomous lab assistant that could navigate
    and map out its surrounding environment. We have since renamed that project to C1C0 and given it the 
    ability to interact with its surroundings. This allows the droid to complete tasks such as opening a 
    door, recognizing and greeting individual people, and even firing a nerf dart at a target! To generate
    excitement and interest in robotics and engineering, the team has advertised the C1C0 project at various 
    events like (Club Fairs, Science Fairs, whatever else you can think of), and are looking for more.
    """    
    print(api.response(message, context))
