from urllib import request
from ..models import User,Follower
from django.shortcuts import get_object_or_404
from django.db.models import Q, Case, When, Value, BooleanField
from social_network.constants.default_values import Role


def list_users():
    return User.objects.all()

def create_user(first_name, last_name, email):
    return User.objects.create(first_name=first_name, last_name=last_name, email=email)

def get_user(user_id):
    return get_object_or_404(User, id=user_id, is_active = True)

def update_user(request, user_id, first_name, last_name, email, phone, gender, address, dob, country, bio, hobbies, relationship_status, profile_picture=None):
    try:
        user_id = int(user_id) 
    except ValueError:
        raise ValueError("Invalid user_id. It must be a number.")
    
    user = User.objects.get(id=user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    # user.phone = phone
    user.gender = gender
    user.address = address
    user.dob = dob
    user.country = country
    user.bio = bio
    user.hobbies = hobbies
    user.relationship_status = relationship_status
    if profile_picture:
        user.profile_photo_url = profile_picture
    user.updated_by = request.user
    user.save()

def filter_user(user_id):
    return User.objects.filter(id=user_id)


def calculate_age(date_of_birth):
    """
    Calculate age from date of birth.
    """
    from datetime import date
    if date_of_birth:
        today = date.today()
        return today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    return "0"

def delete_user(user):
    user.delete()

def get_user_by_email(email):
    return User.objects.filter(email=email).first()

def change_theme(user, ui_mode):
    user.ui_mode = ui_mode
    user.save()
    return user


def get_user_details(user_id):
    return get_object_or_404(User, id=user_id)

def get_user_name_and_img(user_id):
    return User.objects.filter(id=user_id,is_active = True)

def friends_count(user_id):
    friends = Follower.objects.filter(user_id=user_id).select_related( 'following').count()
    return friends

def updateFCMToken(user_id,fcm_token):
    user = User.objects.get(id=user_id)
    user.fcm_token = fcm_token
    user.save()

def getFCMtoken(user_id):
    return User.objects.filter(id=user_id).values_list('fcm_token', flat=True).first()

def get_user_obj(user_id):
    return User.objects.filter(id=user_id,is_active=True).first()


def user_search_api(request):
    query = request.GET.get('search', '').strip()
    if query:
        terms = query.split()
        # Start with all active users with the END_USER role
        users = User.objects.filter(is_active=True, roles__contains=[Role.END_USER.value])
        for term in terms:
            users = users.filter(
                Q(first_name__icontains=term) |
                Q(middle_name__icontains=term) |
                Q(last_name__icontains=term)
            )
        
        # Get the current user from the request
        current_user = request.user

        # Retrieve followers and followings
        followers_query = Follower.objects.filter(following=current_user, is_active=True).values_list('user_id', flat=True)
        followings_query = Follower.objects.filter(user_id=current_user, is_active=True).values_list('following_id', flat=True)

        # Combine the queries
        related_users = followers_query.union(followings_query)

        # Annotate users with is_related field
        users = users.annotate(
            is_related=Case(
                When(id__in=related_users, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )

        # Order by is_related descending, then by name
        users = users.order_by('-is_related', 'first_name', 'middle_name', 'last_name')
    else:
        users = User.objects.none()

    users_data = [
        {
            "id": user.id,
            "full_name": " ".join(filter(None, [user.first_name, user.middle_name, user.last_name])),
            "profile_photo": user.profile_photo_url
        }
        for user in users
    ]
    return {"users": users_data}

