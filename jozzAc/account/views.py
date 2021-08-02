from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from .forms import accountForm
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .models import Account
from .forms import accountForm, passwordForm, updateForm

# Create your views here.
class loginAdmin(LoginView):
	success_url = reverse_lazy('dasboardAdmin')
	template_name = 'account/login.html'
	query_string = True

	def get(self, request, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('dasboardAdmin')
		else:
			 self.extra_context = {
							'title':'LOGIN',
							'next':self.request.GET.get('next', "")
						}
		return self.render_to_response(self.get_context_data())

	def get_success_url(self):
		url = self.request.GET.get('next', False)
		if url is False:
			return self.success_url
		else:
			self.success_url = self.request.GET['next']
			if self.success_url == '':
				self.success_url = reverse_lazy('dasboardAdmin')
			return self.success_url


class Logout(LogoutView):
	next_page = reverse_lazy('account:login')


class createUser(CreateView):
	model = Account
	template_name = 'account/create.html'
	form_class = accountForm
	success_url = reverse_lazy('account:list')

class listUser(ListView):
	model = Account
	context_object_name = 'object'
	template_name = 'account/list.html'
	queryset = model.objects.filter(is_superuser=False)

class updateUser(UpdateView):
    model = Account
    context_object_name = 'object'
    template_name = "account/update.html"
    success_url = reverse_lazy('account:list')
    # fields = ['username', 'jabatan']
    form_class = updateForm
    pk_url_kwarg = 'pk'

class updatePassword(UpdateView):
	model = Account
	context_object_name = 'object'
	template_name = 'account/password.html'
	success_url = reverse_lazy('account:list')
	form_class = accountForm

	pk_url_kwarg = 'pk'

	def post(self, request, *args, **kwargs):
		print(self.request.POST)
		password1 = self.request.POST['password1']
		password2 = self.request.POST['password2']
		user = self.model.objects.get(pk=self.kwargs['pk'])
		if password1 == password2:
			user.set_password(password1)
			user.save()
		return redirect(self.success_url)

class DeleteUser(DeleteView):
    model = Account
    template_name = None
    success_url = reverse_lazy('account:list')