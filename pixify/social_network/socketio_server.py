from django.core.wsgi import get_wsgi_application
import socketio

sio = socketio.Server(async_mode="eventlet")
django_app = get_wsgi_application()  # Use the callable, not a string
application = socketio.WSGIApp(sio, django_app)

@sio.event
def connect(sid, environ):
    print(f"Client {sid} connected")

@sio.event
def disconnect(sid):
    print(f"Client {sid} disconnected")
