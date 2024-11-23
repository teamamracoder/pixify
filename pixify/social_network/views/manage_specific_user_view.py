# from django.shortcuts import get_object_or_404, render, redirect
# from django.http import HttpResponseBadRequest, JsonResponse
# from django.views import View

# from ..models.post_specific_user_model import PostSpecificUser

# from ..forms.manage_user_forms import ManageUserCreateForm
# from ..models.post_model import Post
# from ..decorators.exception_decorators import catch_error
# from ..forms.manage_post_forms import ManagePostCreateForm, ManagePostSpecificUserCreateForm, ManagePostUpdateForm
# from .. import services
# from ..models import User
# from django.core.paginator import Paginator 
# from django.http import HttpResponseBadRequest
# from ..forms import ManagePostCreateForm


# # class ManagePostSpecificUserView(View):
# #     @catch_error
# #     def get(self,request,post_id):
# #         form = ManagePostSpecificUserCreateForm()
# #         return render(request, 'adminuser/post_specific_user/create.html', {"form": form, "post_id":post_id})
    
# #     @catch_error
# #     def post(self, request):
# #         post = request.user
# #         form = ManagePostSpecificUserCreateForm(request.POST)
# #         if form.is_valid():
# #              post_data = {
# #                  'created_by' : form.cleaned_data['created_by'],
# #                  'post_id'    :form.cleaned_data['post_id'],
# #                  'specific_user_id' :form.cleaned_data['specific_user_id']
# #              }
# #              services.manage_specific_user_service.manage_post_specific_user_create(**post_data) 
# #              return redirect('manage_post_specific_user_list')
# #         return render(request, 'adminuser/post_specific_user/create.html', {"form": form})
    

# # class ManagePostSpecificUserListView(View):
# #     def get(self,request):
# #         return render(request,'adminuser/post_specific_user/list.html')
    





