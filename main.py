import os

from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin

from fstore import add_new_message, get_all_message

app = Flask(__name__)
CORS(app, resources={
    r'/getallmsg': {
        "origins": [
            'https://dshaw0004.netlify.app',
            'https://dshaw0004.web.app',
            'https://dshaw0004.firebaseapp.com',
            'https://dshaw0004.vercel.app',
            # 'http://192.168.199.249:6970/index.html'
        ]
    },
    r'/addnewmsg': {
        "origins": [
            'https://dshaw0004.netlify.app',
            'https://dshaw0004.web.app',
            'https://dshaw0004.firebaseapp.com',
            'https://dshaw0004.vercel.app',
            # 'http://192.168.199.249:6970/index.html'
        ]
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
    }
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
    allmess = get_all_message()
    return allmess


@app.route("/addnewmsg", methods=['POST'])
def addnewmsg():
    data = request.json
    add_new_message(data.get('message'), data.get('senderName'), data.get('senderContact'))
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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6969)
