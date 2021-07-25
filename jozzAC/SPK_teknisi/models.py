from django.db import models
from pesanan.models import approvalModel, InvoiceModel
from client.models import ClientModel
from django.conf import settings
from django.utils.text import slugify

from collections import OrderedDict

# Create your models here.

class SPKModel(models.Model):
    """
    Description: Model Description
    """
    statusChoice        = [
        ('PENDING','ON PROGRESS'),
        ('CANCEL','CANCEL'),
        ('SELESAI','SELESAI'),
    ]

    no_SPK			= models.CharField(max_length=30, verbose_name='Nomor SPK', blank=True, unique=True)
    tgl_input		= models.DateField(auto_now=True, verbose_name='Tanggal Input')
    teknisi			= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='teknisiUser', verbose_name='Teknisi', null=True)
    pesanan		    = models.OneToOneField(InvoiceModel, related_name='SPK', on_delete=models.SET_NULL, verbose_name='Invoice', null=True)
    tgl_pengerjaan	= models.DateField(verbose_name='Tanggal Pengerjaan')
    keterangan		= models.TextField(verbose_name='Keterangan')
    status			= models.CharField(choices=statusChoice, max_length=10, default='PENDING')
    slug_SPK		= models.SlugField()

    class Meta:
        verbose_name='Surat Perintah Kerja'
        verbose_name_plural='Surat Perintah Kerja'

    def save(self):
        self.slug_SPK       = slugify(f"{self.no_SPK} {self.teknisi}")
        super().save()

    def __str__(self):
    	return self.no_SPK