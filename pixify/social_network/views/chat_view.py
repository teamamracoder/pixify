from django.shortcuts import render, redirect
from django.views import View

# everyone insert data manually
# user (5)
# chats (4)--> perasonal chat(2)
#           --> group chat(2)
# messages (each chats, 3 message)-->use different sender_id
# message read status (as required, initially blank)
class ChatView(View):
    def get(self, request):

    #    get all chats for the logged in user
    #      loop over the chats
    #           
        #     # chat type
        #     # if chattype personal
        #         # chat->member(who is not the loggedinuser)->fullname 
        #         # chat->member(who is not the loggedinuser)->photo
        #     #if group
        #         #chat->title
        #         #chat->coverphoto
        #     # message->findby_chat_id->all->id(desc)->first
        #     #                                       ->created_at
        #     #                                        ->msg
    
    #   users = [all follower/following without self]  but follwer/following of the logged user
    #     data = {
    #         'title'=>'fetch',
    #         'photo'=>'fetch',
    #         'last_message'=>'fetch',
    #         'last_message_time'=>'fetch',
    #         'unread_count'=>'fetch',
    #          'users'=>users
    #     }
        return render(request, 'enduser/message/index.html')
    
    def createChat():
        return
        # loggin = 3
        
        # memebers (2,4,3)
        # dinal members =set(2,4,3,3)
        
        # as memebers=single,  then, type=pesonal
        # chats(memeber), 2,1 and type=pesonal   
        # if chat available do not create new chat, redirect to that chatbox
        # else create new chat, redirect to their chatbox
        
        # mmebers 1,3
        # as memebers=multiple, then type=group
        # create new group 