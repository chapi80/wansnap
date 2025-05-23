from django.urls import path
from . import views

urlpatterns = [
    path('portfolio/', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.home_view, name='home'),
    path('mypage/', views.mypage_view, name='mypage'),
    path('dog/<int:dog_id>/', views.dog_detail_view, name='dog_detail'),
    path('favorite/', views.favorite_list_views, name='favorite_list'),
    
]
