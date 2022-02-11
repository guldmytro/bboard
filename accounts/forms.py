from django import forms
from django.contrib.auth.models import User
from girls.models import Girl, City, Service
from clients.models import Client, Review
from django.utils.translation import gettext_lazy as _


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(label=_('Repeat Password'), widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_email(self):
        cd = self.cleaned_data
        try:
            User.objects.get(email=cd['email'])
            raise forms.ValidationError(_('User with this email is already registered'))
        except User.DoesNotExist:
            return cd['email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError(_('Password mismatch'))
        if len(cd['password2']) < 8:
            raise forms.ValidationError(_('Password length must be at least 8 characters'))
        return cd['password2']


class ProfileEditForm(forms.ModelForm):
    name = forms.CharField(label=False, min_length=2,
                           widget=forms.TextInput(attrs={
                               'placeholder': _('Your Name*')
                           }))
    age = forms.IntegerField(label=False, min_value=18, max_value=70,
                             widget=forms.NumberInput(attrs={
                                 'placeholder': _('Age*')
                             }))
    breast = forms.IntegerField(label=False, min_value=0, max_value=10,
                                widget=forms.NumberInput(attrs={
                                    'placeholder': _('Breast*')
                                }))
    growth = forms.IntegerField(label=False, min_value=100, max_value=250,
                                widget=forms.NumberInput(attrs={
                                    'placeholder': _('Height*')
                                }))
    weight = forms.IntegerField(label=False, min_value=30, max_value=200,
                                widget=forms.NumberInput(attrs={
                                    'placeholder': _('Weight*')
                                }))
    city = forms.ModelChoiceField(label=False, queryset=City.objects.all(),
                                  empty_label=_('Choose city*'),
                                  widget=forms.Select())
    about = forms.CharField(label=False, max_length=400,
                            widget=forms.Textarea(attrs={
                                'placeholder': _('Text about you*')
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
                                'placeholder': _('Phone*')
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


class ProfileServicesEditForm(forms.ModelForm):
    services = forms.ModelMultipleChoiceField(queryset=Service.objects.all().order_by('name'),
                                              widget=forms.CheckboxSelectMultiple,
                                              required=False)

    class Meta:
        model = Girl
        fields = ('services',)


class ProfileAdditionalEditForm(forms.ModelForm):
    parking = forms.CheckboxInput()
    apartment = forms.CheckboxInput()
    arrive = forms.CheckboxInput()

    class Meta:
        model = Girl
        fields = ('parking', 'apartment', 'arrive')


class ProfileCheckPhotoForm(forms.ModelForm):
    class Meta:
        model = Girl
        fields = ('test_photo',)


class CheckPhoneForm(forms.Form):
    phone = forms.CharField(label=False,
                            widget=forms.TextInput(attrs={
                                'type': 'tel',
                                'placeholder': _('Phone*')
                            }))


class ClientForm(forms.ModelForm):
    phone = forms.CharField(label=False,
                            widget=forms.TextInput(attrs={
                                'type': 'tel',
                                'placeholder': _('Phone*')
                            }))

    class Meta:
        model = Client
        fields = ('phone',)


class ClientReviewForm(forms.ModelForm):
    body = forms.CharField(max_length=200,
                           widget=forms.Textarea(attrs={
                               'placeholder': _('Review*')
                           }))

    type = forms.ChoiceField(choices=Review.RATE_CHOICES,
                             widget=forms.RadioSelect)

    class Meta:
        model = Review
        fields = ('body', 'type')


class RateForm(forms.ModelForm):
    active_advertising = forms.BooleanField(label=_('Autoflips'),
                                            required=False,
                                            widget=forms.RadioSelect(
                                                choices=[
                                                    (True, _('Yes')),
                                                    (False, _('No'))
                                                ]
                                            ))

    class Meta:
        model = Girl
        fields = ('active_advertising',)
