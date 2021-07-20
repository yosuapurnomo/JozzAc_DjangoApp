from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import eventContentModel
from account.models import Account
from .forms import eventForm

# Create your views here.
class ListContent(LoginRequiredMixin, ListView):
	login_url = reverse_lazy('account:login')
	model = eventContentModel
	context_object_name = 'object'
	template_name = 'eventContent/list.html'
	queryset = model.objects.all().order_by('tgl_upload')

class CreateContent(LoginRequiredMixin, CreateView):
	login_url = reverse_lazy('account:login')
	model = eventContentModel
	form_class = eventForm
	template_name = 'eventContent/add.html'
	success_url = reverse_lazy('eventContent:list')

	def get_initial(self):
		return {'admin':self.request.user}

class UpdateContent(LoginRequiredMixin, UpdateView):
	login_url = reverse_lazy('account:login')
	model = eventContentModel
	form_class = eventForm
	template_name = 'eventContent/update.html'
	success_url = reverse_lazy('eventContent:list')
	slug_field = 'slug_Content'
	slug_url_kwarg = 'slug'

	def get_initial(self):
		return {'admin':self.request.user}

class DeleteContent(LoginRequiredMixin, DeleteView):
	login_url = reverse_lazy('account:login')
	model = eventContentModel
	success_url = reverse_lazy('eventContent:list')
	slug_field = 'slug_Content'
	slug_url_kwarg = 'slug'

	def get(self, request, **kwargs):
		try:
			data = self.model.objects.get(slug_Content=kwargs['slug'])
			return redirect(reverse('eventContent:update', kwargs={"slug": kwargs['slug']}))
		except:
			return redirect('eventContent:list')