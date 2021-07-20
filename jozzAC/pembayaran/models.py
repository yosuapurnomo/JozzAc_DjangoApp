from django.db import models
from django.conf import settings
from django.utils.text import slugify
from pesanan.models import InvoiceModel

# Create your models here.
class pembayaranModel(models.Model):

    no_pembayaran       = models.CharField(max_length=30, verbose_name='Nomor Pembayaran')
    tgl_input           = models.DateField(auto_now=True, verbose_name='Tanggal Input')
    invoice             = models.ForeignKey(InvoiceModel, on_delete=models.SET_NULL, related_name='payment', null=True)
    admin               = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='admin')
    jumlah              = models.PositiveIntegerField(default=0, verbose_name='Jumlah Pembayaran')
    keterangan          = models.TextField()
    tgl_pembayaran      = models.DateField(verbose_name='Tanggal Pembayaran')
    slug_pembayaran     = models.SlugField()

    class Meta:
        verbose_name='Pembayaran'
        verbose_name_plural='Pembayaran'

    def save(self):
    	self.slug_pembayaran = slugify(f'{self.no_pembayaran}')
    	super().save()

    def __str__(self):
        return self.no_pembayaran