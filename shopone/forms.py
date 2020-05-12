import json
from django import forms
from .models import *


def is_anagram(x,y):
    return sorted(x) == sorted(y)

def is_chktrue(x,y):
    return x == y

class FormName(forms.Form):
    name = forms.CharField(
        label = 'name',
        widget=forms.TextInput(attrs={'class': "input"})
    )
    text = forms.CharField(
        label = 'text',
        widget=forms.TextInput(attrs={'class': "input"})
    )

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        text = cleaned_data.get('text')

        if name and text:
            if not is_anagram(name,text):
                raise forms.ValidationError('This is not anagram')

class FormRegist(forms.Form):

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2:
            if not is_chktrue(password1,password2):
                raise forms.ValidationError('password this not match.')
        

    # def clean_test_value(self):
    #     data = self.cleaned_data.get('name')

    #     if not is_anagram(data, 'listen'):
    #         raise forms.ValidationError('This is not anagram listen')

    #     return data

class StateForm(forms.ModelForm):
    dcars = {}
    list_cars = []
    for subgroup in Setsubgroup.objects.all():
        if subgroup.group.id in dcars:
            dcars[subgroup.group.id].append(subgroup.name)
        else:
            dcars[subgroup.group.id] = [subgroup.name]
        list_cars.append((subgroup.id,subgroup.name))

    # brands = [str(group.id) for group in Setgroup.objects.all()]
    brands={}
    listgroup = []
    for group in Setgroup.objects.all():
        if group.id in brands:
            brands[group.id].append(group.name)
        else:
            brands[group.id] = [group.id]
        listgroup.append((group.id,group.name))

    # brand_select = forms.ChoiceField(choices=([(group, group) for group in brands]))
    brand_select = forms.ChoiceField(choices=(listgroup))
    car_select = forms.ChoiceField(choices=(list_cars))

    brands = json.dumps(brands)
    cars = json.dumps(dcars)

    class Meta:
        model = Settypegroup
        fields = ('brand_select', 'car_select', 'name',)

