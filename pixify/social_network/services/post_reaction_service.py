from ..models import PostReaction,Post,User


def post_reaction(reaction_id):
    return PostReaction.objects.filter(id=reaction_id).first()

def create_post_reaction(post_id,user_id):
    created = PostReaction.objects.create(post_id_id=post_id,reacted_by_id=user_id,
                                          created_by_id= user_id,is_active= True)
    
    return  created

def create_or_update_message_reaction(post_id,user_id):
   created = PostReaction.objects.update_or_create(post_id_id=post_id,reacted_by_id=user_id,
                                          created_by_id= user_id,is_active= True)
   return created

# def get_reaction_count(post_id, reaction_id):

#     return PostReaction.objects.filter(
#         post_id=post_id,
#         reaction_id=reaction_id,
#         is_active=True
#     ).count()
#     return


def get_reaction_count(post_id, reaction_id):
    return PostReaction.objects.filter(
        post_id=post_id,
        reaction_id=reaction_id,
        is_active=True
    ).count()