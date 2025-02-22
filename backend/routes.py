import os
import datetime
import sqlite3
import requests
from backend import app, get_db, socketio
from flask import request, jsonify
from flask_socketio import join_room
from flask_socketio import emit
from uuid import uuid4


@app.route('/')
def index():
    return '<h1>I am working</h1>'

@app.route('/addnewapp', methods=['POST'])
def add_new_app():
    data = request.get_json()

    name = data['name']
    description = data.get('description', '')
    app_link = data['appLink']
    platform = data['platform']
    thumbnail = data.get('thumbnail', '')
    version = data.get('version')

    author = 'dshaw0004'
    app_id = author + '.' + name.replace(' ', '-')

    db = get_db()
    cur = db.cursor()

    # TODO: implement warning system for duplicate record.

    cur.execute('''
        INSERT INTO AppInfo VALUES(?, ?, ?, ?, ?, ?, ?, ?)''',
        (app_id, name, description, app_link, platform, thumbnail, version, author)
            )
    db.commit()

    return f'{name} is successfully added.'

@app.route('/getallapp')
def get_all_app():
    db = get_db()
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute('SELECT * FROM AppInfo')
    rows = cur.fetchall()
    data = [dict(row) for row in rows]
    return jsonify(data)

@app.route('/getapp/<app_id>', methods=['GET'])
def get_app_by_id(app_id):
    db = get_db()
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute('SELECT * FROM AppInfo WHERE id = ?', (app_id,))
    res = cur.fetchone()
    return jsonify(dict(res)), 200

@app.route('/updateapp', methods=['POST'])
def updateapp():
    # TODO: implement this.
    return 'this endpoint is not implement yet.'

@app.route('/deleteapp/<app_id>', methods=['DELETE'])
def delete_app(app_id):
    db = get_db()
    cur = db.cursor()
    # TODO: implement warning system for new record.
    # cur.execute('SELECT COUNT(*) FROM AppInfo WHERE id = ?')
    cur.execute('DELETE FROM AppInfo WHERE id = ?', (app_id,))
    return jsonify({'message': 'App deleted successfully'}), 200

@app.route('/deleteappbyname', methods=['DELETE'])
def delete_app_by_name():
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({'message': 'App name is required'}), 400

    # if not app_to_delete:
    #     return jsonify({'message': 'App not found'}), 404
    db = get_db()
    cur = db.cursor()
    # TODO: implement warning system for new record.
    # cur.execute('SELECT COUNT(*) FROM AppInfo WHERE id = ?')
    cur.execute('DELETE FROM AppInfo WHERE name = ?', (name,))

    return jsonify({'message': 'App deleted successfully'}), 200

@app.route('/digital-gold')
def digital_gold():
    current_date = datetime.date.today()

    today = f'{current_date.year}-{current_date.month}-{current_date.day}'
    tomorrow = f'{current_date.year}-{current_date.month}-{current_date.day + 1}'

    # filename: str = 'gold-price-today.json'
    # if os.path.exists(filename):
    #     with open(filename, 'r') as file:
    #         file_content = file.read()
    #         if file_content:
    #             quote_dict = json.loads(file_content)
    #             if quote_dict.get('date') == today:
    #                 return quote_dict
    #     "https://www.safegold.com/user-trends/gold-rates?start_date=2017-06-23&end_date=2024-06-23&frequency=d"
    res = requests.get(
        f"https://www.safegold.com/user-trends/gold-rates?start_date={today}&end_date={tomorrow}&frequency=d"
    )

    res_json: dict = res.json()

    data: list[dict] = res_json.get('data')

    # with open(filename, 'w') as file:
    #     json.dump(data[-1], file)

    return data[-1]



# @app.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     name = data['name']
#     email = data['email']
#     password = data['password']

#     if User.query.filter_by(email=email).first():
#         return jsonify({'message': 'User already exists'}), 400

#     new_user = User(name=name, email=email)
#     new_user.set_password(password)
#     db.session.add(new_user)
#     db.session.commit()

#     return str(new_user.id), 201

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     email = data['email']
#     password = data['password']

#     user = User.query.filter_by(email=email).first()

#     if user and user.check_password(password):
#         return str(user.id), 200
#     else:
#         return jsonify({'message': 'Invalid email or password'}), 401

# @app.route('/user/<int:user_id>', methods=['GET'])
# def get_user_info(user_id):
#     user = User.query.get(user_id)
#     if not user:
#         return jsonify({'message': 'User not found'}), 404

#     friends = Friend.query.filter((Friend.user_id == user_id) | (Friend.friend_id == user_id)).all()
#     friends_info = []
#     for friend in friends:
#         friend_id = friend.friend_id if friend.user_id == user_id else friend.user_id
#         friend_user = User.query.get(friend_id)
#         friends_info.append({'id': friend_user.id, 'name': friend_user.name})

#     user_info = {
#         'id': user.id,
#         'name': user.name,
#         'friends': friends_info
#     }

#     return jsonify(user_info), 200

# @app.route('/messages/<int:user1_id>/<int:user2_id>', methods=['GET'])
# def get_messages(user1_id, user2_id):
#     messages = Chat.query.filter(
#         ((Chat.sender_id == user1_id) & (Chat.receiver_id == user2_id)) |
#         ((Chat.sender_id == user2_id) & (Chat.receiver_id == user1_id))
#     ).all()

#     messages_info = []
#     for message in messages:
#         messages_info.append({
#             'sender_id': message.sender_id,
#             'receiver_id': message.receiver_id,
#             'message': message.message
#         })

#     return jsonify(messages_info), 200

# @socketio.on('send_message')
# def handle_send_message(data):
#     sender_id = data['sender_id']
#     receiver_id = data['receiver_id']
#     message_text = data['message']

#     # Save the message to the database
#     new_message = Chat(sender_id=sender_id, receiver_id=receiver_id, message=message_text)
#     db.session.add(new_message)
#     db.session.commit()

#     # Forward the message to the receiver
#     emit('receive_message', {
#         'sender_id': sender_id,
#         'receiver_id': receiver_id,
#         'message': message_text
#     }, to=receiver_id)

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    # print(room)
    join_room(room)
    # send(username + ' has entered the room.', to=room)
    emit('newjoin', {'username': username}, broadcast=True, include_self=False, to=room)

@socketio.on('text')
def text(msg, room):
    emit('meessageBroadcast', {'message': msg, 'id': str(uuid4())}, broadcast=True, include_self=False, to=room)

@socketio.on('client_disconnecting')
def disconnect_details(username, room):
    emit('remove', {'username': f'{username} user disconnected.'}, broadcast=True, include_self=False, to=room)

@socketio.on('textync')
def textync(msg, room) -> None:
    emit( 'textsync', msg, broadcast=True, include_self=False, to=room)
