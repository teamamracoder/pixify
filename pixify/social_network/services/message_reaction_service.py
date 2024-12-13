from ..models import MessageReaction,MasterList
from ..constants import MasterType


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

def get_reaction_by_name(reaction_id):
    return MasterList.objects.filter(id=reaction_id).first()

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

def get_reaction_details(message_id, reaction_type):
    reactions = get_active_message_reactions(message_id)
    default_gif_url="https://t4.ftcdn.net/jpg/05/11/55/91/360_F_511559113_UTxNAE1EP40z1qZ8hIzGNrB0LwqwjruK.jpg"
    user_reactions = [
        {
            "name": f"{reaction.reacted_by.first_name or ''} {reaction.reacted_by.last_name or ''}".strip(),
            "reaction": reaction.reaction_id.value,
            "photo":reaction.reacted_by.profile_photo_url or default_gif_url
        }
        for reaction in reactions
        if reaction.reacted_by  # Ensure reacted_by is not None
    ]

    reaction_count = len(user_reactions)

    return {
        "users": user_reactions,
        "reaction_count": reaction_count
    }
def show_reactions():
    reactions = MasterList.objects.filter(type=MasterType.REACTION.value, is_active=True).values("id", "value")
    return list(reactions) 





