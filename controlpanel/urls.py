from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_control_panel, name='index_control_panel')
]
