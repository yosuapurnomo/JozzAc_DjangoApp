from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Account
from django.contrib.auth.models import User


class accountForm(UserCreationForm):
    password1 = forms.CharField(
        label= "Password",
        strip=False,
        widget= forms.PasswordInput(attrs={
            'class':'form-control',
            
            }),
        )

    password2 = forms.CharField(
        label= "Confirm Password",
        strip=False,
        widget= forms.PasswordInput(attrs={
            'class':'form-control',
            
            }),
        )
    class Meta:
        model = Account
        fields = ['id', 'username', 'jabatan']

        widgets = {
        'jabatan':forms.Select(attrs={
            'class':'custom-select',

            }),
        'username':forms.TextInput(attrs={
            'class':'form-control',
            }),
        }

class updateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['username', 'jabatan']

        widgets = {
        'jabatan':forms.Select(attrs={
            'class':'custom-select',

            }),
        'username':forms.TextInput(attrs={
            'class':'form-control',
            }),
        }

class passwordForm(PasswordChangeForm):
    old_password = forms.CharField(
    label= "Password Lama",
    strip=False,
    widget= forms.PasswordInput(attrs={
    'class':'form-control',

    }),
    )
    new_password1 = forms.CharField(
    label= "Password Baru",
    strip=False,
    widget= forms.PasswordInput(attrs={
    'class':'form-control',

    }),
    )

    new_password2 = forms.CharField(
    label= "Confirm Password",
    strip=False,
    widget= forms.PasswordInput(attrs={
    'class':'form-control',

    }),
    )

    class Meta:
        model = Account
        fields = ['new_password1', 'new_password2']