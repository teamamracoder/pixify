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
    path('chat/', views.ChatListView.as_view(), name='chat_list'),
    path('chat/create', views.ChatCreateView.as_view(), name='chat_create'),
    path('chat/<int:chat_id>', views.ChatDetailsView.as_view(), name='chat_details'),
    path('chat/<int:chat_id>/update', views.ChatUpdateView.as_view(), name='chat_update'),
    path('chat/<int:chat_id>/delete', views.ChatDeleteView.as_view(), name='chat_delete'),

    path('admin/chat/', views.ManageChatListView.as_view(), name='manage_chat_list'),
    path('admin/chat/create/', views.ManageChatCreateView.as_view(), name='manage_chat_create'),
    path('admin/chat/<int:chat_id>/', views.ManageChatDetailView.as_view(), name='manage_chat_detail'),
    path('admin/chat/<int:chat_id>/update/', views.ManageChatUpdateView.as_view(), name='manage_chat_update'),
   # path('admin/chat/<int:chat_id>/delete/', views.ManageChatDeleteView.as_view(), name='manage_chat_delete'),
    path('admin/chat/toggle-active/<int:chat_id>/', views.ManageToggleChatActiveView.as_view(), name='manage_toggle_chat_active'),
    


    # notification
    path('notification/', views.NotificationView.as_view(), name='notification'),
    
    # profile
    path('profile/', views.EnduserprofileView.as_view(), name='userprofile'),
    
    # aboutus
    path('aboutus/', views.AboutUsView.as_view(), name='aboutus'),

    # contact
    path('contactus/', views.ContactUsView.as_view(), name='contact'),
    
    path('comments/', views.CommentsView.as_view(), name='comments'),

    path('friendrequest/', views.FriendRequestView.as_view(), name='friendrequest'),

    path('birthday/', views.BirthdayView.as_view(), name='birthday'),

    path('friends/', views.FriendsView.as_view(), name='friends'),
    path('birthday/', views.BirthdayView.as_view(), name='birthday'),

    path('userprofile/', views.UserprofileView.as_view(), name='userprofile'),

    # message
    path('message/', views.MessageListView.as_view(), name='message'),
    path('message/create', views.MessageCreateView.as_view(), name='message_create'),
    path('message/<int:message_id>/update', views.MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:message_id>/delete', views.MessageDeleteView.as_view(), name='message_delete'),
    
    # auth
    path('request-otp/', views.RequestOTPView.as_view(), name='request_otp'),
    path('verify-otp/', views.VerifyOTPView.as_view(), name='verify_otp'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('resend-otp/', views.ResendOTPView.as_view(), name='resend_otp'),
    
    #chatlist api 
    path('chat/chats/api', views.ChatListViewApi.as_view(), name='chats_api'),
    
    #flolowers api 
    path('chat/followers/api', views.FollowerListViewApi.as_view(), name='followers_api'),
    
     # message reaction
    path('message-reaction/create/', views.MessageReactionCreateView.as_view(), name='message_reaction_create'),
    path('message-reaction/<int:message_reaction_id>/update/', views.MessageReactionUpdateView.as_view(), name='message_reaction_update'),
    path('message-reaction/<int:message_reaction_id>/delete/', views.MessageReactionDeleteView.as_view(), name='message_reaction_delete'),

    # message mention
    path('message-mention/<int:message_id>', views.MessageMentionCreateView.as_view(), name='message_mention'),
    
    # message reply
    path('message-reply/<int:message_id>/', views.MessageReplyCreateView.as_view(), name='message_reply'),
]



