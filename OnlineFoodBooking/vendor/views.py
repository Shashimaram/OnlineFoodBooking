from django.shortcuts import render, get_object_or_404,redirect
from .forms import VendorForm
from accounts.models import UserProfile
from accounts.forms import UserProfileForm
from vendor.models import Vendor
from django.contrib import messages
from django.http import Http404

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

def v_profile(request):

    print(request.user)

    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        raise Http404("User profile does not exist")

    try:
        vendor = request.user.vendor
    except Vendor.DoesNotExist:
        raise Http404("Vendor does not exist")

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