from django.shortcuts import render, get_object_or_404,redirect
from .forms import VendorForm
from accounts.models import UserProfile
from accounts.forms import UserProfileForm
from vendor.models import Vendor
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
from menu.models import Category,Fooditem

# Create your views here.

# def v_profile(request):
#     try:
#         profile= get_object_or_404(UserProfile,user=request.user)
#         vendor=get_object_or_404(Vendor,user=request.user)
#     except UserProfile.DoesNotExist:
#         raise Http404("User profile does not exist")

#     if request.method == 'POST':
#         profile_form = UserProfileForm(request.POST,request.FILES,instance=profile)
#         vendor_form = VendorForm(request.POST,request.FILES,instance=vendor)
#         if profile_form.is_valid() and vendor_form.is_valid():
#             print('forms updated successfully')
#             profile_form.save()
#             vendor_form.save()
#             messages.success(request,'Restaurant has been updated')
#             return redirect('accounts:vendor:profile')
#         else:
#             print(profile_form.errors)
#             print(vendor_form.errors)
#     else:
#         profile_form = UserProfileForm(instance=profile)
#         vendor_form = VendorForm(instance=vendor)
#     context={
#         'profile_form': profile_form,
#         'vendor_form': vendor_form,
#         'profile': profile,
#         'vendor': vendor,
#     }
#     return render(request, 'vendor/vprofile.html', context)


def get_vendor(request):
    vendor=Vendor.objects.get(user = request.user)
    return vendor

@login_required(login_url='accounts:login')
@user_passes_test(check_role_vendor)
def v_profile(request):

    print(request.user)

    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)

        if profile_form.is_valid() and vendor_form.is_valid():
            try:
                profile_form.save()
                vendor_form.save()
                messages.success(request, 'Profile updated!')
                return redirect('accounts:vendor:profile')
            except:
                messages.error(request, 'Error updating profile')

        else:
            print(profile_form.errors)
            print(vendor_form.errors)
            messages.error(request, 'Error updating profile')


    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)

    context = {
        'profile': profile,
        'vendor': vendor,
        'profile_form': profile_form,
        'vendor_form': vendor_form
    }

    return render(request, 'vendor/vprofile.html', context)


def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor)
    context = {
        'categories': categories,

    }
    return render(request, 'vendor/menu_builder.html',context=context)

def fooditems_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category,pk=pk)
    fooditems = Fooditem.objects.filter(vendor=vendor, category=category)
    print(fooditems)
    print(category)
    context = {'fooditems':fooditems,
               'category':category,}
    return render(request, 'vendor/fooditems_by_category.html', context=context)