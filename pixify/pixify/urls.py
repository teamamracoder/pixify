from django.urls import path, include

urlpatterns = [
    path('', include('social_network.urls')),
]
