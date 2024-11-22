from ..models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q   


def list_users():
    return User.objects.all()

def create_user(first_name, last_name, email):
    return User.objects.create(first_name=first_name, last_name=last_name, email=email)

def get_user(user_id):
    return get_object_or_404(User, id=user_id)

def update_user(user, first_name, last_name, email):
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.save()
    return user

def delete_user(user):
    user.delete()

def get_user_by_email(email):
    return User.objects.filter(email=email).first()