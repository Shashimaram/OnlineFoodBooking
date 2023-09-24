from django.urls import path
from accounts import views as AccountViews
from . import views

app_name ="customers"


urlpatterns = [
    path("",AccountViews.custDashboard,name="customer"),
    path("profile/", views.cprofile, name="cprofile")
]
