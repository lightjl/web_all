"""web_all URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
import moivesDownload.urls
import followXS.urls
import xjgl.urls
import smzdm.urls
import control.urls
import book.views
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
import moivesDownload.views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('control/', include('control.urls')),
    path('mv/', include('moivesDownload.urls')),
    path('xs/', include('followXS.urls')),
    path('xjgl/', include('xjgl.urls')),
    path('mmm/', include('smzdm.urls')),
    path('mebook/', book.views.CheckMeBook),
    path('mebook/zzbook/', book.views.zzbook),
    path('', moivesDownload.views.show),
    path('accounts/login/', auth_views.LoginView.as_view()),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
