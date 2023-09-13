from django.shortcuts import render
from vendor.models import Vendor
from django.shortcuts import get_object_or_404
# Create your views here.

def marketplace(request):
    vendor= Vendor.objects.filter(is_approved=True,user__is_active=True)[:8]
    vendor_count= vendor.count()
    context ={"vendors":vendor, "vendor_count":vendor_count}

    return render(request, 'marketplace/listings.html',context=context)

def vendor_detail(request,vendor_slug):
    vendor = get_object_or_404(Vendor,vendor_slug=vendor_slug)

    context={ "vendor_slug":vendor_slug,"vendor":vendor}
    return render(request, 'marketplace/vendor_details.html', context=context)