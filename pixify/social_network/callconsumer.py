from channels.generic.websocket import AsyncWebsocketConsumer
import json

class CallConsumer(AsyncWebsocketConsumer):
    active_users = {}  # Dictionary to track active users in each call

    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.call_group_name = f"call_{self.chat_id}"

        # Add user to active users list
        if self.call_group_name not in self.active_users:
            self.active_users[self.call_group_name] = 0
        self.active_users[self.call_group_name] += 1

        # Join room group
        await self.channel_layer.group_add(self.call_group_name, self.channel_name)
        await self.accept()

        # Notify others about user joining
        await self.channel_layer.group_send(
            self.call_group_name,
            {
                "type": "user.joined",
                "chat_id": self.chat_id,
                "active_users": self.active_users[self.call_group_name]
            }
        )

        print(f"[WebSocket] User connected to chat {self.chat_id}, Active users: {self.active_users[self.call_group_name]}")

    async def disconnect(self, close_code):
        # Remove user from active users list
        if self.call_group_name in self.active_users:
            self.active_users[self.call_group_name] -= 1
            if self.active_users[self.call_group_name] <= 0:
                del self.active_users[self.call_group_name]

        # Leave room group
        await self.channel_layer.group_discard(self.call_group_name, self.channel_name)

        # Notify others about user leaving
        await self.channel_layer.group_send(
            self.call_group_name,
            {
                "type": "user.left",
                "chat_id": self.chat_id,
                "active_users": self.active_users.get(self.call_group_name, 0)
            }
        )

        print(f"[WebSocket] User disconnected from chat {self.chat_id}, Remaining users: {self.active_users.get(self.call_group_name, 0)}")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            action = data.get("action")

            if action == "call_started":
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

        except Exception as e:
            print(f"[WebSocket Error] Failed to process message: {e}")

    # Event Handlers

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
