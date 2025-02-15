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
        # countMonthlyUser  = services.manage_home_service.manage_user_monthly_count(date,interval)
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

              # Calculate the start date based on selected days
            start_date = now() - timedelta(days=days)

            # Fetch user, post, and admin count based on selected interval
            user_count = User.objects.filter(date_joined__gte=start_date).count()
            post_count = Post.objects.filter(created_at__gte=start_date).count()
            admin_count = User.objects.filter(Q(date_joined__gte=start_date) & Q(roles__contains=[1])).count()

            # Adjust interval data based on selected range
            interval_data = []
            interval_start = now() - timedelta(days=days)  # Start from selected days ago
            num_intervals = days // 60  # Number of 2-month intervals in selected range

            for i in range(0, 12, 2):  # Loop every 2 months
                interval_start = start_date + timedelta(days=i * 30)  # Approximate months as 30 days
                interval_end = interval_start + timedelta(days=60)  # 2-month range
                count_month_2intervel = User.objects.filter(date_joined__gte=interval_start, date_joined__lt=interval_end).count()
                
                interval_data.append({
                    "start_date": interval_start.strftime("%Y-%m-%d"),  
                    "end_date": interval_end.strftime("%Y-%m-%d"),
                    "count_month_2intervel": count_month_2intervel,
                    # "count_month_2intervel1": count_month_2intervel1
                })

            print(f"Interval Data: {interval_data}")


                    # **🔹 Second Loop - Pie Chart Data (4-Month Intervals, Admin Count)**
            piechart_data = []
            start_date = now() - timedelta(days=days)  # Adjust days if needed (e.g., last year)
            num_intervals = days // 3  # Number of 3-month intervals

            for i in range(0, 12, 3):  # Loop every 3 months
                interval_start = start_date + timedelta(days=i * 30)  # Approximate start of 3-month range
                interval_end = interval_start + timedelta(days=90)  # End of 3-month range

                # Filter users where roles contains [1] (admin role) and date joined is within interval
                admin_count_interval = User.objects.filter(date_joined__gte=interval_start,date_joined__lt=interval_end,roles__contains=[1]).count()

                # Append data to pie chart list
                piechart_data.append({
                    "start_date": interval_start.strftime("%Y-%m-%d"),  
                    "end_date": interval_end.strftime("%Y-%m-%d"),
                    "admin_count": admin_count_interval,
                })


            print(f"Pie Chart Data: {piechart_data}")

            linechart_data = []
            days_start = now() - timedelta(days=days)  # Start from selected days ago

            for i in range(0, 12, 1):  # Loop every 1 month
                days_start = start_date + timedelta(days=i * 30)  # Approximate each month as 30 days
                days_end = days_start + timedelta(days=30)  # 1-month range
                
                # Fetch the number of posts created in the given month
                post_count_interval = Post.objects.filter(created_at__gte=days_start, created_at__lt=days_end).count()

                linechart_data.append({
                    "start_date": days_start.strftime("%Y-%m-%d"),
                    "end_date": days_end.strftime("%Y-%m-%d"),
                    "post_count": post_count_interval,  # Now correctly retrieving post data
                })

            print(f"Linechart Data: {linechart_data}")


            all_data = {
                "user_count": user_count,
                "post_count": post_count,
                "admin_count": admin_count,
            }

            return JsonResponse({
                "all_data": all_data,
                "interval_data": interval_data,
                "piechart_data": piechart_data,
                "linechart_data":linechart_data,
            })                

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        

        #------------------------------------------------------------------

        