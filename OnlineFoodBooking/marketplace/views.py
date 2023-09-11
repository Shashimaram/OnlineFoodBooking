from django.shortcuts import render
from vendor.models import Vendor
# Create your views here.

def marketplace(request):
    vendor= Vendor.objects.filter(is_approved=True,user__is_active=True)[:8]
    vendor_count= vendor.count()
    context ={"vendors":vendor, "vendor_count":vendor_count}

    return render(request, 'marketplace/listings.html',context=context)