from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Message, Chat, ChatMember,User
from .services import message_service, message_mention_service, user_service
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
        user = self.scope['user']

        # Debug logs
        print(f"Received action: {action}, message_id: {message_id}, chat_id: {chat_id}, user: {user}")
        print(text_data_json)

        if action == 'create':
            await self.create_message(text_data_json, user)
        elif action == 'edit':
            await self.edit_message(message_id, text_data_json, user)
        elif action == 'reply':
            await self.reply_message(message_id, text_data_json, user)
        elif action == 'delete':
            await self.delete_message(message_id, user)

    async def create_message(self, text_data_json, user):        
        text = text_data_json.get('message', '')
        media_files = text_data_json.get('media_files', [])
        mentions = text_data_json.get('mention', [])
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


    # Handle mentions
            # Handle mentions
        mention_ids = []
        for mention in mentions:
            if 'all' in mention:
                chat_members = await sync_to_async(lambda: list(ChatMember.objects.filter(chat_id=chat.id).exclude(member_id=user).values_list('member_id', flat=True)))()
                mention_ids.extend(chat_members)
            else:
                user_obj = await sync_to_async(lambda: User.objects.filter(first_name__iexact=mention).first())()
                if user_obj:
                    mention_ids.append(user_obj.id)

        print('Mentioned IDs:', mention_ids)
        for mentioned_user in mention_ids:
            mentioned_user_instance = await sync_to_async(user_service.get_user)(mentioned_user)
            await sync_to_async(message_mention_service.create_message_mentions)(message, mentioned_user_instance, user)



        # Send the message to the WebSocket group
        await self.send_message_to_group(message)

    async def edit_message(self, message_id, text_data_json, user):
        message = await sync_to_async(message_service.get_message_by_id)(message_id)
        new_text = text_data_json.get('message', '')
        mentions = text_data_json.get('mention', [])
        chat_id = text_data_json.get('chat_id')
        media_files = text_data_json.get('media_files', [])
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
        for mention in mentions:
            if 'all' in mention:
                chat_members = await sync_to_async(lambda: list(ChatMember.objects.filter(chat_id=chat.id).exclude(member_id=user).values_list('member_id', flat=True)))()
                mention_ids.extend(chat_members)
            else:
                user_obj = await sync_to_async(lambda: User.objects.filter(first_name__iexact=mention).first())()
                if user_obj:
                    mention_ids.append(user_obj.id)
        
        current_mentions = await sync_to_async(message_mention_service.get_message_mentions)(message)
        current_mention_ids = set(await sync_to_async(lambda: list(current_mentions.values_list('user_id', flat=True)))())


        new_mention_ids = set(mention_ids)        
        removed_mentions = current_mention_ids - new_mention_ids
        added_mentions = new_mention_ids - current_mention_ids

        for mentioned_user in removed_mentions:
            mentioned_user_instance = user_service.get_user(mentioned_user)
            message_mention_service.delete_message_mentions(message, user, [mentioned_user_instance])

        for mentioned_user in added_mentions:
            mentioned_user_instance = user_service.get_user(mentioned_user)
            message_mention_service.create_message_mentions(message, mentioned_user_instance, user)

        # Send the edited message to the WebSocket group
        await self.send_message_to_group(updated_message)

    async def reply_message(self, message_id, text_data_json, user):
        text = text_data_json.get('message', '')
        media_files = text_data_json.get('media_files', [])
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

        # Process mentions
        mention_ids = [int(id) for id in mentions if id.isdigit()]
        if '@All' in mentions:
            chat_members = ChatMember.objects.filter(chat_id=chat.id).exclude(member_id=user)
            mention_ids.extend([member.member_id.id for member in chat_members])

        # Create the reply message
        reply_message = await sync_to_async(message_service.reply_message)(user, text, media_urls, user, chat, original_message)

        # Handle mentions in the reply
        for mentioned_user in mention_ids:
            mentioned_user_instance = await sync_to_async(user_service.get_user)(mentioned_user)
            await sync_to_async(message_mention_service.create_message_mentions)(reply_message, mentioned_user_instance, user)

        # Send the reply message to the WebSocket group
        await self.send_message_to_group(reply_message)

    async def delete_message(self, message_id, user):
        message = await sync_to_async(message_service.get_message_by_id)(message_id)

        # Delete the message
        await sync_to_async(message_service.delete_message)(message, user)

        # Notify the WebSocket group that the message was deleted
        await self.send_message_to_group(message, deleted=True)

    async def send_message_to_group(self, message, deleted=False):
        sender = await sync_to_async(User.objects.get)(id=message.sender_id_id)

        
        if message.updated_by_id:
            updated=True
        else:
            updated=False            

        print(updated)
            
        try:
            replied_message = await sync_to_async(Message.objects.get)(id=message.reply_for_message_id)
            replied_user = replied_message.sender_id  # Assuming the 'sender' is the user who replied
        except Message.DoesNotExist:
            replied_user = None  # Handle appropriately if message does not exist


        message_data = {
            'message_id': message.id,
            'message': message.text,
            'update':updated,
            'reply':replied_user,
            'user': sender.first_name,
            'user_pic':sender.profile_photo_url,
            'media_urls': message.media_url,
            'deleted': deleted
        }

        # Debug log
        print(f"Sending message to group: {message_data}")

        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': message_data,
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Debug log
        print(f"Chat message event: {message}")

        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': message['message'],
            'update':message['update'],
            'reply':message['reply'],
            'user': message['user'],
            'ProfilePic': message['user_pic'],
            'message_id': message['message_id'],
            'media_urls': message['media_urls'],
            'deleted': message['deleted']
        }))
