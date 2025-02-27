from ..models import User, Post, PostReaction, Comment, CommentReaction
from ..constants import PostType,PostContentType
from django.utils import timezone

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


def format_relative_time(timestamp):
    now = timezone.now()

    # Ensure both 'timestamp' and 'now' are timezone-aware
    if timezone.is_naive(timestamp):
        timestamp = timezone.make_aware(timestamp, timezone.get_current_timezone())
    else:
        timestamp = timestamp.astimezone(timezone.get_current_timezone())

    if timezone.is_naive(now):
        now = timezone.make_aware(now, timezone.get_current_timezone())

    # Now, both `timestamp` and `now` should be timezone-aware
    diff_seconds = (now - timestamp).total_seconds()

    if diff_seconds < 60:
        return "Just now"
    elif diff_seconds < 3600:
        return f"{int(diff_seconds // 60)}m ago"
    elif diff_seconds < 86400:
        return f"{int(diff_seconds // 3600)}h ago"
    elif diff_seconds < 604800:
        return f"{int(diff_seconds // 86400)}d ago"
    elif diff_seconds < 2592000:
        return f"{int(diff_seconds // 604800)}w ago"
    elif diff_seconds < 31536000:
        return f"{int(diff_seconds // 2592000)}m ago"
    else:
        return f"{int(diff_seconds // 31536000)}y ago"


def get_comment_replies(parent_comment_id, user):
    # Order replies chronologically (oldest first)
    replies = Comment.objects.filter(reply_for_id=parent_comment_id, is_active=True).order_by('created_at')

    result = []
    for reply in replies:
        reply_dict = {
            'id': reply.id,
            'comment': reply.comment,
            'comment_by__first_name': reply.comment_by.first_name,
            'comment_by__last_name': reply.comment_by.last_name,
            'comment_by__profile_photo_url': reply.comment_by.profile_photo_url,
            'created_at': format_relative_time(reply.created_at),
            'like_count': CommentReaction.objects.filter(comment_id=reply.id, is_active=True).count(),
            'user_liked': CommentReaction.objects.filter(comment_id=reply.id, reacted_by=user, is_active=True).exists(),
            'replies': get_comment_replies(reply.id, user),
            'can_delete': Comment.objects.filter(id=reply.id, comment_by=user).exists()
        }
        result.append(reply_dict)

    return result


def short_comments(short, user):
    comments = Comment.objects.filter(post_id=short, reply_for_id=None, is_active=True).order_by('-created_at')

    result = []
    for comment in comments:
        comment_dict = {
            'id': comment.id,
            'comment': comment.comment,
            'comment_by__first_name': comment.comment_by.first_name,
            'comment_by__last_name': comment.comment_by.last_name,
            'comment_by__profile_photo_url': comment.comment_by.profile_photo_url,
            'created_at': format_relative_time(comment.created_at),
            'like_count': CommentReaction.objects.filter(comment_id=comment.id, is_active=True).count(),
            'user_liked': CommentReaction.objects.filter(comment_id=comment.id, reacted_by=user, is_active=True).exists(),
            'replies': get_comment_replies(comment.id, user),
            'can_delete': Comment.objects.filter(id=comment.id, comment_by=user).exists()
        }
        result.append(comment_dict)

    return result


def get_short_comment(comment_id):
    return Comment.objects.select_related('post_id').get(id=comment_id, is_active=True)

def short_comment_create(text, post, user):
    return Comment.objects.create(
        comment_by=user,
        comment=text,
        post_id=post,        
        created_by=user,
    )

def short_comment_reply(text, post, comment, user):
    return Comment.objects.create(
        comment=text,
        post_id = post,
        reply_for = comment,
        comment_by = user,
        created_by= user,
    )


def delete_comment_and_replies(comment, user):
    # Retrieve all replies associated with this comment
    replies = Comment.objects.filter(reply_for=comment, is_active=True)

    # Mark all replies as inactive
    for reply in replies:
        delete_comment_and_replies(reply, user)
    
    # Mark the comment as inactive
    comment.is_active = False
    comment.updated_by = user
    comment.save()

def short_comment_delete(comment_id, user):
    # Retrieve the comment object
    comment = Comment.objects.get(id=comment_id, is_active=True)
    
    # Delete the comment and its replies
    delete_comment_and_replies(comment, user)

            
def comment_count(short):
    return Comment.objects.filter(post_id=short, is_active=True).count()

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

def toggle_like(comment, user):

    like_obj, created = CommentReaction.objects.filter(comment_id=comment, reacted_by=user).get_or_create(defaults={
        'reacted_by': user,
        'comment_id' : comment,
        'created_by' : user,
        })

    if created:
        return True
    else:
        # If like exists, toggle the is_active field
        like_obj.is_active = not like_obj.is_active
        like_obj.updated_by = user
        like_obj.save()
        return like_obj.is_active  # Return the new state (True = liked, False = unliked)

def comment_reaction_count(comment):
    return CommentReaction.objects.filter(comment_id = comment, is_active = True).count()


def get_short_media(post_id):
    return Post.objects.filter(id=post_id, is_active=True).values('media_url')


def get_post_by_id(post_id):
    return Post.objects.get(id=post_id)  # Ensure this is `.get()` and NOT `.filter()`
