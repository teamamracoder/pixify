from django.views import View
from ..services import message_mention_service
from django.http import JsonResponse
from ..models import ChatMember

class MessageMentionListViewApi(View):
    def get(self, request, chat_id):
        user = request.user
        search_query = request.GET.get('search', '')        
        members_count = ChatMember.objects.filter(chat_id=chat_id).exclude(member_id=user).count()                        
        if members_count > 1:
            mention_list = message_mention_service.list_messages_mention_Api(chat_id, user, search_query)
            return JsonResponse(mention_list, safe=False)
        else:
            return JsonResponse([], safe=False)



