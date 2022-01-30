from django import forms
from .models import Review


class AddReviewForm(forms.ModelForm):
    name = forms.CharField(label=False,
                           max_length=100,
                           widget=forms.TextInput(attrs={
                               'placeholder': 'Имя*',
                           }))
    phone = forms.CharField(label=False,
                            max_length=30,
                            widget=forms.TextInput(attrs={
                                'type': 'tel',
                                'placeholder': 'Телефон*'
                            }))
    body = forms.CharField(label=False,
                           max_length=400,
                           widget=forms.Textarea(
                               attrs={
                                   'placeholder': 'Отзыв*'
                               }
                           ))

    class Meta:
        model = Review
        fields = ('name', 'phone', 'body')
