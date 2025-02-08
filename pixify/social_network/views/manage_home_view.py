from django.db.models import Q
from datetime import timedelta
from django.utils.timezone import now
from itertools import count
import json
from os import truncate
from urllib import request
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from social_network.models.user_model import User
from social_network.models.post_model import Post
from social_network import services

class ManageAdminHomeView(View):#
    def get(self, request):
        countUser  = services.manage_home_service.manage_user_count()
        # print(f"============{countUser}")

        countPost = services.manage_home_service.manage_post_count()
        # print(f"============{countPost}")

        countAdmin = services.manage_home_service.manage_admin_user_count()
        # print(f"::::::::::::::::::{countAdmin}")

        data = {
            'countUser':countUser,
            'countPost':countPost,
            'countAdmin':countAdmin
        }
        
        return render(request, 'adminuser/home/index.html',{'data':data})

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            days = data.get("days")
                

            # Convert "year" option to 365 days
            if days == "year":
                days = 365
            else:
                days = int(days)  # Convert string to integer

            # Calculate the start date
            start_date = now() - timedelta(days=days)

            # Count users registered within the selected time range
            user_count = User.objects.filter(date_joined__gte=start_date).count()
            post_count = Post.objects.filter(created_at__gte=start_date).count()
            admin_count = User.objects.filter(Q(date_joined__gte=start_date) & Q(roles__contains=[1])).count()


            # return JsonResponse({"user_count": user_count})
            all_data ={"user_count": user_count,"post_count": post_count,"admin_count":admin_count}
            return JsonResponse({"all_data": all_data})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

        
    