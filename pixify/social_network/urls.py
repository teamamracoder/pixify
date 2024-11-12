from django.urls import path
from . import views

urlpatterns = [
    # home
    path('admin/', views.AdminHomeView.as_view(), name='home'),

    # home
    path('', views.HomeView.as_view(), name='home'),


    # user
    path('admin/users/', views.UserListView.as_view(), name='user_list'),
    path('admin/users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('admin/users/<int:user_id>/', views.UserDetailView.as_view(), name='user_detail'),
    path('admin/users/<int:user_id>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('admin/users/<int:user_id>/delete/', views.UserDeleteView.as_view(), name='user_delete'),

    # post
    path('admin/posts/', views.PostListView.as_view(), name='post_list'),
    path('admin/posts/create/', views.PostCreateView.as_view(), name='post_create'),
    path('admin/posts/<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
    path('admin/posts/<int:post_id>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('admin/posts/<int:post_id>/delete/', views.PostDeleteView.as_view(), name='post_delete'),


    # message
    path('chat/', views.ChatListView.as_view(), name='chat_list'),
    path('chat/create', views.ChatCreateView.as_view(), name='chat_list'),
    path('chat/<int:chat_id>', views.ChatDetailsView.as_view(), name='chat_details'),
    path('chat/<int:chat_id>/update', views.ChatUpdatesView.as_view(), name='chat_update'),
    path('chat/<int:chat_id>/delete', views.ChatDeleteView.as_view(), name='chat_delete'),

    # notification
    path('notification/', views.notificationView.as_view(), name='notification'),

    #message reaction 
    path('message_reaction/create/', views.MessageReactionCreateView.as_view(), name='message_reaction_create'),
    path('message_reaction/<int:Message_reaction_id>/update/', views.MessageReactionUpdateView.as_view(), name='Message_reaction_update'),
    path('message_reaction/<int:Message_reaction_id>/delete/', views.MessageReactionDeleteView.as_view(), name='Message_reaction_delete'),
]

