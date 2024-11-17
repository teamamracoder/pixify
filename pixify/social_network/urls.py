from django.urls import path
from . import views

urlpatterns = [
    # home
    path('admin/', views.AdminHomeView.as_view(), name='home'),

    # home
    path('', views.HomeView.as_view(), name='home'),


    # user
    path('admin/users/', views.UserListView.as_view(), name='user_list'),
    path('admin/users/profile', views.UserProfileView.as_view(), name='user_profile'),
    path('users/toggle-active/<int:user_id>/', views.ToggleUserActiveView.as_view(), name='toggle_user_active'),
    path('admin/users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('admin/users/<int:user_id>/', views.UserDetailView.as_view(), name='user_detail'),
    path('admin/users/<int:user_id>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('admin/users/<int:user_id>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    #admin_notification
    path('admin/notifications/', views.NotificationListView.as_view(), name='notification_list'),
    path('admin/notifications/create/', views.NotificationCreateView.as_view(), name='notification_create'),
    path('admin/notifications/<int:notification_id>/detail/', views.NotificationDetailView.as_view(), name='notification_detail'),
    path('admin/notifications/<int:notification_id>/update/', views.NotificationUpdateView.as_view(), name='notification_update'),
    # path('admin/notifications/<int:delete_id>/delete/', views.NotificationDeleteView.as_view(), name='notification_delete'),

    # post
    path('admin/posts/', views.PostListView.as_view(), name='post_list'),
    path('admin/posts/toggle-active/<int:post_id>/', views.TogglePostActiveView.as_view(), name='toggle_post_active'),
    path('admin/posts/create/', views.PostCreateView.as_view(), name='post_create'),
    path('admin/posts/<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
    path('admin/posts/<int:post_id>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('admin/posts/<int:post_id>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

    #chat
    path('admin/chat/', views.ChatAdminListView.as_view(), name='chat_list'),
    path('admin/chat/create/', views.ChatAdminCreateView.as_view(), name='chat_create'),
    path('admin/chat/<int:chat_id>/', views.ChatAdminDetailView.as_view(), name='chat_detail'),
    path('admin/chat/<int:chat_id>/update/', views.ChatAdminUpdateView.as_view(), name='chat_update'),
    path('admin/chat/<int:chat_id>/delete/', views.ChatAdminDeleteView.as_view(), name='chat_delete'),
    


    # message
    # path('message/', views.messageView.as_view(), name='message'),
    path('chat/', views.ChatView.as_view(), name='chat'),

    # notification
    path('notification/', views.notificationView.as_view(), name='notification')
]  
