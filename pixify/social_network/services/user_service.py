from ..models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q


def list_users():
    return User.objects.all()

def create_user(first_name, last_name, email):
    return User.objects.create(first_name=first_name, last_name=last_name, email=email)

def get_user(user_id):
    return get_object_or_404(User, id=user_id, is_active = True)

# Work By Badhan
def update_user(user_id,first_name,last_name,email,phone,gender,address,dob,country,bio,hobbies,relationship_status,profile_picture):
    user = User.objects.get(id=user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    #user.phone = phone
    user.gender = gender
    user.address = address
    user.dob = dob
    user.country = country
    user.bio=bio
    user.hobbies=hobbies
    user.relationship_status=relationship_status
    #if profile_picture:
     #   user.profile_photo_url = profile_picture
    user.updated_by = user
    user.save()
    return user

def filter_user(user_id):
    return User.objects.filter(id=user_id)

  # End by Badhan

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

