from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, update_session_auth_hash
from .forms import LoginForm, SignupForm, DogForm, EmailChangeForm, PostForm,DogFormSet
from .models import Post, Dog, Favorite
from django.db.models import Q, F, ExpressionWrapper, fields
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import modelformset_factory
from django.contrib import messages
from django.http import JsonResponse
from datetime import date
from dateutil.relativedelta import relativedelta
import re

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
        dog_formset = DogFormSet(request.POST, request.FILES)
        
        if user_form.is_valid() and dog_formset.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data.get('password1')
            if password:
                user.set_password(password)
            user.is_active = True
            user.save()
            
            for dog_form in dog_formset:
                if dog_form.cleaned_data and not dog_form.cleaned_data.get('DELETE', False):
                    dog = dog_form.save(commit=False)
                    dog.owner = user
                    dog.save()          
                       
            login(request, user)
            return redirect('home')

    else:
        user_form = SignupForm()
        dog_formset = DogFormSet(queryset=Dog.objects.none())
        
    return render(request, 'app/signup.html', {
        'user_form': user_form,
        'dog_formset': dog_formset,
    })
    
@login_required
def home_view(request):
    query = request.GET.get('q')
    sort = request.GET.get('sort','new')
    
    posts = Post.objects.all()
    total_months = None
    
    if query:
        month_match = re.search(r'(?:(\d+)\s*[歳才]?)?\s*(\d+)\s*[かヶケカヵ]?月', query)
        
        if month_match:
            years = int(month_match.group(1)) if month_match.group(1) else 0
            months = int(month_match.group(2))
            total_months = years * 12 + months
        
    if total_months is not None:
        posts = posts.filter(dog__birthday__isnull=False)
        posts = [
            post for post in posts
            if post.dog.age_months is not None and abs(post.dog.age_months - total_months) <= 1
        ]
    
    elif query: 
        base_filter = (
            Q(dog__breed__icontains=query) |
            Q(dog__dog_name__icontains=query) |
            Q(caption__icontains=query)
        )       
        posts = posts.filter(base_filter)
    
    if sort == 'old':
        posts = sorted(posts, key=lambda x: x.created_at)
    else:
        posts = sorted(posts, key=lambda x: x.created_at, reverse=True)
        
    context = {
        'posts': posts,
        'query': query,
        'sort': sort,
    }
    
    return render(request, 'app/home.html', context)

@login_required
def mypage_view(request):
    dogs = Dog.objects.filter(owner=request.user)
    return render(request, 'app/mypage.html', {'dogs':dogs})

@login_required
def dog_detail_view(request, dog_id):
    dog = get_object_or_404(Dog, id=dog_id, owner=request.user)
    posts = Post.objects.filter(dog=dog)
    
    sort_order = request.GET.get('sort','new')
    q = request.GET.get('q')
    
    posts = Post.objects.select_related('dog').filter(dog=dog)
    
    if sort_order == 'old':
        posts = posts.order_by('created_at')
    else:
        posts = posts.order_by('-created_at')
    
    if q:
        try:
            year, month = map(int, q.split('-'))
            posts = posts.filter(created_at__year=year, created_at__month=month)
        except ValueError:
            pass
    
    for post in posts:
        post.is_own = (post.dog.owner == request.user)
        
    if dog.birthday:
        today = date.today()
        diff = relativedelta(today, dog.birthday)
        if diff.years == 0:
            age_display = f"{diff.months}ヶ月"
        else:
            age_display = f"{diff.years}歳{diff.months}ヶ月"
    else:
        age_display = "不明"
    
    
    dog_breed = dog.breed
    dog_gender = dog.gender
    dog_birthday = dog.birthday
    dog_biography = dog.biography
    
    return render(request, 'app/dog_detail.html', {
        'dog':dog,
        'posts':posts,
        'dog_breed':dog_breed,
        'dog_gender':dog_gender,
        'dog_birthday':dog_birthday,
        'dog_biography':dog_biography,
        'dog_age_months':age_display,       
        'request':request,
    })
    
@login_required
def favorite_list_view(request):
    favorite_posts = Post.objects.filter(favorites__user=request.user).order_by('-created_at')
    return render(request, 'app/favorite.html', {'favorites':favorite_posts})

@login_required
def toggle_favorite(request):
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, post=post)
        
        if not created:
            favorite.delete()
            return JsonResponse({'status': 'removed'})
        else:
            return JsonResponse({'status': 'added'})

@login_required
def is_favorited(request):
    if request.method == "GET":
        post_id = request.GET.get('post_id')
        
        if not post_id or not post_id.isdigit():
            return JsonResponse({'error': 'Invalid post_id'}, status=400)
        
        post = get_object_or_404(Post, id=post_id)
        is_fav = Favorite.objects.filter(user=request.user, post=post).exists()
        return JsonResponse({'is_favorited': is_fav})
    
@login_required   
def add_dog_view(request):
    if request.method == 'POST':
        dog_form = DogForm(request.POST, request.FILES)
        if dog_form.is_valid():
            dog = dog_form.save(commit=False)
            dog.owner = request.user
            dog.save()
            return redirect('mypage')
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
            messages.success(request, f'{dog.dog_name}の情報を変更しました')
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
            messages.success(request, 'メールアドレスを変更しました')
            return redirect('mypage')

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
            messages.success(request, 'パスワードを変更しました')
            return redirect('mypage')
    else:
        password_form = PasswordChangeForm(user=request.user)
        
    return render(request, 'app/edit_user_password.html', {
        'password_form':password_form
    })

@login_required
def create_post_view(request):
    if request.method == 'POST':
        create_post_form = PostForm(request.POST, request.FILES, user=request.user)
        
        if create_post_form.is_valid():
            dog = create_post_form.cleaned_data.get('dog')

            if not dog:
                create_post_form.add_error('dog', 'うちの子を選択してください')
            elif not request.FILES.get('image'):
                create_post_form.add_error('image', '画像を選択してください')
            else:
                post = create_post_form.save(commit=False)
                post.dog = dog
                post.dog_name = dog.dog_name
                post.breed = dog.breed
                post.gender = dog.gender
                post.birthday = dog.birthday
                post.save()
                return redirect('home')   
        
    else:
        create_post_form = PostForm(user=request.user)
    
    return render(request, 'app/create_post.html',{
        'create_post_form':create_post_form,
    })

@login_required
def edit_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, dog__owner=request.user)
    original_image = post.image
    
    if request.method == 'POST':
        edit_post_form = PostForm(request.POST, request.FILES, instance=post, user=request.user)
        if edit_post_form.is_valid():
            post = edit_post_form.save(commit=False)
            
            if not post.image:
                post.image = original_image
            
            dog = edit_post_form.cleaned_data['dog']
            post.dog = dog
            post.dog_name = dog.dog_name
            post.breed = dog.breed
            post.gender = dog.gender
            post.birthday = dog.birthday
            
            post.save()
            messages.success(request, '投稿を変更しました')
            return redirect('mypage')
    else:
        edit_post_form = PostForm(instance=post, user=request.user)
        
    return render(request, 'app/edit_post.html',{
        'edit_post_form':edit_post_form,
        'post_id':post.id,
    })

@login_required
def delete_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, dog__owner=request.user)
    
    if request.method == 'POST':
        dog_id = post.dog.id
        post.delete()
        messages.success(request, '投稿を削除しました')
        return redirect('dog_detail', dog_id=dog_id)
    
    return redirect('edit_post', post_id=post_id)

@login_required
def delete_dog_view(request, dog_id):
    dog = get_object_or_404(Dog, id=dog_id, owner=request.user)

    if request.method == "POST":
        posts = Post.objects.filter(dog=dog)
        for post in posts:
            post.dog_name = dog.dog_name
            post.breed = dog.breed
            post.gender = dog.gender
            post.birthday = dog.birthday
            post.save()
                
        dog.delete()
        messages.success(request, f'{dog.dog_name}の情報を削除しました')    
        return redirect('mypage')
    
    return redirect('mypage')
