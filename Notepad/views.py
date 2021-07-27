from django.shortcuts import render

# Create your views here.



def home(request):
    pass
    

def login(request):
    return render(request, "Notepad/login.html")
    