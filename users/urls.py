from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from config.utils import generate_new_password
from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, UserListView, UserBlockView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/genpassword/', generate_new_password, name='generate_new_password'),
    path('users/all/register/', UserListView.as_view(), name='all_users_register'),
    path('<int:pk>/block/', UserBlockView.as_view(), name='user_block')
]
