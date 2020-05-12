from django import forms
from shopone.models import *

class SetsubgroupForm(forms.ModelForm):
    code = forms.CharField(
        label='code',
        widget=forms.TextInput(
            attrs={
                'placeholder': '',
                'class': 'form-control form-control-sm',
                'maxlength': 255,
            }
        )
    )
    name = forms.CharField(
        label='คำอธิบาย',
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': '',
                'class': 'form-control form-control-sm',
                'maxlength': 255,
            }
        )
    )
    slug = forms.SlugField(
        label='slug',        
        widget=forms.TextInput(
            attrs={
                'placeholder': '',
                'class': 'form-control form-control-sm',
                'maxlength': 255,
            }
        )
    )
    group = forms.ModelChoiceField(
        queryset = Setgroup.objects.all().order_by('code'),
        label='กลุ่มสินค้า',
        widget=forms.Select(
            attrs={
                'class': 'form-control select2',
            }
        )
    )


    class Meta:
        model = Setsubgroup
        fields = '__all__'


class FileFieldForm(forms.Form):
    file_field = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={
                'multiple': True
            }
        )
    )


class PicItemForm(forms.ModelForm):
    name = forms.CharField(
        label='คำอธิบาย',
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'คำอธิบาย',
                'class': 'form-control form-control-sm',
                'maxlength': 100,
            }
        )
    )
    slug = forms.ModelChoiceField(
        queryset=Product.objects.order_by('slug'),
        label='slug',
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-sm',
            }
        )
    )
    image = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={
                'multiple': True
            }
        )
    )
    class Meta:
        model = ProductImageItem
        fields = ('name','slug','image')