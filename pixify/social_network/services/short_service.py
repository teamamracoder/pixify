from ..models import User, Post, PostReaction, Comment, CommentReaction
from ..constants import PostType,PostContentType

def get_short(short_id):
    return Post.objects.get(id=short_id, is_active=True)

def get_shorts():
    shorts = Post.objects.filter(type=PostType.SHOTS.value, content_type=PostContentType.VIDEO.value, is_active=True)
    return list(shorts)

def short_reaction(post, user):
    reaction, created = PostReaction.objects.get_or_create(
        reacted_by=user,
        post_id=post,
        created_by=user,
    )

    if not created:
        reaction.is_active = True
        reaction.updated_by = user
        reaction.save()

    return PostReaction.objects.filter(post_id=post, is_active=True).count()

def reaction_count(short):
    return PostReaction.objects.filter(post_id=short, is_active=True).count()

def user_has_reacted(short, user):
    return PostReaction.objects.filter(post_id=short, reacted_by=user, is_active=True).exists()

def short_reaction_delete(post, user):    
    reaction = PostReaction.objects.get(post_id=post, reacted_by=user, is_active=True)
    reaction.is_active = False
    reaction.updated_by = user
    reaction.save()

    return PostReaction.objects.filter(post_id=post, is_active=True).count()

def format_count(count):
    if count >= 1_000_000:  # Millions
        return f"{count / 1_000_000:.2f}m".rstrip('0').rstrip('.')
    elif count >= 1_000:  # Thousands
        return f"{count / 1_000:.2f}k".rstrip('0').rstrip('.')
    return str(count)  # Less than 1,000: Show the full number




