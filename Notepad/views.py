from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, Http404
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.serializers import serialize
from .models import Notepad, Page
from json import loads
# Create your views here.



def home_view(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    elif request.is_ajax and request.method == "POST":
        data = loads(request.body)
        if 'action' not in data:
            raise Http404('Bad request!')
        action = data['action']
        
        if action == "get-notebooks":
            q = Notepad.objects.all()
            json_data = serialize("json", q)
            return JsonResponse({'notebooks': json_data})
            
        elif action == 'add-notebook':
            pass
        elif action == 'del-notebook':
            pass
        elif action == 'ren-notebook':
            pass
        elif action == 'get-pages':
            pass
        elif action == 'add-page':
            pass
        elif action == 'del-page':
            pass
        elif action == 'get-page':
            pass
        elif action == 'set-page':
            pass
    else:
        return render(request, "Notepad/home.html",
                      {'username': request.user.username})
        
    

def login_view(request):
    if request.is_ajax and request.method == "POST":
        data = loads(request.body)
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
                login(request, user)
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

