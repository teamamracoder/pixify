from django.shortcuts import get_object_or_404, render
from django.views import View
import json
from social_network.constants.default_values import Role
from ..decorators import auth_required, role_required
from social_network.decorators.exception_decorators import catch_error
from django.http import JsonResponse
from ..services import user_service,chat_service,post_service,message_reaction_service,comment_service
from ..models import User,Comment


class EnduserprofileListView(View):
    def get(self, request, user_id):
        detail = user_service.get_user_details(user_id)
        if not detail:
            return render(request, 'enduser/profile/userprofile.html', {'user_details': None})

        dob = detail.dob
        age = user_service.calculate_age(dob)
        user_posts = post_service.get_user_posts(user_id)
        reactions = message_reaction_service.show_reactions()

        user_details = {
            'id':user_id,
            'user_name': f"{detail.first_name} {detail.last_name}",
            'profile_photo': detail.profile_photo_url if detail.profile_photo_url else '/images/avatar.jpg',
            'cover_photo': detail.cover_photo_url if detail.cover_photo_url else '/images/defaultcoverimg.png',
            'age': age,
            'status': "Active" if detail.is_active else "Deactive",
            'posts': user_posts,
            'reactions':reactions,
            'bio':detail.bio if detail.bio else " "
        }

        return render(request, 'enduser/profile/userprofile.html', {'user_details': user_details,'user':request.user})


class FetchPostReactions(View):
    """Fetch all reactions for a given post."""
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request, post_id):
        try:
            reactions = post_service.get_active_post_reactions(post_id)
            
            # Build the full list
            reaction_list = [
                {
                    "id": reaction.master_list_id.id,
                    "value": reaction.master_list_id.value,
                    "user_id": reaction.reacted_by.id,
                    "user_name": "You" if reaction.reacted_by.id == request.user.id else reaction.reacted_by.first_name,
                    "is_you": reaction.reacted_by.id == request.user.id  # Add this for sorting
                }
                for reaction in reactions
            ]

            # Sort so "You" (the requester) is first if present
            reaction_list.sort(key=lambda r: not r["is_you"])  # False (user is 'You') comes first

            # Extract current user's reaction (if any)
            user_reaction = next((r["value"] for r in reaction_list if r["is_you"]), None)

            # Remove the helper key before returning
            for r in reaction_list:
                r.pop("is_you")

            return JsonResponse({'success': True, 'reactions': reaction_list, 'user_reaction': user_reaction}, status=200)
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
        print(post_id)
        post_details=post_service.get_post_by_post_id(post_id)
        comments = comment_service.get_comments_by_post(post_id,user_id)
        return JsonResponse({"comments": comments,'post_data':post_details}, safe=False)

    


class CommentCreate(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def post(self, request, post_id):
        try:
            data = json.loads(request.body)
            comment_text = data.get("comment_text")
            reply_for_id = data.get("reply_for")  # Get reply_for field
            # print(data)
            print(post_id)
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
            response_data = comment_service.toggle_reaction(comment_id, reacted_by)
            return JsonResponse(response_data)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        

class ToggleFollowView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request):
        return JsonResponse({"error": "GET method not allowed"}, status=405)

    def post(self, request):
        try:
            data = json.loads(request.body)
            print(data)
            following_id = data.get("following_id")
            created_by = data.get("created_by") 

            response_data, status_code = comment_service.toggle_follow(following_id,created_by)
            return JsonResponse(response_data, status=status_code)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        

class CheckFollowState(View):
    def get(self, request):
        following_id = request.GET.get("following_id")
        created_by_id = request.user.id  # Assuming user is authenticated

        if not following_id:
            return JsonResponse({"error": "Missing 'following_id'"}, status=400)

        is_following = comment_service.is_user_following(created_by_id, following_id)

        if is_following is None:
            return JsonResponse({"error": "User not found"}, status=404)

        return JsonResponse({"is_following": is_following})
    


import logging

logger = logging.getLogger(__name__)  # Logger for debugging

class GetFollowersFollowing(View):
    def get(self, request):
        user_id = request.GET.get("user_id")
        # print(user_id)
        try:
            count_follower, count_following =chat_service.get_all_user_follow(user_id)
            return JsonResponse({
                "count_follower": count_follower,
                "count_following": count_following
            })

        except Exception as e:
            logger.error(f"Error fetching followers/followings for user {user_id}: {str(e)}", exc_info=True)
            return JsonResponse({"error": "Internal server error"}, status=500)
        


class GetUserPostsComments(View):
    def get(self, request, user_id):
        posts = post_service.get_user_post_comment_count(user_id)
        # print(posts)
        return JsonResponse({'posts': list(posts)})
    


class GetCommentsLikes(View):
    def get(self, request, user_id, post_id):
        comments_data = comment_service.get_comments_likes(user_id, post_id)
        return JsonResponse({"comments": comments_data})
    



class PostReactionDetailsView(View):
    def get(self, request, post_id):
        reactions = post_service.get_all_reactions(post_id)
        print(reactions)
        reaction_data = [
            {
                'user_name': f"{reaction.reacted_by.first_name} {reaction.reacted_by.last_name}" or "unknown",
                'user_pic':reaction.reacted_by.profile_photo_url or '/static/images/avatar.jpg',
                'reaction': reaction.master_list_id.value,
            }
            for reaction in reactions
        ]
        print(reaction_data)
        return JsonResponse({'post_id': post_id, 'reactions': reaction_data})


