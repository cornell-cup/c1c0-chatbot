from flask import Flask, request
from flask_s3 import FlaskS3

s3 = FlaskS3()
config_filename = 'app.cfg'

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    s3.init_app(app)

    from views import chatbot_qa, sentiment_analysis, weather_restaurant, command_type
    app.register_blueprint(chatbot_qa.chatbot_qa)
    app.register_blueprint(sentiment_analysis.sentiment_analysis)
    app.register_blueprint(weather_restaurant.weather_restaurant)
    app.register_blueprint(command_type.command_type_blueprint)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=80)
