from client.audio import speech_to_text, file_to_text, recognize_C1C0, remove_C1C0  # Audio Interface
from client.client import OpenAPI # Client Interface
from client.config import FILE_MODE # Configuration

from labels.config import recognize as config_recognize, handler as config_handler  # Configuration Specifications
from labels.question import recognize as question_recognize, handler as question_handler  # Question Specifications
from labels.movement import recognize as movement_recognize, handler as movement_handler  # Movement Specifications
from labels.facial import recognize as facial_recognize, handler as facial_handler  # Facial Specifications
from labels.general import recognize as general_recognize, handler as general_handler # General Specifications

from client.audio import text_to_speech, play_random_sound, play_sound

import numpy as np
from typing import Callable, Dict # Type Hinting
import collections


#inputs audio responses from the user, creates mappings to handlers, maps the input to the correct handler
if __name__ == '__main__':
    # Initializing OpenAI client
    chatbot_client: OpenAPI = OpenAPI()
    scheduler_client = None

    # Initialzing response handlers and mapping
    mapping: Dict[str, Callable[[str], None]] = {
        facial_recognize:   lambda msg: facial_handler(chatbot_client, msg, scheduler_client),
        movement_recognize: lambda msg: movement_handler(chatbot_client, msg, scheduler_client),
        question_recognize:  lambda msg: question_handler(chatbot_client, msg, scheduler_client),
        config_recognize:   lambda msg: config_handler(chatbot_client, msg, scheduler_client)
        # general_recognize:  lambda msg: general_handler(chatbot_client, msg, scheduler_client)
    }

    #Initialize threshold for each task 
    thresholds: Dict[str, int] = {
        facial_recognize: 0.5,
        movement_recognize: 0.4,
        question_recognize: 0.3,
        config_recognize: 0.8
    }
    
    
    # Infinite loop for chatbot
    while True:
        # Receiving audio from user or file
        msg: str = file_to_text() if FILE_MODE else speech_to_text()
        print(f"\033[32mUser: {msg}\033[0m")

        # Checking and removing C1C0 name from message
        if (not msg) or (not remove_C1C0(msg)) or not recognize_C1C0(msg):
            print('C1C0 Command Not Recognized.')
            continue
        msg = remove_C1C0(msg)

        #converts any similar words from message to C1C0 so it can interpret properly 
        msg = msg.split()
        buzzWords = set(["Kiko", "Chico", "Keeko", "kiko", "chico", "keeko"])
        for i in range(len(msg)):
            if msg[i] in buzzWords:
                msg[i] = 'C1C0'
        msg = " ".join(msg)

        #storing message to previous messages to store context, deletes if exceeds 10 
        if msg:
            chatbot_client.context.append(msg)
            if len(chatbot_client.context)>5:
                chatbot_client.context.popleft()
        print(chatbot_client.context)

        # Finding and calling handler for message
        print(f"\033[32mCommand: {msg}\033[0m")
        best_handler, best_score = None, 0

        #make copy of context
        #while copy of context still has context and no best handler is assigned
        # prevcopy = prevtexts[:]
        # while prevcopy and not best_handler:
        for recognize, handler in mapping.items():
            score = recognize(chatbot_client, msg)
            #this ensures only best score is chosen and nothing that does not meet threshold is chosen
            if (score-thresholds[recognize])>best_score: 
                best_handler, best_score = handler, score   
            # cont = prevcopy.pop()
            
        play_random_sound()
        if best_handler:
            text_to_speech(best_handler(msg))    

        #goes to the general handler if there are no other matches    
        else:    
            # print(chatbot_client.response("Summarize context in at most three words", chatbot_client.context))
            text_to_speech(general_handler(chatbot_client, msg, scheduler_client))
        play_random_sound()



            


