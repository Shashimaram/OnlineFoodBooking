from django.shortcuts import render,redirect
from .models import User
from django.shortcuts import HttpResponse
from .forms import UserForm
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
                user = myform.save(commit=False)
                user.set_password(request.POST.get('password'))
                user.role = User.CUSTOMER
                myform.save()
                print("form data saved successfully")
                return redirect('accounts:registerUser')
            else:
                print('Some thing went wrong')
                print("Something went wrong")
                print(myform.errors)

        except Exception as e:
            print(f"error{e}")

    return render(request, template_name='accounts/registration.html', context={'form': form})