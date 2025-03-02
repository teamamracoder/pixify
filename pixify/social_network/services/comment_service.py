from django.http import JsonResponse
from django.utils import timezone
from ..models import Post,User,Comment
from django.shortcuts import get_object_or_404
from django.db.models import Q
from ..models import User,CommentReaction
from .. import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model






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
    elif diff.days < 7:
        return f"{diff.days} days ago"
    else:
        months = (now.year - timestamp.year) * 12 + now.month - timestamp.month
        if months < 12:
            return f"{months} months ago"
        else:
            years = months // 12
            return f"{years} years ago"


def get_created_by_react(comment_id, user_id):
    reacted_users = list(
        CommentReaction.objects.filter(comment_id=comment_id, is_active=True)
        .values_list("reacted_by", flat=True)  # Get all reacted user IDs
    )

    return {
        "react_created_by": user_id in reacted_users,  # True if current user reacted
        "reacted_by": reacted_users if reacted_users else []  # Ensure always an array
    }


def get_comments_by_post(post_id, user_id):
    """
    Fetch all top-level comments for a post along with their nested replies.
    """

    def get_replies(parent_comment):
        """ Recursively get replies for a given comment """
        replies = Comment.objects.filter(reply_for=parent_comment, is_active=True).select_related("comment_by")
        return [
            {
                "id": reply.id,
                "user_id": reply.comment_by.id,
                "user": reply.comment_by.first_name,
                "user_profile": reply.comment_by.profile_photo_url if reply.comment_by.profile_photo_url else "",
                "text": reply.comment,
                "reply_for": reply.reply_for_id,
                "timestamp": format_timestamp(reply.created_at),
                "replies": get_replies(reply),
                "react_count": get_count_react(reply.id) or 0,
                **get_created_by_react(reply.id, user_id)  # Ensures reacted_by is included
            }
            for reply in replies
        ]

    comments = Comment.objects.filter(post_id=post_id, reply_for__isnull=True, is_active=True).select_related("comment_by")

    return [
        {
            "id": comment.id,
            "user_id": comment.comment_by.id,
            "user": comment.comment_by.first_name,
            "user_profile": comment.comment_by.profile_photo_url if comment.comment_by.profile_photo_url else "",
            "text": comment.comment,
            "reply_for": comment.reply_for_id,
            "timestamp": format_timestamp(comment.created_at),
            "replies": get_replies(comment),
            "react_count": get_count_react(comment.id) or 0,
            **get_created_by_react(comment.id, user_id)  # Ensures reacted_by is included
        }
        for comment in comments
    ]




def get_count_react(comment_id):
    cmt_count=CommentReaction.objects.filter(comment_id=comment_id, is_active=True).count()
    print(cmt_count)
    return cmt_count

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




def get_post_comment(comment_id):
    return get_object_or_404(Comment, id=comment_id, is_active=True)


def post_comment_delete(comment_id, user):
    # Retrieve the comment object
    comment = Comment.objects.get(id=comment_id, is_active=True)
    # Delete the comment and its replies
    delete_comment_and_replies(comment, user)

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



User = get_user_model()  # Get the custom user model

def toggle_reaction(comment_id, reacted_by):
    try:
        # Retrieve the comment
        comment = Comment.objects.get(id=comment_id)
        user = User.objects.get(id=reacted_by)  # Get the correct User model instance

        # print("comment_id:", comment.id, "reacted_by:", user.id)

        # Find an existing reaction
        reaction, created = CommentReaction.objects.get_or_create(
            comment_id=comment, reacted_by=user,
            defaults={"created_by": user, "is_active": True}
        )

        # print("hello")

        if not created:
            # Toggle `is_active` instead of deleting the reaction
            reaction.is_active = not reaction.is_active
            reaction.save()

            if not reaction.is_active:
                print("Reaction removed (Unliked)")
                return {
                    "status": "unliked",
                    "total_likes": CommentReaction.objects.filter(comment_id=comment, is_active=True).count()
                }

        print("Reaction added (Liked)")
        return {
            "status": "liked",
            "total_likes": CommentReaction.objects.filter(comment_id=comment, is_active=True).count()
        }

    except ObjectDoesNotExist:
        print("Error: Comment or User not found")
        return {"error": "Comment or User not found"}

    except Exception as e:
        print("🔴 ERROR:", str(e))
        return {"error": "Something went wrong on the server"}



