# from pyexpat.errors import messages
# from django.shortcuts import get_object_or_404, render, redirect
# from django.http import JsonResponse
# from django.views import View

# from ..forms.manage_post_forms import ManagePostUpdateForm,ManagePostCreateForm

# from ..models.post_model import Post
# from ..decorators.exception_decorators import catch_error
# from .. import services
# from ..models import User
# from django.core.paginator import Paginator
# from django.http import HttpResponseBadRequest
# from social_network.packages.response import success_response
# from social_network.constants.default_values import SortingOrder
from pyexpat.errors import messages  # Importing messages (likely incorrect import, Django's messages should be used instead)
from django.shortcuts import get_object_or_404, render, redirect  # Importing shortcuts for common view operations
from django.http import JsonResponse  # Importing JsonResponse to send JSON responses
from django.views import View  # Importing Django's class-based view system
from ..forms.manage_post_forms import ManagePostUpdateForm, ManagePostCreateForm    # Importing forms for managing post creation and updates
from ..models.post_model import Post    # Importing Post model
from ..decorators.exception_decorators import catch_error   # Importing custom exception handling decorator
from .. import services # Importing service functions (possibly handling business logic)
from ..models import User   # Importing User model
from django.core.paginator import Paginator  # Importing Paginator for handling pagination
from django.http import HttpResponseBadRequest  # Importing HttpResponseBadRequest for handling bad requests
from social_network.packages.response import success_response   # Importing custom response formatting utility
from social_network.constants.default_values import SortingOrder    # Importing constants for sorting behavior


class ManagePostListView(View):
    def get(self, request):
        # Fetch the search query from the URL parameters
        search_query = request.GET.get('search', '')
        sort_by = request.GET.get('sort_by', 'id')
        sort_order = request.GET.get('sort_order', SortingOrder.DESC.value)
        page_number = request.GET.get('page', 1)

        # get data
        data = services.post_service.manage_list_posts_filtered(
            search_query=search_query,
            sort_by=sort_by,
            sorting_order=sort_order,
            page_number=page_number
        )
        # if "data" in data and isinstance(data["data"], list):
        for val in data["data"]:
            user_id = val.get("posted_by_id")
            val["user_data"] = list(services.get_users_by_id(user_id))    
        return render(request,
            'adminuser/post/list.html',
            success_response("post data fetched successfully", data)
        )


class ManagePostDetailView(View):  # Class-based view to handle post details
    def get(self, request, post_id):  # Handles GET requests for a specific post
        comment_count = services.get_comment_count_by_post(post_id)  # Get the total number of comments on the post
        
        post_likes = services.post_service.manage_list_likes_filtered(post_id)  # Retrieve the list of likes for the post
        post_liked_users = services.get_post_user(post_likes)  # Get the users who liked the post
        
        # Create a dictionary with all necessary post details
        post_dic = {
            'post': services.post_service.manage_get_post(post_id),  # Fetch the post details
            'comment': services.post_service.manage_list_comments_filtered(post_id),  # Get filtered list of comments
            'post_likes': post_likes,  # Store the list of post likes
            'post_liked_users': post_liked_users  # Store the list of users who liked the post
        }
        
        # Render the template and pass the post details and comment count to the frontend
        return render(request, 'adminuser/post/detail.html', {'post_dic': post_dic, 'comment_count': comment_count})


class ManageTogglePostActiveView(View):
    def post(self, request, post_id):
        # Call service function to toggle post active status
        is_active = services.toggle_post_active_status(post_id)

        # Return the updated active status as a JSON response
        return JsonResponse({'is_active': is_active})
    

class ManageToggleCommentActiveView(View):
    def post(self, request, comment_id):
        # Call the service function to toggle the active status of the comment
        is_active = services.toggle_comment_active_status(comment_id)

        # Return the updated active status as a JSON response
        return JsonResponse({'is_active': is_active})