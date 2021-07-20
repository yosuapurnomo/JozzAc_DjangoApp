from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from product.models import ProductModel
from client.models import ClientModel
from eventContent.models import eventContentModel
from django.db.models import Q

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