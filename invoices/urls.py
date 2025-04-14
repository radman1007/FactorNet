from django.urls import path
from . import views

app_name = 'invoices'

urlpatterns = [
    path('list/', views.invoice_list_view, name='invoice_list'),
    path('crate/', views.invoice_create_or_update, name='invoice_create'),
    path('edit/<int:pk>/', views.invoice_create_or_update, name='invoice_edit'),
    path('delete/<int:pk>/', views.invoice_delete_view, name='invoice_delete'),
]
