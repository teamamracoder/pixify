from django.urls import path
from . import views

urlpatterns = [
    # home
    path('', views.HomeView.as_view(), name='home'),

    # user
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('users/<int:user_id>/', views.UserDetailView.as_view(), name='user_detail'),
    path('users/<int:user_id>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('users/<int:user_id>/delete/', views.UserDeleteView.as_view(), name='user_delete'),

    # post
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/create/', views.PostCreateView.as_view(), name='post_create'),
    path('posts/<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:post_id>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:post_id>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
 
]
