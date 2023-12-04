from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return {
            'name': 'dshaw0004',
            'lang': 'python'
            }


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6969)
