from django.shortcuts import render, redirect
from .models import User, UserProfile
from django.shortcuts import HttpResponse
from .forms import UserForm
from vendor.forms import VendorForm
from django.contrib import messages
from django.contrib import auth
from .utils import detectUser
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
from .utils import send_verification_email,send_password_reset_email
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

# Create your views here.

# def registerUser(request):
#     return render(request, 'accounts/registration.html')


#Restrict the  vendor from accessing customer page

def check_role_vendor(user):
    if user.role ==1:
        return True
    else:
        raise PermissionDenied

# Restrict the Customer from accessing Vendor pages
def check_role_customer(user):
    if user.role ==2:
        return True
    else:
        raise PermissionDenied


def registerUser(request):
    form = UserForm()
    if request.user.is_authenticated:
        messages.warning(request, 'User is already logged in!')
        return redirect('accounts:myaccount')

    elif request.method == 'POST':
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
                user = User.objects.create(
                    first_name=frist_name, last_name=last_name, username=username, email=email, password=password)
                user.role = User.CUSTOMER
                user.save()

                #  Send Verification Email
                mail_subject = 'please activate your account'
                email_template='accounts/email/account_verification_email.html'
                send_verification_email(request,user, mail_subject,email_template)

                print("user data saved successfully")
                messages.success(request, "User data saved successfully")
                return redirect('accounts:registerUser')
            else:
                print("Something went wrong")
                print(myform.errors)
                messages.error(request, "Something went wrong")
                return render(request, template_name='accounts/registration.html', context={'form': myform})

        except Exception as e:
            print(f"error{e}")

    return render(request, template_name='accounts/registration.html', context={'form': form})


def registerVendor(request):
    form = UserForm()
    vform = VendorForm()
    if request.user.is_authenticated:
        messages.warning(request, 'User is already logged in!')
        return redirect('accounts:myaccount')

    if request.method == 'POST':
        myform = UserForm(request.POST)
        vform = VendorForm(request.POST, request.FILES)
        if myform.is_valid() and vform.is_valid():
            first_name = myform.cleaned_data['first_name']
            last_name = myform.cleaned_data['last_name']
            username = myform.cleaned_data['username']
            email = myform.cleaned_data['email']
            password = myform.cleaned_data['password']
            user = User.objects.create_user(
                first_name=first_name, last_name=last_name, username=username, email=email, password=password,)
            user.role = User.VENDOR
            user.save()
            vendor = vform.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            #  Send Verification Email
            mail_subject = 'please activate your account'
            email_template='accounts/email/account_verification_email.html'
            send_verification_email(request,user, mail_subject, email_template)
            messages.success(
                request, 'Your account has been created successfully, Please wait for your Approval')
            return redirect('accounts:registerVendor')
        else:
            print(form.errors)
            print(vform.errors)

    return render(request, template_name='accounts/registerVendor.html', context={'form': form, 'vform': vform})

def activate(request,uidb64, token):
    #Activate the user
    try:
        uid=urlsafe_base64_decode(uidb64)
        user =User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user =None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,'Congratulations! Your account is activated and varified.')
        return redirect('accounts:myaccount')
    else:
        messages.error(request,'invalid token or activatation link')
        return redirect('accounts:myaccount')





def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'User is already logged in!')
        return redirect('accounts:myaccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'you are logged in successfully')
            return redirect('accounts:myaccount')
        else:
            messages.error(request, 'invalid email or password')

            return redirect('accounts:login')

    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    messages.info(request, 'you are logged out successfully')
    return redirect('accounts:login')


@login_required(login_url='accounts:login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)


@login_required(login_url='accounts:login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, 'accounts/custDashboard.html')


@login_required(login_url='accounts:login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')


def forgot_password(request):
    if request.method == 'POST':
        email =  request.POST.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email__exact=email)

            #send reset password
            mail_subject = "Reset your password"
            email_template='accounts/emails/reset_password_email.html'
            send_password_reset_email(request, user, mail_subject, email_template)
            messages.success(request, 'password reset link has been sent to your email address successfully')
            return redirect('accounts:login')
        else:
            messages.error(request,'account doesnot exist')
            return redirect('accounts:forgot_password')


    return render(request, 'accounts/forgot_password.html')

def reset_password_validate(request, uidb64, token):
#Validate the password decode the token and user pk
    try:
        uid=urlsafe_base64_decode(uidb64)
        user =User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user =None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid']=uid
        messages.info(request,'please reset your password')
        return redirect('accounts:reset_password')
    else:
        messages.error(request,'please reset your password')
        return redirect('accounts:myaccount')





    pass

def reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password == confirm_password:
            pk =  request.session.get('uid')
            user= User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active=True
            user.save()
            messages.success(request,'password reset successful')
            
        else:
            messages.error(request, 'password doesnot match')
            return redirect('reset_password')
        
    return render(request, 'accounts/reset_password.html')
