from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .. import services

class NotificationView(View):
    def get(self, request):
        notifications_fetch = services.user_Notification_service.count_notification()
        notification_list = list(notifications_fetch.values())

        # Sort notifications by created_at in descending order (newest first)
        notification_list.sort(key=lambda x: x['created_at'], reverse=True)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Handle pagination
            page = int(request.GET.get('page', 1))
            per_page = 10
            start = (page - 1) * per_page
            end = start + per_page
            paginated_notifications = notification_list[start:end]

            # Check if there are more notifications to load
            has_more = end < len(notification_list)

            return JsonResponse({
                'notifications': paginated_notifications,
                'has_more': has_more
            })

        # Render the initial HTML for regular requests
        return render(request, 'enduser/notification/index.html', {'notification_list': notification_list})

