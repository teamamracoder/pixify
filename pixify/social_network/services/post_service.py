from ..models import Post,User
from django.shortcuts import get_object_or_404
from django.db.models import Q

def list_posts():
    return Post.objects.all()

def create_post(title, description,media_url):
    return Post.objects.create(title=title, description=description,media_url=media_url)

def get_post(post_id):
    return get_object_or_404(Post, id=post_id)

def update_post(post, title, description):
    post.title = title
    post.description = description
    post.save()
    return post

def delete_post(post):
    post.delete()



# new added by sujit
def admin_list_posts(sort_by = 'title'):
    return Post.objects.all().order_by(sort_by)

def admin_create_post(**kwargs):
    post = Post.objects.create(
            posted_by=kwargs['posted_by'],
            created_by=kwargs['created_by']
            # type=kwargs['type'],
            # content_type=kwargs['content_type'],
            # media_url=kwargs.get('media_url'),
            # title=kwargs['title'],
            # description=kwargs['description'],
            # accessability=kwargs['accessability'],
            # members  = kwargs['members'],
            # treat_as = kwargs['treat_as'],
            # is_active=kwargs.get('is_active', True)
        )
    return post

def admin_list_posts_filtered(search_query, sort_by='posted_by'):
    if search_query:
        # Use Q objects to filter by first_name, last_name, or email
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
    return Post.objects.all()

# comment
