from django.db import models
from django.conf import settings
from django.utils.text import slugify

from product.models import ProductModel
from client.models import ClientModel

from collections import OrderedDict

# Create your models here.
    

      
class InvoiceModel(models.Model):
    """
    Description: Model Description
    """
    statusChoise = [
    ('LUNAS','LUNAS'),
    ('BELUM', 'BELUM LUNAS'),
    ]

    Invoice             = models.CharField(max_length=20, verbose_name='Nomor Invoice')
    clientINV           = models.OneToOneField(ClientModel, blank=True, null=True, related_name='InvoiceClient', verbose_name='Invoice Client', on_delete=models.SET_NULL)
    statusPembayaran    = models.CharField(choices=statusChoise, max_length=20, default='BELUM')
    Keterangan          = models.TextField()
    tanggal			    = models.DateField(auto_now=True, editable=False, verbose_name='Tanggal')
    totalInvoice	    = models.PositiveIntegerField(default=0, verbose_name='Total Pembayaran')
    slug_Invoice	    = models.SlugField()

    class Meta:
        verbose_name='Invoice'
        verbose_name_plural='Invoice'

    def save(self):
        self.slug_Invoice   = slugify(f"{self.Invoice}")
        super().save()

    def __str__(self):
    	return f"{self.Invoice}"


class Job_OrderModel(models.Model):

    nomor_jo        = models.CharField(max_length=20, blank=True, verbose_name='NOMOR JO')
    product         = models.ForeignKey(ProductModel, on_delete=models.SET_NULL, related_name='productJO', null=True)
    client          = models.ForeignKey(ClientModel, on_delete=models.SET_NULL, related_name='clientJO', blank=True, null=True)
    keterangan      = models.CharField(max_length=255, blank=True, null=True, verbose_name='Keterangan')
    jumlah_Ac       = models.PositiveIntegerField()
    tgl_input       = models.DateField(auto_now=True)
    slugJO          = models.SlugField()

    def save(self):
        super().save()
        if self.slugJO == "":

            self.nomor_jo       = f"{str(self.id).zfill(4)}/JO/{write_roman(self.tgl_input.month)}/{self.tgl_input.year}".upper()

            self.slugJO   = slugify(f"{self.nomor_jo}")

            self.save()


    class Meta:
        verbose_name = "Job Order"
        verbose_name_plural = "Job Order"

    def __str__(self):
        return self.nomor_jo


class approvalModel(models.Model):
    statusChoice        = [
        ('SELESAI','SELESAI'),
        ('PENDING','PENDING'),
        ('CANCEL','CANCEL'),
    ]

    invoice             = models.OneToOneField(InvoiceModel, on_delete=models.CASCADE, related_name='ApprovPesanan', null=True, blank=True)
    client              = models.OneToOneField(ClientModel, on_delete=models.SET_NULL, related_name='clientApprov', null=True)
    admin               = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='adminUser')
    approve             = models.BooleanField(default=False)
    tgl_approve         = models.DateField(null=True, blank=True, verbose_name='Tanggal Approval', auto_now=True)
    slug_Approv         = models.SlugField()

    class Meta:
        verbose_name = "Approval"
        verbose_name_plural = "Approval Pesanan"

    
    def save(self):
        self.slug_Approv = slugify(f"Approv-{self.client}")
        super().save()

    def __str__(self):
        return f"{self.client}"


def write_roman(num):
    def change(num):
        roman = OrderedDict()
        roman[10] = "X"
        roman[9] = "IX"
        roman[5] = "V"
        roman[4] = "IV"
        roman[1] = "I"

        for r in roman.keys():
            x, y = divmod(num, r)
            yield roman[r] * x
            num -= (r * x)
            if num <= 0:
                break

    return "".join([a for a in change(num)])