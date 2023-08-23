from flask_socketio import SocketIO, disconnect, emit

socketio = SocketIO()


@socketio.on("connect", namespace="/a")
def connect():
    emit("resp", {"data": "Connected", "count": 0})


@socketio.on("web_event", namespace="/a")
def message(mess):
    emit("resp", {"data": mess["data"]})


@socketio.on("disconnect_request", namespace="/a")
def local_disconnect_request():
    emit("resp", {"data": "Disconnected!"})
    socketio.sleep(0)
    disconnect()
