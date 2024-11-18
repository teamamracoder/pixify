from ..models import MessageMention

def create_message_mentions(message,user):
    MessageMention.objects.create(message=message,user=user)