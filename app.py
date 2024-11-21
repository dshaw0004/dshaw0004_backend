from uuid import uuid4
from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_socketio import join_room, leave_room
from flask_socketio import send, emit
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
cors = CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="http://localhost:5173")

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    print(room)
    join_room(room)
    # send(username + ' has entered the room.', to=room)
    emit('newjoin', {'username': username}, broadcast=True, include_self=False, to=room)

@socketio.on('text')
def text(msg, room):
    # print(data)
    emit('meessageBroadcast', {'message': msg, 'id': str(uuid4())}, broadcast=True, include_self=False, to=room)

@socketio.on('client_disconnecting')
def disconnect_details(username, room):
    emit('remove', {'username': f'{username} user disconnected.'}, broadcast=True, include_self=False, to=room)

if __name__ == '__main__':
    socketio.run(app, port=3428, host='0.0.0.0')
