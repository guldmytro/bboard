from django import forms
from django.contrib.auth.models import User
from girls.models import Girl, City

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


class ProfileEditForm(forms.ModelForm):
    name = forms.CharField(label=False, min_length=2,
                           widget=forms.TextInput(attrs={
                               'placeholder': 'Ваше имя*'
                           }))
    age = forms.IntegerField(label=False, min_value=18, max_value=70,
                             widget=forms.NumberInput(attrs={
                                 'placeholder': 'Возраст*'
                             }))
    breast = forms.IntegerField(label=False, min_value=0, max_value=10,
                                widget=forms.NumberInput(attrs={
                                    'placeholder': 'Грудь*'
                                }))
    growth = forms.IntegerField(label=False, min_value=100, max_value=250,
                                widget=forms.NumberInput(attrs={
                                    'placeholder': 'Рост*'
                                }))
    weight = forms.IntegerField(label=False, min_value=30, max_value=200,
                                widget=forms.NumberInput(attrs={
                                    'placeholder': 'Вес*'
                                }))
    city = forms.ModelChoiceField(label=False, queryset=City.objects.all(),
                                  empty_label='Выберите город*',
                                  widget=forms.Select())
    about = forms.CharField(label=False, max_length=400,
                            widget=forms.Textarea(attrs={
                                'placeholder': 'Текст о Вас*'
                            }))
    whatsapp = forms.CharField(label=False, required=False,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'WhatsApp'
                               }))
    telegram = forms.CharField(label=False, required=False,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'Telegram'
                               }))
    phone = forms.CharField(label=False,
                            widget=forms.TextInput(attrs={
                                'placeholder': 'Телефон*'
                            }))

    class Meta:
        model = Girl
        fields = ('name', 'age', 'breast', 'growth', 'weight', 'city',
                  'about', 'whatsapp', 'telegram', 'phone')


class ProfilePriceEditForm(forms.ModelForm):
    price_30_home = forms.IntegerField(label=False, required=False,
                                       min_value=0, max_value=100000
                                       )
    price_1h_home = forms.IntegerField(label=False, required=False,
                                       min_value=0, max_value=100000
                                       )
    price_2h_home = forms.IntegerField(label=False, required=False,
                                       min_value=0, max_value=100000
                                       )
    price_night_home = forms.IntegerField(label=False, required=False,
                                          min_value=0, max_value=100000
                                          )
    price_1h_departure = forms.IntegerField(label=False, required=False,
                                            min_value=0, max_value=100000
                                            )
    price_2h_departure = forms.IntegerField(label=False, required=False,
                                            min_value=0, max_value=100000
                                            )
    price_night_departure = forms.IntegerField(label=False, required=False,
                                               min_value=0, max_value=100000
                                               )

    class Meta:
        model = Girl
        fields = ('price_30_home', 'price_1h_home',
                  'price_2h_home', 'price_night_home',
                  'price_1h_departure', 'price_2h_departure',
                  'price_night_departure')