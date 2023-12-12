import os

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin

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
        "origins": ALLOWED_ORIGIN
    },
    r'/addnewmsg': {
        "origins": ALLOWED_ORIGIN
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
    auth = request.headers.get('Authorization')
    if auth == os.getenv('AUTH'):
        allmess = get_all_message()
        return jsonify(allmess)
    else:
        return jsonify({"permission": "denied"}), 404

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

@app.route("/appstore", methods=['post'])
def addnewmsg_appstore():
    
    data = request.json
    add_new_message(message="for appstore"+data.get('message'), senderName=data.get(
        'senderName'), senderContact=data.get('senderContact'))
    return {
        'your_name': data.get('senderName'),
        'your_message': data.get('message'),
        'your_contact': data.get('senderContact')
    }



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6969)
