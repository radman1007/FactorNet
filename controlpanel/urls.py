from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_control_panel, name='index_control_panel'),
    path('charts/', views.chart_control_panel, name='chart_control_panel'),
    path('invoices/', views.invoices_control_panel, name='invoices_control_panel'),
    path('messages/', views.messages_control_panel, name='messages_control_panel'),
    path('transactions/', views.transactions_control_panel, name='transactions_control_panel'),
]
