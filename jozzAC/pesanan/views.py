from django.shortcuts import redirect
from django.http import HttpResponse

from django.template.loader import get_template
from xhtml2pdf import pisa
import socket
from terbilang import Terbilang

from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction

from .models import InvoiceModel, approvalModel, Job_OrderModel
from client.models import ClientModel
from product.models import ProductModel

from account.models import Account
from django.db.models import Q

from .forms import InvoiceForm, JOForm
from .forms import OrderFormSet
from client.forms import clientForm
# from account.forms import accountForm

# Create your views here.
class pesananKhusus(LoginRequiredMixin, CreateView):
	login_url = reverse_lazy('account:login')
	model = InvoiceModel
	form_class = InvoiceForm
	template_name = 'admin/add.html'
	success_url = reverse_lazy('pesanan:tracking')

	def get_context_data(self, **kwargs):
	    kwargs['form'] = self.get_form()
	    kwargs['last_invoice'] = self.model.objects.order_by('Invoice').last()
	    kwargs['formClient'] = clientForm
	    kwargs['formJO'] = JOForm
	    kwargs['account'] = Account.objects.filter(jabatan='TEKNISI')
	    return super().get_context_data(**kwargs)

	def post(self,request, **kwargs):
		client = clientForm(
			request.POST
			)
		
		if client.is_valid():
			idClient = client.save()
			print(idClient.id)
			dataClient = ClientModel.objects.get(id=idClient.id)
			print(dataClient)

			JO = Job_OrderModel(
				product=ProductModel.objects.get(namaProduct='KHUSUS'),
				client=dataClient,
				keterangan=request.POST.get('keterangan'),
				jumlah_Ac=request.POST.get('jumlah_Ac'))

			JO.save()

			invoice = InvoiceModel(
			Invoice=request.POST.get('Invoice'), 
			clientINV=dataClient, 
			statusPembayaran=request.POST.get('statusPembayaran'), 
			Keterangan=request.POST.get('Keterangan'), 
			totalInvoice=request.POST.get('totalInvoice')
			)

			invoice.save()

			approve = approvalModel(invoice=invoice, client=dataClient, admin=request.user, approve=True)
			approve.save()
		
		return redirect(self.success_url)

class Tracking(LoginRequiredMixin, ListView):
	login_url = reverse_lazy('account:login')
	model = InvoiceModel
	context_object_name = 'pesanan'
	template_name = 'admin/tracking.html'
	queryset = model.objects.filter(Q(statusPembayaran='BELUM') | ~Q(SPK__status='SELESAI'))

class ApprovalView(LoginRequiredMixin, ListView):
	login_url = reverse_lazy('account:login')
	model = ClientModel
	template_name = 'admin/Approvel.html'
	context_object_name = 'pesanan'
	queryset = model.objects.filter(clientApprov__isnull=True).exclude(InvoiceClient__isnull=False)
	query_string = True

	def post(self, request, **kwargs):
		client = self.model.objects.get(slug_Client=request.POST.get('slug'))
		data = approvalModel(invoice=None, client=client, admin=request.user, approve=False)
		data.save()
		return super().get(request, **kwargs)

class InvoiceApprov(LoginRequiredMixin, CreateView):
	login_url = reverse_lazy('account:login')
	model = InvoiceModel
	form_class = InvoiceForm
	template_name = 'admin/InvoiceCreate.html'
	success_url = reverse_lazy('pesanan:approval')


	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['last_invoice'] = self.model.objects.order_by('Invoice').last()
	    context['client'] = ClientModel.objects.get(slug_Client=self.kwargs['slug'])
	    return context

	def get(self, request, **kwargs):
		dataClient = ClientModel.objects.get(slug_Client=kwargs['slug'])
		data = dataClient.clientApprov if hasattr(dataClient, 'clientApprov') else False
		
		if data != False:
			return redirect(self.success_url)
		else:
			return super().get(self.request, **kwargs)

	def post(self, request, *args, **kwargs):
		form = self.get_form()
		client = ClientModel.objects.get(slug_Client=kwargs['slug'])
		dataInvoice = self.model(
			Invoice=request.POST.get('Invoice'), 
			clientINV=client, 
			statusPembayaran=request.POST.get('statusPembayaran'), 
			Keterangan=request.POST.get('Keterangan'), 
			totalInvoice=request.POST.get('totalInvoice')
			)

		dataInvoice.save()
		if form.is_valid():
			invoiceObject = self.model.objects.get(Invoice=request.POST.get('Invoice'))
			data = approvalModel(invoice=dataInvoice, client=client, admin=request.user, approve=True)
			data.save()
		return redirect(self.success_url)

class InvoiceView(LoginRequiredMixin, ListView):
	login_url = reverse_lazy('account:login')
	model = InvoiceModel
	template_name = 'admin/invoiceView.html'
	extra_context = {
	'listInvoice': model.objects.all().order_by('-Invoice')
	}

class InvoiceDetail(LoginRequiredMixin, UpdateView):
	login_url = reverse_lazy('account:login')
	model = InvoiceModel
	template_name = 'admin/updateInvoice.html'
	form_class = InvoiceForm
	success_url = reverse_lazy('pesanan:invoiceView')
	slug_url_kwarg = 'slug'
	slug_field = 'slug_Invoice'
	extra_context = {
	'last_invoice': model.objects.order_by('Invoice').last()
	}

class InvoiceDelete(LoginRequiredMixin, DeleteView):
	login_url = reverse_lazy('account:login')
	model = InvoiceModel
	template_name = 'admin/updateInvoice.html'
	success_url = reverse_lazy('pesanan:invoiceView')
	slug_url_kwarg = 'slug'
	slug_field = 'slug_Invoice'

	def get(self, request, **kwargs):
		try:
			data = self.model.objects.get(slug_Invoice=kwargs['slug'])
			return redirect(reverse('pesanan:invoiceUpdate', kwargs={"slug": kwargs['slug']}))
		except:
			return redirect('pesanan:invoiceView')

	def form_valid(self, form):
		context = self.get_context_data()
		OrderClient = context['OrderClient']
		with transaction.atomic():
			self.objects = form.save()

			if OrderClient.is_valid():
				OrderClient.instance = self.objects
				OrderClient.save()
		return super().form_valid(form)

class cetakInvoice(LoginRequiredMixin, View):
	login_url = reverse_lazy('account:login')
	model = InvoiceModel
	template_name = 'admin/invoicePDF.html'

	def get(self, request, *args, **kwargs):
		objects = self.model.objects.get(slug_Invoice=kwargs['slug'])
		terbilang = Terbilang()
		context = {'object': objects,
					'terbilang': str(terbilang.parse(str(objects.totalInvoice)).getresult() + ' rupiah').capitalize(),
					'hostname' : request.META['HTTP_HOST']}
		title = objects.Invoice
		

		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] = f'inline; filename="{title}.pdf"'
		
		template = get_template(self.template_name)
		html = template.render(context)

		
		pisa_status = pisa.CreatePDF(
		html, dest=response)
		
		if pisa_status.err:
			return HttpResponse('We had some errors <pre>' + html + '</pre>')
		return response


# CLient

class ClientOrder(CreateView):
    model = ClientModel
    template_name = "client/AddOrder.html"
    form_class = clientForm
    success_url = reverse_lazy('landingPage')
    extra_context = {
    'navbar': 'pesan',
    'product':ProductModel.objects.all()
    }

    def post(self, request, *args, **kwargs):
    	data = ProductModel.objects.filter(~Q(slugProduct='khusus'))
    	nama = self.request.POST.get('nama')
    	telp = self.request.POST.get('Telp')
    	email = self.request.POST.get('email')
    	alamat = self.request.POST.get('alamat')
    	kota = self.request.POST.get('kota')
    	client = clientForm(self.request.POST)
    	if client.is_valid():
    		client = client.save()
    		
    		for x in ProductModel.objects.filter(~Q(slugProduct='khusus')):
    			if self.request.POST.get(x.slugProduct, False) == 'on':
    				ket = self.request.POST.get(f"{x.slugProduct}Keterangan", "")
    				jum = self.request.POST.get(f"{x.slugProduct}Jumlah", 0)
    				job = Job_OrderModel(product=x, client=client, keterangan=ket, jumlah_Ac=jum)
    				job.save()
    				print(job.nomor_jo)

    	return redirect(self.success_url)

