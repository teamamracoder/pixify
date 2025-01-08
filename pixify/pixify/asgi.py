import os
from django.core.asgi import get_asgi_application
from socketio import AsyncServer, ASGIApp

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pixify.settings")

# Socket.IO server
sio = AsyncServer(async_mode="asgi", cors_allowed_origins="*")

# Django ASGI application
django_asgi_app = get_asgi_application()

# Combined ASGI application
application = ASGIApp(sio, other_asgi_app=django_asgi_app)

# Define socket events
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    # await sio.emit("response", {"message": "Welcome!"}, to=sid)

@sio.event
async def message(sid, data):
    print(f"Message from {sid}: {data}")
    # Broadcast message to all connected clients
    await sio.emit("response", {"message": data})

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")
