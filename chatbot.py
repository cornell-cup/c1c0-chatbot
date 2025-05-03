from client.audio import *  # Audio Interface
from client.client import OpenAPI # Client Interface
from client.config import FILE_MODE, MAC_MODE # Configuration

from labels.config import recognize as config_recognize, handler as config_handler  # Configuration Specifications
from labels.facial import recognize as facial_recognize, handler as facial_handler  # Facial Specifications
from labels.object import recognize as object_recognize, handler as object_handler # Object Specifications
from labels.general import recognize as general_recognize, handler as general_handler # General Specifications
from labels.movement import recognize as movement_recognize, handler as movement_handler  # Movement Specifications
from labels.question import recognize as question_recognize, handler as question_handler  # Question Specifications

from typing import Callable, Dict # Type Hinting


if __name__ == '__main__':
    # Initializing OpenAI client
    chatbot_client: OpenAPI = OpenAPI()
    scheduler_client = None

    # Initializing response handlers and mapping
    def config_lambda(msg: str): return config_handler(chatbot_client, msg, scheduler_client)
    def facial_lambda(msg: str): return facial_handler(chatbot_client, msg, scheduler_client)
    def object_lambda(msg: str): return object_handler(chatbot_client, msg, scheduler_client)
    def general_lambda(msg: str): return general_handler(chatbot_client, msg, scheduler_client)
    def movement_lambda(msg: str): return movement_handler(chatbot_client, msg, scheduler_client)
    def question_lambda(msg: str): return question_handler(chatbot_client, msg, scheduler_client)

    mapping: Dict[str, Callable[[str], None]] = {
        config_recognize:   config_lambda,
        facial_recognize:   facial_lambda,
        object_recognize:   object_lambda,
        general_recognize:  general_lambda,
        movement_recognize: movement_lambda,
        question_recognize: question_lambda,
    }

    # Initialize threshold for each task
    thresholds: Dict[str, int] = {
        config_recognize: 0.6,
        facial_recognize: 0.5,
        object_recognize: 0.5,
        general_recognize: 0.3,
        movement_recognize: 0.4,
        question_recognize: 0.3,
    }

    # Infinite loop for chatbot
    while True:
        # Receiving audio from user or file
        msg: str = file_to_text() if FILE_MODE else speech_to_text()
        print(f"\033[32mUser: {msg}\033[0m")

        # Checking and converting STT message
        if msg is None or not recognize_C1C0(msg):
            print('C1C0 Command Not Recognized.')
            continue
        msg = remove_C1C0(msg)
        msg = convert_C1C0(msg)

        # Finding and calling handler for message
        print(f"\033[32mCommand: {msg}\033[0m")
        best_handler, best_score = None, 0

        for recognize, handler in mapping.items():
            score = recognize(chatbot_client, msg)
            if score - thresholds[recognize] > best_score:
                best_handler, best_score = handler, score - thresholds[recognize]
        print("Best Handler: ", best_handler if best_handler else "None")

        if (not MAC_MODE): play_random_sound()
        text = best_handler(msg) if best_handler \
            else "I did not understand the message. Please repeat it again or elaborate."
        if (text is not None): text_to_speech(text)
        if (not MAC_MODE): play_random_sound()

        # Storing previous messages
        chatbot_client.previous.append(msg)
        if len(chatbot_client.previous) > 5:
            chatbot_client.previous.remove(0)
