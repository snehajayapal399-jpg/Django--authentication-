from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages  #---> MESSAGE MODULE
# messages.debug(), messages.info(), messages.success , messages.warning(), messages.error()


# Create your views here.
def signup(request):
    if request.method == 'POST':
        User.objects.create_user(

            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            username = request.POST['username'],
            password = request.POST['password'],
            
        )
        messages.success(request, 'Registration successful')
        return redirect('signin')

    return render(request,'signup.html')

def signin(request):
    if request.method == 'POST':
        user = authenticate(request, 
                            username = request.POST['username'],
                            password = request.POST['password'],
                            )
        if user:
            login(request, user)
            messages.success(request,'login Successful')

            return redirect('profile') 
        else:
            messages.warning(request,'Invalid user')
         
    return render(request,'signin.html')


@login_required(login_url='signin')
def profile(request):
    return render(request,'profile.html',{'user':request.user})

@login_required(login_url='signin')
def signout(request):
    logout(request)
    messages.success(request,'Logout Successful')
    return redirect('signin')

@login_required(login_url='signin')
def update_profile(request):
    if request.method == 'POST':

        user = request.user
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.username = request.POST['username']
        
        user.save()
        messages.success(request,'Profile updated Successfully')
        return redirect('profile')
    else:
        messages.warning(request,'Failed to upload profile')
    return render(request,'update_profile.html',{'user':request.user})

@login_required(login_url='signin')
def update_password(request):
    if request.method == 'POST':
        user = request.user   # extracting password by requesting the user
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        if not user.check_password(old_password):
            messages.error(request,'Old Password is invalid')
        elif new_password == confirm_password and new_password != old_password: # password will be in string format
            user.set_password(new_password)   # encrypting the password
            user.save()
            update_session_auth_hash(request,user)   # keep the user as login
            messages.success(request,'Password updated Successfully')
            return redirect('profile')  
        else:
            messages.error(request,'New Password and Confirm password do not match') 
    return render(request,'update_password.html',{'user':request.user})





