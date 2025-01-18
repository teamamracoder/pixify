from django.views import View
from ..constants import ChatType
from ..services import message_mention_service,chat_service
from django.http import JsonResponse
from social_network.decorators.exception_decorators import catch_error
from social_network.constants.default_values import Role
from ..decorators import auth_required, role_required
from social_network.utils.common_utils import print_log 

class MessageMentionListViewApi(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request, chat_id):
        user = request.user
        search_query = request.GET.get('search', '').strip()
        exclude_str = request.GET.get('exclude', '')
        mentioned_all = request.GET.get('mentionedAll', 'false').lower() == 'true'

        exclude_ids = [id for id in exclude_str.split(',') if id]
        
        # Validate chat
        chat = chat_service.get_chat_by_id(chat_id)        
        if not chat:
            return JsonResponse({"error": "Chat not found"}, status=404)
        
        # Only proceed if it's a group chat
        if chat.type != ChatType.GROUP.value:
            return JsonResponse([], safe=False)

        mention_list = message_mention_service.list_messages_mention_Api(chat, user, search_query, exclude_ids, mentioned_all)
        return JsonResponse(mention_list, safe=False)
