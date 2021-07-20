from django import forms
from .models import SPKModel
from account.models import Account

class SPK_Form(forms.ModelForm):
    class Meta:
        model = SPKModel
        fields = ('no_SPK', 'teknisi', 'pesanan', 'tgl_pengerjaan', 'keterangan', 'status')

        widgets={
            'no_SPK':forms.TextInput(attrs={
                'class':"form-control",
                'onchange':"SPK_Value(this.value)",
                }),

            'keterangan': forms.Textarea(attrs={
                'class':"form-control",
                'style': 'height: 100px',
                }),


        	'teknisi': forms.Select(attrs={
        		'class':"form-control",
        		}),

        	'tgl_pengerjaan':forms.DateInput(attrs={
        		'class':"datepicker form-control",
                'type':"date"
        		}),

            'status':forms.Select(attrs={
                'class':"form-control",
                }),
            'pesanan':forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teknisi'].queryset = Account.objects.filter(jabatan='TEKNISI')

class SPK_Update_Status(forms.ModelForm):
    class Meta:
        model = SPKModel
        fields = ('no_SPK', 'teknisi', 'pesanan', 'tgl_pengerjaan', 'keterangan', 'status')

        widgets={
            'no_SPK':forms.TextInput(attrs={
                'class':"form-control",
                'onchange':"SPK_Value(this.value)",
                'readonly':True,
                }),

            'keterangan': forms.Textarea(attrs={
                'class':"form-control",
                'style': 'height: 100px',
                'readonly':True,
                }),


            'teknisi': forms.Select(attrs={
                'class':"form-control",
                'readonly':True,
                }),

            'tgl_pengerjaan':forms.TextInput(attrs={
                'class':"datepicker form-control",
                
                'readonly':True,
                }),

            'status':forms.Select(attrs={
                'class':"form-control",
                }),
            'pesanan':forms.HiddenInput(),
        }
