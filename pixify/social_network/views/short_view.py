from django.views import View
from django.shortcuts import render, redirect
from ..services import short_service
import random
from django.http import JsonResponse

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

        random.shuffle(shorts)  # Randomize the list
        return render(request, 'enduser/short/index.html', {'shorts': shorts})          

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
       comments = short_service.short_comments(post_id)  
             
       return JsonResponse({"comments": list(comments)}, safe=False)

class ShortCommentCreateView(View):
    def post(self, request, post_id):
        user = request.user
        post = short_service.get_short(post_id)
        text = request.get('text')

        comment = short_service.comment_creat(text, post, user)

class ShortCommentDeleteView(View):
    def post(self, request, comment_id):
        user=request.user
        short_service.short_comment_delete(comment_id, user)

class ShortCommentReplyView(View):
    def post(self, request, comment_id):
        user=request.user
        text=request.get('text')
        comment=short_service.get_short_comment(comment_id)
        short_service.short_comment_reply(text, comment.post_id, comment_id, user)
        
class ShortCommentReactionView(View):    
    def post(self, request, comment_id):
        pass

class ShortCommentReactionDeleteView(View):
    def post(self, request, comment_id):
        pass