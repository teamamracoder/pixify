from django.forms import IntegerField
from ..models import Post,Follower
from django.shortcuts import get_object_or_404
from django.db.models import Q, Case, When, IntegerField,Max
from ..constants import PostType

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



# priya
def user_story(media_urls,user_id):
    return Post.objects.create(media_url=media_urls,created_by_id=user_id,posted_by_id=user_id)

# priya
def storylist_storys():
    following_ids = Follower.objects.filter(user_id_id=1).values_list('following_id', flat=True)
    print(following_ids)
    return Post.objects.filter(
    Q(type=PostType.STATUS.value) &
    (Q(posted_by_id=1) | Q(posted_by_id__in=following_ids))
    ).order_by(
        'posted_by_id',
        Case(
            When(posted_by_id=1, then=0),
            default=1,
            output_field=IntegerField()
        ),
        '-created_at'
    ).distinct('posted_by_id')




def get_post(post_id):
    return get_object_or_404(Post, id=post_id)


def uploadStory(media_urls,user_id):
    return Post.objects.create(media_url=media_urls,created_by_id=user_id,posted_by_id=user_id,type=PostType.STATUS.value)
