from client.config import * # Configuration
from client.client import OpenAPI # Client Interface

from labels.config import handler as config_handler # Configuration Specifications
from labels.config import IDKhandler

from typing import Any # Type Hinting


def recognize(api: OpenAPI, message: str) -> bool:
    desc: str     = 'Any request for general knowledge or information.'
    example1: str = 'What is Cornell Cup Robotics?'
    example2: str = 'What about the laboratory?'
    example3: str = 'What is C1C0?'
    example4: str = 'Questions about you.'

    matches: list[str] = [desc, example1, example2, example3, example4]
    _, score = api.categorize(message, matches)
    if (DEBUG): print(f"General: {score}")
    return score


def handler(api: OpenAPI, message: str, client: Any) -> None:
    subtask1: str = 'Answer a Cornell Cup Robotics question.'
    subtask2: str = 'Answer a lab-related or experiment question.'
    subtask3: str = 'Answer a question or request about Kiko, Chico, or you'
    gentask: str = 'Answer a question or request'

    subtasks: list[str] = [subtask1, subtask2, subtask3, gentask]
    label, score = api.categorize(message, subtasks)
    print(label, score)

    if label == subtask1 and score >= SPECIFIC_THRESHOLD:
        print("subtask1")
        return subtask1_handler(api, message, client)
    if label == subtask2 and score >= SPECIFIC_THRESHOLD:
        print("subtask2")
        return subtask2_handler(api, message, client)

    if (label == subtask3 and score >= SPECIFIC_THRESHOLD):
        print("subtask3")
        return subtask3_handler(api, message, client)
    if (label == gentask and score >= GENERAL_THRESHOLD):
        print("gentask")
        return gentask_handler(api, message, client)

    return IDKhandler(api, message, client)


def subtask1_handler(api: OpenAPI, message: str, client: Any) -> str:
    context = """You are helping to answer a question or request related to Cornell Cup Robotics. Cornell
    Cup Robotics is a project team at Cornell University - comprised of over 70 students that works on
    innovative robotics projects. Their projects have been showcased at many conferences and have been
    supported by numerous robotics and technology companies.
    """

    print("1: This is related to CORNELL CUP ROBOTICS")
    return api.response(message, context)


def subtask2_handler(api: OpenAPI, message: str, client: Any) -> str:
    context = """You are helping to answer a question or request related lab. This can include questions
    about measurements, laboratory instruments, experiments, chemical recipes, and experimental design."""

    print("2: This is related to LAB")
    return api.response(message, context)


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
    print(message)

    print("3: This is related to C1C0")
    return api.response(message, context)


def gentask_handler(api: OpenAPI, message: str, client: Any) -> None:
    context = """"You are answering a question or request."""
    print("4: This is related to GENERAL TASKS")
    # print(api.response(message, context))
    return api.response(message, context)
