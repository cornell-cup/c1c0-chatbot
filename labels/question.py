from client.config import * # Configuration
from client.client import OpenAPI # Client Interface

from typing import Any # Type Hinting


def recognize(api: OpenAPI, message: str) -> bool:
    desc: str     = 'Questions about Cornell Cup Robotics, C1C0, or related topics.'
    example1: str = 'What is Cornell Cup Robotics?'
    example2: str = 'Questions about C1C0 or you'
    example3: str = 'What are you, what can you do?'
    example4: str = 'What features does C1C0 have?'

    matches: list[str] = [desc, example1, example2, example3, example4]
    _, score = api.categorize(message, matches)
    if (DEBUG): print(f"Question: {score}")
    return score


def handler(api: OpenAPI, message: str, client: Any) -> None:
    subtask1: str = ['Cornell Cup Robotics question', 'Cornell Cup Robotics projects', 'Cup Robotics', 'Minibot', 'BOB', 'Bidirectional Operational Bot']
    subtask2: str = ['Lab-related', 'Experiment', 'Laboratory instruments', 'Experimental design', 'Measurements']
    subtask3: str = ['C1C0', 'You', 'Features', 'Looks', 'What C1C0 does', 'What you do']
 
    _, score1 = api.categorize(message, subtask1)
    _, score2 = api.categorize(message, subtask2)
    _, score3 = api.categorize(message, subtask3)

    if score1 == max(score1, score2, score3) and score1 >= SPECIFIC_THRESHOLD:
        return subtask1_handler(api, message, client)  
    if score2 == max(score1, score2, score3) and score2 >= SPECIFIC_THRESHOLD: 
        return subtask2_handler(api, message, client)
    if score3 == max(score1, score2, score3) and score3 >= SPECIFIC_THRESHOLD:
        return subtask3_handler(api, message, client)  
    return "I did not understand the message. Please repeat it again or elaborate."


def subtask1_handler(api: OpenAPI, message: str, client: Any) -> str:
    context = """You are helping to answer a question or request related to Cup 
    Robotics. Cornell Cup Robotics is a project team at Cornell University - 
    comprised of over 70 students - that works on innovative robotics projects. 
    Some projects include Minibot, C1C0, and BOB (Bidirectional Operational Bot).
    Their projects have been showcased at many conferences and have been supported
    by numerous robotics and technology companies."""
    return api.response(message, context)


def subtask2_handler(api: OpenAPI, message: str, client: Any) -> str:
    context = """You are helping to answer a question or request related lab. 
    This can include questions about measurements, laboratory instruments,
    experiments, chemical recipes, and experimental design."""
    return api.response(message, context)


def subtask3_handler(api: OpenAPI, message: str, client: Any) -> None:
    context = """You are helping to answer a question or request about yourself,
    so refer in first person. Anything about you is also related to C1C0. C1C0
    is an R2D2 project focused upon creating a semi-autonomous lab assistant that
    could navigate its surrounding environment, interact with its surroundings,
    and greet people! We have advertised C1C0 in events to promote enthusiasm for
    robotics. The features you have are a LIDAR sensor for navigation, an Intel 
    Realsense depth camera for vision, and a microphone for audio input/output.
    List your features when someone asks.
    """
    return api.response(message, context)


