from django.shortcuts import render, redirect
from datetime import date
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from product.models import ProductModel
from client.models import ClientModel
from pesanan.models import InvoiceModel
from SPK_teknisi.models import SPKModel
from eventContent.models import eventContentModel
from django.db.models import Q, Sum, Count

class dasboardList(ListView):
	model = ProductModel
	context_object_name = 'object'
	queryset = model.objects.filter(~Q(namaProduct='KHUSUS'))
	extra_context = {
	'navbar':'home',
	'title':"JozzAc Surabaya",
	'eventContent': eventContentModel.objects.all()
	}
	template_name = 'client/Home.html'

class dasboardAdmin(LoginRequiredMixin, ListView):
	login_url = reverse_lazy('account:login')
	model = ClientModel
	template_name = 'admin/dasboardAdmin.html'
	context_object_name = 'pesanan'
	queryset = model.objects.filter(clientApprov__isnull=True).exclude(InvoiceClient__isnull=False)
	query_string = True

	def get(self, request, **kwargs):
		if self.request.user.jabatan == 'TEKNISI':
			return redirect('spk:teknisiSPK')
		return super().get(request, kwargs)

	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    today = date.today()
	    year = today.strftime("%Y")
	    month = today.strftime("%m")
	    context['month'] = today.strftime("%B %Y")
	    pendapatan = InvoiceModel.objects.filter(tanggal__year__gte=year, tanggal__month__gte=month,
	    													tanggal__year__lte=year, tanggal__month__lte=month).aggregate(Total=Sum('totalInvoice'))
	    
	    if pendapatan['Total'] is None:
	    	context['pendapatan'] = {'Total':0}
	    else:
	    	context['pendapatan'] = pendapatan
	    context['piutang'] = InvoiceModel.objects.filter(statusPembayaran='BELUM').aggregate(Total=Sum('totalInvoice'))
	    jumlahSPK = SPKModel.objects.filter(tgl_input__year__gte=year, tgl_input__month__gte=month,
	    													tgl_input__year__lte=year, tgl_input__month__lte=month).aggregate(Total=Count('no_SPK'))
	    jumlahPending = SPKModel.objects.filter(tgl_input__year__gte=year, tgl_input__month__gte=month,
	    													tgl_input__year__lte=year, tgl_input__month__lte=month,
	    													status='PENDING').aggregate(Total=Count('no_SPK'))
	    print(jumlahPending['Total'], jumlahSPK['Total'])
	    if jumlahPending['Total'] > 0:
	    	context['OnProgress'] = round(jumlahPending['Total']/jumlahSPK['Total']*100)
	    else: context['OnProgress'] = 0
	    
	    context['panding'] = self.model.objects.filter(clientApprov__isnull=True).exclude(InvoiceClient__isnull=False).aggregate(Total=Count('nama_Client'))
	    return context

class landingPage(TemplateView):
    template_name = "client/landingPage.html"
    extra_context = {
    'navbar': 'pesan'
    }

def handle404(request, exception=None):
	if request.user is None:
		return redirect('dasboard')
	elif request.user.is_authenticated:
		return redirect('dasboardAdmin')