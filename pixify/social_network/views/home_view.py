from django.shortcuts import get_object_or_404, render
from django.views import View

from social_network import services
from .. models.post_model import Post

from social_network.constants.default_values import Role
from social_network.decorators.exception_decorators import catch_error

from ..decorators import auth_required, role_required
from social_network.packages.response import success_response


# class HomeView(View):

#     @catch_error
#     @auth_required
#     @role_required(Role.ADMIN.value, Role.END_USER.value)
#     def get(self, request):
#         message = request.session.pop("message", "")
#         message_type = request.session.pop("message_type", "")
#         posts =services.post_service.Postlist_posts()
#         post_id = request.GET.get('post_id')
#         comment_list = services.comment_service.comment_list(post_id)
#         post_dict={
#                   'posts':posts,
#                   'name':'priya',
#                   'comment_list':comment_list,
#                   'count_commnet' :services.comment_service.get_count_comment(59)
#                 }

#         context = success_response(message=message, message_type=message_type)
#         context.update({'post_dict': post_dict})

#         storys = services.story_service.storylist_storys()
#         story_dict={
#                   'storys':storys,
#                   'name':'sribash',
#                 }
#         context2 = success_response(message=message, message_type=message_type)
#         context2.update({'story_dict': story_dict})

#         return render(request, "enduser/home/index.html", context)


class HomeView(View):

    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request):
        message = request.session.pop("message", "")
        message_type = request.session.pop("message_type", "")

        # Fetch posts
        posts = services.post_service.Postlist_posts()
        post_id = request.GET.get('post_id')
        comment_list = services.comment_service.comment_list(post_id)

        post_dict = {
            'posts': posts,
            #'name': 'priya',
            'comment_list': comment_list,
            'count_comment': services.comment_service.get_count_comment(59),
        }

        # Fetch stories
        storys = services.story_service.storylist_storys()
        story_dict = {
            'storys': storys,
            #'name': 'sribash',
        }

        # Merge everything into a single context
        context = success_response(message=message, message_type=message_type)
        context.update({
            'post_dict': post_dict,
            'story_dict': story_dict,
        })

        return render(request, "enduser/home/index.html", context)
