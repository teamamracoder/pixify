
from ..models import Post,Comment,PostReaction
from django.shortcuts import get_object_or_404
from django.db.models import Q
from ..constants.default_values import PostType

def manage_list_posts():
    return Post.objects.all()

def manage_get_post(post_id):
    return get_object_or_404(Post, id=post_id)

def manage_update_post(post, title, description):
    post.title = title
    post.description = description
    post.save()
    return post

def manage_delete_post(post):
    post.delete()

def delete_post(post):
    post.delete()

# new added by sujit
def manage_list_posts(sort_by = 'title'):
    return Post.objects.all().order_by(sort_by)

def manage_create_post(**kwargs):
    post = Post.objects.create(
            posted_by=kwargs['posted_by'],
            created_by=kwargs['created_by'],
            title=kwargs['title'],
            description=kwargs['description'],
        )
    return post

def manage_list_posts_filtered(search_query,sort_by='posted_by'):
    if search_query:
        # Use Q objects to filter by posted_by, title, or descriptions
        return Post.objects.filter(
            Q(posted_by__icontains=search_query) |
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        ).order_by(sort_by)
    return Post.objects.all().order_by(sort_by)



# priya
def user_post(post_Title,media_urls,user_id):
          return Post.objects.create(title=post_Title,media_url=media_urls,created_by_id=user_id,posted_by_id=user_id)

# priya
def Postlist_posts():
    return Post.objects.filter(type=PostType.NORMAL.value).order_by('-created_at')


# def get_post(post_id):
#      return get_object_or_404(Post, id=post_id)






def admin_list_posts_filtered(search_query, sort_by='posted_by'):
    if search_query:
        # Use Q objects to filter by first_name, last_name, or email
        return Post.objects.filter(
            Q(posted_by__icontains=search_query) |
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        ).order_by(sort_by)
    return Post.objects.all().order_by(sort_by)


def get_comment_count_by_post(post_id):
    comment_count = Comment.objects.filter(post_id=post_id, reply_for__isnull=True, is_active=True).count()
    return comment_count


def get_post(post_id):
    return Post.objects.filter(id=post_id)



# update post
def update_post(user_id,post_id,post_titile):
    post = Post.objects.get(id=post_id)
    post.title = post_titile
    post.updated_by=user_id
    post.save()
    # return post

# comment
def reaction_name(post_id):
   return PostReaction.objects.filter( post_id_id=post_id, is_active=True).first()