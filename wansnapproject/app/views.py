from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.models import User
from .forms import SignupForm


def index(request):
    return render(request, 'portfolio/index.html')

def login_view(request):
    form = LoginForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'メールアドレスまたはパスワードが間違っています')
       
    return render(request, 'app/login.html', {'form':form})

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_date['password']
            user.set_password(password)
            user.save()
            login(request.user)
            return redirect('home')
        else:
            form =SignupForm()
        
        return render(request, 'app/signup.html', {'form':form})