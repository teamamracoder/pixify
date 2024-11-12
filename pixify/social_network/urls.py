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

    # path('message/', views.messageView.as_view(), name='message'),
    path('chat/', views.ChatView.as_view(), name='chat'),

    # notification
    path('notification/', views.NotificationView.as_view(), name='notification'),

     # profile
    path('profile/', views.EnduserprofileView.as_view(), name='userprofile'),

     # aboutus
    path('aboutus/', views.AboutUsView.as_view(), name='aboutus'),

     # contact
    path('contactus/', views.ContactUsView.as_view(), name='contact'),

     path('comments/', views.CommentsView.as_view(), name='comments'),


]
