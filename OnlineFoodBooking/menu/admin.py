from django.contrib import admin
from .models import Category, Fooditem

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields ={'slug':['category_name']}
    list_display=('category_name','vendor')
    search_fields=('category_name','vendor__vendor_name')


class FooditemAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':['food_title']}
    list_display = ('food_title','category', 'vendor', 'price','is_available')
    search_fields = ('food_title','category__category_name','vendor__vendor_name')
    list_filter=('is_available',)








admin.site.register(Category, CategoryAdmin)
admin.site.register(Fooditem, FooditemAdmin)
