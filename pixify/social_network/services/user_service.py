from urllib import request
from ..models import User,Follower
from django.shortcuts import get_object_or_404
from django.db.models import Q


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

