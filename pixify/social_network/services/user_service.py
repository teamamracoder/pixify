from .. import models
from django.shortcuts import get_object_or_404

def list_users():
    return models.User.objects.all()

def create_user(first_name,middle_name, last_name, email,hobbies):
    return models.User.objects.create(first_name=first_name,middle_name=middle_name, last_name=last_name, email=email,hobbies=hobbies)

def get_user(user_id):
    return get_object_or_404(models.User, id=user_id)

def update_user(user, first_name,middle_name,last_name, email,hobbies):
    user.first_name = first_name
    user.middle_name = middle_name
    user.last_name = last_name
    user.email = email
    user.hobbies=hobbies
    user.save()
    return user

def delete_user(user):
    user.delete()
