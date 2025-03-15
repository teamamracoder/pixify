#story_service.py
from django.db.models import Max
from itertools import chain
from operator import attrgetter

from requests import request
from ..models import Post,Follower
from django.shortcuts import get_object_or_404
from django.db.models import Q , When , Value ,Case ,IntegerField
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

#sribash sarkar

from ..constants import PostContentType,PostType

def user_story(media_urls, media_types, user_id, music_url=None, story_text=None):
    posts = []
    if story_text:
        posts.append(Post(
            description=story_text,  # Store the text story in the description field
            created_by_id=user_id,
            posted_by_id=user_id,
            type=PostType.STATUS.value,
            media_url=[],  # No media for text stories
            content_type=media_types,  # No media type for text stories
        ))
    else:
        for media_url, media_type in zip(media_urls, media_types):
            posts.append(Post(
                media_url=[media_url],
                #media_type=media_type,
                type=PostType.STATUS.value,
                content_type=media_type,
                created_by_id=user_id,
                posted_by_id=user_id,
            ))
    return Post.objects.bulk_create(posts)
def storylist_storys(user_id):
    following_users = list(Follower.objects.filter(created_by=user_id).values_list('following_id', flat=True))
    following_users.append(user_id)
    latest_posts = (
    Post.objects.filter(posted_by__in=following_users, type=PostType.STATUS.value)
    .values('posted_by')
    .annotate(latest_created_at=Max('created_at'))
    .values_list('posted_by', 'latest_created_at')
)
    # latest_posts = (
    #     Post.objects.values('posted_by')
    #     .annotate(latest_created_at=Max('created_at'))
    #     .values_list('posted_by', 'latest_created_at')
    #     .filter(type=PostType.STATUS.value)
    # )

    latest_post_filters = [
        Q(posted_by=user_id, created_at=created_at)
        for user_id, created_at in latest_posts
    ]
    if latest_post_filters:
    # Get the filtered querysets
        queries = [Post.objects.filter(f) for f in latest_post_filters]

    # Combine them using `chain`
        combined_results = list(chain(*queries))

    # Sort manually with custom logic
        sorted_results = sorted(
        combined_results,
        key=lambda post: (0 if post.posted_by == 15 else 1, -post.created_at.timestamp())
    )

        return sorted_results  # Returns a sorted list, not a QuerySet

    return Post.objects.none()

def get_post(post_id):
    return get_object_or_404(Post, id=post_id)
def get_all_stories():
    # Fetch all the stories, ordered by creation time.
    return Post.objects.all().order_by('-created_at')

def get_latest_story():
    # Fetch the latest story for each user (or just the latest story if that's the desired behavior).
    latest_story = Post.objects.latest('created_at')
    return latest_story
def get_user_stories(user_id):
    """
    Fetch all stories for a given user.
    """
    return Post.objects.filter(posted_by_id=user_id).order_by('-created_at')
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ..models import User, Post  # Adjust the import based on your project structure

def view_stories(request, user_id):
    user = get_object_or_404(User, id=user_id)
    stories = Post.objects.filter(posted_by=user).values('id', 'media_url', 'content_type', 'description')

    response_data = {
        'stories': list(stories),
        'first_name': user.first_name,  # Include the user's first name
        'profile_photo_url': user.profile_photo_url  # Include profile image (if needed)
    }

    return JsonResponse(response_data)
