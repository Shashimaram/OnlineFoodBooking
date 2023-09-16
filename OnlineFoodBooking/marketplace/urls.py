from django.urls import path,include
from . import views

urlpatterns = [
    path("", views.marketplace, name="marketplace"),

    path('<slug:vendor_slug>',views.vendor_detail,name="vendor_detail"),


    #ADD TO CART
    path("add_to_cart/<int:item_id>/", views.add_to_cart, name="add_to_cart"),

    # Decreasing Item from the cart
    path("decrease_cart/<int:item_id>" , views.decrease_cart, name="decrease_cart"),

    # Deleting Item from the cart
    path("delete/<int:cart_id>",views.delete_cart, name="delete_cart"),

]
