from django.db.models import Count
from ..models.user_model import User
from . import GetData
from ..models import Post,Comment,PostReaction,PostReaction,MasterList
from django.shortcuts import get_object_or_404
from django.db.models import Q
from ..constants.default_values import PostType, PostContentType
from ..models import models
from ..services import comment_service

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

# priya
def user_post(post_Title,media_urls,user_id):
          return Post.objects.create(title=post_Title,media_url=media_urls,created_by_id=user_id,posted_by_id=user_id)

# priya
def Postlist_posts():
    return Post.objects.filter(type__in=[PostType.NORMAL.value, PostType.SHOTS.value]).order_by('-created_at')



def manage_list_posts_filtered(search_query, sorting_order, sort_by, page_number):
    # get data
    data = (
        GetData(Post)
        .search(search_query,"title","description")
        .sort(sort_by, sorting_order)
        .paginate(limit=10, page=page_number)
        .execute()
    )
    # print(f"Post data = {data}")
    # for val in data['data']:
    #     # print(f"Post data = {val}")
    #     # print(f"Post data = {val['id']}")
    #     print(f"Post data = {val['posted_by_id']}")
    #     posted_by_id = val['posted_by_id']
    return data


def manage_list_likes_filtered(post_id):
    return PostReaction.objects.filter(post_id=post_id).values_list('reacted_by_id', flat=True)

def manage__posts_user():
    return User.objects.all()


def get_post_user(post_likes):
    post_liked_users = User.objects.filter(id__in=post_likes)
    post_liked_users_data = [  {'id': user.id,'first_name': user.first_name,'middle_name': user.middle_name,'last_name': user.last_name, }
                            for user in post_liked_users
                       ]
    return {'post_liked_users' : post_liked_users_data}


def manage_list_comments_filtered(post_id):
    return Comment.objects.filter(post_id=post_id, reply_for__isnull=True, is_active=True)



def get_users_by_id(user_id):
            return User.objects.filter(id=user_id).all()


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


def get_user_posts(user_id):
    user_posts = Post.objects.filter(posted_by=user_id).values('id', 'type', 'media_url', 'title', 'description', 'created_at').order_by('-created_at')


    # Format the created_at timestamp after fetching data
    formatted_posts = [
        {**post, 'created_at': comment_service.format_timestamp(post['created_at'])}
        for post in user_posts
    ]

    return formatted_posts


def get_active_post_reactions(post_id):
    return PostReaction.objects.filter(post_id=post_id, is_active=True)



def create_or_update_post_reaction(post_id, user, reaction):
    post = Post.objects.get(id=post_id)

    post_reaction, created = PostReaction.objects.get_or_create(
        post_id=post,
        created_by=user,
        reacted_by=user,
        defaults={'master_list_id': reaction}
    )

    if not created:

        post_reaction.master_list_id = reaction
        post_reaction.is_active=True
        post_reaction.updated_by =user
        post_reaction.save()



def get_active_reaction(post_id, user):
    return PostReaction.objects.filter(
        post_id=post_id,
        reacted_by=user,
        is_active=True
    ).first()


def deactivate_reaction(reaction_instance):
    reaction_instance.is_active = False
    reaction_instance.save()
    return reaction_instance
def get_reaction_by_name(post_id):
    return MasterList.objects.filter(id=post_id).first()


def get_user_post_comment_count(user_id):
    posts = Post.objects.filter(posted_by=user_id).annotate(
        comment_count=Count('fk_post_comments_post_id', filter=Q(fk_post_comments_post_id__is_active=True))
    ).values('id', 'comment_count')

    return list(posts)  # Returns a list of dictionaries with 'id' and 'comment_count'



def get_users_by_id(user_id):
            return User.objects.filter(id=user_id).all()

def get_post_by_post_id(post_id):
    post=Post.objects.filter(id=post_id,is_active=True).first()
    post_data={}
    if post:
        post_data={
            'id':post.id,
            'post_media':post.media_url,
            'type':post.type,
            'posted_by_name':f"{post.posted_by.first_name} {post.posted_by.last_name}",
            'posted_by_image':post.posted_by.profile_photo_url or '/images/avatar.jpg',
            'created_at':comment_service.format_timestamp(post.created_at),
            'content_type':PostContentType(post.content_type).name
        }
        print(post_data)
        return post_data
    return post_data



def get_all_reactions(post_id):
     return PostReaction.objects.filter(post_id=post_id,is_active=True).select_related('reacted_by','master_list_id')