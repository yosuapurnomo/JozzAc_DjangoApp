from django.urls import path

from .views import produkView, productDetail, productCreate, productDelete

app_name = 'product'
urlpatterns = [
    path('admin/', produkView.as_view(), name='produkView'),
    path('admin/add/', productCreate.as_view(), name='produkCreate'),
    path('admin/detail/<slug:slug>/', productDetail.as_view(), name='produkDetail'),
    path('admin/delete/<slug:slug>/', productDelete.as_view(), name='produkDelete'),
]