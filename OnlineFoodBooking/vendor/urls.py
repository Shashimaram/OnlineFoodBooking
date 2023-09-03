from django.shortcuts import redirect
from django.urls import reverse, path
from . import views
from accounts import views as Accounts

# Namespaces
app_name = 'vendor'

urlpatterns = [
    path('',Accounts.vendorDashboard,name='vendorDashboard'),
    path('profile/',views.v_profile, name='profile'),
    path('menu-builder/',views.menu_builder, name='menu_builder'),
    path("menu-builder/category/<int:pk>/",views.fooditems_by_category, name="fooditems_by_category")
]