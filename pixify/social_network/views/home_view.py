from django.shortcuts import render
from django.views import View

from social_network import services
from social_network.constants.default_values import Role
from social_network.decorators.exception_decorators import catch_error

from ..decorators import auth_required, role_required
from social_network.packages.response import success_response


class HomeView(View):

    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request):
        message = request.session.pop("message", "")
        message_type = request.session.pop("message_type", "")
        # user post create by priya
        posts =services.post_service.Postlist_posts()
        count_commnet =services.comment_service.get_count_comment(15)
        print(count_commnet)
        post_dict={
                  'posts':posts,
                  'name':'priya',
                  
                }

        context = success_response(message=message, message_type=message_type)
        context.update({'post_dict': post_dict})  # Merge with the posts data

        return render(request, "enduser/home/index.html", context)
      
    
