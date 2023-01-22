#from datetime import timedelta
from time import timezone
import datetime
from django.db import connection
from django.conf import settings

from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
##from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, QuickCreateForm, UserLoginForm, NOT_SC_UserLoginForm, NOT_SC_UserRegisterForm, \
    NOT_SC_QuickCreateForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from Comunication_LTD.models import NS_user
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm



# Create your views here.

# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('password_change')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = PasswordChangeForm(request.user)
#     return render(request, 'users/password_change.html', {'form': form})


# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         u = User.objects.get(username__exact=username)
#         if u is not None:
#             hashPassword = check_password(password, u.password)
#             if hashPassword: #is not None:
#                 login(request, u)
#                 return redirect('profile')
#             else:
#                 messages.info(request, 'Username OR password is incorrect')
#         else:
#             messages.info(request, 'Username OR password is incorrect')
#
#     form = UserLoginForm()
#     return render(request, 'users/login.html', {'form':form})



########

def check_admin(user):
   return user.is_superuser


#############     START:     FOR Not Secure Version        #############
def NOT_SC_login(request):
    if request.method == 'POST':
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')
        query = "SELECT * FROM Comunication_LTD_ns_user WHERE password = '"+password_input+"' AND username = '"+username_input+"'"
        cursor = connection.cursor()
        a = None
        try:
            cursor.execute(query)
            a = cursor.fetchall()
            username = a[0][1]
            password = a[0][2]
            user = authenticate(username=username, password=password)
            login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
            print(a)
            print(query)
            return redirect('profile')

        except:
            messages.info(request, 'Username OR password is incorrect')
            print(query)
            print(a)

        else:
            messages.info(request, 'Username OR password is incorrect')

    form = NOT_SC_UserLoginForm()
    return render(request, 'users/login.html', {'form':form})

def NOT_SC_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        if password1 == password2:
            user = User.objects.create_user(username, email, password1)
            user.save()
            NSuser = NS_user(user.id, username=username, password=password1, email=email)
            NSuser.save()
            messages.success(request, 'Your account has been created. You are now able to log in.')
            return redirect('login')
        else:
            messages.error(request, "Passwords don't match.")

    form = NOT_SC_UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})






@user_passes_test(check_admin)
def NOT_SC_quickUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        email = request.POST.get('email')
        user = User.objects.create_user(username, email, password)
        user.save()

        NSuser = NS_user(user.id, username=username, password=password, email=email)
        NSuser.save()
        messages.success(request, 'Account ' + ' ' + username + ' has been created.')
        return redirect('system')
    else:
        form = NOT_SC_QuickCreateForm()
    return render(request, 'users/quick_user.html', {'form':form})

#############     END:     FOR Not Secure Version        #############



#########################################################################
#########################################################################
#########################################################################



############     START:     FOR Secure Version        #############
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            #update_session_auth_hash(request, user)
            #username = form.cleaned_data.get('username')
            messages.success(request, 'Your account has been created. You are now able to log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})


@user_passes_test(check_admin)
def quickUser(request):
    if request.method == 'POST':
        form = QuickCreateForm(request.POST)
        if form.is_valid():
            form.save()
            #update_session_auth_hash(request, user)
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account ' + ' ' + username + ' has been created.')
            return redirect('system')
    else:
        form = QuickCreateForm()
    return render(request, 'users/quick_user.html', {'form':form})


#############     END:     FOR Secure Version        #############



@login_required
def profile(request):
    return render(request, 'users/profile.html')


@user_passes_test(check_admin)
def system(request):
    context = {
        'users': User.objects.all().order_by('-id')
    }
    return render(request, 'users/system.html', context)



