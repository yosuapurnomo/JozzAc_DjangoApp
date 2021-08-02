from django import forms
from .models import ProductModel

class productForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = ('namaProduct' , 'keteranganProduct', 'hargaProduct', )

        widgets={
	            'namaProduct':forms.TextInput(attrs={
	                'id':"namaProduct",
	                'class':"form-control col-3",
	                }),

	        	'keteranganProduct': forms.Textarea(attrs={
	        		'name':"keterangan",
	        		'id':"inputKeterangan",
	        		'class':"form-control col-5",
	        		'style': 'height: 100px',
	                
	        		}),
	        	'hargaProduct':forms.NumberInput(attrs={
	        		'name':"harga",
	        		'class':"form-control col-3",
	        		'id':"inputTotal",
	                
	        		})
	        }
