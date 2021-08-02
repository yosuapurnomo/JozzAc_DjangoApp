from django import forms
from .models import ClientModel

class clientForm(forms.ModelForm):
    class Meta:
        model = ClientModel
        fields = ('nama_Client','noTelp_Client', 'email_Client', 'alamat_Client', 
        			'kecamatan_Client', 'kelurahan_Client', 'kodePos_Client', 'kota_Client')

        widgets={
        	'nama_Client': forms.TextInput(attrs={
        		'class':"form-control",
                'placeholder':"Nama Client",
                
        		}),

        	'noTelp_Client': forms.TextInput(attrs={
        		
        		'class':"form-control",
        		'placeholder':"Nomor Telp",
                'aria-describedby':"emailHelp",

        		}),

        	'email_Client': forms.EmailInput(attrs={
        		'class':"form-control",
                'aria-describedby':"emailHelp",
                'placeholder':"@Email",
        		}),

        	'alamat_Client': forms.TextInput(attrs={
        		'placeholder':"Alamat",
        		'class':"form-control",
        		}),

            'kecamatan_Client': forms.TextInput(attrs={
                'placeholder':"Kecamatan",
                'class':"form-control",
                }),

            'kelurahan_Client': forms.TextInput(attrs={
                'placeholder':"Kelurahan",
                'class':"form-control",
                }),

            'kota_Client': forms.TextInput(attrs={
                'placeholder':"Kota",
                'class':"form-control",
                })
        }