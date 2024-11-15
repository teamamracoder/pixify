from .. import models
from django.shortcuts import get_object_or_404
from django.db.models import Q    # added by sujit


def list_users(sort_by='first_name'):
    return models.User.objects.all().order_by(sort_by)
# def list_users():
#     return models.User.objects.all()

def create_user(**kwargs):
    user = models.User.objects.create(
        first_name=kwargs['first_name'],
        middle_name=kwargs['middle_name'],
        last_name=kwargs['last_name'],
        dob=kwargs['dob'],
        email=kwargs['email'],
        address=kwargs['address'],
        gender=kwargs['gender'],
        relationship_status=kwargs['relationship_status'],
        hobbies=kwargs['hobbies']     
    )
    return user

def get_user(user_id):
    return get_object_or_404(models.User, id=user_id)

def update_user(user, first_name,middle_name,last_name, email,dob,gender,address,relationship_status,hobbies):
    user.first_name = first_name
    user.middle_name = middle_name
    user.last_name = last_name
    user.email = email
    user.gender=gender
    user.dob=dob
    
    user.address=address
    user.relationship_status=relationship_status
    user.hobbies=hobbies

    user.save()
    return user

def delete_user(user):
    user.delete()

# new added by sujit
def list_users_filtered(search_query, sort_by='first_name'):
    if search_query:
        # Use Q objects to filter by first_name, last_name, or email
        return models.User.objects.filter(
            Q(first_name__icontains=search_query) | 
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        ).order_by(sort_by)
    return models.User.objects.all().order_by(sort_by)

