from django.views import View 
from ..services import follower_service
from django.http import JsonResponse 
from social_network.decorators.exception_decorators import catch_error
from social_network.constants.default_values import Role
from ..decorators import auth_required, role_required
 
class FollowerListViewApi(View): 
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request): 
        user = request.user 
        follower_data = follower_service.list_followers_api(request, user)
        return JsonResponse(follower_data, safe=False)