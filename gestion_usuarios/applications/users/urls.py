from django.urls import URLPattern, path, include
from . import views

app_name = 'users_app'

urlpatterns = [
    path('register/',views.UserRegisterView.as_view(), name='user_register'),
    path('login/',views.LoginUser.as_view(), name='user_login'),
    path('logout/',views.LogoutView.as_view(), name='user_logout'),
    path('update/password/',views.UpdatePassword.as_view(), name='user_update_password'),
    path('user-verification/<pk>/',views.CodeVerificationView.as_view(), name='user_verification'),
]