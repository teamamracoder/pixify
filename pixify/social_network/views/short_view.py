from django.views import View
from django.shortcuts import render, redirect
from ..services import (
    short_service,
    chat_service,
    follower_service,    
    chat_member_service,    
    story_service,
    post_reaction_service,
    post_service,
    comment_service,
)
import random
from django.http import JsonResponse
import json
from ..constants import ChatType, PostType
from social_network.packages.response import success_response


class ShortListView(View):
    def get(self, request):
        user=request.user
        shorts = short_service.get_shorts()
        for short in shorts:
            count = short_service.reaction_count(short.id)
            short.reaction_count = short_service.format_count(count)
            comments = short_service.comment_count(short.id)
            short.comments_count = short_service.format_count(comments)
            short.user_reacted = short_service.user_has_reacted(short, user)
            short.created_at = short_service.format_created_time(short.created_at)
            short.followed = follower_service.follower_check(short.posted_by,user)

        random.shuffle(shorts)  # Randomize the list
        return render(request, 'enduser/short/index.html', {'shorts': shorts,'user':user})
    
    
class PostDetailView(View):
    def get(self, request, post_id):
        user = request.user
        selected_post = short_service.get_short(post_id)
        
        if selected_post.type == PostType.SHOTS.value:
            # Process and render the shots template
            count = short_service.reaction_count(selected_post.id)
            selected_post.reaction_count = short_service.format_count(count)
            comments = short_service.comment_count(selected_post.id)
            selected_post.comments_count = short_service.format_count(comments)
            selected_post.user_reacted = short_service.user_has_reacted(selected_post, user)
            
            shorts = short_service.get_shorts()
            for s in shorts:
                if s.id != selected_post.id:
                    cnt = short_service.reaction_count(s.id)
                    s.reaction_count = short_service.format_count(cnt)
                    comm = short_service.comment_count(s.id)
                    s.comments_count = short_service.format_count(comm)
                    s.user_reacted = short_service.user_has_reacted(s, user)
            
            shorts = [s for s in shorts if s.id != selected_post.id]
            random.shuffle(shorts)
            shorts.insert(0, selected_post)
            
            return render(request, 'enduser/short/index.html', {'shorts': shorts, 'user': user})
        else:
            # For all other post types, process the post view
            message = request.session.pop("message", "")
            message_type = request.session.pop("message_type", "")
            userid = user.id

            post = post_service.Postlist_posts()
            posts = [s for s in post if s.id != selected_post.id]
            posts.insert(0, selected_post)

            postreaction = post_reaction_service.get_reaction()
            post_id_param = request.GET.get('post_id')
            comment_list = comment_service.comment_list(post_id_param)
            post_dict = {
                'posts': posts,
                'comment_list': comment_list,
                'postreaction': postreaction,
            }

            storys = story_service.storylist_storys()
            story_dict = {'storys': storys}
            shorts = short_service.get_shorts()
            for short in shorts:
                count = short_service.reaction_count(short.id)
                short.reaction_count = short_service.format_count(count)
                comments = short_service.comment_count(short.id)
                short.comments_count = short_service.format_count(comments)
                short.user_reacted = short_service.user_has_reacted(short, user)
            random.shuffle(shorts)

            context = success_response(message=message, message_type=message_type)
            context.update({
                'post_dict': post_dict,
                'story_dict': story_dict,
                'shorts': shorts,
                'userid': userid,
            })

            return render(request, "enduser/home/index.html", context)




class ShortReactionCreateView(View):
    def post(self, request, post_id):
        user = request.user
        post = short_service.get_short(post_id)

        reaction_count = short_service.short_reaction(post, user)
        reaction_count = short_service.format_count(reaction_count)

        return JsonResponse({
            "success": True,
            "reaction_count": reaction_count,
        })


class ShortReactionDeleteView(View):
    def post(self, request, post_id):
        user = request.user
        post = short_service.get_short(post_id)

        reaction_count = short_service.short_reaction_delete(post, user)
        reaction_count = short_service.format_count(reaction_count)

        return JsonResponse({
        "success": True,
        "reaction_count":reaction_count,
        })


class ShortCommentListView(View):
    def get(self, request, post_id):
       user=request.user
       comments = short_service.short_comments(post_id, user)

       return JsonResponse({"comments": list(comments)}, safe=False)


class ShortCommentCreateView(View):
    def post(self, request, post_id):
        user = request.user
        post = short_service.get_short(post_id)

        data = json.loads(request.body)
        text = data.get('text')  # Extract text from parsed JSON

        # Create the comment (assume likes are set to 0 by default)
        comment = short_service.short_comment_create(text, post, user)

        comments = short_service.comment_count(post.id)
        comment.comments_count = short_service.format_count(comments)

        can_delete = comment.comment_by == user

        # Return the comment data in the response with like_count = 0 initially
        return JsonResponse({
            'success': True,
            'comment': {
                'id': comment.id,
                'comment': comment.comment,
                'comment_by__id': comment.comment_by.id,
                'comment_by__first_name': comment.comment_by.first_name,
                'comment_by__last_name': comment.comment_by.last_name,
                'comment_by__profile_photo_url': comment.comment_by.profile_photo_url or None,  # Handle null cases
                'created_at': 'Just now', #predefine string
                'can_delete':can_delete,
                'like_count': 0,  # Initialize like_count as 0
                'comment_count': comment.comments_count,
                'replies': []  # Empty replies for new comments
            }
        })

class ShortCommentReplyView(View):
    def post(self, request, comment_id):
        user = request.user
        data = json.loads(request.body)
        text = data.get('text')  # Extract text from parsed JSON

        comment = short_service.get_short_comment(comment_id)

        # Create the reply (initial like_count is set to 0)
        reply = short_service.short_comment_reply(text, comment.post_id, comment, user)

        comments = short_service.comment_count(reply.post_id)
        reply.comments_count = short_service.format_count(comments)

        can_delete = reply.comment_by == user  # Only allow deletion if it's the current user's reply

        # Return the reply data with like_count = 0 initially
        return JsonResponse({
            'success': True,
            'reply': {
                'id': reply.id,
                'comment': reply.comment,
                'comment_by__id': reply.comment_by.id,
                'comment_by__first_name': reply.comment_by.first_name,
                'comment_by__last_name': reply.comment_by.last_name,
                'comment_by__profile_photo_url': reply.comment_by.profile_photo_url or None,  # Handle null cases
                'reply_to':comment.comment_by.first_name,
                'can_delete':can_delete,
                'created_at': 'Just now', #predefine string
                'like_count': 0,  # Initialize like_count as 0
                'comment_count': reply.comments_count,
                'replies': []  # Replies to a reply are not supported
            }
        })

class ShortCommentDeleteView(View):
    def post(self, request, comment_id):
        user = request.user
        try:
            short =short_service.get_short_comment(comment_id)
            short_service.short_comment_delete(comment_id, user)

            comments = short_service.comment_count(short.post_id)
            comments_count = short_service.format_count(comments)

            return JsonResponse({'success': True, 'comment_count': comments_count})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)



class ShortCommentReactionView(View):
    def post(self, request, comment_id):
        user = request.user
        comment = short_service.get_short_comment(comment_id)

        # Toggle the like status
        user_liked = short_service.toggle_like(comment, user)

        count = short_service.comment_reaction_count(comment)
        comment.likes = short_service.format_count(count)

        return JsonResponse({
            'success': True,
            'like_count': comment.likes,  # Count only active likes
            'user_liked': user_liked  # Whether the user liked the comment
        })




class PostShareListViewApi(View):
    def get(self, request):
        user = request.user
        chats = chat_service.list_top_chats_api(request, user)
        follow = follower_service.list_follow_api(request, user)
        
        data = {
            "chats": chats,
            "follow": follow
        }
        return JsonResponse(data)




class PostSendView(View):
    def post(self, request):
        user = request.user
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)

        chats = data.get("chats", [])
        members = data.get("members", [])

        chat_ids = []  # List to collect chat ids
        
        # Send the video to the selected chats
        for chat_id in chats:
            chat = chat_service.get_chat_by_id(chat_id)
            chat_ids.append(chat.id)

        # Send the video to the selected members (create a personal chat for each)
        for member_id in members:
            chat = chat_service.create_chat(user, None, None, ChatType.PERSONAL.value)
            chat_member_service.add_chat_member(chat.id, user.id, user)
            chat_member_service.add_chat_member(chat.id, member_id, user)
            chat_ids.append(chat.id)

        return JsonResponse({"success": True, "chat": chat_ids})

