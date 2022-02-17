from django import forms
from .models import Review
from girls.models import City, Girl
from django.utils.translation import gettext_lazy as _


class AddReviewForm(forms.ModelForm):
    name = forms.CharField(label=False,
                           max_length=100,
                           widget=forms.TextInput(attrs={
                               'placeholder': _('Name*'),
                           }))
    phone = forms.CharField(label=False,
                            max_length=30,
                            widget=forms.TextInput(attrs={
                                'type': 'tel',
                                'placeholder': _('Phone*')
                            }))
    body = forms.CharField(label=False,
                           max_length=400,
                           widget=forms.Textarea(
                               attrs={
                                   'placeholder': _('Review*')
                               }
                           ))

    class Meta:
        model = Review
        fields = ('name', 'phone', 'body')


class SearchForm(forms.Form):
    # city = forms.ModelChoiceField(queryset=City.objects.all(),
    #                               label=_('City'),
    #                               required=False)
    age = forms.ChoiceField(label=_('Age'),
                            required=False)
    price_from = forms.IntegerField(min_value=0,
                                    label=_('Min price'),
                                    required=False)
    price_to = forms.IntegerField(min_value=0,
                                  label=_('Max price'),
                                  required=False)
    apartments = forms.BooleanField(required=False,
                                    label=_('Apartments'),
                                    widget=forms.CheckboxInput)
    arrive = forms.BooleanField(required=False,
                                label=_('Departure'),
                                widget=forms.CheckboxInput)
    search = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'search'}))

    def __init__(self, *args, **kwargs):
        """Adding choices for age"""
        super(SearchForm, self).__init__(*args, **kwargs)
        choices = []
        ages = Girl.published.all().values_list('age', 'age').distinct()
        for age in ages:
            choices.append(tuple(age))
        choices.sort(key=lambda x:x[0])
        choices = [('', '---------')] + choices
        self.fields['age'].choices = choices
