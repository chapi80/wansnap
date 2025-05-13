from django.urls import path
from . import views

urlpatterns = [
    path('portfolio/', views.index, name='index'),
    path('login/', views.login_view, name='login'),
]
