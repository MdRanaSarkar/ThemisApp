from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm #add this
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import User, UserProfile
# Create your views here.

def UserSignin(request):
    context = {}
    return render(request, 'UserInfo/signin_page.html', context=context)


def UserSignup(request):
    context = {}
    return render(request, 'UserInfo/registerpage.html', context=context)

def LoginFunc(request):
    if request.method == 'POST':
        print("login")
        email = request.POST.get('email')
        pass1 = request.POST.get('password')
        print(email, pass1)
        user = authenticate(request, email=email, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('userDashbord')
        else:
            messages.error(request, "Invalid information.Check passoword or Email ")
            return redirect('signin')
    return render(request, 'UserInfo/signin_page.html')


def SignUpFunc(request):
    if request.method == 'POST':
        print("signup ")
        firstname = request.POST.get('firstname')
        lastname  = request.POST.get('lastname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        phonenumber = request.POST.get('phonenumber')
        userdesignation = request.POST.get('userdesignation')
        gender = request.POST.get('inlineRadioOptionsGender')

        print(firstname, lastname, email, password1, password2, phonenumber, userdesignation, gender)
        
        if password1 != password2:
            messages.error(request, "Your Password is incorrect ")
        else:            
            user = User.objects.create_user(
            first_name = firstname,
            last_name = lastname,
            username = firstname,
            email = email,
            password = password1 )
            userprofile = UserProfile()
            userprofile.user_id = user.id
            userprofile.phone_number =  phonenumber
            userprofile.designation =  userdesignation
            userprofile.usergender =  gender
            userprofile.save()
            #user.refresh_from_db()
            user  = authenticate(request, email=email, password=password1)
            if user is not None:
                login(request, user)
                return redirect('userDashbord')
            else:
                messages.error(request, "Invalid information.Check passoword or Email ")
 
    return render(request, 'UserInfo/registerpage.html')

def LogoutFun(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("home")
    

@login_required(login_url='signin')
def UserDashbord(request):
    context = {}
    return render(request, 'UserDashbord/HomePage.html', context=context)