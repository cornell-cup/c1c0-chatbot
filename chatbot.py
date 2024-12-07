from client.audio import speech_to_text, file_to_text, recognize_C1C0, remove_C1C0, convert_C1C0  # Audio Interface
from client.client import OpenAPI # Client Interface
from client.config import FILE_MODE # Configuration

from labels.config import recognize as config_recognize, handler as config_handler  # Configuration Specifications
from labels.question import recognize as question_recognize, handler as question_handler  # Question Specifications
from labels.movement import recognize as movement_recognize, handler as movement_handler  # Movement Specifications
from labels.facial import recognize as facial_recognize, handler as facial_handler  # Facial Specifications
from labels.general import recognize as general_recognize, handler as general_handler # General Specifications

from client.audio import text_to_speech, play_random_sound, play_sound

from typing import Callable, Dict # Type Hinting


if __name__ == '__main__':
    # Initializing OpenAI client
    chatbot_client: OpenAPI = OpenAPI()
    scheduler_client = None

    # Initialzing response handlers and mapping
    mapping: Dict[str, Callable[[str], None]] = {
        config_recognize:   lambda msg: config_handler(chatbot_client, msg, scheduler_client),
        facial_recognize:   lambda msg: facial_handler(chatbot_client, msg, scheduler_client),
        general_recognize:  lambda msg: general_handler(chatbot_client, msg, scheduler_client),
        movement_recognize: lambda msg: movement_handler(chatbot_client, msg, scheduler_client),
        question_recognize: lambda msg: question_handler(chatbot_client, msg, scheduler_client),
    }

    # Initialize threshold for each task 
    thresholds: Dict[str, int] = {
        config_recognize: 0.8,
        facial_recognize: 0.5,
        movement_recognize: 0.4,
        question_recognize: 0.3,
        general_recognize: 0.3,
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
            if score-thresholds[recognize] > best_score: 
                best_handler, best_score = handler, score   
            
        play_random_sound()
        if best_handler: text_to_speech(best_handler(msg))     
        else: text_to_speech("I did not understand the message. Please repeat it again or elaborate.")
        play_random_sound()

        # Storing previous messages
        chatbot_client.previous.append(msg)
        if len(chatbot_client.previous) > 5: 
            chatbot_client.previous.remove(0)



            


