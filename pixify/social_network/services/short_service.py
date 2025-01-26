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

def short_comments(short):
    # Fetch active comments for the given post ID
    comments = Comment.objects.filter(post_id=short, is_active=True).values(
        'id',
        'comment',
        'comment_by__first_name',
        'comment_by__last_name',
        'comment_by__profile_photo_url',
    )

    for comment in comments:
        # Calculate like count for the parent comment
        comment['like_count'] = CommentReaction.objects.filter(
            comment_id=comment['id'], is_active=True
        ).count()

        # Fetch and process replies for the current comment
        replies = Comment.objects.filter(reply_for_id=comment['id'], is_active=True).values(
            'id',
            'comment',
            'comment_by__first_name',
            'comment_by__last_name',
            'comment_by__profile_photo_url',
        )

        # Add like_count to each reply
        for reply in replies:
            reply['like_count'] = CommentReaction.objects.filter(
                comment_id=reply['id'], is_active=True
            ).count()

        # Attach replies to the parent comment
        comment['replies'] = list(replies)

    return comments

def get_short_comment(comment_id):
    return Comment.objects.filter(id=comment_id, is_active=True)

def short_comment(text, post, user):
    return Comment.objects.create(
        comment_by=user,
        Comment=text,
        post_id=post,        
        created_by=user,
    )

def short_comment_reply(text, post, comment, user):
    return Comment.objects.create(
        Comment=text,
        post_id = post,
        reply_for = comment,
        comment_by = user,
        created_by= user,
    )

def short_comment_delete(comment_id, user):
    comment = Comment.objects.filter(id=comment_id, is_active=True)

    comment.is_active=False
    comment.updated_by=user
    comment.save()
            
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

