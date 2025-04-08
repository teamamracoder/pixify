from social_network.constants.default_values import SortingOrder  # Import sorting order constants
from social_network.packages.get_data import GetData  # Import a utility package for fetching data
from ..models import User, Post, Follower  # Import User, Post, and Follower models from the current app
from django.shortcuts import get_object_or_404  # Import shortcut function to fetch an object or return 404 error if not found
from django.db.models import Q  # Import Q object for complex queries with OR, AND conditions
from django.core.exceptions import ValidationError  # Import ValidationError to handle form and model validation errors


# admin-user section
def manage_list_users(sort_by='first_name'):
    return User.objects.all().order_by(sort_by)


def manage_get_user(user_id):
    # Fetch the user object by ID or return a 404 error if not found
    return get_object_or_404(User, id=user_id)


def manage_create_user(**kwargs):
    # Create a new user instance with the provided keyword arguments
    user = User.objects.create(
        first_name=kwargs['first_name'],  # Set first name
        middle_name=kwargs['middle_name'],  # Set middle name
        last_name=kwargs['last_name'],  # Set last name
        email=kwargs['email'],  # Set email address
        dob=kwargs['dob'],  # Set date of birth
        address=kwargs['address'],  # Set address
        gender=kwargs['gender'],  # Set gender
        relationship_status=kwargs['relationship_status'],  # Set relationship status
        hobbies=kwargs['hobbies'],  # Set hobbies
        roles=kwargs['roles'],  # Assign user roles
        created_by=kwargs['created_by']  # Set the user who created this profile
    )
    return user  # Return the newly created user object

def manage_update_user(user_id, **kwargs):
    """
    Updates the user with the given user_id and provided fields.
    """
    user = get_object_or_404(User, id=user_id)

    try:
        # Update fields only if they exist in kwargs
        user.first_name = kwargs.get('first_name', user.first_name)
        user.middle_name = kwargs.get('middle_name', user.middle_name)
        user.last_name = kwargs.get('last_name', user.last_name)
        user.address = kwargs.get('address', user.address)
        user.hobbies = kwargs.get('hobbies', user.hobbies)
        user.dob = kwargs.get('dob', user.dob)
        
        # Update the 'updated_by' field
        if 'updated_by' in kwargs:
            user.updated_by = kwargs['updated_by']

        user.save()
        return user

    except ValidationError as e:
        raise ValidationError(f"Validation Error: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected Error: {str(e)}")
    

def manage_list_users_filtered(search_query, sorting_order, sort_by, page_number):
    # get data
    data = (
        GetData(User)
        .search(search_query,"first_name","last_name", "email")
        .sort(sort_by, sorting_order)
        .paginate(limit=10, page=page_number)
        .execute()
    )
    # return data
    return data

def get_all_posts_by_user(user_id):
    # Retrieve all posts created by the user and return the count
    return Post.objects.filter(posted_by=user_id).count()

def get_all_followers_by_user(user_id):
    # Retrieve all followers of the user and return the count
    return Follower.objects.filter(follower=user_id).count()


def manage_update_admin_profile(user_id, **kwargs):
    """
    Updates the admin user's profile with the given user_id.
    """
    # Retrieve the user object with the given user_id or return a 404 error if not found
    user = get_object_or_404(User, id=user_id)

    try:
        # Update user fields only if they exist in kwargs
        user.first_name = kwargs.get('first_name', user.first_name)  # Update first name if provided
        user.middle_name = kwargs.get('middle_name', user.middle_name)  # Update middle name if provided
        user.last_name = kwargs.get('last_name', user.last_name)  # Update last name if provided
        user.address = kwargs.get('address', user.address)  # Update address if provided
        user.hobbies = kwargs.get('hobbies', user.hobbies)  # Update hobbies if provided
        user.dob = kwargs.get('dob', user.dob)  # Update date of birth if provided

        # Set 'updated_by' field if provided in kwargs
        if 'updated_by' in kwargs:
            user.updated_by = kwargs['updated_by']

        # Save the updated user object in the database
        user.save()
        return user  # Return the updated user object

    except ValidationError as e:
        # Raise a validation error if any field fails validation
        raise ValidationError(f"Validation Error: {str(e)}")
    except Exception as e:
        # Raise a generic exception for unexpected errors
        raise Exception(f"Unexpected Error: {str(e)}")
