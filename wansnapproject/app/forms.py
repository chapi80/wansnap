from django import forms
from django.core.exceptions import ValidationError
from .models import User, Dog, Post
from django.contrib.auth import get_user_model

class LoginForm(forms.Form):
    email = forms.EmailField(label='メールアドレス', required=True)
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput, required=True)

class SignupForm(forms.ModelForm):
    password1 = forms.CharField(label='パスワード', widget=forms.PasswordInput)
    password2 = forms.CharField(label='パスワード（再入力）', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username':'ユーザー名',
            'email':'メールアドレス',
        }
        
        def clean(self):
            cleaned_data = super().clean()
            password1 = cleaned_data.get("password1")
            password2 = cleaned_data.get("password2")
            
            if password1 and password2 and password1 != password2:
                self.add_error('password2', "パスワードが一致しません")

class DogForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('男の子', '男の子'),
        ('女の子', '女の子'),
    ]
    
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.RadioSelect,
        label='性別',
    )
    
      
    class Meta:
        model = Dog
        fields = ('dog_name', 'breed', 'birthday', 'gender', 'dog_image')
        labels = {
            'dog_name':'うちの子の名前',
            'breed':'犬種',
            'birthday':'うちの子の誕生日',
            'dog_image':'マイページ用写真',
        }

User = get_user_model()
        
class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        labels = {
            'email':'新しいメールアドレス',
        }
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['dog', 'image', 'caption'] 
        labels = {
            'dog':'投稿するうちの子',
            'image':'写真',
            'caption':'うちの子からひとこと',
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user',None)
        super().__init__(*args,**kwargs)
        if user is not None:
            self.fields['dog'].queryset = Dog.objects.filter(owner=user)