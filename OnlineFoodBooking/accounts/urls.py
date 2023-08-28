from django.urls import path, include
from . import views


app_name = 'accounts'


urlpatterns = [
    path('',views.myAccount, name='myAccount'),
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerVendor/', views.registerVendor,name='registerVendor'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('myaccount/', views.myAccount, name='myaccount'),
    path('custdashboard/', views.custDashboard, name='custDashboard'),
    path('vendordashboard/', views.vendorDashboard, name='vendorDashboard'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    #Password reset paths
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('vendor/', include('vendor.urls',namespace='vendor')),

]