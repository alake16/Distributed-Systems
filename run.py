from app import app, socketio

if __name__ == '__main__':
    socketio.run(app, host="localhost", debug=True,port=4000)