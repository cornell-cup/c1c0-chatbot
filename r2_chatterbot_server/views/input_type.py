from flask import current_app, Blueprint, request

import sys
sys.path.insert(0,'/home/ec2-user/c1c0_aws_flask/r2-chatbot/r2_chatterbot')

from util import input_type

input_type = Blueprint('input_type', __name__, url_prefix='/input_type')

@input_type.route('/', methods=['GET'])
def get_input_type():
    if request.method == 'GET':
        speech = request.args.get('speech', '')
        print("SPEECH: ", speech)
        data = keywords.get_topic(speech, parse_location=False)
        print(data)
        keywords.modify_topic_data(data, parse_location=True)
        print(data)
        response = "TEST"
        if "name" in data.keys() and data["name"] == "weather":
            keywords.modify_topic_data(data, parse_location=True)
            api_data = weather.lookup_weather_today_city(
                data["info"]["location"]["name"])
            response = make_response.make_response_api(
                data, api_data)
        elif "name" in data.keys() and data["name"] == "restaurant":
            keywords.modify_topic_data(data, parse_location=True)
            api_data = restaurant.lookup_restaurant_city(
                data["info"]["location"]["name"])
            response = make_response.make_response_api(
                data, api_data)


        return response
