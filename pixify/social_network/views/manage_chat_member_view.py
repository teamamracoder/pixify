
# Manage_Chat_Member
#======================================================================
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from ..models.chat_model import Chat

from ..import services
from ..constants.default_values import Role
from ..decorators.auth_decorators import auth_required, role_required
from ..decorators.exception_decorators import catch_error
from ..forms.manage_chat_forms import ManageMemberChatCreateForm

class ManageMemberChatCreateView(View):
    @catch_error
    def get(self, request): 
        form = ManageMemberChatCreateForm()
        return render(request, 'adminuser/chat/membercreate.html', {"form": form })
    
    @catch_error
    def post(self, request,chat_id):
       
        form = ManageMemberChatCreateForm(request.POST)
        if form.is_valid():
            chat_member = {
                'member_id': form.cleaned_data['member_id'],
                'chat_id':form.cleaned_data['chat.id'],
                
            }
            services.manage_chat_member_service.manage_member_create_chats(**chat_member)
            return redirect('manage_chat_memberlist')
        return render(request, 'adminuser/chat/membercreate.html', {"form": form})

#      Manage_Chat_Member_List
#==================================================================

class ManageMemberChatListView(View):

    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request):
        search_query = request.GET.get('search', '') 
        sort_by = request.GET.get('sort_by', 'chat_id')
        sort_order = request.GET.get('sort_order', 'asc')
        page_number = request.GET.get('page', 1)


        # Adjust sort order for descending order
        if sort_order == 'desc':
            sort_by = '-' + sort_by

        # print(f"Search Query: {search_query}")
        # Get filtered and sorted users based on search
        chat = services.manage_chat_member_service.manage_member_list_chats_filtered(search_query, sort_by)

        # Paginate the users
        paginator = paginator(chat, 10)  # Show 10 users per page
        page_obj = paginator.get_page(page_number)        

        return render(request, 'adminuser/chat/memberlist.html', {
            'chats': page_obj,
            'sort_by': sort_by,
            'sort_order': sort_order,
            'search_query': search_query,  # Ensure this is being passed to the template
            'page_obj': page_obj,
        })
    



   