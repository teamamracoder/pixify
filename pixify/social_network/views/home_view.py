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
        storys = services.story_service.storylist_storys()
        story_dict={
                  'storys':storys,
                  'name':'sribash',
                #   'count_commnet' :services.comment_service.get_count_comment()
                  
                 
  
                }
        context = success_response(message=message, message_type=message_type)
        context.update({'story_dict': story_dict}) 
        return render(
            request,
            "enduser/home/index.html",
           context
        )
