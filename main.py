from util import live_streaming
from util import nlp_util
from util import keywords
from util import make_response
from util import playtrack
from util import path_planning
from util import object_detection
from util.api import weather
from util.api import restaurant
from playsound import playsound
import re
import sys
import os

print(os.getcwd())
credential_path = "api_keys/Speech to Text-bef030531cd1.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

if "CLASSPATH" not in os.environ:
    os.environ["CLASSPATH"] = ""
os.environ["CLASSPATH"] += (":%s/dep/stanford-ner/stanford-ner.jar"%(os.getcwd()))
print(os.environ["CLASSPATH"])

def main():
    while True:
        #gets a tuple of phrase and confidence
        answer = live_streaming.main()
        speech = live_streaming.get_string(answer)
        confidence = live_streaming.get_confidence(answer)
        topic = keywords.get_topic(speech)
        print(speech)

        if "quit" in speech or "stop" in speech:
            break
        if path_planning.isLocCommand(speech.lower()):
            print(path_planning.pathPlanning(speech.lower()))
        if object_detection.isObjCommand(speech.lower()):
            print(object_detection.object_parse(speech.lower()))
        if topic["name"] == "weather":
            '''
            weather_data = weather.lookup_weather_today_city(
                    "ithaca new york")
            '''
            weather_data = weather.lookup_weather_today_city(topic["info"]["location"]["name"])
            response = make_response.make_response_api(topic, weather_data)
            print(response)
        elif topic["name"] == "restaurant":
            restaurant_data = restaurant.lookup_restaurant_city(topic["info"]["location"]["name"])
            response = make_response.make_response_api(topic, restaurant_data)
            print(response)


if __name__ == '__main__':
    #playsound('sounds/cicoremix.mp3')
    main()
