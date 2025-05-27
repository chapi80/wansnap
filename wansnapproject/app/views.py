from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, update_session_auth_hash
from .forms import LoginForm, SignupForm, DogForm, EmailChangeForm, PostForm
from .models import Post, Dog, Favorite
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.forms import PasswordChangeForm



def index(request):
    return render(request, 'portfolio/index.html')

def login_view(request):
    login_form = LoginForm(request.POST or None)
    
    if request.method == 'POST':
        if login_form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                login_form.add_error(None, 'メールアドレスまたはパスワードが間違っています')
       
    return render(request, 'app/login.html', {'login_form':login_form})

def signup_view(request):
    if request.method == 'POST':
        user_form = SignupForm(request.POST)
        dog_form = DogForm(request.POST, request.FILES)

        
        if user_form.is_valid() and dog_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data['password']
            user.set_password(password)
            user.save()
            
            dog = dog_form.save(commit=False)
            dog.owner = user
            dog.save()
            
            login(request, user)
            return redirect('home')
    else:
        user_form = SignupForm()
        dog_form = DogForm()
        
    return render(request, 'app/signup.html', {
        'user_form': user_form,
        'dog_form': dog_form,
    })
    
@login_required
def home_view(request):
    sort_order = request.GET.get('sort','new')
    
    if sort_order == 'old':
        posts = Post.objects.all().order_by('created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')
        
    context = {
        'posts':posts,
        'sort_order':sort_order,
    }
    
    return render(request, 'app/home.html', context)

@login_required
def mypage_view(request):
    return render(request, 'app/mypage.html')

@login_required
def dog_detail_view(request, dog_id):
    dog = get_object_or_404(Dog, id=dog_id)
    posts = Post.objects.filter(dog=dog)
    
    sort_order = request.GET.get('sort','new')
    
    if sort_order == 'old':
        posts = Post.objects.all().order_by('created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')
    
    q = request.GET.get('q')
    if q:
        try:
            year, month = map(int, q.split('-'))
            posts = posts.filter(created_at__year=year, created_at__month=month)
        except:
            pass
    
    return render(request, 'app/dog_detail.html', {
        'dog':dog,
        'posts':posts,
        'request':request,
    })
    
@login_required
def favorite_list_view(request):
    favorites = Post.objects.filter(favorite_users=request.user)
    return render(request, 'app/favorite.html', {'posts':favorites})

@login_required
def add_dog_view(request):
    if request.method == 'POST':
        dog_form = DogForm(request.POST, request.FILES)
        if dog_form.is_valid():
            dog = dog_form.save(commit=False)
            dog.owner = request.user
            dog.save()
            return redirect('home')
    else:
        dog_form = DogForm()
    
    return render(request, 'app/add_dog.html', {'dog_form':dog_form})

@login_required
def edit_dog_view(request, dog_id):
    dog = get_object_or_404(Dog, id=dog_id, owner=request.user)
    
    if request.method == 'POST':
        dog_form = DogForm(request.POST, request.FILES, instance=dog)
        if dog_form.is_valid():
            dog_form.save()
            return redirect('dog_detail', dog_id=dog.id)
    else:
        dog_form = DogForm(instance=dog)
        
    return render(request, 'app/edit_dog.html', {'dog_form':dog_form, 'dog':dog})

@login_required
def edit_user_email_view(request):
    if request.method == 'POST':
        email_form = EmailChangeForm(request.POST, instance=request.user)
        if email_form.is_valid():
            email_form.save()
            return redirect('home')
    else:
        email_form = EmailChangeForm(instance=request.user)
    return render(request, 'app/edit_user_email.html',{
        'user_form':email_form,
        })
    
@login_required
def edit_user_password_view(request):
    if request.method == 'POST':
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            return redirect('home')
    else:
        password_form = PasswordChangeForm(user=request.user)
        
    return render(request, 'app/edit_user_password.html', {
        'form':password_form
    })

@login_required
def create_post_view(request):
    if request.method == 'POST':
        create_post_form = PostForm(request.POST, request.FILES, user=request.user)
        if create_post_form.is_valid():
            post = create_post_form.save(commit=False)
            post.save()
            return redirect('home')
    else:
        create_post_form = PostForm(user=request.user)
    
    return render(request, 'app/create_post.html',{
        'create_post_form':create_post_form,
    })