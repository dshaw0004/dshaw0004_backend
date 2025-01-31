import sqlite3
from flask import Flask, g
# from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import  Bcrypt
from flask_cors import CORS
from flask_socketio import SocketIO
# from flask_migrate import  Migrate
from backend.constants import ROOT_DIR

db_path = ROOT_DIR + '/database.db'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///default.db'
# db = SQLAlchemy(app, session_options={"autoflush":False})
# migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_path)
        db.cursor().execute('''
        CREATE TABLE IF NOT EXISTS AppInfo(
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        app_link TEXT NOT NULL,
        platform TEXT NOT NULL,
        thumbnail TEXT,
        version TEXT,
        author TEXT
        )'''
        )
    return db

@app.teardown_appcontext
def shutdown_session(exception=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
