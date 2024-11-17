import socketio
from django.conf import settings

# Initialize the Socket.IO server with threading
sio = socketio.Server(async_mode='threading')

# Wrap Django’s WSGI application
django_app = settings.WSGI_APPLICATION
application = socketio.WSGIApp(sio, django_app)

# Define Socket.IO events
@sio.event
def connect(sid, environ):
    print(f"Client {sid} connected")

@sio.event
def disconnect(sid):
    print(f"Client {sid} disconnected")

@sio.event
def message(sid, data):
    print(f"Received message: {data}")
    # Send back a response
    sio.emit("response", {"message": f"Server received: {data}"}, room=sid)
