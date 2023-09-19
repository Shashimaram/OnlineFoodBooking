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
    path("menu-builder/category/<int:pk>/",views.fooditems_by_category, name="fooditems_by_category"),

    # Category CRUD
    path("menu-builder/category/add/",views.add_category, name="add_category"),
    path("menu-builder/category/edit/<int:pk>/",views.edit_category, name="edit_category"),
    path("menu-builder/category/delete/<int:pk>/",views.delete_category, name="delete_category"),

    # Fooditems CRUD
    path('menu-builder/food/add/',views.add_food, name='add_food'),
    path("menu-builder/food/edit/<int:pk>/",views.edit_food, name="edit_food"),
    path("menu-builder/food/delete/<int:pk>/",views.delete_food, name="delete_food"),

    # Opening Hours

    path("opening-hours/",views.opening_hours, name="open_hours"),
    path("opening-hours/add/",views.add_opening_hours, name="add_open_hours"),



]