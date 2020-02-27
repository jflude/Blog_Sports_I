"""Blog_Sports_I URL Configuration

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
from django.views.generic.base import TemplateView
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', TemplateView.as_view(template_name='index.html')),
    path('accounts/account_logout', include('allauth.urls')),
    path('memberships/', include('apps.memberships.urls' ,namespace = "memberships")),
    path('posts/', include('apps.posts.urls', namespace = "posts")),
    path('daily_pick/', include('apps.daily_pick.urls', namespace = 'daily_picks')),
    path('hockey/', include('apps.hockey.urls', namespace = "hockey")),
    path('pro_hoops/', include('apps.pro_hoops.urls', namespace = "pro_hoops")),
    path('college_hoops/', include('apps.college_hoops.urls', namespace = "college_hoops")),
    path('baseball/', include('apps.baseball.urls', namespace = "MLB_baseball")),
]
