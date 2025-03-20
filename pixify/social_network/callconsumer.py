from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .services import chat_service, user_service
from asgiref.sync import sync_to_async

class CallConsumer(AsyncWebsocketConsumer):
    # For simplicity, these remain class-level; in production, consider using external storage.
    active_users = {}
    joined_users = {}
    accepted_users = {}  # New: mapping: group_name -> list of users who accepted the call
    call_initiators = {}  # Mapping: call_id -> caller's channel name
    call_declines = {}     # Mapping: call_id -> set of callee channel names who declined

    async def get_user_chat_ids(self, user):
        """
        Return a list of chat IDs the user is part of.
        """
        print(user)
        chats = await sync_to_async(lambda: list(chat_service.get_all_user_chats(user)))()
        return chats

    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        user = self.scope.get("user")
        if self.chat_id == "all":
            self.chat_ids = await self.get_user_chat_ids(user)
        else:
            self.chat_ids = [self.chat_id]

        for cid in self.chat_ids:
            group_name = f"call_{cid}"
            if group_name not in self.active_users:
                self.active_users[group_name] = 0
            self.active_users[group_name] += 1

            if group_name not in self.joined_users:
                self.joined_users[group_name] = []
            # Build user details.
            if user and user.is_authenticated:
                user_id = user.id
                full_name = (
                    f"{user.first_name} " +
                    (f"{user.middle_name} " if user.middle_name else "") +
                    f"{user.last_name}"
                ).strip() or user.username
                profile_photo = user.profile_photo_url or "/static/images/avatar.jpg"
            else:
                user_id = None
                full_name = "Anonymous"
                profile_photo = "/static/images/avatar.jpg"

            user_details = {
                "id": user_id,
                "name": full_name,
                "photo": profile_photo
            }
            self.user_details = user_details
            self.joined_users[group_name].append(user_details)
            await self.channel_layer.group_add(group_name, self.channel_name)

        await self.accept()

        for cid in self.chat_ids:
            group_name = f"call_{cid}"
            # On connection, broadcast the joined users (this list shows everyone who connected).
            await self.channel_layer.group_send(
                group_name,
                {
                    "type": "user.joined",
                    "chat_id": cid,
                    "active_users": len(self.accepted_users.get(group_name, [])),
                    "user_list": self.accepted_users.get(group_name, [])
                }
            )
            print(f"[WebSocket] {self.user_details['name']} connected to chat {cid}, Active users: {self.active_users[group_name]}")

    async def disconnect(self, close_code):
        user_id = self.user_details.get("id")
        for cid in self.chat_ids:
            group_name = f"call_{cid}"
            if group_name in self.active_users:
                self.active_users[group_name] -= 1
                if self.active_users[group_name] <= 0:
                    del self.active_users[group_name]
            if group_name in self.joined_users and user_id is not None:
                self.joined_users[group_name] = [
                    user for user in self.joined_users[group_name] if user.get("id") != user_id
                ]
                if not self.joined_users[group_name]:
                    del self.joined_users[group_name]
            # Remove from accepted_users if present.
            if group_name in self.accepted_users and user_id is not None:
                self.accepted_users[group_name] = [
                    user for user in self.accepted_users[group_name] if user.get("id") != user_id
                ]
            await self.channel_layer.group_discard(group_name, self.channel_name)
            await self.channel_layer.group_send(
                group_name,
                {
                    "type": "user.left",
                    "chat_id": cid,
                    "active_users": len(self.accepted_users.get(group_name, [])),
                    "user_list": self.accepted_users.get(group_name, [])
                }
            )
            print(f"[WebSocket] {self.user_details['name']} disconnected from chat {cid}, Remaining users: {self.active_users.get(group_name, 0)}")

        # Also remove from call_initiators if present.
        for call_id, channel in list(self.call_initiators.items()):
            if channel == self.channel_name:
                del self.call_initiators[call_id]

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            action = data.get("action")
            if action == "ringing":
                call_id = data["call_id"]
                # Save caller's channel for this call.
                self.call_initiators[call_id] = self.channel_name
                actual_chat_id = data.get("chat_id")
                caller = await sync_to_async(user_service.get_user)(data.get("caller_id"))
                caller_full_name = (
                    f"{caller.first_name} " +
                    (f"{caller.middle_name} " if caller.middle_name else "") +
                    f"{caller.last_name}"
                )
                caller_image = caller.profile_photo_url or "/static/images/avatar.jpg"
                group_name = f"call_{actual_chat_id}"
                await self.channel_layer.group_send(
                    group_name,
                    {
                        "type": "ringing",
                        "call_id": call_id,
                        "chat_id": actual_chat_id,
                        "caller_id": data.get("caller_id"),
                        "caller_name": caller_full_name,
                        "caller_photo": caller_image
                    }
                )
            elif action == "call_accepted":
                call_id = data["call_id"]
                receiver = data["receiver"]
                actual_chat_id = data.get("chat_id")
                group_name = f"call_{actual_chat_id}"
                # Update accepted_users list for this group.
                if group_name not in self.accepted_users:
                    self.accepted_users[group_name] = []
                # Add this user only if not already added.
                if self.user_details not in self.accepted_users[group_name]:
                    self.accepted_users[group_name].append(self.user_details)
                # Notify the caller if present.
                caller_channel = self.call_initiators.get(call_id)
                if caller_channel:
                    await self.channel_layer.send(
                        caller_channel,
                        {
                            "type": "call.accepted",
                            "call_id": call_id,
                            "chat_id": actual_chat_id,
                            "receiver": receiver
                        }
                    )
                    del self.call_initiators[call_id]
                # Broadcast the updated active (accepted) participants list.
                await self.channel_layer.group_send(
                    group_name,
                    {
                        "type": "user.joined",
                        "chat_id": actual_chat_id,
                        "active_users": len(self.accepted_users[group_name]),
                        "user_list": self.accepted_users[group_name]
                    }
                )
            elif action == "webrtc_signal":
                actual_chat_id = data.get("chat_id")
                group_name = f"call_{actual_chat_id}"
                await self.channel_layer.group_send(
                    group_name,
                    {
                        "type": "webrtc.signal",
                        "signal": data["signal"],
                        "from": data["from"],
                        "chat_id": actual_chat_id
                    }
                )
            elif action == "user_joined":
                actual_chat_id = data.get("chat_id")
                group_name = f"call_{actual_chat_id}"
                # For active call page, treat a "user_joined" as acceptance.
                if group_name not in self.accepted_users:
                    self.accepted_users[group_name] = []
                if self.user_details not in self.accepted_users[group_name]:
                    self.accepted_users[group_name].append(self.user_details)
                # Broadcast updated accepted participants list.
                await self.channel_layer.group_send(
                    group_name,
                    {
                        "type": "user.joined",
                        "chat_id": actual_chat_id,
                        "active_users": len(self.accepted_users[group_name]),
                        "user_list": self.accepted_users[group_name]
                    }
                )
            elif action == "user_left":
                actual_chat_id = data.get("chat_id")
                group_name = f"call_{actual_chat_id}"
                await self.channel_layer.group_send(
                    group_name,
                    {
                        "type": "user.left",
                        "chat_id": actual_chat_id,
                        "active_users": len(self.accepted_users.get(group_name, [])),
                        "user_list": self.accepted_users.get(group_name, [])
                    }
                )
            elif action == "call_declined":
                call_id = data["call_id"]
                actual_chat_id = data.get("chat_id")
                group_name = f"call_{actual_chat_id}"
                if call_id not in self.call_declines:
                    self.call_declines[call_id] = set()
                self.call_declines[call_id].add(self.channel_name)
                
                total_in_group = self.active_users.get(group_name, 0)
                num_callees = total_in_group - 1 if call_id in self.call_initiators else total_in_group
                
                if len(self.call_declines[call_id]) >= num_callees:
                    caller_channel = self.call_initiators.get(call_id)
                    if caller_channel:
                        await self.channel_layer.send(
                            caller_channel,
                            {
                                "type": "call.terminated",
                                "call_id": call_id,
                                "chat_id": actual_chat_id
                            }
                        )
                    await self.channel_layer.group_send(
                        group_name,
                        {
                            "type": "call.terminated",
                            "call_id": call_id,
                            "chat_id": actual_chat_id
                        }
                    )
                    if call_id in self.call_initiators:
                        del self.call_initiators[call_id]
                    if call_id in self.call_declines:
                        del self.call_declines[call_id]
            elif action == "call_terminated":
                actual_chat_id = data.get("chat_id")
                call_id = data.get("call_id")
                group_name = f"call_{actual_chat_id}"
                await self.channel_layer.group_send(
                    group_name,
                    {
                        "type": "call.terminated",
                        "chat_id": actual_chat_id,
                        "call_id": call_id
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
            "caller_id": event["caller_id"],
            "caller_name": event.get("caller_name"),
            "caller_photo": event.get("caller_photo")
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

    async def call_terminated(self, event):
        await self.send(text_data=json.dumps({
            "action": "call_terminated",
            "chat_id": event["chat_id"],
            "call_id": event["call_id"]
        }))
