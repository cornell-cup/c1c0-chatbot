import sys
import os
sys.path.insert(1, "util")

import json
import keywords
import make_response
from api import weather
from util import nlp_util
from util import utils

if __name__ == "__main__":
    utils.set_classpath()
    with open("tests/weather_and_places.txt") as f:
    #with open("tests/weather_question_tests.txt") as f:
        for line in f:
            print(line.strip())
            topic_data = keywords.get_topic(line)
            if topic_data["name"] == "weather":
                '''
                data = None
                if "location" in topic_data["info"]:
                    data = weather.lookup_weather_today_city(topic_data["info"]["location"])
                else:
                    data = weather.lookup_weather_today_city("ithaca new york")
                '''
                data = weather.lookup_weather_today_city(topic_data["info"]["location"]["name"])
                
                #print(json.dumps(data))
                print(make_response.make_response_api(topic_data, data))
                print()


