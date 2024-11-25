from django.shortcuts import render,redirect
from ..models.user_model import User
from .. import services
from django.core.paginator import Paginator 
from django.http import HttpResponseBadRequest, JsonResponse
from social_network.constants.default_values import ChatType, Role
from social_network.decorators.exception_decorators import catch_error
from ..decorators import auth_required, role_required
from social_network.packages.response import success_response
from ..models.chat_model import Chat
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseBadRequest
from django.views import View
from ..decorators.exception_decorators import catch_error
from ..forms import ManageChatCreateForm, ManageChatUpdateForm,ManageMemberChatCreateForm
from .. import services


class ManageChatCreateView(View):     
    @catch_error
    def get(self, request):
        choices_type = [{type.value: type.name} for type in ChatType]
        form = ManageChatCreateForm()
        return render(request, 'adminuser/chat/create.html', {"form": form ,"choices_type":choices_type})

    @catch_error
    def post(self, request):
        user=request.user
        form = ManageChatCreateForm(request.POST)
        if form.is_valid():
            chat_data = {
                'title': form.cleaned_data['title'],
                'type': form.cleaned_data['type'],
                'chat_cover': form.cleaned_data['chat_cover'],
                'created_by': user              
            }
            services.manage_chat_service.manage_create_chats(**chat_data)
            return redirect('manage_chat_list')
        return render(request, 'adminuser/chat/create.html', {"form": form})


# UPDATE
# =============================================================

class ManageChatUpdateView(View):
    @catch_error
    def get(self, request, chat_id):
        choices_type = [{type.value: type.name} for type in ChatType]
        chat = get_object_or_404(Chat, id=chat_id)  
        form = ManageChatUpdateForm(initial={
            'title': chat.title,
            'type': chat.type,
            'chat_cover': chat.chat_cover            
        })
        return render(request, 'adminuser/chat/update.html', {"form": form, "chat_id": chat.id, "choices_type":choices_type})
    @catch_error
    def post(self, request, chat_id):
        chat = get_object_or_404(Chat, id=chat_id)
        form = ManageChatUpdateForm(request.POST)
        if form.is_valid():
            chat.title = form.cleaned_data['title']
            chat.type = form.cleaned_data['type']
            chat.chat_cover = form.cleaned_data['chat_cover']
            chat.save()  
            return redirect('manage_chat_list')
        return render(request, 'adminuser/chat/update.html', {"form": form, "chat_id": chat.id})


class ManageChatListView(View):

    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request):
        search_query = request.GET.get('search', '') 
        sort_by = request.GET.get('sort_by', 'title')
        sort_order = request.GET.get('sort_order', 'asc')
        page_number = request.GET.get('page', 1)

        # Adjust sort order for descending order
        if sort_order == 'desc':
            sort_by = '-' + sort_by

        # print(f"Search Query: {search_query}")
        # Get filtered and sorted users based on search
        chat = services.manage_chat_service.manage_list_chats_filtered(search_query, sort_by)

        # Paginate the users
        paginator = Paginator(chat, 10)  # Show 10 users per page
        page_obj = paginator.get_page(page_number)
       
        choices_type = [{type.value: type.name} for type in ChatType]

        return render(request, 'adminuser/chat/list.html', {
            'chats': page_obj,
            'choices_type': choices_type,
            'sort_by': sort_by,
            'sort_order': sort_order,
            'search_query': search_query,  # Ensure this is being passed to the template
            'page_obj': page_obj,
        })
           
class ManageChatDetailView(View):
    def get(self, request, chat_id):  
        choices_type = [{type.value: type.name} for type in ChatType]     
        chat = services.manage_chat_service.manage_get_chat(chat_id)
        return render(request, 'adminuser/chat/detail.html',{'chat':chat, "choices_type":choices_type }) 
        

class ManageToggleChatActiveView(View):
    def post(self, request, chat_id):
        chat = services.manage_chat_service.manage_get_chat(chat_id)
        chat.is_active = not chat.is_active  # Toggle active status
        chat.save()
        return JsonResponse({'is_active': chat.is_active})


