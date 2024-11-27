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
        search_query = request.GET.get('search', '')
        exclude_str = request.GET.get('exclude', '')
        exclude_ids = [int(id) for id in exclude_str.split(',') if id.isdigit()]
        mentioned_all = request.GET.get('mentionedAll', 'false') == 'true'

        print_log(f"Search query: {search_query}")
        print_log(f"Exclude IDs: {exclude_ids}")
        print_log(f"Mentioned all: {mentioned_all}")

        chat = chat_service.get_chat_by_id(chat_id)
        if chat.type == ChatType.GROUP.value:
            mention_list = message_mention_service.list_messages_mention_Api(chat_id, user, search_query, exclude_ids, mentioned_all)
            print(f"Mention list: {mention_list}")
            return JsonResponse(mention_list, safe=False)
        else:
            return JsonResponse([], safe=False)