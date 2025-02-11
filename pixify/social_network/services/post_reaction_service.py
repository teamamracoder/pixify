from ..models import PostReaction,Post,User,MasterList


def post_reactionby_name(post):
    return PostReaction.objects.filter(post_id_id=post)

def create_post_reaction(post_id,user_id):
    created = PostReaction.objects.create(post_id_id=post_id,reacted_by_id=user_id,
                                          created_by_id= user_id,is_active= True)
    
    return  created

def create_or_update_message_reaction(post_id,user_id):
   created = PostReaction.objects.update_or_create(post_id_id=post_id,reacted_by_id=user_id,
                                          created_by_id= user_id,is_active= True)
   return created



def get_reaction_count(post_id, reaction_id):
    return PostReaction.objects.filter(
        post_id=post_id,
        reaction_id=reaction_id,
        is_active=True
    ).count()



def getemoji(reaction_id):
    return MasterList.objects.filter(id=reaction_id)

def get_active_post_reactions(post_id):
    reactions = PostReaction.objects.filter(
        post_id_id=post_id,
        is_active=True
    ).select_related('reacted_by', 'reaction_id')
    return reactions
