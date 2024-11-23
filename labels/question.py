from client.config import * # Configuration
from client.client import OpenAPI # Client Interface

from labels.config import handler as config_handler # Configuration Specifications
from labels.config import IDKhandler

from typing import Any # Type Hinting


#recognizes if message is a request or question, examples are just certain instances that belong to subtasks
#example1 belongs to subtask2, example2 belongs to subtask1, etc 
def recognize(api: OpenAPI, message: str) -> bool:
    desc: str     = 'Questions about Cornell Cup Robotics, laboratory, or C1C0.'
    example1: str = 'What is Cornell Cup Robotics?'
    example2: str = 'What about the laboratory?'
    example3: str = 'What is C1C0?'
    example4: str = 'Questions about you.'
    # example2: str = 'What is today\'s date?'
    # example3: str = 'Tell me a joke.'

    matches: list[str] = [desc, example1, example2, example3, example4]
    _, score = api.categorize(message, matches)
    if (DEBUG): print(f"Question: {score}")
    return score


def handler(api: OpenAPI, message: str, client: Any) -> None:
    subtask1: str = 'Answer a Cornell Cup Robotics question.'
    subtask2: str = 'Answer a lab-related or experiment question.'
    subtask3: str = 'Answer anything about C1C0 or you.'
 

    subtasks: list[str] = [subtask1, subtask2, subtask3]
    label, score = api.categorize(message, subtasks)
    # thresholds = {subtask1: SPECIFIC_THRESHOLD, subtask2: SPECIFIC_THRESHOLD, subtask3: SPECIFIC_THRESHOLD}
    if (DEBUG): print(label, score)

    if label == subtask1 and score >= SPECIFIC_THRESHOLD: 
        if (DEBUG): print("subtask1")
        return subtask1_handler(api, message, client)
    if label == subtask2 and score >= SPECIFIC_THRESHOLD: 
        if (DEBUG): print("subtask2")
        return subtask2_handler(api, message, client)
    
    if (label == subtask3 and score >= SPECIFIC_THRESHOLD):
        if (DEBUG): print("subtask3")
        return subtask3_handler(api, message, client)
    
    return IDKhandler(api, message, client)


#handles requests and questions related to cornell cup robotics
def subtask1_handler(api: OpenAPI, message: str, client: Any) -> str:
    context = """You are helping to answer a question or request related to Cup Robotics. Cornell 
    Cup Robotics is a project team at Cornell University - comprised of over 70 students that works on 
    innovative robotics projects, like Minibot, C1C0, and BOB (Bidirectional Operational Bot). Their 
    projects have been showcased at many conferences and have been supported by numerous robotics and 
    technology companies. Cornell University undergraduates who are interested in computer science, 
    engineering, or communications can join. 
    """
    if (DEBUG): print("1: This is related to CORNELL CUP ROBOTICS")
    return api.response(message, context)


#handles requests and questions related to lab
def subtask2_handler(api: OpenAPI, message: str, client: Any) -> str:
    context = """You are helping to answer a question or request related lab. This can include questions 
    about measurements, laboratory instruments, experiments, chemical recipes, and experimental design."""
    
    if (DEBUG): print("2: This is related to LAB")
    return api.response(message, context)

#handles requests and questions related to C1C0
def subtask3_handler(api: OpenAPI, message: str, client: Any) -> None:
    context = """You are helping to answer a question or request about yourself. C1C0 (which is you) 
    is an R2D2 project focused upon creating a semi-autonomous lab assistant that could navigate
    its surrounding environment, interact with its surroundings, and greet people! We have advertised 
    C1C0 in events to promote enthusiasm for robotics.
    """    

    #converts any similar words from message to C1C0 so it can interpret properly 
    message = message.split()
    buzzWords = set(["Kiko", "Chico", "Keeko", "kiko", "chico", "keeko"])
    for i in range(len(message)):
        if message[i] in buzzWords:
            message[i] = 'C1C0'
    message = " ".join(message)
    if (DEBUG): print(message)

    print("3: This is related to C1C0")

    return api.response(message, context)


