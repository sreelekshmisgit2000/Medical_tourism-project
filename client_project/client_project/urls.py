"""
URL configuration for client_project project.

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
from django.urls import path,include
from django.conf import settings
from client_app.views import GlobalSearchAPIView,super_admin_login 
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/admin/', include('admin_app.urls')),  
    path("api/client_app/", include("client_app.urls")), 
    path('api/otp/', include('otp_app.urls')), # Include your app's URLs
    path("api/hospitals/", include("hospital_app.urls")),
    path("api/doctors/", include("doctor_app.urls")),
    path('', include('treatment_app.urls')),
    path('api/', include('review_app.urls')),
    
    path('api/', include('hospital_review.urls')),
    path("ckeditor5/", include("django_ckeditor_5.urls")),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('webinar_app.urls')),
    path('api/search/', GlobalSearchAPIView.as_view(), name='global-search'),
    path('api/', include('client_app.urls')),  # 👈 Make sure this line exists!
    path('super-admin-login/', super_admin_login, name='super_admin_login')
    



]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)