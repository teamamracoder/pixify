import json
import time
from channels.generic.websocket import AsyncWebsocketConsumer

class CallConsumer(AsyncWebsocketConsumer):
    # Dictionary to track active users in each call room (per chat)
    active_users = {}

    async def connect(self):
        # Retrieve chat_id from the URL route.
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.call_group_name = f"call_{self.chat_id}"

        # Update active user count for this room.
        if self.call_group_name not in self.active_users:
            self.active_users[self.call_group_name] = 0
        self.active_users[self.call_group_name] += 1

        # Optionally, store the last heartbeat timestamp.
        self.last_heartbeat = time.time()

        # Join the call group.
        await self.channel_layer.group_add(
            self.call_group_name,
            self.channel_name
        )
        await self.accept()

        # Notify the group that a new user has joined.
        await self.channel_layer.group_send(
            self.call_group_name,
            {
                "type": "user.joined",
                "chat_id": self.chat_id,
                "active_users": self.active_users[self.call_group_name]
            }
        )
        print(f"[WebSocket] User connected to chat {self.chat_id}. Active users: {self.active_users[self.call_group_name]}")

    async def disconnect(self, close_code):
        # Decrement active user count.
        if self.call_group_name in self.active_users:
            self.active_users[self.call_group_name] -= 1
            if self.active_users[self.call_group_name] <= 0:
                del self.active_users[self.call_group_name]

        # Leave the call group.
        await self.channel_layer.group_discard(
            self.call_group_name,
            self.channel_name
        )

        # Notify the group that a user has left.
        await self.channel_layer.group_send(
            self.call_group_name,
            {
                "type": "user.left",
                "chat_id": self.chat_id,
                "active_users": self.active_users.get(self.call_group_name, 0)
            }
        )
        print(f"[WebSocket] User disconnected from chat {self.chat_id}. Remaining users: {self.active_users.get(self.call_group_name, 0)}")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            action = data.get("action")

            if action == "heartbeat":
                self.last_heartbeat = time.time()
                await self.send(text_data=json.dumps({"action": "heartbeat_ack"}))
            elif action == "call_started":
                await self.channel_layer.group_send(
                    self.call_group_name,
                    {
                        "type": "call.started",
                        "call_id": data["call_id"],
                        "chat_id": self.chat_id
                    }
                )
            elif action == "call_accepted":
                await self.channel_layer.group_send(
                    self.call_group_name,
                    {
                        "type": "call.accepted",
                        "call_id": data["call_id"],
                        "chat_id": self.chat_id
                    }
                )
            elif action == "webrtc_signal":
                await self.channel_layer.group_send(
                    self.call_group_name,
                    {
                        "type": "webrtc.signal",
                        "signal": data["signal"],
                        "from": data["from"],
                        "chat_id": self.chat_id
                    }
                )
            elif action == "ringing":
                await self.channel_layer.group_send(
                    self.call_group_name,
                    {
                        "type": "call.ringing",
                        "call_id": data["call_id"],
                        "caller_id": data["caller_id"],
                        "chat_id": self.chat_id
                    }
                )
            elif action == "user_joined":
                await self.channel_layer.group_send(
                    self.call_group_name,
                    {
                        "type": "user.joined",
                        "chat_id": self.chat_id,
                        "active_users": self.active_users[self.call_group_name]
                    }
                )
            elif action == "user_left":
                await self.channel_layer.group_send(
                    self.call_group_name,
                    {
                        "type": "user.left",
                        "chat_id": self.chat_id,
                        "active_users": self.active_users.get(self.call_group_name, 0)
                    }
                )
            # Add additional actions as needed.
        except Exception as e:
            print(f"[WebSocket Error] Failed to process message: {e}")

    async def call_started(self, event):
        await self.send(text_data=json.dumps({
            "action": "call_started",
            "call_id": event["call_id"],
            "chat_id": event["chat_id"]
        }))

    async def call_accepted(self, event):
        await self.send(text_data=json.dumps({
            "action": "call_accepted",
            "call_id": event["call_id"],
            "chat_id": event["chat_id"]
        }))

    async def webrtc_signal(self, event):
        await self.send(text_data=json.dumps({
            "action": "webrtc_signal",
            "signal": event["signal"],
            "from": event["from"],
            "chat_id": event["chat_id"]
        }))

    async def user_joined(self, event):
        await self.send(text_data=json.dumps({
            "action": "user_joined",
            "chat_id": event["chat_id"],
            "active_users": event["active_users"]
        }))

    async def user_left(self, event):
        await self.send(text_data=json.dumps({
            "action": "user_left",
            "chat_id": event["chat_id"],
            "active_users": event["active_users"]
        }))

    async def call_ringing(self, event):
        await self.send(text_data=json.dumps({
            "action": "ringing",
            "call_id": event["call_id"],
            "caller_id": event["caller_id"],
            "chat_id": event["chat_id"]
        }))

    # Optional: send active speaker command.
    async def set_active_speaker(self, event):
        await self.send(text_data=json.dumps({
            "action": "set_active_speaker",
            "active_speaker": event["active_speaker"],
            "chat_id": event["chat_id"]
        }))
