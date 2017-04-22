import os
from flask import Flask, render_template, request
import json
from flask_cors import CORS, cross_origin
from src.scripts.script import get_all_event_details_by_user_id
from src.scripts.script import initialize

application = Flask(__name__)
application.debug=True
CORS(application)

@application.route('/user/<user_id>', methods=['GET'])
def index(user_id):
    try:
        if request.method == "GET":
            initialize("crawler/cities/" + 'LCHICAGO')
            user_events_details = get_all_event_details_by_user_id(str(user_id))
            return json.dumps(user_events_details)
    except Exception as e:
        print e

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 33508))
    application.run(host='0.0.0.0', debug=True, port=port)
