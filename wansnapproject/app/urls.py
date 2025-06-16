from django.urls import path,reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView


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
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
    path('post/<int:post_id>/delete/', views.delete_post_view, name='delete_post'),
    path('toggle_favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('is_favorited/', views.is_favorited, name='is_favorited'),
    path('dog/<int:dog_id>/delete/', views.delete_dog, name='delete_dog'),
]
