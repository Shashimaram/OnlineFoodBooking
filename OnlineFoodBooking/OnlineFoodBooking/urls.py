"""
URL configuration for OnlineFoodBooking project.

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
from django.urls import path,include
from .views import home
from django.conf.urls.static import static
from django.conf import settings
from marketplace import views as marketplace_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("cart/",marketplace_views.cart, name="cart"),
    path('',home, name='home'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('marketplace/', include('marketplace.urls')),
    #search
    path("search/", marketplace_views.search, name="search"),

    path("customers/",include('customers.urls')),

    # Orders Checkout
    path('checkout/',marketplace_views.checkout, name="checkout"),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
