from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def index(request):
    return render(request, 'portfolio/index.html')

def login_view(request):
    if request.meshod == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(redirect, 'メールアドレスまたはパスワードが間違っています')
    
    return render(request, 'app/login.html')