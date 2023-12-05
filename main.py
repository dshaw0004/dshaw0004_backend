from flask import Flask, render_template

from .fstore import get_all_message

app = Flask(__name__)


@app.route("/")
def index():
    return {
        'name': 'dshaw0004',
        'lang': 'python'
    }


@app.route("/allmes")
def allmes():
    allmess = get_all_message()
    return allmess


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6969)
