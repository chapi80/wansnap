from django import forms
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory
from django.contrib.auth import get_user_model
from .models import User, Dog, Post
from django.forms.widgets import FileInput
import re

User = get_user_model()

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
            
        if password1 and password2:
            if password1 != password2:
                self.add_error('password2', "パスワードが一致しません")
            
            if not re.search(r'[A-Za-z]', password1):
                self.add_error('password1', "パスワードには英字を含めてください")
            
            if not re.search(r'[0-9]', password1):
                self.add_error('password1', "パスワードには数字を含めてください")
            
            if len(password1) < 8:
                self.add_error('password1', "パスワードは8文字以上にしてください")           

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
        fields = ['dog_name', 'breed', 'birthday', 'gender', 'dog_image']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'dog_name':'うちの子の名前',
            'breed':'犬種',
            'birthday':'うちの子の誕生日',
            'dog_image':'マイページ用写真',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dog_image'].widget.attrs.update({'class': 'file-input'})
 
DogFormSet = modelformset_factory(Dog, form=DogForm, extra=1, can_delete=False)       
       
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
        fields = ['dog', 'image', 'caption', 'memo'] 
        labels = {
            'dog':'投稿するうちの子',
            'image':'写真',
            'caption':'うちの子からひとこと',
            'memo':'メモ欄（体調など）',
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user',None)
        super().__init__(*args,**kwargs)
        if user is not None:
            self.fields['dog'].queryset = Dog.objects.filter(owner=user)
        
        self.fields['image'].required = False
        self.fields['image'].widget = FileInput()
        self.fields['image'].widget.attrs.update({'class': 'file-input'})
        