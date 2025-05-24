from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignupForm, DogForm
from .models import Post, Dog, Favorite
from django.db.models import Q



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
    
    return render(request, 'app/home.html')

def mypage_view(request):
    return render(request, 'app/mypage.html')

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
    
    return render(request, 'app/dog_detail.html'), {
        'dog':dog,
        'posts':posts,
        'request':request,
    }
    
def favorite_list_view(request):
    favorites = Post.objects.filter(favorite_users=request.user)
    return render(request, 'app/favorite.html', {'posts':favorites})