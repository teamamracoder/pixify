import random
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from social_network import services
from .. models.post_model import Post

from social_network.constants.default_values import Role
from social_network.decorators.exception_decorators import catch_error

from ..decorators import auth_required, role_required
from social_network.packages.response import success_response
import random
from django.forms import model_to_dict


class HomeView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request):
        user=request.user
        message = request.session.pop("message", "")
        message_type = request.session.pop("message_type", "")
        userid=request.user.id


        posts = services.post_service.Postlist_posts()
        postreaction=services.post_reaction_service.get_reaction()

        post_id = request.GET.get('post_id')
        comment_list = services.comment_service.comment_list(post_id)
        post_dict = {
            'posts': posts,
            'comment_list': comment_list,
            'postreaction':postreaction,

        }

        # Fetch stories
        storys = services.story_service.storylist_storys()
        story_dict = {
            'storys': storys,
            #'name': 'sribash',
        }
        shorts = services.short_service.get_shorts()
        for short in shorts:
            count = services.short_service.reaction_count(short.id)
            short.reaction_count = services.short_service.format_count(count)
            comments = services.short_service.comment_count(short.id)
            short.comments_count = services.short_service.format_count(comments)
            short.user_reacted = services.short_service.user_has_reacted(short, user)

        random.shuffle(shorts)  # Randomize the list

        # Merge everything into a single context
        context = success_response(message=message, message_type=message_type)
        context.update({
            'post_dict': post_dict,
            'story_dict': story_dict,
            'shorts':shorts,
            'userid':userid,
        })

        return render(request, "enduser/home/index.html", context)

class LoginUserDetailsView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    # def get(self,request):
    #     user_id= request.user.id
    #     user_details=services.user_service.get_user(user_id)
    #     user_details_dict = model_to_dict(user_details)
    #     post_del=services.comment_service.get_post(1)
    #     comment=services.comment_service.comment_list(1)
    #     print(comment)
    #     post_del = list(services.comment_service.get_post(1).values())
    #     comment_queryset = services.comment_service.comment_list(1)
    #     comments = [model_to_dict(comment) for comment in comment_queryset]

    #     return JsonResponse({
    #         "status": "success",
    #         "user_details": user_details_dict,
    #         "post_del": list(post_del),
    #         "comments": comments
    #     })

    def get(self, request):
        user_id = request.user.id
        user_details = services.user_service.get_user(user_id)

        user_details_dict = model_to_dict(user_details)
        totalUnreadNotification=services.user_Notification_service.count_unread_notifications(user_id)
        user_details_dict = {
            "id": user_details.id,
            "first_name": user_details.first_name,
            "last_name":user_details.last_name,
            "email": user_details.email,
            "country":user_details.country,
            "profile_image_url":user_details.profile_photo_url,
            "unreadNotification":totalUnreadNotification,
            "unreadMessage":0

        }

        return JsonResponse({
            "status": "success",
            "user_details": user_details_dict,
        })

