from client.audio import speech_to_text, file_to_text, recognize_C1C0, remove_C1C0  # Audio Interface
from client.client import OpenAPI # Client Interface
from client.config import FILE_MODE # Configuration

from labels.config import recognize as config_recognize, handler as config_handler  # Configuration Specifications
from labels.general import recognize as general_recognize, handler as general_handler  # General Info Specifications
from labels.movement import recognize as movement_recognize, handler as movement_handler  # Movement Specifications
from labels.facial import recognize as facial_recognize, handler as facial_handler  # Facial Specifications
from client.audio import text_to_speech, play_random_sound

import numpy as np
from typing import Callable, Dict # Type Hinting



#inputs audio responses from the user, creates mappings to handlers, maps the input to the correct handler
if __name__ == '__main__':
    # Initializing OpenAI client
    chatbot_client: OpenAPI = OpenAPI()
    scheduler_client = None

    # Initialzing response handlers and mapping
    mapping: Dict[str, Callable[[str], None]] = {
        facial_recognize:   lambda msg: facial_handler(chatbot_client, msg, scheduler_client),
        movement_recognize: lambda msg: movement_handler(chatbot_client, msg, scheduler_client),
        general_recognize:  lambda msg: general_handler(chatbot_client, msg, scheduler_client),
        config_recognize:   lambda msg: config_handler(chatbot_client, msg, scheduler_client),
    }

    # Infinite loop for chatbot
    while True:
        # Receiving audio from user or file
        msg: str = file_to_text() if FILE_MODE else speech_to_text()
        # text_to_speech(msg)


        print(f"\033[32mUser: {msg}\033[0m")

        # Checking and removing C1C0 name from message
        if (not msg) or (not remove_C1C0(msg)) or not recognize_C1C0(msg):
            print('C1C0 Command Not Recognized.')
            continue
        msg = remove_C1C0(msg)

        #another check after removing C1C0 name 
        # if msg is None or not recognize_C1C0(msg):
        #     print('C1C0 Command Not Recognized.')
        #     continue

        # Finding and calling handler for message
        print(f"\033[32mCommand: {msg}\033[0m")
        best_handler, best_score = None, 0

        for recognize, handler in mapping.items():
            score = recognize(chatbot_client, msg)
            if score>best_score:
                best_handler, best_score = handler, score   
        best_handler(msg)

        # if best_handler==general_handler:
        play_random_sound()
        
        text_to_speech(best_handler(msg))
        play_random_sound()

        # index = np.argmax([recognize(chatbot_client, msg) for recognize, _ in mapping.items()])
        # _, handler = list(mapping.items())[index]
        # handler(msg)
