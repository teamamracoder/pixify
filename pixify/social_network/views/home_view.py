from django.shortcuts import render, redirect
from django.views import View

class HomeView(View):
    def get(self, request):
        return render(request, 'enduser/home/index.html')
    

# class HomeView(View):
#     def get(self, request):
#         return render(request, 'enduser/home/userprofile.html')

    
      
