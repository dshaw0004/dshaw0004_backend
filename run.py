from app import app, socketio
from app import db
import routes

if '__main__' == __name__:
    print('going to run the app.')
    with app.app_context():
        db.create_all()
        socketio.run(app, port=5000, host='0.0.0.0', allow_unsafe_werkzeug=True )
    # app.run(host='0.0.0.0', debug=True)