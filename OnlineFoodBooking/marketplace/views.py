from django.shortcuts import render,redirect
from vendor.models import Vendor,OpeningHour
from menu.models import Category, Fooditem
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.http import HttpResponse,JsonResponse
from .models import Cart
from .context_processors import get_cart_counter, get_cart_amounts
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime as dt
from datetime import date
from orders.forms import OrderForm
from accounts.models import UserProfile
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

    opening_hours = OpeningHour.objects.filter(vendor=vendor).order_by('day','-from_hours')

    # CHECK CURRENT DAYS OPENING HOURS
    today_date= date.today()
    today = today_date.isoweekday()
    current_opening_hours = OpeningHour.objects.filter(vendor=vendor, day = today)


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
        'opening_hours': opening_hours,
        "current_opening_hours":current_opening_hours,

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
                    return JsonResponse({'status':"Success","mssage":"Increase the cart Quantity",'cart_counter':get_cart_counter(request),'qty':chkCart.quantity,'cart_amounts':get_cart_amounts(request)})
                except:
                    chkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status':"Success","message":"Addes the food to the cart",'qty':chkCart.quantity,'cart_counter':get_cart_counter(request),"cart_amount":get_cart_amounts(request),'cart_amounts':get_cart_amounts(request)})

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

                    return JsonResponse({'cart_amounts':get_cart_amounts(request),'status':"Success","message":"Increase the cart Quantity",'cart_counter':get_cart_counter(request),'qty':chkCart.quantity})
                except:
                    # chkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'cart_amounts':get_cart_amounts(request),'status':"Success","message":"you dont have item in your cart",'cart_counter':get_cart_counter(request)})

            except:
                return JsonResponse({'status':"Failed","message":"This Fooditem is not available"})

        else:
            return JsonResponse({'status':"Failed","message":"Invalid Request"})
    else:
        return JsonResponse({'status':"login_required","message":"Login to continue"})


@login_required(login_url='/login')
def cart(request):
    cart_items = Cart.objects.filter(user = request.user).order_by('created_at')
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
                    return JsonResponse({"status":"success","message":"cart item has been deleted",'cart_amounts':get_cart_amounts(request), "cart_counter":get_cart_counter(request)})
            except:
                    return JsonResponse({"status":"failed","message":"cart item does not exist"})
        else:
            return JsonResponse({"status":"failed","message":"invalid request"})


def search(request):
    address = request.GET.get('address')
    latitude = request.GET.get('lat')
    longitude = request.GET.get('lng')
    radius = request.GET.get('radius')
    keyword= request.GET.get('keyword')

    # get vendor ids that has the fooditem the user is looking for

    fetch_vendors_by_fooditem = Fooditem.objects.filter(food_title__icontains=keyword, is_available=True).values_list('vendor',flat=True)
    vendors  = Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditem) | Q(vendor_name__icontains =keyword, is_approved = True, user__is_active=True))
    vendor_count = vendors.count()
    context = {
        "vendor_count" : vendor_count,
        "vendors" : vendors,
    }

    return render(request, 'marketplace/listings.html', context=context)

@login_required(login_url='/login')
def checkout(request):
    cart_items = Cart.objects.filter(user = request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0 :
        return redirect('marketplace')
    user_profile = UserProfile.objects.get(user=request.user)
    default_value = {
        'first_name':request.user.first_name,
        'last_name':request.user.last_name,
        'phone': request.user.phone_number,
        'email':request.user.email,
        'address':user_profile.address,
        'country':user_profile.country,
        'state':user_profile.state,
        'city':user_profile.city,
        'pin_code':user_profile.pin_code,
    }
    form = OrderForm(initial=default_value)
    context = {
        'form' : form,
        'cart_items' :cart_items,
        'cart_count' : cart_count,
    }
    return render(request, 'marketplace/checkout.html',context=context)