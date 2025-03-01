from django.http import JsonResponse
from django.utils import timezone
from ..models import Post,User,Comment
from django.shortcuts import get_object_or_404
from django.db.models import Q
from ..models import User,CommentReaction
from .. import models





def user_comments_create(commentstext,post_id,user_id,):
    return Comment.objects.create(comment=commentstext,created_by_id=user_id,comment_by_id=user_id,post_id_id=post_id)



def get_count_comment(postid):
    return Comment.objects.filter(post_id_id=postid).count()


# def comment_list(post_id):
#     return models.Comment.objects.filter(post_id=post_id).order_by('created_at').values()

# def comment_list(post_id):
#     comments = Comment.objects.filter(post_id=post_id)
#     return list(comments.values('id', 'comment', 'created_at',
#                                 'comment_by__first_name', 'comment_by__last_name','reply_for_id'))
def comment_list(post_id):
    comments = Comment.objects.filter(post_id=post_id).values(
        'id', 'comment', 'created_at',
        'comment_by__first_name', 'comment_by__last_name',
        'comment_by__profile_photo_url', 'reply_for_id'
    )
    return list(comments)

    #.select_related('comment_by')

def comments_filtered(post_id):
    return  Comment.objects.filter(post_id_id=post_id)


def get_post(post_id):
    return Post.objects.filter(id=post_id)


def get_user(user_id):
    return User.objects.filter(id=user_id)

def get_comment_by(comment_by_id):
    return User.objects.filter(id=comment_by_id)



def user_reply_create(reply_text, post_id, user_id, comment_id):
    return Comment.objects.create(comment=reply_text,created_by_id=user_id,comment_by_id=user_id,post_id_id=post_id,reply_for_id=comment_id)


def reply_list(comment_id):
     return Comment.objects.filter(reply_for_id=comment_id)


def comment_count(post_id):
     return Comment.objects.filter(post_id_id=post_id, is_active=True).count()

def create_reaction(comment_id,user_id):
        created = CommentReaction.objects.create(comment_id_id=comment_id, reacted_by_id=user_id,
                                              created_by_id=user_id, is_active=True)

        return created





def format_timestamp(timestamp):
    """ Format timestamp as 'Just now', 'X minutes ago', 'Yesterday', or date """
    if not timestamp:
        return ''

    now = timezone.now()
    diff = now - timestamp

    if diff.total_seconds() < 60:
        return "Just now"
    elif diff.total_seconds() < 3600:
        minutes = int(diff.total_seconds() / 60)
        return f"{minutes} minutes ago"
    elif diff.total_seconds() < 86400:
        hours = int(diff.total_seconds() / 3600)
        return f"{hours} hours ago"
    elif diff.days == 1:
        return "Yesterday"
    elif diff.days < 7:
        return f"{diff.days} days ago"
    else:
        return timestamp.strftime('%d/%m/%Y')  # Example: "01/03/2025"

    
def get_comments_by_post(post_id):
    def get_replies(parent_comment):
        """ Recursively get replies for a given comment """
        replies = Comment.objects.filter(reply_for=parent_comment).select_related("comment_by")
        return [
            {
                "id":reply.id,
                "user": reply.comment_by.first_name,
                "user_profile": reply.comment_by.profile_photo_url if reply.comment_by.profile_photo_url else "",  # Fix here!
                "text": reply.comment,
                "reply_for": reply.reply_for_id,
                "timestamp": format_timestamp(reply.created_at),
                "replies": get_replies(reply)
            }
            for reply in replies
        ]

    # Fetch only top-level comments (where reply_for is NULL)
    comments = Comment.objects.filter(post_id=post_id, reply_for__isnull=True).select_related("comment_by")
    return [
        {
            "id":comment.id,
            "user": comment.comment_by.first_name,
            "user_profile": comment.comment_by.profile_photo_url if comment.comment_by.profile_photo_url else "",  # Fix here!
            "text": comment.comment,
            "reply_for": comment.reply_for_id,
            "timestamp": format_timestamp(comment.created_at),
            "replies": get_replies(comment)
        }
        for comment in comments
    ]



def get_comments_by_post(post_id):
    """
    Fetch all top-level comments for a post along with their nested replies.
    """

    def get_replies(parent_comment):
        """ Recursively get replies for a given comment """
        replies = Comment.objects.filter(reply_for=parent_comment).select_related("comment_by")
        return [
            {
                "id": reply.id,
                "user": reply.comment_by.first_name,
                "user_profile": reply.comment_by.profile_photo_url if reply.comment_by.profile_photo_url else "",
                "text": reply.comment,
                "reply_for": reply.reply_for_id,
                "timestamp": format_timestamp(reply.created_at),
                "replies": get_replies(reply)
            }
            for reply in replies
        ]

    # Fetch only top-level comments (where reply_for is NULL)
    comments = Comment.objects.filter(post_id=post_id, reply_for__isnull=True).select_related("comment_by")
    return [
        {
            "id": comment.id,
            "user": comment.comment_by.first_name,
            "user_profile": comment.comment_by.profile_photo_url if comment.comment_by.profile_photo_url else "",
            "text": comment.comment,
            "reply_for": comment.reply_for_id,
            "timestamp": format_timestamp(comment.created_at),
            "replies": get_replies(comment)
        }
        for comment in comments
    ]

def create_comment(user, post_id, comment_text, reply_for_id=None):
    """
    Create a comment or reply under a specific post.
    """
    if not comment_text:
        return {"error": "Comment text is required."}

    post = get_object_or_404(Post, id=post_id)

    if not user or not user.is_authenticated:
        return {"error": "User must be authenticated."}

    # Convert invalid reply_for_id values to None
    if not isinstance(reply_for_id, int):  
        reply_for_id = None  

    reply_for = None
    if reply_for_id:
        reply_for = get_object_or_404(Comment, id=reply_for_id)

    # ✅ Debugging before saving
    print(f"🔍 DEBUG: Creating comment by User: {user} (ID: {user.id}), Reply for: {reply_for_id}")

    # ✅ Save comment
    comment = Comment.objects.create(
        comment_by=user,  
        post_id=post,  
        comment=comment_text,
        reply_for=reply_for,
        created_by=user,
    )

    # ✅ Debugging saved comment
    print(f"✅ Comment created by: {comment.comment_by} (ID: {comment.comment_by.id if comment.comment_by else 'None'})")

    return {
        "id": comment.id,
        "user": comment.comment_by.first_name if comment.comment_by else "Unknown",
        "post_id": comment.post_id.id,
        "text": comment.comment,
        "reply_for": comment.reply_for.id if comment.reply_for else None,
        "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    }
