from django.shortcuts import get_object_or_404, render
from django.views import View

from social_network import services
from .. models.post_model import Post

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
        
        # Merge everything into a single context
        context = success_response(message=message, message_type=message_type)
        context.update({
            'post_dict': post_dict,
            'story_dict': story_dict,
            'userid':userid,
            
        })

        return render(request, "enduser/home/index.html", context)
