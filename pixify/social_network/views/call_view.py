# from django.shortcuts import render
# from django.views import View

# class MakeCallView(View):
#     def get(self, request, page_type, call_id, chat_id):
#         context = {
#             'call_id': call_id,
#             'chat_id': chat_id  # Add chat_id to the context
#         }
#         if page_type == 'calling':
#             return render(request, 'enduser/chat/calling.html', context=context)
#         return render(request, 'enduser/chat/ringing.html', context=context)

# class CallView(View):
#     def get(self,request,call_id,chat_id):
#         print(chat_id)
#         print(call_id)
#         context = {
#             'call_id': call_id,
#             'chat_id': chat_id  # Add chat_id to the context
#         }
#         return render(request,'enduser/chat/call.html',context=context)