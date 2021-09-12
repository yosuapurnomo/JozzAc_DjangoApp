from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template, render_to_string

from xhtml2pdf import pisa
from django.db.models import Q, Count, Sum
import socket
from django import forms
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, TemplateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import SPKModel
from pesanan.models import InvoiceModel
from account.models import Account
from .forms import SPK_Form, SPK_Update_Status
from datetime import datetime

# Create your views here.
class SPK_Create(LoginRequiredMixin, CreateView):
	login_url = reverse_lazy('account:login')
	model = SPKModel
	template_name = 'SPK_teknisi/create.html'
	form_class = SPK_Form
	success_url = reverse_lazy('spk:invoiceView')

	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['lastSPK'] = self.model.objects.all().last()
	    context['invoice'] = InvoiceModel.objects.get(slug_Invoice=self.kwargs['slug'])
	    return context

	def get_initial(self):
		initial = super().get_initial()
		initial['pesanan'] = InvoiceModel.objects.get(slug_Invoice=self.kwargs['slug'])
		return initial

class SPK_Update(LoginRequiredMixin, UpdateView):
	login_url = reverse_lazy('account:login')
	model = SPKModel
	template_name = 'SPK_teknisi/update.html'
	form_class = SPK_Form
	success_url = reverse_lazy('spk:invoiceView')
	slug_url_kwarg = 'slug'
	slug_field = 'slug_SPK'
	extra_context = {
	'lastSPK': model.objects.all().last()
	# 'lastSPK': model.objects.all()
	}

class SPK_Delete(LoginRequiredMixin, DeleteView):
	login_url = reverse_lazy('account:login')
	model = SPKModel
	template_name = None
	success_url = reverse_lazy('spk:listSPK')
	slug_url_kwarg = 'slug'
	slug_field = 'slug_SPK'

	def get(self, request, **kwargs):
		try:
			data = self.model.objects.get(slug_SPK=kwargs['slug'])
			return redirect(reverse('spk:update', kwargs={"slug": kwargs['slug']}))
		except:
			return redirect('spk:listSPK')

class SPK_InvoiceView(LoginRequiredMixin, ListView):
	login_url = reverse_lazy('account:login')
	model = InvoiceModel
	template_name = 'SPk_teknisi/SPK_Invoice_View.html'
	context_object_name = 'object'
	queryset = model.objects.filter(SPK__isnull=True)

class SPK_Progress_List(LoginRequiredMixin, ListView):
	login_url = reverse_lazy('account:login')
	model = SPKModel
	template_name = 'SPk_teknisi/OnProgress.html'
	context_object_name = 'object'
	if model.objects.filter(status='PENDING') != None:
		queryset = model.objects.filter(status='PENDING')
	else:queryset = None

class searchSPK(LoginRequiredMixin, ListView):
	login_url = reverse_lazy('account:login')
	template_name = 'SPK_teknisi/searchSPK.html'
	model = SPKModel
	context_object_name = 'object'
	queryset = model.objects.order_by('tgl_input')

class list_SPK_teknisi(LoginRequiredMixin, ListView):
	login_url = reverse_lazy('account:login')
	model = SPKModel
	template_name = 'SPK_teknisi/list_SPK_teknisi.html'

	context_object_name = 'object'
	queryset = model.objects.filter(status='PENDING')

	def get(self, request, **kwargs):
		if self.request.user.jabatan == 'TEKNISI':
			self.queryset = self.model.objects.filter(status='PENDING', teknisi=self.request.user)
		return super().get(request, kwargs)

class SPK_UpdateStatus(LoginRequiredMixin, UpdateView):
	login_url = reverse_lazy('account:login')
	model = SPKModel
	template_name = 'SPK_teknisi/updateStatus.html'
	form_class = SPK_Update_Status
	success_url = reverse_lazy('spk:teknisiSPK')
	slug_url_kwarg = 'slug'
	slug_field = 'slug_SPK'

	def post(self, request, **kwargs):
		
		spk = self.model.objects.get(slug_SPK = self.kwargs['slug'])
		spk.status=self.request.POST.get('status') 
		spk.save()
		return redirect(self.success_url)

class cetakPDF(LoginRequiredMixin, View):
	login_url = reverse_lazy('account:login')
	model = SPKModel
	template_name = 'SPK_teknisi/cetakPDF.html'

	def get(self, request, **kwargs):
		objects = self.model.objects.get(slug_SPK=kwargs['slug'])
		client = objects.pesanan.clientINV
		context = {'object': objects,
					'client':client,
					'hostname' : request.META['HTTP_HOST']}
		title = objects.no_SPK
		

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

class cetakReport(LoginRequiredMixin, View):
	login_url = reverse_lazy('account:login')
	model = SPKModel
	template_name = 'SPK_teknisi/Report.html'

	def get(self, request, **kwargs):
		if self.request.GET.get('first', False) != False:
			data = self.model.objects.filter(tgl_input__range=[self.request.GET.get('first'), self.request.GET.get('last')])
			first = datetime.strptime(self.request.GET.get('first'), "%Y-%m-%d")
			last = datetime.strptime(self.request.GET.get('last'), "%Y-%m-%d")
			context = {
			'objects':data,'hostname' : request.META['HTTP_HOST'], 'first':datetime.strftime(first, "%d-%B-%Y"), 'last':datetime.strftime(last, "%d-%B-%Y")
			}
		else:
			print(self.model.objects.all())
			data = self.model.objects.all()
			context = {
			'objects':data,'hostname':request.META['HTTP_HOST']
			}
		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] = "inline; filename='LAPORAN SPK'"

		template = get_template(self.template_name)
		html = template.render(context)

		pisa_status = pisa.CreatePDF(html, dest=response)

		if pisa_status.err:
			return HttpResponse('We had some errors <pre>' + html + '</pre>')
		return response

class getSPKView(View):
	success_url = reverse_lazy('spk:listSPK')
	model = SPKModel

	def get(self, request):
		html_form = dict()
		if self.request.is_ajax():
			if self.request.GET.get('button_text') != "":
				data = self.model.objects.filter(no_SPK__contains=self.request.GET.get('button_text'))
				html_form["list_spk"] = render_to_string("SPK_teknisi/listSPK_View.html", {"spk":data})
				return JsonResponse(html_form)

		return redirect(self.success_url)