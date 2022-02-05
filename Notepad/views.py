from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, Http404
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import Notepad, Page
from json import loads
# Create your views here.


def is_ajax(request):
    """
    From django 3.1 the request.is_ajax has been deprecated, so I wrote this to check if
    a reqeust is ajax or not
    """
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def home_view(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    elif is_ajax(request) and request.method == "POST" and request.user.is_authenticated:
        data = loads(request.body)
        if 'action' not in data:
            raise Http404('Bad request!')
        action = data['action']
        
        if action == "get-notebooks":
            q = Notepad.objects.filter(owner=request.user)
            result = {}
            for notepad in q:
                result[notepad.pk] = notepad.name
            return JsonResponse({"notebooks": result, "res": "True"})
            
        elif action == 'add-notebook':
            if 'name' in data:
                q = Notepad(owner=request.user, name=data['name'])
                q.save()
                return JsonResponse({'res': 'True'})
            
        elif action == 'del-notebook':
            if 'pk' in data:
                q = Notepad.objects.get(pk=data['pk'])
                if q and q.owner == request.user:
                    q.delete()
                    return JsonResponse({'res': 'True'})
                    
        elif action == 'ren-notebook':
            if 'pk' in data and 'name' in data:
                q = Notepad.objects.get(pk=data['pk'])
                if q and q.owner == request.user:
                    q.name = data['name']
                    q.save()
                    return JsonResponse({'res': 'True'})
        
        elif action == 'get-pages':
            if 'pk' in data and 'sort' in data:
                q = Notepad.objects.get(pk=data['pk'])
                if q and q.owner == request.user:
                    result = {}
                    if data['sort'] == 'Created':
                        sorting = '-date_created'
                    else:
                        sorting = '-date_modified'
                    for page in q.page_set.order_by(sorting):
                        result[page.pk] = {'title': page.title, 
                                           'created': page.date_created,
                                           'modified': page.date_modified}
                    return JsonResponse({"pages": result, "res": "True"})

        elif action == 'add-page':
            if 'pk' in data and 'name' in data:
                q = Notepad.objects.get(pk=data['pk'])
                if q and q.owner == request.user:
                    p = Page(master=q, title=data['name'], body="")
                    p.save()
                    return JsonResponse({"res": "True"})
            
        elif action == 'del-page':
            if 'pk' in data and 'pkp' in data:
                q = Notepad.objects.get(pk=data['pk'])
                p = q.page_set.get(pk=data['pkp'])
                if p and q and q.owner == request.user:
                    p.delete()
                    return JsonResponse({'res': 'True'})
                    
        elif action == 'get-page':
            if 'pk' in data and 'pkp' in data:
                q = Notepad.objects.get(pk=data['pk'])
                p = q.page_set.get(pk=data['pkp'])
                if p and q and q.owner == request.user:
                    return JsonResponse({'res': 'True', 'body': p.body})
                    
        elif action == 'set-page':
            if 'pk' in data and 'pkp' in data and 'body' in data:
                q = Notepad.objects.get(pk=data['pk'])
                p = q.page_set.get(pk=data['pkp'])
                if p and q and q.owner == request.user:
                    p.body = data['body']
                    p.save()
                    return JsonResponse({'res': 'True'})
        
        raise Http404('Bad request!')
    else:
        return render(request, "Notepad/home.html",
                      {'username': request.user.username})


def login_view(request):
    if request.method == "POST" and is_ajax(request):
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

