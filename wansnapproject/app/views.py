from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def index(request):
    return render(request, 'portfolio/index.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(redirect, 'app/login.html', {'error': 'メールアドレスまたはパスワードが間違っています'})
    
    return render(request, 'app/login.html')