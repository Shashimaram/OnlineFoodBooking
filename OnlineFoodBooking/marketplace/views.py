from django.shortcuts import render
from vendor.models import Vendor
from menu.models import Category, Fooditem
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
# Create your views here.

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