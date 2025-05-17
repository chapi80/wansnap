from django import forms

class LoginFrom(froms.From):
    email = froms.EmailField(label='メールアドレス', required=True)
    password = froms.CharFild(label='パスワード', widget=froms.PasswordInput, required=True)
    