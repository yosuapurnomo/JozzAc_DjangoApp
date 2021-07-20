from django import forms
from .models import eventContentModel

class eventForm(forms.ModelForm):
    class Meta:
        model = eventContentModel
        fields = ('nama_Content', 'keterangan_Content', 'image', 'admin')

        widgets = {
        'nama_Content':forms.TextInput(attrs={
        	'class':"form-control",
        	}),
        'keterangan_Content':forms.Textarea(attrs={
        	'class':"form-control",
        	'style': 'height: 100px',
        	}),
        'image': forms.FileInput(),
        'admin':forms.HiddenInput()
        }
    