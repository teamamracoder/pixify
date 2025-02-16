# from django.shortcuts import render
# from django.http import JsonResponse
# from django.shortcuts import render
# from django.views import View
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# from ..decorators.exception_decorators import catch_error
# from ..services import verification_service
# import json
# from social_network.constants.default_values import Role
# from ..decorators import auth_required, role_required



# @method_decorator(csrf_exempt, name='dispatch')
# class UserVerificationView(View):
#     @catch_error
#     @auth_required
#     @role_required(Role.ADMIN.value, Role.END_USER.value)
#     def get(self, request):
#         user=request.user
#         user_details=verification_service.user(user.id)
#         print(user_details)
#         return render(request, 'verification/web_cam.html', {
#             'user': user,
#             'user_details':user_details
#               # Pass the user object to the template
#         })

#     @catch_error
#     def post(self, request):
    

#         try:
#             # Parse JSON data
#             data = json.loads(request.body)
#             image_data = data.get('image')
#             user_id = request.user.id  # Assuming the user is authenticated

#             if not image_data:
#                 return JsonResponse({'success': False, 'message': 'No image provided.'})

#             # Save user image and perform verification
#             result = verification_service.save_user_image(image_data, user_id)

#             # Return the response
#             return JsonResponse({
#                 'success': result['success'],
#                 'message': result['message'],
#                 'is_verified': result.get('is_verified', False),
#                 'image_url': result.get('image_url', None)  # Assuming `save_user_image` returns `image_url`
#             })

#         except Exception as e:
#             return JsonResponse({'success': False, 'message': f"An error occurred: {str(e)}"})


