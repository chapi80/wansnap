from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Dog

class LoginForm(forms.Form):
    email = forms.EmailField(label='メールアドレス', required=True)
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput, required=True)

class SignupForm(forms.ModelForm):
    password1 = forms.CharField(label='パスワード', widget=forms.PasswordInput)
    password2 = forms.CharField(label='パスワード（再入力）', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email']
        
        def clean(self):
            cleaned_date = super().clean()
            password1 = cleaned_date.get("password1")
            password2 = cleaned_date.get("password2")
            
            if password1 and password2 and password1 != password2:
                self.add_error('password2', "パスワードが一致しません")

class DogForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('男の子', '男の子'),
        ('女の子', '女の子'),
    ]
    
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.RadioSelect
    )
    
    dog_name = forms.CharField(label='うちの子の名前')
    
    class Meta:
        model = Dog
        fields = ['dog_name', 'breed', 'birthday', 'gender', 'dog_image']                