from ..models import User,Follower
from django.shortcuts import get_object_or_404
from django.db.models import Q   


def list_users():
    return User.objects.all() 

def create_user(first_name, last_name, email):
    return User.objects.create(first_name=first_name, last_name=last_name, email=email)

def get_user(user_id):
    return get_object_or_404(User, id=user_id) 

# Work By Badhan
def update_user(user_id,first_name,last_name,email,phone,gender,address,dob,country,bio,hobbies,relationship_status,profile_picture):
    user = User.objects.get(id=user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.phone = phone
    user.gender = gender
    user.address = address
    user.dob = dob
    user.country = country
    user.bio=bio
    user.hobbies=hobbies
    user.relationship_status=relationship_status
    if profile_picture: 
        user.profile_photo_url = profile_picture
    user.updated_by = user
    user.save()
    return user 


# ds jfl
# from ..models import User

# def get_user_profile(user):
#     """
#     Fetch the profile details for the given user.
#     """
#     try:
#         profile_data = {
#             'name': f"{user.first_name} {user.last_name}",
#             'status': "Active" if user.is_active else "Inactive",
#             'age': calculate_age(user.date_of_birth),  # Assuming `date_of_birth` is a field in your User model
#             'friends_count': user.following.count(),  # Assuming `following` is a related name for user's friends
#             'messages_count': user.messages_received.count(),  # Assuming `messages_received` is a related name
#             'notifications_count': user.notifications.filter(is_read=False).count(),  # Unread notifications count
#             'profile_photo': user.profile_photo_url or '/static/images/avatar.jpg',  # Default image if not provided
#         }
#     except Exception as e:
#         # Handle any exceptions gracefully
#         profile_data = {
#             'name': "Unknown",
#             'status': "Unavailable",
#             'age': "N/A",
#             'friends_count': 0,
#             'messages_count': 0,
#             'notifications_count': 0,
#             'profile_photo': '/static/images/avatar.jpg',
#         }

#     return profile_data

def calculate_age(date_of_birth):
    """
    Calculate age from date of birth.
    """
    from datetime import date
    if date_of_birth:
        today = date.today()
        return today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    return "N/A"

  # End by Badhan  
 
def delete_user(user):
    user.delete()

def get_user_by_email(email):
    return User.objects.filter(email=email).first()

def get_user_details(user_id):
    user_details=User.objects.filter(id=user_id)
    return user_details

def friends_count(user_id):
    friends = Follower.objects.filter(user_id=user_id).select_related( 'following').count()
    return friends 
# 'follower',

