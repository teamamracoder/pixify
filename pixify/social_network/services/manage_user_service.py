from ..models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q   


# def list_users():
#     return User.objects.all()

# def create_user(first_name, last_name, email):
#     return User.objects.create(first_name=first_name, last_name=last_name, email=email)

# def get_user(user_id):
#     return get_object_or_404(User, id=user_id)

# def update_user(user, first_name, last_name, email):
#     user.first_name = first_name
#     user.last_name = last_name
#     user.email = email
#     user.save()
#     return user

# def delete_user(user):
#     user.delete()

# def list_users_api(request):
#     search_query = request.GET['search']
#     if search_query:
#         # recipient name/ group name should start with search param
#         users = User.objects.filter(first_name__icontains=search_query).values()
#     else:
#         users = User.objects.all().values()
#     return users

# def get_user_by_email(email):
#     return User.objects.filter(email=email).first()




# admin-user section
def manage_list_users(sort_by='first_name'):
    return User.objects.all().order_by(sort_by)

def manage_get_user(user_id):
    return get_object_or_404(User, id=user_id)

def manage_create_user(**kwargs):
    user = User.objects.create(
        first_name=kwargs['first_name'],
        middle_name=kwargs['middle_name'],
        last_name=kwargs['last_name'],
        dob=kwargs['dob'],
        email=kwargs['email'],
        address=kwargs['address'],
        gender=kwargs['gender'],
        relationship_status=kwargs['relationship_status'],
        hobbies=kwargs['hobbies'],
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

def manage_list_users_filtered(search_query, sort_by='first_name'):
    if search_query:
        # Use Q objects to filter by first_name, last_name, or email
        return User.objects.filter(
            Q(first_name__icontains=search_query) | 
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        ).order_by(sort_by)
    return User.objects.all().order_by(sort_by)



