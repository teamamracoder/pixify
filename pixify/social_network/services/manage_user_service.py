from social_network.constants.default_values import SortingOrder
from social_network.packages.get_data import GetData
from ..models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q   

# admin-user section
def manage_list_users(sort_by='first_name'):
    return User.objects.all().order_by(sort_by)

def manage_get_user(user_id):
    return get_object_or_404(User, id=user_id)

def manage_create_user(**kwargs):
    user = User.objects.create(
        first_name=kwargs['first_name'],
        # middle_name=kwargs['middle_name'],
        last_name=kwargs['last_name'],
        # dob=kwargs['dob'],
        email=kwargs['email'],
        # address=kwargs['address'],
        # gender=kwargs['gender'],
        # relationship_status=kwargs['relationship_status'],
        # hobbies=kwargs['hobbies'],
        roles=kwargs['roles']    
    )
    return user

def manage_update_user(user, first_name,middle_name,last_name, email,dob,gender,address,relationship_status,hobbies):
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

def manage_list_users_filtered(search_query, sorting_order, sort_by, page_number):
    # get data
    data = (
        GetData(User)
        .search(search_query,"first_name","last_name", "email")
        .sort(sort_by, sorting_order)
        .paginate(limit=3, page=page_number)
        .execute()
    )
    # return data
    return data



