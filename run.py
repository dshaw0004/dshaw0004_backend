from app import app, socketio
from app import db

if '__main__' == __name__:
    with app.app_context():
        db.create_all()
        socketio.run(app, port=5000, host='0.0.0.0')
    # app.run(host='0.0.0.0', debug=True)