from app import app, db, socketio
from flask import render_template, request, jsonify
from .models import User, Friend, Chat
from flask_socketio import join_room, leave_room
from flask_socketio import send, emit
from uuid import uuid4

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'User already exists'}), 400

    new_user = User(name=name, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return new_user.id, 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        return user.id, 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_info(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    friends = Friend.query.filter((Friend.user_id == user_id) | (Friend.friend_id == user_id)).all()
    friends_info = []
    for friend in friends:
        friend_id = friend.friend_id if friend.user_id == user_id else friend.user_id
        friend_user = User.query.get(friend_id)
        friends_info.append({'id': friend_user.id, 'name': friend_user.name})

    user_info = {
        'id': user.id,
        'name': user.name,
        'friends': friends_info
    }

    return jsonify(user_info), 200

@app.route('/messages/<int:user1_id>/<int:user2_id>', methods=['GET'])
def get_messages(user1_id, user2_id):
    messages = Chat.query.filter(
        ((Chat.sender_id == user1_id) & (Chat.receiver_id == user2_id)) |
        ((Chat.sender_id == user2_id) & (Chat.receiver_id == user1_id))
    ).all()

    messages_info = []
    for message in messages:
        messages_info.append({
            'sender_id': message.sender_id,
            'receiver_id': message.receiver_id,
            'message': message.message
        })

    return jsonify(messages_info), 200

@socketio.on('send_message')
def handle_send_message(data):
    sender_id = data['sender_id']
    receiver_id = data['receiver_id']
    message_text = data['message']

    # Save the message to the database
    new_message = Chat(sender_id=sender_id, receiver_id=receiver_id, message=message_text)
    db.session.add(new_message)
    db.session.commit()

    # Forward the message to the receiver
    emit('receive_message', {
        'sender_id': sender_id,
        'receiver_id': receiver_id,
        'message': message_text
    }, to=receiver_id)

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

@socketio.on('textync')
def textync(msg, room) -> None:
    emit( 'textsync', msg, broadcast=True, include_self=False, to=room)
