from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, InvoiceViewSet, InvoiceItemViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'invoice-items', InvoiceItemViewSet, basename='invoiceitem')

urlpatterns = [
    path('create/', views.invoice_create_or_update, name='invoice_create'),
    path('edit/<int:pk>/', views.invoice_create_or_update, name='invoice_edit'),
    path('delete/<int:pk>/', views.invoice_delete_view, name='invoice_delete'),
    path('detail/<int:pk>/', views.invoice_detail_view, name='invoice_detail'),
    
    path('api/', include(router.urls)),
]