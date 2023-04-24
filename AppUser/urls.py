from django.urls import path
from AppUser.views import (UserSignin, UserSignup, UserDashbord,
                           LoginFunc, LogoutFun, SignUpFunc)

urlpatterns = [
    path('signin/', UserSignin, name = 'signin'),
    path('signup/', UserSignup, name = 'signup'),
    path('dashbord/', UserDashbord, name = 'userDashbord'),
    path('loginfunc/', LoginFunc, name = 'loginfunc'),
    path('registerfunc/', SignUpFunc, name = 'registerfunc'),
    path('logout/', LogoutFun, name = 'LogoutFun'), 
  
]


