from django.urls import path, re_path
from .views import loginAdmin, Logout, createUser, listUser, updateUser, updatePassword, DeleteUser

app_name = 'account'

urlpatterns = [
	path('login/', loginAdmin.as_view(), name='login'),
	path('logout/', Logout.as_view(), name='logout'),
	path('register/', createUser.as_view(), name='create'),
	path('list/', listUser.as_view(), name='list'),
	path('update/<pk>', updateUser.as_view(), name='update'),
	path('password/<pk>', updatePassword.as_view(), name='password'),
	path('delete/<pk>', DeleteUser.as_view(), name='delete'),
]