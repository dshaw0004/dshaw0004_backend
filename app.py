from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import  Bcrypt
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_migrate import  Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///default.db'
db = SQLAlchemy(app, session_options={"autoflush":False})
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()
