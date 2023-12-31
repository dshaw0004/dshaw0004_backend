import os

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from appbucket import add_new_app, get_all_app_info
from appbucket import get_all_suggestions, add_new_suggestion
from fstore import add_new_message, get_all_message

ALLOWED_ORIGIN = [
    'https://dshaw0004.netlify.app',
    'https://dshaw0004.web.app',
    'https://dshaw0004.firebaseapp.com',
    'https://dshaw0004.vercel.app',
    # 'http://192.168.199.249:6970/index.html',
    'http://localhost:3000'
]

app = Flask(__name__)
CORS(app, resources={
    r'/getallmsg': {
        "origins": ['*']
    },
    r'/addnewmsg': {
        "origins": ['*']
    },
    r'/': {
        "origins": [
            "*"
        ]
    },
    r'/login': {
        "origins": [
            "*"
        ]
    },
    r"/appstore/appsinfo/add": {
        "origins": [
            "*"
        ]
    },
    r"/appstore/appsinfo/get": {
        "origins": [
            "*"
        ]
    },
    r"/appstore/suggestion/get": {
        "origins": [
            "*"
        ]
    },
    r"/appstore/suggestion/add": {
        "origins": [
            "*"
        ]
    },
})


@app.route("/")
def index():
    return {
        'username': 'dshaw0004',
        'portfolio': 'https://dshaw0004.netlify.app',
        'fullname': 'Dipankar Shaw',
        'linkedin': 'https://www.linkedin.com/in/dshaw0004',
        'twitter': 'https://twitter.com/dshaw0004',
        'github': 'https://github.com/dshaw0004'
    }


@app.route("/getallmsg")
def allmes():
    auth = request.headers.get('Authorization')
    if auth == os.getenv('AUTH'):
        allmess = get_all_message()
        return jsonify(allmess)
    else:
        return jsonify({"permission": "denied"}), 404


@app.route("/addnewmsg", methods=['POST'])
def addnewmsg():
    data = request.json
    add_new_message(data.get('message'), data.get(
        'senderName'), data.get('senderContact'))
    return {
        'your_name': data.get('senderName'),
        'your_message': data.get('message'),
        'your_contact': data.get('senderContact')
    }


@app.route("/login", methods=['POST'])
def login():
    data = request.json
    if data.get('email') == os.getenv("email") and data.get("password") == os.getenv("password"):
        return {
            'access': 'granted',
            'id': 'admin'
        }
    else:
        return {
            'access': 'denied',
            'id': 'unknown'
        }


@app.route("/appstore/suggestion/add", methods=['post'])
def add_new_suggestion_appstore():

    data = request.json
    add_new_suggestion(name=data.get('name'), description=data.get(
        'suggestion'), senderContact=data.get('senderContact'))
    return {
        'your_name': data.get('name'),
        'your_suggestion': data.get('suggestion'),
        'your_contact': data.get('senderContact')
    }


@app.route("/appstore/suggestion/get")
def get_suggestion_appstore():
    auth = request.headers.get('Authorization')
    if auth == os.getenv('AUTH'):
        allmess = get_all_suggestions()
        return jsonify(allmess)
    else:
        return jsonify({"permission": "denied"}), 404


@app.route("/appstore/appsinfo/get")
def all_apps_info():
    auth = request.headers.get('Authorization')
    if auth == os.getenv('AUTH'):
        allmess = get_all_app_info()
        return jsonify(allmess)
    else:
        return jsonify({"permission": "denied"}), 404


@app.route("/appstore/appsinfo/add", methods=['POST'])
def add_new_app_info():
    data = request.json
    app_info = {
        'name': data.get('name'),
        'description': data.get('description'),
        'appLink': data.get('appLink'),
        'platform': data.get("platform"),
        'thumbnail': data.get("thumbnail"),
        'version': data.get("version")
    }
    add_new_app(app_info)
    return app_info


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6969)
