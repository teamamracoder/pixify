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
            short.user_reacted = short_service.user_has_reacted(short, user)

        random.shuffle(shorts)  # Randomize the list        
        return render(request, 'enduser/short/index.html', {'shorts': shorts})
    
class ShortReactionView(View):
    def post(self, request, post_id):        
        post_id=post_id
        user=request.user     
        post=short_service.get_short(post_id)
        print(post)
        reaction_count=short_service.short_reaction(post, user)
        print(reaction_count)        
        return JsonResponse({
                "success": True,                
                "reaction_count":reaction_count,
            })

class ShortReactionDeleteView(View):
    def post(self, request, post_id):        
        post_id=post_id
        user=request.user     
        post=short_service.get_short(post_id)
        print(post)
        print(post_id)
        reaction_count=short_service.short_reaction_delete(post, user)
        return JsonResponse({
        "success": True,                
        "reaction_count":reaction_count,
        })


