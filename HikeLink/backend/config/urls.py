"""
URL configuration for config project.

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
from django.conf import settings
from django.conf.urls.static import static
# Import que permite iniciar sesion con JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from django.views.generic import TemplateView

class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html")),

    path('admin/', admin.site.urls),
    path('api/', include('hikelink_app.urls')), # Cualquier llamada a la API se delega al urls.py de hikelink_app

    # AllAuth se usa internamente por dj_rest_auth
    path('accounts/', include('allauth.urls')),

    # Ruta de Google
    path('api/auth/google/', GoogleLoginView.as_view(), name='google_login'),
]

# Funciona SOLO en desarrollo (no en producción)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)