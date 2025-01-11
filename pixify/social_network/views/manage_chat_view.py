from pyexpat.errors import messages
from django.shortcuts import render,redirect
from ..models.user_model import User
from .. import services
from django.core.paginator import Paginator 
from django.http import HttpResponseBadRequest, JsonResponse
from social_network.constants.default_values import ChatType, Role, SortingOrder
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
        # return render(request, 'adminuser/chat/create.html', {"form": form})
        return render(request, 'adminuser/chat/create.html',   success_response(
            message=messages),
                {"form": form})
     
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
        #return render(request, 'adminuser/chat/update.html', {"form": form, "chat_id": chat.id})
        return render(request, 'adminuser/chat/update.html',   success_response(
            message=messages),
                {"form": form})


class ManageChatListView(View):

    @catch_error
    def get(self, request):
        # Fetch the search query from the URL parameters
        search_query = request.GET.get('search', '')
        sort_by = request.GET.get('sort_by', "title")
        sort_order = request.GET.get('sort_order', SortingOrder.DESC.value)
        page_number = request.GET.get('page', 1)

        # get data
        data = services.manage_chat_service.manage_list_chats_filtered(
            search_query=search_query,
            sort_by=sort_by,
            sorting_order=sort_order,
            page_number=page_number
        )

        # add more data
        data["choices_type"] = [{type.value: type.name} for type in ChatType ]

        # return
        return render(
            request,
            'adminuser/chat/list.html',
            success_response("User data fetched successfully", data)
        ) 
           
class ManageChatDetailView(View):
    def get(self, request, chat_id):
        choices_type = [{type.value: type.name} for type in ChatType]
        chat = services.manage_chat_service.manage_get_chat(chat_id)
        chat_member= services.manage_chat_service.manage_get_member(chat_id)
        print(chat_member)
        return render(
            request,
            'adminuser/chat/detail.html',
            {'chat': chat, 'chat_member': chat_member, "choices_type": choices_type}
        )  
        

class ManageToggleChatActiveView(View):
    def post(self, request, chat_id):
        chat = services.manage_chat_service.manage_get_chat(chat_id)
        chat.is_active = not chat.is_active  # Toggle active status
        chat.save()
        return JsonResponse({'is_active': chat.is_active})


