from django.shortcuts import render, redirect
from .models import ProductModel
from .forms import productForm
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import ModelFormMixin
from django.urls import reverse_lazy, reverse

# Create your views here.
class productCreate(LoginRequiredMixin, CreateView):
	login_url = reverse_lazy('account:login')
	model = ProductModel
	template_name = 'product/productCreate.html'
	form_class = productForm
	success_url = reverse_lazy('product:produkView')

class produkView(LoginRequiredMixin, ListView):
	login_url = reverse_lazy('account:login')
	model = ProductModel
	template_name = 'product/productView.html'
	context_object_name = 'objects'

class productDetail(LoginRequiredMixin, UpdateView):
	login_url = reverse_lazy('account:login')
	model = ProductModel
	template_name = 'product/productDetail.html'
	form_class = productForm
	success_url = reverse_lazy('product:produkView')
	slug_url_kwarg = 'slug'
	slug_field = 'slugProduct'

	def get(self, request, **kwargs):
		print(kwargs['slug'])
		return super().get(request, **kwargs)

class productDelete(LoginRequiredMixin, DeleteView):
	login_url = reverse_lazy('account:login')
	model = ProductModel
	template_name = 'product/productDetail.html'
	success_url = reverse_lazy('product:produkView')
	slug_url_kwarg = 'slug'
	slug_field = 'slugProduct'

	def get(self, request, **kwargs):
		data = None
		try:
			data = self.model.objects.get(slugProduct=kwargs['slug'])
			return redirect(reverse('product:produkDetail', kwargs={"slug": kwargs['slug']}))
		except:
			return redirect('product:produkView')