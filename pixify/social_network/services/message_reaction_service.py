from ..models  import  MessageReaction 
from django.shortcuts import get_object_or_404


def create_message_reaction(reacted_by,message_id,reaction_type):
    return MessageReaction.objects.create(
        reacted_by= reacted_by,
        message_id = message_id,
        reaction_type =reaction_type
    )
def get_message_reaction(message_reaction_id):
    return get_object_or_404(MessageReaction, id=message_reaction_id)

def update_message_reaction(reacted_by,message_reaction,reaction_type):
    message_reaction.reacted_by= reacted_by,
    message_reaction.message_reaction = message_reaction,
    message_reaction.reaction_type = reaction_type
    message_reaction.save()
    return message_reaction

def delete_message_reaction(message_reaction):
    message_reaction.is_active=False
    message_reaction.save()
   