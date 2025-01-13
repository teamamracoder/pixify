
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View

from ..models.post_model import Post


from ..import services
from ..models import Notification
from django.core.paginator import Paginator
from ..constants.default_values import SortingOrder
from ..decorators.exception_decorators import catch_error
from ..decorators import auth_required, role_required
from ..packages.response import success_response
from ..forms.manage_comment_form import ManageCommentCreateForm

    

# class ManageCommentListView(View):
#     @catch_error
#     def get(self, request):
#         # Fetch the search query from the URL parameters
#         # search_query = request.GET.get('search', '')
#         # sort_by = request.GET.get('sort_by', "created_at")
#         # sort_order = request.GET.get('sort_order', SortingOrder.DESC.value)
#         # page_number = request.GET.get('page', 1)

#         # get data
#         data= services.manage_comment_service.manage_list_comments_filtered(
#             # search_query=search_query,
#             # sort_by=sort_by,
#             # sorting_order=sort_order,
#             # page_number=page_number
#         )
#         print("this is comment pagedata",data)
       
#         return render(request,'adminuser/comment/list.html',
#             success_response("User data fetched successfully", data)
#         ) 
       

 

class ManageCommentListView(View):
    # @catch_error
    # def get(self, request):
    #     # Fetch the search query from the URL parameters
    #     search_query = request.GET.get('search', '')
    #     sort_by = request.GET.get('sort_by', "created_at")
    #     sort_order = request.GET.get('sort_order', SortingOrder.DESC.value)
    #     page_number = request.GET.get('page', 1)

    #     data = services.manage_comment_service.manage_list_comments(
    #         search_query=search_query,
    #         sort_by=sort_by,
    #         sorting_order=sort_order,
    #         page_number=page_number
    #     )
        # return 

      def get (self,request):
        data=services.manage_comment_service.manage_list_comments()
        return render(request, 'adminuser/comment/list.html', {'data': data})





class ManageCommentCreateView(View):
    @catch_error
    def get(self, request):
        form = ManageCommentCreateForm()
        return render(request, 'adminuser/comment/create.html', {"form": form})

    # @catch_error
    def post(self, request):
        user=request.user
        form = ManageCommentCreateForm(request.POST)
        if form.is_valid():
            comment_data = {
                'comment': form.cleaned_data['comment'],
                'post_id': Post.objects.get(id=request.POST['post_id']),
                'comment_by':user,
                'created_by':user
                
               
            }
            services.manage_comment_service.manage_create_comment(**comment_data)
            return redirect('manage_comment_list')
        return render(request, 'adminuser/comment/create.html', {"form": form})




     