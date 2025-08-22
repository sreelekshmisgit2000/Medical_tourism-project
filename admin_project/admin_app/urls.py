from django.urls import path
from .views import admin_login_api, LogoutView


urlpatterns = [
    path('login/', admin_login_api, name='admin-login-api'),
       path('logout/', LogoutView.as_view(), name='admin-logout-api')
]
