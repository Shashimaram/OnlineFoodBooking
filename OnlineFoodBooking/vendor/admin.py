from django.contrib import admin
from.models import Vendor

# Register your models here.
class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'vendor_name','is_approved','created_at')



admin.site.register(Vendor, VendorAdmin)