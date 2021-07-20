from django.urls import path, re_path
from .views import ListContent, CreateContent, UpdateContent, DeleteContent

app_name = 'eventContent'

urlpatterns = [
	path('admin/list/', ListContent.as_view(), name='list'),
	path('admin/add/', CreateContent.as_view(), name='add'),
	path('admin/update/<slug:slug>', UpdateContent.as_view(), name='update'),
	path('admin/delete/<slug:slug>', DeleteContent.as_view(), name='delete'),
]