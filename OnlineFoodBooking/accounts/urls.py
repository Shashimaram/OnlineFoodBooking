from django.urls import path
from . import views


app_name = 'accounts'


urlpatterns = [
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerVendor/', views.registerVendor,name='registerVendor'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('myaccount/', views.myAccount, name='myaccount'),
    path('custdashboard/', views.custDashboard, name='custDashboard'),
    path('vendordashboard/', views.vendorDashboard, name='vendorDashboard'),
]