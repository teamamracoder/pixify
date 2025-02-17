import json
import os
from django.http import FileResponse, HttpResponse, JsonResponse
import firebase_admin
from firebase_admin import credentials
from pixify import settings
from firebase_admin import messaging

from social_network import services

FIREBASE_CREDENTIALS_PATH = os.path.join(settings.BASE_DIR, 'static/js/serviceAccountKey.json')

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)


def FirebaseMessagingSwFile(request):

    file_path = os.path.join(settings.BASE_DIR, 'static/js/firebase-messaging-sw.js')
    try:
        with open(file_path, 'r') as f:
            file_content = f.read()
        return HttpResponse(file_content, content_type='application/javascript')
    except FileNotFoundError:
        return HttpResponse("File not found", status=404)


# def Firebasenotify (request):
#     # Replace this with the actual token that you've retrieved from the frontend
#     token = 'ezXkUn5eFVk-i4aRmL92Ij:APA91bEgcLOLnaW_FpSOdwu2dqfPEtEb9akpKEvHHGBmR8fkHvew4Ji6l4YZ0jM_hNZpuY22KJbNtkkCIRKJwWvit4lqRR1rrSVBo5zlXO15p5co-n2SG_8'
#     # Create a message
#     message = messaging.Message(
#         notification=messaging.Notification(
#             title='New Notification',
#             body=' Rima You have new notification',
#         ),
#         token=token
#         user =request.user
#         user.fcm_token=token
#         user.save()
#     )

#     try:
#         # Send the message
#         response = messaging.send(message)
#         print('Successfully sent message:', response)

#         return JsonResponse({'status': 'success', 'message': 'Notification sent successfully.'})

#     except Exception as e:
#         print('Error sending message:', e)
#         return JsonResponse({'status': 'error', 'message': str(e)})


def Firebasenotify(request):
    # Replace this with the actual token retrieved from the frontend
    token = 'ezXkUn5eFVk-i4aRmL92Ij:APA91bEgcLOLnaW_FpSOdwu2dqfPEtEb9akpKEvHHGBmR8fkHvew4Ji6l4YZ0jM_hNZpuY22KJbNtkkCIRKJwWvit4lqRR1rrSVBo5zlXO15p5co-n2SG_8'
    user_id=request.user.id
    # Get the user from the request
    user = request.user  # Ensure request.user is available
    user.fcm_token = token  # Save the token to the user model
    user.save()

    # Create a notification message
    message = messaging.Message(
        notification=messaging.Notification(
            title='New Notification',
            body='Rima, you have a new notification',


        ),
        token=token  # Missing comma issue is fixed
    )
    print( message.notification.title,  message.notification.body)
    notifications=services.user_Notification_service.create_notification( message.notification.title,user_id)

    try:
        # Send the message
        response = messaging.send(message)
        print('Successfully sent message:', response)

        return JsonResponse({'status': 'success', 'message': 'Notification sent successfully.'})

    except Exception as e:
        print('Error sending message:', e)
        return JsonResponse({'status': 'error', 'message': str(e)})



import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
#from ..models import UserFCMToken
from django.contrib.auth.models import User

@csrf_exempt
def save_fcm_token(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = request.user.id
            user_id=6
            fcm_token = data.get("fcm_token")

            if not user_id or not fcm_token:
                return JsonResponse({"status": "error", "message": "Invalid data"}, status=400)

            services.user_service.updateFCMToken(user_id,fcm_token)

            return JsonResponse({"status": "success", "message": "FCM Token saved successfully"})
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "User not found"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=405)



from firebase_admin import messaging

def send_notification(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_id = data.get("user_id")
        title = data.get("title")
        body = data.get("body")

        if not user_id or not title or not body:
            return JsonResponse({"status": "error", "message": "Missing parameters"})

        #  Retrieve FCM token from database
        token=services.user_service.getFCMtoken(user_id)
        # try:
        #     user_fcm = User.objects.get(user_id=user_id)
        #     token = user_fcm.fcm_token
        # except User.DoesNotExist:
        #     return JsonResponse({"status": "error", "message": "User not found or FCM token missing"})

        #  Create FCM message
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=token,
        )

        try:
            # ✅ Send the message via Firebase
            response = messaging.send(message)
            return JsonResponse({"status": "success", "message": "Notification sent successfully", "response": response})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request"})



