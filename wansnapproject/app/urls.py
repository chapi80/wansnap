from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('portfolio/', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.home_view, name='home'),
    path('mypage/', views.mypage_view, name='mypage'),
    path('dog/<int:dog_id>/', views.dog_detail_view, name='dog_detail'),
    path('favorite/', views.favorite_list_view, name='favorite_list'),
    path('add_dog/', views.add_dog_view, name='add_dog'),
    path('dog/<int:dog_id>/edit/', views.edit_dog_view, name='edit_dog'),
    path('edit_user_email/', views.edit_user_email_view, name='edit_user_email'),
    path('edit_user_password/', views.edit_user_password_view, name='edit_user_password'),
    path('create_post/', views.create_post_view, name='create_post'),
    path('edit_post/<int:post_id>/', views.edit_post_view, name='edit_post'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('post/<int:post_id>/delete/', views.delete_post_view, name='delete_post'),
]
