from client.config import FUZZY_THRESHOLD

import re, random
import numpy as np
import sounddevice as sd
import speech_recognition as sr

from fuzzywuzzy import fuzz
from playsound import playsound
import pyttsx3


# Source: https://stackoverflow.com/questions/55984129/attributeerror-could-not-find-pyaudio-check-installation-cant-use-speech-re
class DuckTypedMicrophone( sr.AudioSource ):
    def __init__(self, device=None, samplerate=44100, channels=1):
        self.device     = device
        self.samplerate = samplerate
        self.channels   = channels

    def __enter__(self):
        self._stream = sd.InputStream(samplerate=self.samplerate, channels=self.channels, device=self.device)
        self._stream.start()

        self.CHUNK        = 1024
        self.SAMPLE_RATE  = self.samplerate
        self.SAMPLE_WIDTH = 2  # Assuming 16-bit samples
        return self

    def __exit__(self, *args):
        self._stream.stop()
        self._stream.close()

    def read(self, n_samples):
        audio_data = self._stream.read(n_samples)
        return np.int16(audio_data[0] * 32767).tobytes()  # Convert to 16-bit PCM

    @property
    def stream(self):
        return self


def speech_to_text() -> str:
    recognizer = sr.Recognizer()

    with DuckTypedMicrophone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("\033[94mWaiting for audio...\033[0m")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            return text

        except sr.UnknownValueError or sr.RequestError:
            return None

def text_to_speech(text: str) -> None:
    """
    Converts text to speech and plays it
    Args:
        text (str): The text to be converted to speech
    Returns:
        None
    """
    try:
        engine = pyttsx3.init()
        
        # Optional: Customize voice properties
        engine.setProperty('rate', 150)    # Speed of speech
        engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
        
        # Get available voices and set to a English voice
        voices = engine.getProperty('voices')
        
        # engine.setProperty('voice', voices[1].id)  # Index 0 is usually English
        
        # Convert and play
        engine.say(text)
        engine.runAndWait()
        
    except Exception as e:
        print(f"Error in text-to-speech: {str(e)}")
        return None


def play_sound(sound_file):
    try:
        playsound(sound_file)
    except Exception as e:
        print(f"Error playing sound: {e}")


def file_to_text() -> str:
    file: str = input("Filename: ")
    if (file == "exit" or file == "quit"):
        print("Ending Chatbot Voice Recognition")
        exit(0)

    recognizer = sr.Recognizer()
    path: str = "commands/" + file

    with sr.AudioFile(path) as source:
        audio = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio)
            return text

        except sr.UnknownValueError or sr.RequestError:
            return None


def recognize_C1C0(message: str) -> bool:
    names = ["Hey C1C0", "Hey Kiko", "Hey Google", "Hey Keko", "Hey Kee Koh", "Hey Chico", "Hey Chica"]
    _, score = fuzzy_match(message, names)
    return score >= FUZZY_THRESHOLD


def fuzzy_match(text, targets):
    scores = [fuzz.partial_ratio(text, target) for target in targets]
    return targets[np.argmax(scores)], np.max(scores)


def remove_C1C0(message: str) -> str:
    pattern = r"^(Hey\s(?:C1C0|Kiko|Google|Keko|Kee Koh|Chico|Chica))\s*,?\s*"
    cleaned = re.sub(pattern, "", message, flags=re.IGNORECASE)
    return cleaned.strip()


def play_random_sound():
    sounds = ['assets/r2d2-1.mp3', 'assets/r2d2-2.mp3', 'assets/r2d2-3.mp3', 'assets/r2d2-4.mp3']
    playsound(sounds[random.randint(0, 3)])
