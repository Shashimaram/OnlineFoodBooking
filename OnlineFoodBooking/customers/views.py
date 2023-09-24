from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.forms import UserProfileForm,UserInfoform
from accounts.models import UserProfile
from django.contrib import messages



# Create your views here.
@login_required(login_url='accounts:login')
def cprofile(request):
    profile = get_object_or_404(UserProfile,user= request.user)

    if request.method == 'POST':
        profile_form  =  UserProfileForm(request.POST,request.FILES,instance=profile)
        user_form = UserInfoform(request.POST,instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, "Profile has updated successfully")
            return redirect('customers:cprofile')
    else:
        profile_form  =  UserProfileForm(instance=profile)
        user_form = UserInfoform(instance=request.user)




    context = {
        'profile_form': profile_form,
        'user_form': user_form,
        'profile': profile,
    }

    return render(request,template_name='customers/cprofile.html',context=context)
