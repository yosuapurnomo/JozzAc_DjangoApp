from django import forms
from .models import InvoiceModel
from client.models import ClientModel
from .models import Job_OrderModel

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = InvoiceModel
        fields = ('Invoice' , 'Keterangan', 'totalInvoice', 'statusPembayaran', )

        widgets={
            'statusPembayaran':forms.Select(attrs={
                'id':"id_statusPembayaran",
                'class':"form-control",
                }),

            'Invoice': forms.TextInput(attrs={
                'class':"form-control",
                'id':"id_Invoice",
                'name':"Invoice",
                'onchange':"InvoiceNumber(this.value)",
                }),

        	'Keterangan': forms.Textarea(attrs={
        		'name':"keterangan",
        		'id':"inputKeterangan",
        		'class':"form-control",
        		'style': 'height: 100px',
                
        		}),
        	'totalInvoice':forms.NumberInput(attrs={
        		'name':"total",
        		'class':"form-control",
        		'id':"inputTotal",
                'aria-describedby':"emailHelp",
        		})
        }

class JOForm(forms.ModelForm):
    class Meta:
        model = Job_OrderModel
        fields = ('product', 'jumlah_Ac', 'keterangan')

        widgets={
            'keterangan':forms.TextInput(attrs={
                'placeholder':"Keterangan Order",
                'class':"form-control",
                }),

            'jumlah_Ac': forms.NumberInput(attrs={
                'class':"form-control",
                'placeholder':"Jumlah AC",
                }),
        }

        # def get_data_product()


OrderFormSet = forms.inlineformset_factory(ClientModel, Job_OrderModel, form=JOForm, extra=1)