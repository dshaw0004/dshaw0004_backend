from backend import app, socketio
import backend.routes

if '__main__' == __name__:
    print('going to run the app.')
    with app.app_context():
        socketio.run(app, port=5000, host='0.0.0.0', allow_unsafe_werkzeug=True, debug=True)
    # app.run(host='0.0.0.0', debug=True)
