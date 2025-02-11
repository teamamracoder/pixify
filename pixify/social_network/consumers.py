from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Message, Chat, ChatMember,User
from .services import message_service, message_mention_service, user_service,message_read_status_service,chat_service,message_reaction_service
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        # Accept WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action', None)
        message_id = text_data_json.get('message_id', None)
        chat_id = text_data_json.get('chat_id', None)        
        user_id =text_data_json.get('sender_id')
        del_type = text_data_json.get('del_type')
        user = self.scope['user']
        reaction_id=text_data_json.get('reaction_id')  
        call_id = text_data_json.get('call_id')  
        caller_id= text_data_json.get('caller_id')     

        print(f"The Received Data: {text_data_json}")

        if action == 'create':
            await self.create_message(text_data_json, user)
        elif action == 'edit':
            await self.edit_message(message_id, text_data_json, user)
        elif action == 'reply':
            await self.reply_message(message_id, text_data_json, user)
        elif action == 'delete':
            await self.delete_message(message_id, user_id, del_type)
        elif action == 'mark_as_read':
            await self.mark_message_as_read(message_id, user_id)
        elif action == 'add_reaction':
            await self.add_reaction(message_id,user,reaction_id)
        elif action == 'del_reaction':
            await self.delete_reaction(message_id,user)
        elif action == 'typing':
            await self.typing(user_id)
        elif action == 'stop_typing':
            await self.stop_typing(user_id)
        elif action == 'ringing':
            await self.ringing(chat_id,call_id,caller_id)

    async def typing(self,user_id):
        await self.typing_status(user_id,typing=True)

    async def stop_typing(self, user_id):
        await self.typing_status(user_id,typing=False)


    async def ringing(self, chat_id, call_id, caller_id):
        members = await sync_to_async(chat_service.chat_members)(chat_id)  # Get members list
        ringing_data = {
            'type': 'ringing_notification',
            'call_id': call_id,
            'chat_id': chat_id,
            'members': members,  
            'caller_id': caller_id,  # Include caller ID
        }
        await self.channel_layer.group_send(
            self.chat_group_name,
            ringing_data
        )

    async def ringing_notification(self, event):
        await self.send(text_data=json.dumps({
            'action': 'ringing',
            'call_id': event['call_id'],
            'chat_id': event['chat_id'], 
            'members': event['members'],
            'caller_id': event['caller_id']  # Include caller ID in notification
        }))
















    async def add_reaction(self, message_id, user, reaction_id):
        reaction_instance = await sync_to_async(
            message_reaction_service.create_or_update_message_reaction
        )(message_id, user, reaction_id)
        
        # Send reaction details using the instance
        await self.send_reaction_details(reaction_instance)

    async def delete_reaction(self, message_id, user):        
        react = await sync_to_async(message_reaction_service.get_active_reaction)(message_id, user)
        
        await sync_to_async(message_reaction_service.deactivate_reaction)(react)        
    
        await self.send_reaction_details(react)
        

    async def create_message(self, text_data_json, user):        
        text = text_data_json.get('message', '')
        media_files = text_data_json.get('mediaFiles', [])
        mentions = text_data_json.get('mentions', [])
        chat_id = text_data_json.get('chat_id')
        chat = await sync_to_async(Chat.objects.get)(id=chat_id)            

        # Save media files if any
        media_urls = []
        for file in media_files:
            file_name = default_storage.save(file['name'], ContentFile(file['content']))
            media_url = default_storage.url(file_name)
            media_urls.append(media_url)

        # Create the message
        message = await sync_to_async(message_service.create_message)( text, media_urls, user, chat)
        await sync_to_async (message_read_status_service.create_message_read_status)(message, user)

        # Handle mentions
        mention_ids = []
        numeric_ids = [id for id in mentions if id.isdigit()]
        mention_ids = numeric_ids[:]
        
        for mention in mentions:
            if 'all' in mention:
                chat_members = await sync_to_async(lambda: list(ChatMember.objects.filter(chat_id=chat.id).exclude(member_id=user).values_list('member_id', flat=True)))()
                mention_ids.extend(chat_members)
            else:
                user_obj = await sync_to_async(lambda: User.objects.filter(first_name__iexact=mention).first())()
                if user_obj:
                    mention_ids.append(user_obj.id)

        for mentioned_user in mention_ids:
            mentioned_user_instance = await sync_to_async(user_service.get_user)(mentioned_user)
            await sync_to_async(message_mention_service.create_message_mentions)(message, mentioned_user_instance, user)
                        
        # Send the message to the WebSocket group
        await self.send_message_to_group(message, message_new=True)

    async def edit_message(self, message_id, text_data_json, user):
        message = await sync_to_async(message_service.get_message_by_id)(message_id)
        new_text = text_data_json.get('message', '')
        mentions = text_data_json.get('mentions', [])
        chat_id = text_data_json.get('chat_id')
        media_files = text_data_json.get('mediaFiles', [])
        chat = await sync_to_async(Chat.objects.get)(id=chat_id)

        # Update media files
        media_urls = []
        for file in media_files:
            file_name = default_storage.save(file['name'], ContentFile(file['content']))
            media_url = default_storage.url(file_name)
            media_urls.append(media_url)

        # Edit the message
        updated_message = await sync_to_async(message_service.update_message)(message, new_text, media_urls, user)

        mention_ids = []
        numeric_ids = [id for id in mentions if id.isdigit()]
        mention_ids = numeric_ids[:]

        for mention in mentions:
            if 'all' in mention:
                chat_members = await sync_to_async(lambda: list(ChatMember.objects.filter(chat_id=chat.id).exclude(member_id=user).values_list('member_id', flat=True)))()
                mention_ids.extend(chat_members)
            else:
                user_obj = await sync_to_async(lambda: User.objects.filter(first_name__iexact=mention).first())()
                if user_obj:
                    mention_ids.append(user_obj.id)
  
        # Fetch current mentions and ids asynchronously
        current_mentions = await sync_to_async(message_mention_service.get_message_mentions)(message)
        current_mention_ids = set(await sync_to_async(lambda: list(current_mentions.values_list('user_id', flat=True)))())

        # Calculate added and removed mentions
        new_mention_ids = set(mention_ids)
        removed_mentions = current_mention_ids - new_mention_ids
        added_mentions = new_mention_ids - current_mention_ids

        # Process removed mentions
        for mentioned_user in removed_mentions:
            mentioned_user_instance = await sync_to_async(user_service.get_user)(mentioned_user)
            await sync_to_async(message_mention_service.delete_message_mentions)(message, user, [mentioned_user_instance])

        # Process added mentions
        for mentioned_user in added_mentions:
            mentioned_user_instance = await sync_to_async(user_service.get_user)(mentioned_user)
            await sync_to_async(message_mention_service.create_message_mentions)(message, mentioned_user_instance, user)

        # Send the edited message to the WebSocket group
        await self.send_message_to_group(updated_message)


    async def reply_message(self, message_id, text_data_json, user):
        text = text_data_json.get('message', '')
        media_files = text_data_json.get('mediaFiles', [])
        mentions = text_data_json.get('mentions', [])
        chat_id = text_data_json.get('chat_id')
        chat = await sync_to_async(Chat.objects.get)(id=chat_id)

        # Fetch the original message being replied to
        original_message = await sync_to_async(message_service.get_message_by_id)(message_id)

        # Save media files if any
        media_urls = []
        for file in media_files:
            file_name = default_storage.save(file['name'], ContentFile(file['content']))
            media_url = default_storage.url(file_name)
            media_urls.append(media_url)

        # Create the reply message
        reply_message = await sync_to_async(message_service.reply_message)(user, text, media_urls, user, chat, original_message)
        await sync_to_async (message_read_status_service.create_message_read_status)(reply_message, user)

        # Handle mentions
        mention_ids = []
        numeric_ids = [id for id in mentions if id.isdigit()]
        mention_ids = numeric_ids[:]
        
        for mention in mentions:
            if 'all' in mention:
                chat_members = await sync_to_async(lambda: list(ChatMember.objects.filter(chat_id=chat.id).exclude(member_id=user).values_list('member_id', flat=True)))()
                mention_ids.extend(chat_members)
            else:
                user_obj = await sync_to_async(lambda: User.objects.filter(first_name__iexact=mention).first())()
                if user_obj:
                    mention_ids.append(user_obj.id)
        
        for mentioned_user in mention_ids:
            mentioned_user_instance = await sync_to_async(user_service.get_user)(mentioned_user)
            await sync_to_async(message_mention_service.create_message_mentions)(reply_message, mentioned_user_instance, user)

        # Send the reply message to the WebSocket group
        await self.send_message_to_group(reply_message, message_new=True)

    async def delete_message(self, message_id, user,type):
        message = await sync_to_async(message_service.get_message_by_id)(message_id)

        # Delete the message
        await sync_to_async(message_service.delete_message)(message, user, type)

        # Notify the WebSocket group that the message was deleted
        await self.send_message_to_group(message, deleted=True)

    async def mark_message_as_read(self, message_id, user_id):
        message = await sync_to_async(message_service.get_message_by_id)(message_id)
        user= await sync_to_async(user_service.get_user)(user_id)
        await sync_to_async (message_read_status_service.create_message_read_status)(message, user)
        seen_all = await sync_to_async(chat_service.message_seen_status)(message)

        if seen_all:                
            await self.send_message_to_group(message,seen_by_all=True)
        else:
            await self.send_message_to_group(message,seen_by_all=False)

    async def send_message_to_group(self, message, deleted=False, message_new=False, seen_by_all=False):
        sender = await sync_to_async(User.objects.get)(id=message.sender_id_id)

        updated = bool(message.updated_by_id)

        reply = False
        reply_text = None
        reply_username = None
        reply_user_pic = None

        if message.reply_for_message_id_id:  # Access the ID directly
            reply = True
            try:
                replied_message = await sync_to_async(Message.objects.get)(id=message.reply_for_message_id_id)
                replied_user = await sync_to_async(lambda: replied_message.sender_id)()
                reply_text = replied_message.text
                reply_username = replied_user.first_name
                reply_user_pic = replied_user.profile_photo_url
            except Message.DoesNotExist:
                pass

        # Convert datetime to string using a format for h:m AM/PM
        message_time_str = message.created_at.strftime('%I:%M %p')  # 12-hour format with AM/PM    
        reactions = await self.fetch_reactions()  # fetch emoji from masterlist table          
        message_data = {
            'message_id': message.id,
            'message': message.text,
            'messageTime': message_time_str,
            'update': updated,
            'reply': reply,
            'replyText': reply_text,
            'reply_username': reply_username,
            'reply_userPic': reply_user_pic,
            'user': sender.first_name,
            'user_pic': sender.profile_photo_url,
            'media_urls': message.media_url,
            'deleted': deleted,
            'del_type': message.delete_type,
            'del_by': message.deleted_by,
            'message_new': message_new,
            'seen_by_all': seen_by_all,
            'reactions': reactions,
        }

        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': message_data,
            }
        )

         
    async def send_reaction_details(self, reaction_instance):
        react = bool(reaction_instance.reaction_id_id)
        deleted=not reaction_instance.is_active

        reaction_data = {
            'react':react,
            'message_id': reaction_instance.message_id_id,
            'deleted':deleted,
        }

        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'reaction': reaction_data,
            }
        )

    async def chat_message(self, event):
    # Check if the event contains a reaction
        if 'reaction' in event:
            reaction = event['reaction']
            await self.send(text_data=json.dumps({
                'type': 'reaction',
                'react': reaction['react'],
                'message_id': reaction['message_id'],
                'rac_deleted':reaction['deleted'],
            }))
        else:
            message = event['message']
            await self.send(text_data=json.dumps({
                'type': 'message',
                'message': message['message'],
                'messageTime': message['messageTime'],
                'update': message['update'],
                'reply': message['reply'],
                'replyText': message['replyText'],
                'reply_username': message['reply_username'],
                'reply_userPic': message['reply_userPic'],
                'user': message['user'],
                'ProfilePic': message['user_pic'],
                'message_id': message['message_id'],
                'media_urls': message['media_urls'],
                'deleted': message['deleted'],
                'del_type': message['del_type'],
                'del_by': message['del_by'],
                'message_new': message['message_new'],
                'seen_by_all': message['seen_by_all'],
                'reactions': message['reactions'],
            }))


    async def typing_status(self, user, typing=False):
        sender = await sync_to_async(User.objects.get)(id=user)

        typer = {            
            'user': sender.first_name,
            'user_pic': sender.profile_photo_url,
            'typing': typing,
        }

        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'typing_stat',
                'typer': typer,
            }
        )
        
    async def typing_stat(self, event):
        typer = event['typer']
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'user': typer['user'],
            'user_pic': typer['user_pic'],
            'typing': typer['typing'],
        }))


    async def fetch_reactions(self):
        reactions = await sync_to_async(message_reaction_service.show_reactions)()
        return reactions
    
    async def message_reactions(self,message_id):
        msg_reactions = await sync_to_async(message_reaction_service.message_reaction)(message_id)
        return msg_reactions


   


import json
from channels.generic.websocket import AsyncWebsocketConsumer

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

        # Notify others about user join
        await self.channel_layer.group_send(
            self.call_group_name,
            {
                "type": "user.joined",
                "active_users": self.active_users[self.call_group_name]
            }
        )

    async def disconnect(self, close_code):
        # Remove user from active users list
        if self.call_group_name in self.active_users:
            self.active_users[self.call_group_name] -= 1
            if self.active_users[self.call_group_name] <= 0:
                del self.active_users[self.call_group_name]

        # Leave room group
        await self.channel_layer.group_discard(self.call_group_name, self.channel_name)

        # Notify others about user leave
        await self.channel_layer.group_send(
            self.call_group_name,
            {
                "type": "user.left",
                "active_users": self.active_users.get(self.call_group_name, 0)
            }
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")

        if action == "call_started":
            await self.channel_layer.group_send(
                self.call_group_name,
                {
                    "type": "call.started",
                    "call_id": data["call_id"]
                }
            )

        elif action == "call_accepted":
            await self.channel_layer.group_send(
                self.call_group_name,
                {
                    "type": "call.accepted",
                    "call_id": data["call_id"]
                }
            )

        elif action == "webrtc_signal":
            await self.channel_layer.group_send(
                self.call_group_name,
                {
                    "type": "webrtc.signal",
                    "signal": data["signal"],
                    "from": data["from"]
                }
            )

        elif action == "user_joined":
            await self.channel_layer.group_send(
                self.call_group_name,
                {
                    "type": "user.joined",
                    "active_users": self.active_users[self.call_group_name]
                }
            )

        elif action == "user_left":
            await self.channel_layer.group_send(
                self.call_group_name,
                {
                    "type": "user.left",
                    "active_users": self.active_users.get(self.call_group_name, 0)
                }
            )
        elif action == "call_accepted":
            await self.channel_layer.group_send(
                self.call_group_name,
                {
                    "type": "call.accepted",
                    "call_id": data["call_id"]
                }
            )

    async def call_started(self, event):
        await self.send(text_data=json.dumps({"action": "call_started", "call_id": event["call_id"]}))

    async def call_accepted(self, event):
        await self.send(text_data=json.dumps({"action": "call_accepted", "call_id": event["call_id"]}))

    async def webrtc_signal(self, event):
        await self.send(text_data=json.dumps({"action": "webrtc_signal", "signal": event["signal"], "from": event["from"]}))

    async def user_joined(self, event):
        await self.send(text_data=json.dumps({"action": "user_joined", "active_users": event["active_users"]}))

    async def user_left(self, event):
        await self.send(text_data=json.dumps({"action": "user_left", "active_users": event["active_users"]}))

