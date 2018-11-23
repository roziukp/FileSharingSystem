from django.conf.urls import url
from . import views
from django.urls import path


urlpatterns = [
    path('', views.task_collection, name='tasks_collection'),
    path('', views.Login.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    url(r'^registration/$', views.Registration.as_view(), name='registration'),
    path('chatroom/', views.registered_users, name='registered_users'),
    url(r'^add-new-task/$', views.AddTask.as_view(), name='add_new_task'),
    url(r'^chatroom/(?P<task_id>.+)/$', views.add_reply, name='add_reply')

]



