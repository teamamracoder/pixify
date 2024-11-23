from django.shortcuts import render,redirect

from ..models.user_model import User


# from django.views import View

# from django.utils.timezone import localtime

# from ..services import manage_chat_service
# from ..constants import ChatType
# from django.shortcuts import render,redirect
from .. import services

# from ..constants import ChatType
from django.core.paginator import Paginator 
from django.http import HttpResponseBadRequest, JsonResponse

from social_network.constants.default_values import ChatType, Role
from social_network.decorators.exception_decorators import catch_error

from ..decorators import auth_required, role_required
from social_network.packages.response import success_response
# from social_network.utils.common_utils import print_log

from ..models.chat_model import Chat
from ..services import chat_member_service




from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseBadRequest
from django.views import View
from ..decorators.exception_decorators import catch_error
from ..forms import ManageChatCreateForm, ManageChatUpdateForm
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


# # Admin Section
# #=============================================================================
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



# class ManageChatCreateView(View):
#     def get(self, request):       
#         choices_type = [{type.value: type.name} for type in ChatType]
#         return render(request, 'adminuser/chat/create.html',{"choices_type":choices_type})

#     def post(self, request):
#         user=request.user
#         print_log(user)
#         chat_data={
#         'title': request.POST['title'],      
#         'type': request.POST['type'],       
#         'chat_cover': request.POST.get('chat_cover', ''), 
#         # 'is_active': request.POST.get('is_active', 'on') == 'on',
#         'created_by': user
#         # 'updated_by':User.objects.get(id=request.POST['updated_by'])
#         }
#         services.manage_chat_service.manage_create_chats(**chat_data)
#         return redirect ('manage_chat_list')
        
    
class ManageChatDetailView(View):
    def get(self, request, chat_id):  
        choices_type = [{type.value: type.name} for type in ChatType]     
        chat = services.manage_chat_service.manage_get_chat(chat_id)
        return render(request, 'adminuser/chat/detail.html',{'chat':chat, "choices_type":choices_type }) 
        

# class ManageChatUpdateView(View):
#     def get(self, request,chat_id):
#         choices_type = [{type.value: type.name} for type in ChatType]
#         chat = services.manage_chat_service.manage_get_chat(chat_id)
#         return render(request, 'adminuser/chat/update.html',{'chat': chat, "choices_type":choices_type})

#     def post(self, request, chat_id):
#         user=request.user
#         chat = services.manage_chat_service.manage_get_chat(chat_id)
#         chat_data={
#             'updated_by': user,
#             'title':request.POST.get('title'),
#             'type':request.POST.get('type'),
#             'chat_cover':request.POST.get('chat_cover'),
#             # 'is_active':request.POST.get('is_active', 'on') == 'on',
#             # 'created_by':request.POST.get('created_by'),
#             # 'updated_by':request.POST.get('updated_by'),
#         }

#         required_fields = ['title', 'type', 'chat_cover']
#         for field in required_fields:
#             if not chat_data.get(field):
#                 return HttpResponseBadRequest(f"Missing required field: {field}")
        
#         services.manage_chat_service.manage_update_chats(
#             chat, **chat_data)
#         return redirect('manage_chat_detail', chat_id=chat.id)
    

# class ManageChatDeleteView(View):
#     def get(self, request, chat_id):
#         chat = manage_chat_service.manage_get_chat(chat_id)
#         return render(request, 'adminuser/chat/delete.html',{'chat': chat})

#     def post(self, request, chat_id):
#         chat= manage_chat_service.manage_get_chat(chat_id)
#         manage_chat_service.manage_delete_chats(chat)
#         return redirect('manage_chat_list')


class ManageToggleChatActiveView(View):
    def post(self, request, chat_id):
        chat = services.manage_chat_service.manage_get_chat(chat_id)
        chat.is_active = not chat.is_active  # Toggle active status
        chat.save()
        return JsonResponse({'is_active': chat.is_active})



