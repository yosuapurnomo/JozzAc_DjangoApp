from django import forms
from .models import pembayaranModel

class pembayaranForm(forms.ModelForm):
    class Meta:
        model = pembayaranModel
        fields = ('no_pembayaran', 'jumlah', 'keterangan', 'tgl_pembayaran', 'admin', 'invoice')

        widgets={
            'no_pembayaran':forms.TextInput(attrs={
                'class':"form-control",
                'onchange':"KM_Value(this.value)",
                }),

            'keterangan': forms.Textarea(attrs={
                'class':"form-control",
                'style': 'height: 100px',
                }),

            'tgl_pembayaran':forms.DateInput(attrs={
                'class':"datepicker form-control",
                'type':"date"
                }),

            'jumlah':forms.NumberInput(attrs={
                'class':"form-control",
                }),
            'admin':forms.HiddenInput(),
            'invoice':forms.HiddenInput(),
        }
    