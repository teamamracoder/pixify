from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from Message.models import Message

def send_reply(request, message_id):
    if request.method == "POST":
        content = request.POST.get("content")
        original_message = get_object_or_404(Message, id=message_id)
        
        Message.objects.create(sender=request.user, content=content, reply_to=original_message)
        
    return redirect('chat_view')  
