from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from ..models.chat_model import Chat
from ..forms.manage_message_forms import ManagMessageCreateForm 
from ..import services
from ..models import Message
from django.core.paginator import Paginator
from ..constants.default_values import SortingOrder
from ..decorators.exception_decorators import catch_error
from ..packages.response import success_response

class ManageMessageListView(View):
    @catch_error
    def get(self, request):                
        # Fetch the search query from the URL parameters
        search_query = request.GET.get('search', '')
        sort_by = request.GET.get('sort_by', "created_at")
        sort_order = request.GET.get('sort_order', SortingOrder.DESC.value)
        page_number = request.GET.get('page', 1)

        # get data
        data = services.manage_message_service.manage_list_messages_filtered(
            search_query=search_query,
            sort_by=sort_by,
            sorting_order=sort_order,
            page_number=page_number
        )
        return render(
            request,
            'adminuser/message/list.html',
            success_response("Message data fetched successfully", data)
        )  
class ManageMessageCreateView(View):
    @catch_error
    def get(self, request):
        form = ManagMessageCreateForm()
        return render(request, 'adminuser/message/create.html', {"form": form})
    
    # @catch_error
    def post(self, request):      
        user=request.user       
        # if request.method == 'POST':
        form = ManagMessageCreateForm(request.POST)
        if form.is_valid():            
            message_data = {
                'text': form.cleaned_data['text'],
                'media_url': form.cleaned_data['media_url'],                            
                'chat_id': Chat.objects.get(id=request.POST['chat_id']),
                'created_by': user,
                'sender_id': user
            }
            services.manage_message_service.manage_create_message(**message_data)
            return redirect('manage_message_list')
        return render(request, 'adminuser/message/create.html', {"form": form})        
    
class ManageToggleMessageActiveView(View):
     def post(self, request, message_id):
        message = services.manage_message_service.manage_get_message(message_id)
        message.is_active = not message.is_active  
        message.save()
        return JsonResponse({'is_active': message.is_active})     
     
     