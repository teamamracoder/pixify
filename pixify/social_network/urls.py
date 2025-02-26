from django.urls import path # type: ignore
from . import views

from django.urls import path



urlpatterns = [
    # home
    path('admin/', views.ManageAdminHomeView.as_view(), name='admin_home'),
    path('admin-dashboard/', views.ManageAdminHomeView.as_view(), name='get_filtered_users'),

    # home
    path('', views.HomeView.as_view(), name='home'),
    path('home/loginuserdetails/', views.LoginUserDetailsView.as_view(), name='loginuserdetails'),

    # manage-user
    path('admin/users/', views.ManageUserListView.as_view(), name='user_list'),
    path('admin/users/profile', views.ManageUserProfileView.as_view(), name='user_profile'),
    path('admin/users/toggle-active/<int:user_id>/', views.ManageToggleUserActiveView.as_view(), name='toggle_user_active'),
    path('admin/users/create/', views.ManageUserCreateView.as_view(), name='user_create'),
    path('admin/users/<int:user_id>/', views.ManageUserDetailView.as_view(), name='user_detail'),
    path('admin/users/<int:user_id>/update/', views.ManageUserUpdateView.as_view(), name='user_update'),
    path('admin/users/profile/<int:user_id>/', views.ManageAdminProfileUpdateView.as_view(), name='user_profile_update'),
    path('admin/users/profileimg/<int:user_id>/', views.ManageAdminProfilePicView.as_view(), name='user_profile_pic_update'),

    path('change-my-theme/', views.ChangeMyThemeView.as_view(), name='change_my_theme'),



    #manage-notification
    path('admin/notifications/', views.ManageNotificationListView.as_view(), name='manage_notification_list'),
    path('admin/notifications/toggle-active/<int:notification_id>/', views.ManageToggleNotificationActiveView.as_view(), name='manage_toggle_Notification_active'),
    path('admin/notifications/create/', views.ManageNotificationCreateView.as_view(), name='manage_notification_create'),
    path('admin/notifications/<int:notification_id>/detail/', views.ManageNotificationDetailView.as_view(), name='manage_notification_detail'),
    path('admin/notifications/<int:notification_id>/update/', views.ManageNotificationUpdateView.as_view(), name='manage_notification_update'),
    path('notifications/unread_count/', views.unread_notifications_count, name='unread_notifications_count'),

    # admin message
    path('admin/messages/', views.ManageMessageListView.as_view(), name='manage_message_list'),
    path('admin/messages/create/', views.ManageMessageCreateView.as_view(), name='manage_message_create'),
    path('admin/messages/toggle-active/<int:message_id>/', views.ManageToggleMessageActiveView.as_view(), name='manage_toggle_message_active'),


    path('admin/posts/create/', views.ManagePostCreateView.as_view(), name='manage_post_create'),
    path('admin/posts/', views.ManagePostListView.as_view(), name='manage_post_list'),
    path('admin/posts/<int:post_id>/details', views.ManagePostDetailView.as_view(), name='manage_post_detail'),
    path('admin/posts/toggle-active/<int:post_id>/', views.ManageTogglePostActiveView.as_view(), name='toggle_post_active'),
    path('admin/posts/<int:post_id>/update/', views.ManagePostUpdateView.as_view(), name='manage_post_update'),
    path('admin/posts/toggle-active/<int:comment_id>/', views.ManageToggleCommentActiveView.as_view(), name='manage_toggle_comment_active'),


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
    path('allRecommendedUsers/', views.AllRecommendedUsersView.as_view(), name='allRecommendedUsers'),
    path('follow-user/', views.FollowUserView.as_view(), name="followUser"),

    path('friends/', views.FriendsView.as_view(), name='friends'),

    path('birthday/', views.BirthdayView.as_view(), name='birthday'),


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




    #for enduser post priya
    path('posts/create/', views.UserPostCreatView.as_view(),name='userpost_create'),
    path('post/update/',views.UserPostEditView.as_view(),name='UserPostEdit'),

    path('post/reaction/update/', views.UpdatePostReactionView.as_view(), name='update_post_reaction'),
    path('fetch_reactions/', views.Fetch_reactions.as_view(), name='fetch_reactions'),
    path('delete-post-reaction/', views.DeletePostReactionView.as_view(), name='delete_post_reaction'),


    path('post/delete/',views.UserPostDeleteView.as_view(),name='UserPostDelete'),
    path('comments/reply/',views.CommentReplyView.as_view(), name='reply_comment'),

    path('comments/getReplies/', views.GetRepliesView.as_view(), name="get_replies"),
    #comment priya
    path('comments/',  views.CommentsCreateView.as_view(), name='comment'),
    path('comments/getComment/',views.CommentsListView.as_view(), name='comments_list'),
    path('post/reactions/', views.GetPostReactionsView.as_view(), name='get_post_reactions'),
    path('post/comment/', views.GetPostCommentView.as_view(), name='get_comment_reactions'),
    path("delete-comment/", views.DeleteCommentView.as_view(), name="delete-comment"),
    path('toggle-like/', views.ToggleLikeView.as_view(), name='toggle-like'),
    path("remove_reaction/", views.remove_reaction.as_view(), name="remove_reaction"),
    path("fetch-comment-likes/", views.fetch_comment_likes.as_view(), name="fetch_comment_likes"),
    path("fetch-comment-likess/", views.FetchCommentLikes.as_view(), name="fetch_comment_likes"),





    #for enduser story
    # path('story/create/', views.UserStoryCreatView.as_view(),name='userstory_create'),
    # path('uploadStory/', views.UploadStoryView.as_view(),name='uploadStory'),
    # path('call/<str:page_type>/<str:call_id>/<int:chat_id>/', views.MakeCallView.as_view(), name='make_call_page'),
    #  path('call/<str:call_id>/<int:chat_id>/', views.CallView.as_view(), name='call_page'),
    #for enduser story
    path('story/create/', views.UserStoryCreatView.as_view(),name='userstory_create'),
    # path('', views.UserStoryListView.as_view(), name='Userstory_list'),
    path('stories/user/<int:user_id>/', views.UserstoryListView.as_view(), name='user-stories'),
    path('uploadStory/', views.UploadStoryView.as_view(),name='uploadStory'),
    path('stories/view/<int:user_id>/', views.UserActiveStories.as_view(), name='user_active_stories'),



    #short
    path('short', views.ShortListView.as_view(),name='short'),
    path('short/<int:post_id>/reaction/create', views.ShortReactionCreateView.as_view(),name='short_reaction_create'),
    path('short/reaction/<int:post_id>/delete', views.ShortReactionDeleteView.as_view(),name='short_reaction_delete'),
    path('short/<int:post_id>/comments/', views.ShortCommentListView.as_view(),name='short_comments'),
    path('short/<int:post_id>/comment/create/', views.ShortCommentCreateView.as_view(),name='short_comment_create'),
    path('short/comment/<int:comment_id>/delete/', views.ShortCommentDeleteView.as_view(),name='short_comment_delete'),
    path('short/comment/<int:comment_id>/reply/', views.ShortCommentReplyView.as_view(),name='short_comment_reply'),
    path('short/comment/<int:comment_id>/reaction/', views.ShortCommentReactionView.as_view(),name='short_comment_reaction'),

    # path('save-fcm-token/', views.save_fcm_token, name='save-fcm-token'),
    path('firebase-messaging-sw.js', views.FirebaseMessagingSwFile, name='firebase-messaging-sw'),
    path('firebase-notify/', views.Firebasenotify, name='firebase-notify'),
    path('save_fcm_token/', views.save_fcm_token, name="save_fcm_token"),
    path('send_notification/',views.send_notification, name="send_notification"),

    # Short Share List Api
    path('short/share/api', views.ShortShareListViewApi.as_view(), name='short_share_api'),

]


