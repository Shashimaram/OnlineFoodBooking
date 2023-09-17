from django.shortcuts import render
from vendor.models import Vendor
from menu.models import Category, Fooditem
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.http import HttpResponse,JsonResponse
from .models import Cart
from .context_processors import get_cart_counter
from django.contrib.auth.decorators import login_required
# Create your views here.




def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def marketplace(request):
    vendor= Vendor.objects.filter(is_approved=True,user__is_active=True)[:8]
    vendor_count= vendor.count()
    context ={"vendors":vendor, "vendor_count":vendor_count}

    return render(request, 'marketplace/listings.html',context=context)

def vendor_detail(request,vendor_slug):
    vendor = get_object_or_404(Vendor,vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
       'fooditems',
            queryset=Fooditem.objects.filter(is_available=True)
        )
    )
    fooditem = Fooditem.objects.filter(vendor=vendor)

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user = request.user)
    else:
        cart_items = None

    context={
        "vendor_slug":vendor_slug,
        "vendor":vendor,
        "categories":categories,
        "fooditem":fooditem,
        "cart_items":cart_items,
        }
    return render(request, 'marketplace/vendor_details.html', context=context)

def add_to_cart(request,item_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the Food item exists
            try:
                fooditem= Fooditem.objects.get(id=item_id)
                # Check if the user has already added that food item to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status':"Success","mssage":"Increase the cart Quantity",'cart_counter':get_cart_counter(request),'qty':chkCart.quantity})
                except:
                    chkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status':"Success","message":"Addes the food to the cart",'qty':chkCart.quantity,'cart_counter':get_cart_counter(request)})

            except:
                return JsonResponse({'status':"Failed","message":"This Fooditem doesnot exist"})

        else:
            return JsonResponse({'status':"Failed","message":"Invalid Request"})
    else:
        return JsonResponse({'status':"login_required","message":" Please Login to continue"})


def decrease_cart(request,item_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the Food item exists
            try:
                fooditem= Fooditem.objects.get(id=item_id)
                # Check if the user has already added that food item to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    if chkCart.quantity > 1:
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0

                    return JsonResponse({'status':"Success","message":"Increase the cart Quantity",'cart_counter':get_cart_counter(request),'qty':chkCart.quantity})
                except:
                    # chkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status':"Success","message":"you dont have item in your cart",'cart_counter':get_cart_counter(request)})

            except:
                return JsonResponse({'status':"Failed","message":"This Fooditem is not available"})

        else:
            return JsonResponse({'status':"Failed","message":"Invalid Request"})
    else:
        return JsonResponse({'status':"login_required","message":"Login to continue"})


@login_required(login_url='/login')
def cart(request):
    cart_items = Cart.objects.filter(user = request.user)
    context={'cart_items':cart_items}
    return render(request,'marketplace/cart.html',context=context)


def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # Check if the cart item exist
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({"status":"success","message":"cart item has been deleted", "cart_counter":get_cart_counter(request)})
            except:
                    return JsonResponse({"status":"failed","message":"cart item does not exist"})
        else:
            return JsonResponse({"status":"failed","message":"invalid request"})
