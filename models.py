from sys import platform
from app import db, bcrypt
import random
from sqlalchemy.orm import validates

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    @validates('id')
    def validate_id(self, key, value):
        if not value:
            value = self.generate_unique_id()
        return value

    def generate_unique_id(self):
        while True:
            new_id = random.randint(100000, 999999)
            if not User.query.filter_by(id=new_id).first():
                return new_id

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.name}>'


class Friend(db.Model):
    __tablename__ = 'Friendship'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    user = db.relationship('User', foreign_keys=[user_id])
    friend = db.relationship('User', foreign_keys=[friend_id])

    def __repr__(self):
        return f'<Friend {self.user_id} - {self.friend_id}>'

class Chat(db.Model):
    __tablename__ = 'Chat'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)

    sender = db.relationship('User', foreign_keys=[sender_id])
    receiver = db.relationship('User', foreign_keys=[receiver_id])

    def __repr__(self):
        return f'<Chat {self.sender_id} -> {self.receiver_id}: {self.message}>'


class AppInfo(db.Model):
    __tablename__ = 'AppInfo'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    app_link = db.Column(db.Text, nullable=False)
    platform = db.Column(db.Text, nullable=False)
    thumbnail = db.Column(db.Text, nullable=True)
    version = db.Column(db.Text, nullable=False)
    author = db.Column(db.Text, nullable=False)

    def __repr__(self) -> str:
        return f'<AppInfo {self.name} {self.version} {self.author}>'

    def to_dict(self)-> dict:
        return {
                'id': self.id,
                'name': self.name,
                'description': self.description,
                'app_link': self.app_link,
                'platform': self.platform,
                'thumbnail': self.thumbnail,
                'version': self.version,
                'author': self.author
                }
