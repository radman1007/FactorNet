from django.urls import path
from . import views

app_name = 'invoices'

urlpatterns = [
    path('list/', views.invoice_list_view, name='invoice_list'),
    path('<int:pk>/edit/', views.invoice_update_view, name='invoice_edit'),
    path('<int:pk>/delete/', views.invoice_delete_view, name='invoice_delete'),
]
