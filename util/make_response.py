'''
This file contains functionality to generate chatbot responses to user
input
'''

import sys
sys.path.insert(1, "util")

from api import weather
import keywords

def make_response_api(topic_data, api_data):
    response = ""
    if topic_data["name"] == "weather":
        if "temperature" in topic_data["info"]:
            
            pass
        response = "There is %s"%(api_data["weather"][0]["description"])

    return response

if __name__ == "__main__":
    weather.import_keys()
    
    with open("./tests/question_keyword_tests.txt") as f:
        for line in f:
            topic = keywords.get_topic(line)
            if topic["name"] == "weather":
                weather_data = weather.lookup_weather_today_city(
                        "xian shaanxi")
                print(weather_data)
                response = make_response_api(topic, weather_data)
                print(response)
