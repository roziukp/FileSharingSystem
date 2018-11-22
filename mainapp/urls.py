from django.conf import urls
from . import views
from django.urls import path


urlpatterns = [
    path('', views.Login.as_view(), name='login'),
    path('chatroom/', views.registered_users, name='registered_users'),
    path('add-file/', views.AddFile.as_view(), name='add_file'),
]