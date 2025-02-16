from ..models import User,Post


# def manage_user_count():

    
def manage_user_count():
    return User.objects.count()

def manage_user_monthly_count():
    
    return User.objects.count()


def manage_admin_user_count():
    return User.objects.filter(roles__contains=[1]).count()

def manage_post_count():
    return Post.objects.count()