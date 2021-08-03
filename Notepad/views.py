from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, Http404
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import Notepad, Page
from json import loads
# Create your views here.



def home_view(request):
    pass
    

def login_view(request):
    if request.is_ajax and request.method == "POST":
        data = loads(request.body)
        print(data)
        if "action" in data and data["action"] == "login":
            if 'username' in data and 'password' in data:
                user = authenticate(request, 
                                    username=data['username'],
                                    password=data['password'])
                if user:
                    login(request, user)
                    return JsonResponse({'res':'True'})
                else:
                    return JsonResponse({"res":'False'})
        elif 'action' in data and data['action'] == 'logout':
            if request.user.is_authenticated:
                logout(request)
                return JsonResponse({'res':'True'})
            else:
                return JsonResponse({'res':'False'})
        elif 'action' in data and data['action'] == 'signup':
            if 'username' in data and 'password' in data and 'email' in data:
                if User.objects.filter(username=data['username']).exists():
                    return JsonResponse({'res':'False', 
                                         'err':'1'})
                try:
                    validate_email(data['email'])
                except ValidationError:
                    return JsonResponse({'res':'False', 'err':'2'})
                user = User.objects.create_user(data['username'], 
                                                data['email'],
                                                data['password'])
                user.save()
                return JsonResponse({'res':'True'})
        elif 'action' in data and data['action'] == 'username_exists':
            if 'username' in data and User.objects.filter(username=data['username']).exists():
                return JsonResponse({'res':'True'})
            else:
                return JsonResponse({'res':'False'})
        raise Http404('Bad request!')
    else:    
        logged_in = False
        username = "Guest"
        if request.user.is_authenticated:
            logged_in = True
            username = request.user.username
        return render(request, 
                      "Notepad/login.html",
                      {"logged_in": logged_in,
                       "username": username})

