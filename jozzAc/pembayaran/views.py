from django.shortcuts import render, redirect
from django.http import HttpResponse
from terbilang import Terbilang
from django.template.loader import get_template
from xhtml2pdf import pisa
import socket
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, UpdateView, CreateView, TemplateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import pembayaranModel
from .forms import pembayaranForm
from pesanan.models import InvoiceModel

# Create your views here.
class searchPayment(LoginRequiredMixin, TemplateView):
	login_url = reverse_lazy('account:login')
	template_name = 'pembayaran/search.html'
	extra_context = {'listPayment': pembayaranModel.objects.order_by('tgl_input')}

class ListPayment(LoginRequiredMixin, ListView):
	login_url = reverse_lazy('account:login')
	model = InvoiceModel
	template_name = 'pembayaran/ListView.html'
	queryset = model.objects.filter(statusPembayaran="BELUM")
	extra_context = {
	'invoice':InvoiceModel.objects.filter(statusPembayaran="BELUM")
	}
	context_object_name = 'object'

class UpdatePayment(LoginRequiredMixin, UpdateView):
	login_url = reverse_lazy('account:login')
	model = pembayaranModel
	template_name = 'pembayaran/update.html'
	form_class = pembayaranForm
	success_url = reverse_lazy('pembayaran:search')
	slug_field = 'slug_pembayaran'
	slug_url_kwarg = 'slug'
	extra_context = {
	'lastPayment': model.objects.all().last()
	}

class DeletePayment(LoginRequiredMixin, DeleteView):
	login_url = reverse_lazy('account:login')
	model = pembayaranModel
	success_url = reverse_lazy('pembayaran:search')
	slug_field = 'slug_pembayaran'
	slug_url_kwarg = 'slug'

	def get(self, request, **kwargs):
		try:
			data = self.model.objects.get(slug_pembayaran=kwargs['slug'])
			return redirect(reverse('pembayaran:update', kwargs={"slug": kwargs['slug']}))
		except:
			return redirect('pembayaran:search')

class create(LoginRequiredMixin, CreateView):
	login_url = reverse_lazy('account:login')
	model = pembayaranModel
	template_name = 'pembayaran/create.html'
	success_url = reverse_lazy('pembayaran:list')
	form_class = pembayaranForm
	slug_field = 'slug_pembayaran'
	slug_url_kwarg = 'slug'

	def get_initial(self):
		print(self.kwargs['slug'])
		invoice = InvoiceModel.objects.get(slug_Invoice=self.kwargs['slug'])
		return {'admin':self.request.user,
		'invoice':invoice}

	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    # context['lastPayment'] = self.model.objects.all().last()
	    context['lastPayment'] = self.model.objects.all()
	    context['invoice'] = InvoiceModel.objects.get(slug_Invoice=self.kwargs['slug'])
	    return context

	def post(self, request, **kwargs):
		formModel = self.get_form()
		invoice = InvoiceModel.objects.get(slug_Invoice=self.kwargs['slug'])
		selisih = (invoice.totalInvoice - int(formModel['jumlah'].value()))

		if selisih == 0:
			invoice.statusPembayaran = 'LUNAS'
			invoice.save()
			return super().form_valid(formModel)
		elif selisih < 0:
			pesan = f"Nominal pembayaran tidak balance dengan total Invoice, Pembayaran Selisih {selisih}"
			messages.add_message(request, messages.INFO, pesan)
			return super().get(request, kwargs)
		else:
			invoice.statusPembayaran = 'BELUM'
			invoice.save()

		return super().get(request, kwargs)

class createPDF(LoginRequiredMixin, View):
	login_url = reverse_lazy('account:login')
	model = pembayaranModel
	template_name = 'pembayaran/pdf.html'

	def get(self, request, **kwargs):
		objects = self.model.objects.get(slug_pembayaran=kwargs['slug'])
		terbilang = Terbilang()
		invoice = objects.invoice
		context = {'object': objects,
					'invoice':invoice,
					'terbilang': str(terbilang.parse(str(objects.jumlah)).getresult() + ' rupiah').capitalize(),
					'hostname' : request.META['HTTP_HOST']}
		title = objects.no_pembayaran
		

		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] = f'inline; filename="{title}.pdf"'
		# find the template and render it.
		template = get_template(self.template_name)
		html = template.render(context)

		# create a pdf
		pisa_status = pisa.CreatePDF(
		html, dest=response)
		# if error then show some funy view
		if pisa_status.err:
			return HttpResponse('We had some errors <pre>' + html + '</pre>')
		return response