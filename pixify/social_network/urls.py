from django.urls import path
from . import views

urlpatterns = [
    # home
    path('admin/', views.AdminHomeView.as_view(), name='home'),

    # home
    path('', views.HomeView.as_view(), name='home'),


    # user
    path('admin/users/', views.AdminUserListView.as_view(), name='user_list'),
    path('admin/users/profile', views.AdminUserProfileView.as_view(), name='user_profile'),
    path('admin/users/toggle-active/<int:user_id>/', views.AdminToggleUserActiveView.as_view(), name='toggle_user_active'),
    path('admin/users/create/', views.AdminUserCreateView.as_view(), name='user_create'),
    path('admin/users/<int:user_id>/', views.AdminUserDetailView.as_view(), name='user_detail'),
    path('admin/users/<int:user_id>/update/', views.AdminUserUpdateView.as_view(), name='user_update'),
    path('admin/users/<int:user_id>/delete/', views.AdminUserDeleteView.as_view(), name='user_delete'),

# ==============================


    #admin_notification
    path('admin/notifications/', views.AdminNotificationListView.as_view(), name='notification_list'),
    path('admin/notifications/toggle-active/<int:notification_id>/', views.AdminToggleNotificationActiveView.as_view(), name='toggle_Notification_active'),
    path('admin/notifications/create/', views.AdminNotificationCreateView.as_view(), name='notification_create'),
    path('admin/notifications/<int:notification_id>/detail/', views.AdminNotificationDetailView.as_view(), name='notification_detail'),
    path('admin/notifications/<int:notification_id>/update/', views.AdminNotificationUpdateView.as_view(), name='notification_update'),
    # path('admin/notifications/<int:delete_id>/delete/', views.AdminNotificationDeleteView.as_view(), name='notification_delete'),

    # post
    path('admin/posts/', views.AdminPostListView.as_view(), name='post_list'),
    path('admin/posts/toggle-active/<int:post_id>/', views.AdminTogglePostActiveView.as_view(), name='toggle_post_active'),
    path('admin/posts/create/', views.AdminPostCreateView.as_view(), name='post_create'),
    path('admin/posts/<int:post_id>/', views.AdminPostDetailView.as_view(), name='post_detail'),
    path('admin/posts/<int:post_id>/update/', views.AdminPostUpdateView.as_view(), name='post_update'),
    path('admin/posts/<int:post_id>/delete/', views.AdminPostDeleteView.as_view(), name='post_delete'),

    #chat
    path('admin/chat/', views.ChatAdminListView.as_view(), name='chat_list'),
    path('admin/chat/create/', views.ChatAdminCreateView.as_view(), name='chat_create'),
    path('admin/chat/<int:chat_id>/', views.ChatAdminDetailView.as_view(), name='chat_detail'),
    path('admin/chat/<int:chat_id>/update/', views.ChatAdminUpdateView.as_view(), name='chat_update'),
    path('admin/chat/<int:chat_id>/delete/', views.ChatAdminDeleteView.as_view(), name='chat_delete'),
    path('admin/chat/toggle-active/<int:chat_id>/', views.AdminToggleChatActiveView.as_view(), name='toggle_chat_active'),

    


    # message
    # path('message/', views.messageView.as_view(), name='message'),
    # path('chat/', views.ChatView.as_view(), name='chat'),

    # notification
    path('notification/', views.notificationView.as_view(), name='notification'),

     # auth
    path('request-otp/', views.RequestOTPView.as_view(), name='request_otp'),
    path('verify-otp/', views.VerifyOTPView.as_view(), name='verify_otp'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('resend-otp/', views.ResendOTPView.as_view(), name='resend_otp'),

    # path('users/api', views.userListViewApi.as_view(), name='users_api')
    # message_edit and deleat
    # path('message/<int:message_id>/edit', views.MessageEditView.as_view(), name='message_edit'),
    # path('message/<int:message_id>/delete', views.MessageDeleteView.as_view(), name='message_delete'),

]



