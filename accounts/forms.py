from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_email(self):
        cd = self.cleaned_data
        try:
            User.objects.get(email=cd['email'])
            raise forms.ValidationError('Пользователь с таким email уже зарегистрирован')
        except User.DoesNotExist:
            return cd['email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        if len(cd['password2']) < 8:
            raise forms.ValidationError('Длина пароля должна быть не меньше 8 символов')
        return cd['password2']
