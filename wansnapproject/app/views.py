from django.shortcuts import render

def index(request):
    return render(request, 'portfolio/index.html')

def login_view(reqest):
    return render(reqest, 'app/login/.html')