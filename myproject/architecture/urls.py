from django.urls import path
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('project/<int:pk>', ProjectDetail.as_view(), name='project_detail'),
    path('register', RegisterUser.as_view(), name='register'),
    path('login', MyLoginView.as_view(template_name='architecture/login.html'), name='login'),
    path('user/account/<int:pk>', UserDetail.as_view(), name='user_detail'),
    path('project/add', AddProject.as_view(), name='add_project'),
    path('modify/user/<int:pk>', UpdateUser.as_view(), name='modify_user'),
    path('like/<int:project_id>', Like.as_view(), name='like'),
    path('unlike/<int:project_id>', Unlike.as_view(), name='unlike'),
]
