from django.urls import path
from . import views

urlpatterns = [
    # home
    path('admin/', views.AdminHomeView.as_view(), name='home'),

    # home
    path('', views.HomeView.as_view(), name='home'),


    # user
    path('admin/users/', views.ManageUserListView.as_view(), name='user_list'),
    path('admin/users/profile', views.ManageUserProfileView.as_view(), name='user_profile'),
    path('admin/users/toggle-active/<int:user_id>/', views.ManageToggleUserActiveView.as_view(), name='toggle_user_active'),
    path('admin/users/create/', views.ManageUserCreateView.as_view(), name='user_create'),
    path('admin/users/<int:user_id>/', views.ManageUserDetailView.as_view(), name='user_detail'),
    path('admin/users/<int:user_id>/update/', views.ManageUserUpdateView.as_view(), name='user_update'),
    path('admin/users/<int:user_id>/delete/', views.ManageUserDeleteView.as_view(), name='user_delete'),

# ==============================


    #admin_notification
    path('admin/notifications/', views.ManageNotificationListView.as_view(), name='manage_notification_list'),
    path('admin/notifications/toggle-active/<int:notification_id>/', views.ManageToggleNotificationActiveView.as_view(), name='manage_toggle_Notification_active'),
    path('admin/notifications/create/', views.ManageNotificationCreateView.as_view(), name='manage_notification_create'),
    path('admin/notifications/<int:notification_id>/detail/', views.ManageNotificationDetailView.as_view(), name='manage_notification_detail'),
    path('admin/notifications/<int:notification_id>/update/', views.ManageNotificationUpdateView.as_view(), name='manage_notification_update'),
    # path('admin/notifications/<int:delete_id>/delete/', views.ManageNotificationDeleteView.as_view(), name='manage_notification_delete'),

    # post
    path('admin/posts/', views.AdminPostListView.as_view(), name='post_list'),
    path('admin/posts/toggle-active/<int:post_id>/', views.AdminTogglePostActiveView.as_view(), name='toggle_post_active'),
    path('admin/posts/create/', views.AdminPostCreateView.as_view(), name='post_create'),
    path('admin/posts/<int:post_id>/', views.AdminPostDetailView.as_view(), name='post_detail'),
    path('admin/posts/<int:post_id>/update/', views.AdminPostUpdateView.as_view(), name='post_update'),
    path('admin/posts/<int:post_id>/delete/', views.AdminPostDeleteView.as_view(), name='post_delete'),


    #chat
    path('admin/chat/', views.ManageChatListView.as_view(), name='manage_chat_list'),
    path('admin/chat/create/', views.ManageChatCreateView.as_view(), name='manage_chat_create'),
    path('admin/chat/<int:chat_id>/', views.ManageChatDetailView.as_view(), name='manage_chat_detail'),
    path('admin/chat/<int:chat_id>/update/', views.ManageChatUpdateView.as_view(), name='manage_chat_update'),
    path('admin/chat/<int:chat_id>/delete/', views.ManageChatDeleteView.as_view(), name='manage_chat_delete'),
    path('admin/chat/toggle-active/<int:chat_id>/', views.ManageToggleChatActiveView.as_view(), name='manage_toggle_chat_active'),


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



