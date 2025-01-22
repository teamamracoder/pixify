from django.urls import path # type: ignore
from . import views

urlpatterns = [
    # home
    path('admin/', views.AdminHomeView.as_view(), name='home'),

    # home
    path('', views.HomeView.as_view(), name='home'),


    # manage-user
    path('admin/users/', views.ManageUserListView.as_view(), name='user_list'),
    path('admin/users/profile', views.ManageUserProfileView.as_view(), name='user_profile'),
    path('admin/users/toggle-active/<int:user_id>/', views.ManageToggleUserActiveView.as_view(), name='toggle_user_active'),
    path('admin/users/create/', views.ManageUserCreateView.as_view(), name='user_create'),
    path('admin/users/<int:user_id>/', views.ManageUserDetailView.as_view(), name='user_detail'),
    path('admin/users/<int:user_id>/update/', views.ManageUserUpdateView.as_view(), name='user_update'),
    # path('admin/users/<int:user_id>/delete/', views.ManageUserDeleteView.as_view(), name='user_delete'),

    path('change-my-theme/', views.ChangeMyThemeView.as_view(), name='change_my_theme'),



    #manage-notification
    path('admin/notifications/', views.ManageNotificationListView.as_view(), name='manage_notification_list'),
    path('admin/notifications/toggle-active/<int:notification_id>/', views.ManageToggleNotificationActiveView.as_view(), name='manage_toggle_Notification_active'),
    path('admin/notifications/create/', views.ManageNotificationCreateView.as_view(), name='manage_notification_create'),
    path('admin/notifications/<int:notification_id>/detail/', views.ManageNotificationDetailView.as_view(), name='manage_notification_detail'),
    path('admin/notifications/<int:notification_id>/update/', views.ManageNotificationUpdateView.as_view(), name='manage_notification_update'),

    # admin message
    path('admin/messages/', views.ManageMessageListView.as_view(), name='manage_message_list'),
    path('admin/messages/create/', views.ManageMessageCreateView.as_view(), name='manage_message_create'),
    path('admin/messages/toggle-active/<int:message_id>/', views.ManageToggleMessageActiveView.as_view(), name='manage_toggle_message_active'),

    #manage-post
    path('admin/posts/', views.AdminPostListView.as_view(), name='manage_post_list'),
    path('admin/posts/toggle-active/<int:post_id>/', views.AdminTogglePostActiveView.as_view(), name='toggle_post_active'),
    path('admin/posts/create/', views.AdminPostCreateView.as_view(), name='manage_post_create'),
    path('admin/posts/<int:post_id>/details', views.AdminPostDetailView.as_view(), name='manage_post_detail'),
    path('admin/posts/<int:post_id>/update/', views.AdminPostUpdateView.as_view(), name='manage_post_update'),

    path('admin/posts/', views.ManagePostListView.as_view(), name='manage_post_list'),
    # path('admin/posts/toggle-active/<int:post_id>/', views.ManageTogglePostActiveView.as_view(), name='toggle_post_active'),

    path('admin/posts/create/', views.ManagePostCreateView.as_view(), name='manage_post_create'),
    path('admin/posts/', views.ManagePostListView.as_view(), name='manage_post_list'),
    path('admin/posts/<int:post_id>/details', views.ManagePostDetailView.as_view(), name='manage_post_detail'),
    # path('admin/posts/toggle-active/<int:post_id>/', views.ManageTogglePostActiveView.as_view(), name='toggle_post_active'), 
    path('admin/posts/<int:post_id>/update/', views.ManagePostUpdateView.as_view(), name='manage_post_update'),
    path('admin/posts/toggle-active/<int:comment_id>/', views.ManageToggleCommentActiveView.as_view(), name='manage_toggle_comment_active'),
    
    #admin post specific user
    # path('admin/posts/<int:post_id>/create_specific_user/', views.ManagePostSpecificUserView.as_view(), name='manage_post_specific_user'),
    # path('admin/posts/specific_user_list/', views.ManagePostSpecificUserListView.as_view(), name='manage_post_specific_user_list'),
    # path('admin/posts/specific_user_details/', views.ManagePostSpecificUserDetailView.as_view(), name='manage_post_specific_user_detail'),


    #chat
    path('chat/', views.ChatListView.as_view(), name='chat_list'),
    path('chat/create/', views.ChatCreateView.as_view(), name='chat_create'),
    path('chat/<int:chat_id>', views.ChatDetailsView.as_view(), name='chat_details'),
    path('chat/<int:chat_id>/update/', views.ChatUpdateView.as_view(), name='chat_update'),
    path('chat/<int:chat_id>/delete', views.ChatDeleteView.as_view(), name='chat_delete'),
    path('chat/<int:chat_id>/create-members', views.ChatMemeberCreateView.as_view(), name='create_members'),
    path('chat/<int:chat_id>/delete-members', views.ChatMemeberDeleteView.as_view(), name='delete_members'),

    # manage-chat
    path('admin/chat/', views.ManageChatListView.as_view(), name='manage_chat_list'),
    path('admin/chat/create/', views.ManageChatCreateView.as_view(), name='manage_chat_create'),
    path('admin/chat/<int:chat_id>/', views.ManageChatDetailView.as_view(), name='manage_chat_detail'),
    path('admin/chat/<int:chat_id>/update/', views.ManageChatUpdateView.as_view(), name='manage_chat_update'),
   # path('admin/chat/<int:chat_id>/delete/', views.ManageChatDeleteView.as_view(), name='manage_chat_delete'),
    path('admin/chat/toggle-active/<int:chat_id>/', views.ManageToggleChatActiveView.as_view(), name='manage_toggle_chat_active'),
    path('admin/chat/membercreate/', views.ManageMemberChatCreateView.as_view(), name='manage_chat_membercreate'),
    path('admin/chat/memberlist/', views.ManageMemberChatListView.as_view(), name='manage_chat_memberlist'),

    # manage-comment
    path('admin/comments/', views.ManageCommentListView.as_view(), name='manage_comment_list'),
    path('admin/comments/create/', views.ManageCommentCreateView.as_view(), name='manage_comment_create'),
    path('admin/comments/toggle-active/<int:comment_id>/', views.ManageToggleCommentActiveView.as_view(), name='manage_toggle_comment_active'),






    # notification
    path('notification/', views.NotificationView.as_view(), name='notification-view'), 

    # profile
    path('profile/', views.EnduserprofileView.as_view(), name='userprofile'),
    path('editprofile/<int:user_id>/', views.EnduserprofileUpdateView.as_view(),name='enduser_edit_profile'),

    # aboutus
    path('aboutus/', views.AboutUsView.as_view(), name='aboutus'),

    # contact
    path('contactus/', views.ContactUsView.as_view(), name='contact'),



    path('friendrequest/', views.FriendRequestView.as_view(), name='friendrequest'),

    path('friends/', views.FriendsView.as_view(), name='friends'),

    path('birthday/', views.BirthdayView.as_view(), name='birthday'),

    path('userprofile/', views.UserprofileView.as_view(), name='userprofile'),

    # message
    path('chat/<int:chat_id>/message/', views.MessageListView.as_view(), name='message'),
    path('chat/message/create', views.MessageCreateView.as_view(), name='message_create'),
    path('chat/message/<int:message_id>/update/', views.MessageUpdateView.as_view(), name='message_update'),
    path('chat/message/<int:message_id>/delete/', views.MessageDeleteView.as_view(), name='message_delete'),

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

    #chat member api
    path('chat/<int:chat_id>/members/api', views.MemberListViewApi.as_view(), name='member_api'),

     # message reaction
    path('message-reactions/<int:message_id>/', views.MessageReactionsListView.as_view(), name='message_reaction'),
    path('message-reaction/create/', views.MessageReactionCreateView.as_view(), name='message_reaction_create'),
    path('message-reaction/delete/', views.MessageReactionDeleteView.as_view(), name='message_reaction_delete'),
    path('reaction-details/<int:message_id>/<str:reaction_type>/', views.ReactionDetailsView.as_view(), name='reaction-details'),

    # message mention list api
    path('message-mention/<int:chat_id>/', views.MessageMentionListViewApi.as_view(), name='message_mention'),
    
    # message reply
    path('chat/message-reply/<int:message_id>/', views.MessageReplyCreateView.as_view(), name='message_reply'),

    # path('posts/create/', views.UserPostCreatView.as_view()),

    # path('profile/verification/', views.UserVerificationView.as_view(),name=('Profile_verification')),



    #for enduser post
    path('posts/create/', views.UserPostCreatView.as_view(),name='userpost_create'),
    path('', views.UserPostListView.as_view(), name='Userposts_list'),


    #comment
    # path('comments/<int:post_id>/', views.CommentsCreateView.as_view(), name='comments'),
    path('comments/',  views.CommentsCreateView.as_view(), name='comment'),
    path('comments/getComment/',views.CommentsListView.as_view(), name='comments_list'),
    # path('<int:post_id>/',views.UserPostDetail.as_view(),name="Userdetail" ),

    #for enduser story
    path('story/create/', views.UserStoryCreatView.as_view(),name='userstory_create'),
    # path('', views.UserStoryListView.as_view(), name='Userstory_list'),
    path('uploadStory/', views.UploadStoryView.as_view(),name='uploadStory'),

]


