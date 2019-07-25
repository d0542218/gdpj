"""GraduateProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from rest_framework.routers import DefaultRouter

from Account.views import register
from django.conf import settings
from django.conf.urls.static import static

from EsNoteScore import views

router = DefaultRouter()
router.register('esNoteScore', views.EsNoteScoreView)
router.register('esNoteScorePic',views.EsNoteScorePicView)


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('account/', include("django.contrib.auth.urls")),
    path('account/', include("Account.urls")),
    path('register/', register, name='register'),
    path('', include("Home.urls")),
    path('history/', include("History.urls")),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    # path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/v1/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
