"""
URL configuration for Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from .views import home,index, RegisterView,logout_view
from .import views

urlpatterns = [
    path('', home, name='users-home'),
    path('profile/', views.home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile1/', views.profile, name='users-profile'),
    path('Deploy_8/',views.Deploy_8,name='Deploy_8'),
    path('Deploy_9/',views.Deploy_9,name='Deploy_9'),
    path('Database/',views.Database,name='Database'),
    path('Basic/',views.Basic,name='Basic'),
    path('ML_DB/',views.ML_DB,name='ML_DB'),
    path('profile_list/',views.profile_list,name='profile_list'),
    path('Metrics/',views.Metrics,name='Metrics'),
    path('logout_view/',logout_view,name='logout_view'),   
    
]
