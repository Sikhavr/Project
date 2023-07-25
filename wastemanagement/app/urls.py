"""
URL configuration for wastemanagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('',views.home,name='home'),
    path('userhome',views.userhome,name='userhome'),
    path('driverhome',views.driverhome,name='driverhome'),
    path('admin_home',views.admin_home,name='admin_home'),
    path('admin_login/',views.admin_login,name='admin_login'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('user_reg/',views.user_signup,name='user_reg'),
    path('driver_reg/',views.driver_signup,name='driver_reg'),
    path('user_login/',views.user_login,name='user_login'),
    path('driver_login/',views.driver_login,name='driver_login'),
    path('dustbin_table/', views.dustbin_table, name='dustbin_table'),
    path('save_dailywaste/',views.save_dailywaste,name='save_dailywaste'),
    path('dailywaste_table/',views.dailywaste_table,name='dailywaste_table'),
    path('driver_location/',views.driver_location,name='driver_location'),
    path('complaint_register/',views. user_complaint, name='complaint_register'),
    path('complaint_success/',views. complaint_success, name='complaint_success'),
    path('driver_messages/', views.driver_messages, name='driver_messages'),
    path('driver_home/', views.driver_home, name='driver_home'),
    path('compliant_search/',views.compliant_search,name='compliant_search'),
    path('driver_list/',views.driversignup_list, name='driver_list'),
    path('user_list/',views.user_list,name='user_list'),
    path('update_status/',views.update_status,name='update_status'),
    path('view_complaint_status',views.view_complaint_status,name='view_complaint_status')

]
