from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    email = forms.EmailField(label='メールアドレス', required=True)
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput, required=True)

class SignuoForm(forms.Modelform):
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput)
    password_confirm = cleaned_date.get("password_confirm")
    
    if password and password_confirm and password != password_confirm:
        self.add_error('password_confirm', "パスワードが一致しません")
        