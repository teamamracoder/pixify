from ..models import MessageReaction,MasterList

def get_active_message_reactions(message_id):
    reactions = MessageReaction.objects.filter(
        message_id=message_id,
        is_active=True
    ).select_related('reacted_by', 'reaction_id')
    return reactions

def get_reaction_count(message_id, reaction_id):
    return MessageReaction.objects.filter(
        message_id=message_id,
        reaction_id=reaction_id,
        is_active=True
    ).count()

def get_reaction_by_name(reaction_name):
    return MasterList.objects.filter(name=reaction_name).first()

def create_or_update_message_reaction(message_id, user, reaction):
    reaction_instance, created = MessageReaction.objects.update_or_create(
        message_id_id=message_id,
        reacted_by=user,
        defaults={
            'reaction_id': reaction,
            'created_by': user,
            'is_active': True  
        }
    )
    return reaction_instance, created

def get_active_reaction(message_id, user):
    return MessageReaction.objects.filter(
        message_id=message_id,
        reacted_by=user,
        is_active=True
    ).first()

def deactivate_reaction(reaction_instance):
    reaction_instance.is_active = False
    reaction_instance.save()
    return reaction_instance


