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

from django.utils.text import slugify
# import Forms

from menu.forms import CategoryForm,FooditemForm

# Create your views here.


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


@login_required(login_url='accounts:login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor)
    context = {
        'categories': categories,

    }
    return render(request, 'vendor/menu_builder.html',context=context)

@login_required(login_url='accounts:login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category,pk=pk)
    fooditems = Fooditem.objects.filter(vendor=vendor, category=category)
    print(fooditems)
    print(category)
    context = {'fooditems':fooditems,
               'category':category,}
    return render(request, 'vendor/fooditems_by_category.html', context=context)

@login_required(login_url='accounts:login')
@user_passes_test(check_role_vendor)
def add_category(request):
    form=CategoryForm();
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name=form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            form.save() # here the category id is generated
            # category.slug = slugify(category_name)+'-'+str(category.id) # chicken-12
            category.slug = slugify(category_name) + '-' + str(category.id)  # chicken-12
            form.save() # here the category is saved again with the new slug
            messages.success(request,'Category added Successfully')
            return redirect('accounts:vendor:menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm()
    context={'form':form}
    return render(request, 'vendor/add_category.html', context=context)

@login_required(login_url='accounts:login')
@user_passes_test(check_role_vendor)
def edit_category(request,pk):
    category=get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST,instance=category)
        if form.is_valid():
            category_name=form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request,'Category added Successfully')
            return redirect('accounts:vendor:menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm(instance=category)
    context={'form':form, 'category':category}
    return render(request, 'vendor/edit_category.html', context=context)

def delete_category(request,pk):
    category=get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request,'Category deleted Successfully')
    return redirect('accounts:vendor:menu_builder')


@login_required(login_url='accounts:login')
@user_passes_test(check_role_vendor)
def add_food(request):
    form=FooditemForm();
    if request.method == 'POST':
        form = FooditemForm(request.POST,request.FILES)
        if form.is_valid():
            food_title=form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(food_title)
            form.save()
            messages.success(request,'Food item added Successfully')
            return redirect('accounts:vendor:fooditems_by_category',food.category.id)
        else:
            print(form.errors)
    else:
        form = FooditemForm()
        # Modify this form
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context={'form':form}
    return render(request, 'vendor/add_food.html', context=context)



@login_required(login_url='accounts:login')
@user_passes_test(check_role_vendor)
def edit_food(request,pk):
    food=get_object_or_404(Fooditem, pk=pk)
    if request.method == 'POST':
        form = FooditemForm(request.POST,instance=food)
        if form.is_valid():
            foodtitle=form.cleaned_data['food_title']
            food= form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(foodtitle)
            form.save()
            messages.success(request,'Category added Successfully')
            return redirect('accounts:vendor:fooditems_by_category',food.category.id)
        else:
            print(form.errors)
    else:
        form = FooditemForm(instance=food)
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context={'form':form, 'food':food}
    return render(request, 'vendor/edit_food.html', context=context)


@login_required(login_url='accounts:login')
@user_passes_test(check_role_vendor)
def delete_food(request,pk):
    food=get_object_or_404(Fooditem, pk=pk)
    food.delete()
    messages.success(request,'Category deleted Successfully')
    return redirect('accounts:vendor:menu_builder')