from django.shortcuts import render,redirect
from .models import User,UserProfile
from django.shortcuts import HttpResponse
from .forms import UserForm
from vendor.forms import VendorForm
from django.contrib import messages
# Create your views here.

# def registerUser(request):
#     return render(request, 'accounts/registration.html')

def registerUser(request):
    form = UserForm()

    if request.method == 'POST':
        myform = UserForm(request.POST)
        print(request.POST)

        try:
            if myform.is_valid():
                # user = myform.save(commit=False)
                # user.set_password(request.POST.get('password'))
                # user.role = User.CUSTOMER
                # myform.save()
                # print("form data saved successfully")

                frist_name = myform.cleaned_data['first_name']
                last_name = myform.cleaned_data['last_name']
                username = myform.cleaned_data['username']
                email = myform.cleaned_data['email']
                password = myform.cleaned_data['password']
                user = User.objects.create(first_name=frist_name, last_name=last_name, username=username, email=email, password=password)
                user.role = User.CUSTOMER
                user.save()
                print("user data saved successfully")
                messages.success(request,"User data saved successfully")
                return redirect('accounts:registerUser')
            else:
                print("Something went wrong")
                print(myform.errors)
                messages.error(request,"Something went wrong")
                return render(request, template_name='accounts/registration.html', context={'form': myform})


        except Exception as e:
            print(f"error{e}")

    return render(request, template_name='accounts/registration.html', context={'form': form})

def registerVendor(request):
    form = UserForm()
    vform =VendorForm()

    if request.method == 'POST':
        myform = UserForm(request.POST)
        vform = VendorForm(request.POST, request.FILES)
        if myform.is_valid() and vform.is_valid():
            first_name = myform.cleaned_data['first_name']
            last_name = myform.cleaned_data['last_name']
            username = myform.cleaned_data['username']
            email = myform.cleaned_data['email']
            password = myform.cleaned_data['password']
            user = User.objects.create_user(first_name = first_name, last_name = last_name,username=username,email=email, password=password,)
            user.role= User.VENDOR
            user.save()
            vendor = vform.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, 'Your account has been created successfully, Please wait for your Approval')
            return redirect('accounts:registerVendor')
        else:
            print(form.errors)
            print(vform.errors)



    return render(request, template_name='accounts/registerVendor.html' ,context={'form': form, 'vform': vform})