from django.shortcuts import render
from django.views import View
import json
from social_network.constants.default_values import Role
from ..decorators import auth_required, role_required
from social_network.decorators.exception_decorators import catch_error
from django.http import JsonResponse
from ..services import user_service,chat_service,post_service,message_reaction_service,comment_service


class EnduserprofileListView(View):
    def get(self, request, user_id):
        detail = user_service.get_user_details(user_id)
        if not detail:
            return render(request, 'enduser/profile/userprofile.html', {'user_details': None})

        follower_list, following_list = chat_service.get_all_user_follow(user_id)
        dob = detail.dob
        age = user_service.calculate_age(dob)
        user_posts = post_service.get_user_posts(user_id)
        reactions = message_reaction_service.show_reactions()

        user_details = {
            'user_name': f"{detail.first_name} {detail.last_name}",
            'profile_photo': detail.profile_photo_url if detail.profile_photo_url else '/images/avatar.jpg',
            'age': age,
            'status': "Active" if detail.is_active else "Inactive",
            'following_count': len(following_list),
            'followers_count': len(follower_list),
            'followers': follower_list,
            'followings': following_list,
            'posts': user_posts,
            'reactions':reactions
        }

        return render(request, 'enduser/profile/userprofile.html', {'user_details': user_details})


class FetchPostReactions(View):
    """Fetch all reactions for a given post."""
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request, post_id):
        try:
            # print(f"Fetching reactions for post_id: {post_id}")  # Debugging
            reactions = post_service.get_active_post_reactions(post_id)
            # Build the reaction list; if no reactions exist, reaction_list will be empty.
            reaction_list = [
                {"id": reaction.master_list_id.id, "value": reaction.master_list_id.value}
                for reaction in reactions
            ]
            # print("Reactions:", reaction_list)
            return JsonResponse({'success': True, 'reactions': reaction_list}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)



class CreateUpdatePostReactions(View):
    """ Create or update a post reaction """
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def post(self, request):
        try:
            data = json.loads(request.body)
            post_id = data.get('post_id')
            reaction_id = data.get('reaction_id')

            # print("gnrnyn",data)
            
            # Ensure user is authenticated
            if not request.user or not request.user.is_authenticated:
                return JsonResponse({'success': False, 'error': 'User is not authenticated'}, status=403)

            user = request.user  # Ensure user is authenticated

            reaction = post_service.get_reaction_by_name(reaction_id)
            if not reaction:
                return JsonResponse({'success': False, 'error': 'Invalid reaction'}, status=400)

            post_service.create_or_update_post_reaction(post_id, user, reaction)

            return JsonResponse({'success': True, 'message': 'Reaction updated successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

class DeletePostReactions(View):
    """ Delete a post reaction if it exists """
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def post(self, request):
        try:
            data = json.loads(request.body)
            post_id = data.get('post_id')
            user = request.user

            reaction_instance = post_service.get_active_reaction(post_id, user)
            if not reaction_instance:
                return JsonResponse({'success': True, 'message': 'No active reaction to delete'}, status=200)

            post_service.deactivate_reaction(reaction_instance)
            return JsonResponse({'success': True, 'message': 'Reaction deleted successfully'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON payload'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': 'An unexpected error occurred'}, status=500)

class CommentListViewApi(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request, post_id):
        user_id=request.user.id
        comments = comment_service.get_comments_by_post(post_id,user_id)
        print("comments",comments)
        return JsonResponse({"comments": comments}, safe=False)
    


class CommentCreate(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def post(self, request, post_id):
        try:
            data = json.loads(request.body)
            comment_text = data.get("comment_text")
            reply_for_id = data.get("reply_for")  # Get reply_for field
            
            response = comment_service.create_comment(request.user, post_id, comment_text, reply_for_id)

            if "error" in response:
                return JsonResponse(response, status=400)

            return JsonResponse(response, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        

class DeleteComment(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def post(self, request, *args, **kwargs):
        user = request.user
        comment_id = kwargs.get('comment_id')  # Extract comment_id properly

        if not comment_id:
            return JsonResponse({'success': False, 'message': 'Comment ID is required'}, status=400)

        # print(f"🚀 Attempting to delete comment ID: {comment_id}")  # Debugging

        try:
            comment = comment_service.get_post_comment(comment_id)
            comment_service.post_comment_delete(comment_id, user)
            return JsonResponse({'success': True, 'message': 'Comment deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)



class TogglReactionView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request):
        return JsonResponse({"error": "GET method not allowed"}, status=405)

    def post(self, request):
        try:
            data = json.loads(request.body)
            comment_id = data.get("comment_id")
            reacted_by = request.user.id  # Get logged-in user
            # print("comment_id :",comment_id,"reacted_by:",reacted_by)
            response_data = comment_service.toggle_reaction(comment_id, reacted_by)
            return JsonResponse(response_data)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
