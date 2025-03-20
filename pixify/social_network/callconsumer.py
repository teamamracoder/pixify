from channels.generic.websocket import AsyncWebsocketConsumer
import json

class CallConsumer(AsyncWebsocketConsumer):
    # Track active users per call group and caller channels per call_id
    active_users = {}
    # Mapping: call_group_name -> list of user detail dicts
    joined_users = {}  
    call_initiators = {}  # Mapping: call_id -> caller's channel name

    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.call_group_name = f"call_{self.chat_id}"

        # Get user details from scope; provide fallbacks if needed.
        user = self.scope.get("user")
        if user and user.is_authenticated:
            user_id = user.id
            full_name = f"{user.first_name} {user.last_name}".strip() or user.username
            profile_photo = user.profile_photo_url or "/static/images/default-profile.png"
        else:
            user_id = None
            full_name = "Anonymous"
            profile_photo = "/static/images/default-profile.png"

        # Build a user details dict.
        self.user_details = {
            "id": user_id,
            "name": full_name,
            "photo": profile_photo
        }

        # Increase active users count and add user details to joined_users list.
        if self.call_group_name not in self.active_users:
            self.active_users[self.call_group_name] = 0
        self.active_users[self.call_group_name] += 1

        if self.call_group_name not in self.joined_users:
            self.joined_users[self.call_group_name] = []
        self.joined_users[self.call_group_name].append(self.user_details)

        # Join the room group.
        await self.channel_layer.group_add(self.call_group_name, self.channel_name)
        await self.accept()

        # Broadcast that a user has joined with the updated user list.
        await self.channel_layer.group_send(
            self.call_group_name,
            {
                "type": "user.joined",
                "chat_id": self.chat_id,
                "active_users": self.active_users[self.call_group_name],
                "user_list": self.joined_users[self.call_group_name]
            }
        )

        print(f"[WebSocket] {self.user_details['name']} connected to chat {self.chat_id}, Active users: {self.active_users[self.call_group_name]}")

    async def disconnect(self, close_code):
        # Get user id from our stored details.
        user_id = self.user_details.get("id")

        # Decrease active users count and remove user details from joined_users list.
        if self.call_group_name in self.active_users:
            self.active_users[self.call_group_name] -= 1
            if self.active_users[self.call_group_name] <= 0:
                del self.active_users[self.call_group_name]

        if self.call_group_name in self.joined_users and user_id is not None:
            # Remove any entry with matching id.
            self.joined_users[self.call_group_name] = [
                user for user in self.joined_users[self.call_group_name] if user.get("id") != user_id
            ]
            if not self.joined_users[self.call_group_name]:
                del self.joined_users[self.call_group_name]

        # Remove from call_initiators if this channel was stored.
        for call_id, channel in list(self.call_initiators.items()):
            if channel == self.channel_name:
                del self.call_initiators[call_id]

        # Leave the room group.
        await self.channel_layer.group_discard(self.call_group_name, self.channel_name)

        # Broadcast that a user has left with the updated user list.
        await self.channel_layer.group_send(
            self.call_group_name,
            {
                "type": "user.left",
                "chat_id": self.chat_id,
                "active_users": self.active_users.get(self.call_group_name, 0),
                "user_list": self.joined_users.get(self.call_group_name, [])
            }
        )

        print(f"[WebSocket] {self.user_details['name']} disconnected from chat {self.chat_id}, Remaining users: {self.active_users.get(self.call_group_name, 0)}")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            action = data.get("action")

            if action == "ringing":
                # Called when the caller initiates a call.
                call_id = data["call_id"]
                self.call_initiators[call_id] = self.channel_name
                await self.channel_layer.group_send(
                    self.call_group_name,
                    {
                        "type": "ringing",
                        "call_id": call_id,
                        "chat_id": self.chat_id,
                        "caller_id": data.get("caller_id")
                    }
                )

            elif action == "call_accepted":
                call_id = data["call_id"]
                receiver = data["receiver"]
                caller_channel = self.call_initiators.get(call_id)
                if caller_channel:
                    await self.channel_layer.send(
                        caller_channel,
                        {
                            "type": "call.accepted",
                            "call_id": call_id,
                            "chat_id": self.chat_id,
                            "receiver": receiver
                        }
                    )
                    del self.call_initiators[call_id]

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
                        "active_users": self.active_users[self.call_group_name],
                        "user_list": self.joined_users[self.call_group_name]
                    }
                )

            elif action == "user_left":
                await self.channel_layer.group_send(
                    self.call_group_name,
                    {
                        "type": "user.left",
                        "chat_id": self.chat_id,
                        "active_users": self.active_users.get(self.call_group_name, 0),
                        "user_list": self.joined_users.get(self.call_group_name, [])
                    }
                )

        except Exception as e:
            print(f"[WebSocket Error] Failed to process message: {e}")

    # Event Handlers

    async def ringing(self, event):
        await self.send(text_data=json.dumps({
            "action": "ringing",
            "call_id": event["call_id"],
            "chat_id": event["chat_id"],
            "caller_id": event["caller_id"]
        }))

    async def call_accepted(self, event):
        await self.send(text_data=json.dumps({
            "action": "call_accepted",
            "call_id": event["call_id"],
            "chat_id": event["chat_id"],
            "receiver": event["receiver"]
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
            "active_users": event["active_users"],
            "user_list": event["user_list"]
        }))

    async def user_left(self, event):
        await self.send(text_data=json.dumps({
            "action": "user_left",
            "chat_id": event["chat_id"],
            "active_users": event["active_users"],
            "user_list": event["user_list"]
        }))
