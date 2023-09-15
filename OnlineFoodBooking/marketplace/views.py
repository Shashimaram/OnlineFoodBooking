from django.shortcuts import render
from vendor.models import Vendor
from menu.models import Category, Fooditem
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.http import HttpResponse,JsonResponse
from .models import Cart
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

    context={
        "vendor_slug":vendor_slug,
        "vendor":vendor,
        "categories":categories,
        "fooditem":fooditem,
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
                    return JsonResponse({'status':"Success","mssage":"Increase the cart Quantity"})
                except:
                    chkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status':"Success","mssage":"Addes the food to the cart"})

            except:
                return JsonResponse({'status':"Failed","mssage":"This Fooditem is not available"})

        else:
            return JsonResponse({'status':"Failed","mssage":"Invalid Request"})
    else:
        return JsonResponse({'status':"Failed","mssage":"Login to continue"})