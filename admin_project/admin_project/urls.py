"""
URL configuration for admin_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from hospital_app.api import router 

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('admin_app/', include('admin_app.urls')), 
    path('api/accounts/', include('accounts.urls')),
    path('api/otp/', include('otp_app.urls')),
    path('api/treatment/', include(router.urls)),
    path('api/slot/', include('slot_app.urls')),  
    path('api/web/',include("webinar_app.urls")),
    path('api/intro/',include("introduction_app.urls")),
    path('api/reviews/', include('hospital_reviews.urls')),
    path('api/doctors/', include('doctors_reviews.urls')),
    path('api/permission/',include("permission_app.urls")),
    



]
