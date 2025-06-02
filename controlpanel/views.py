from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import User
from django.db.models import Q

@login_required
def index_control_panel(request):
    return render(request, 'index_control_panel.html')

@login_required
def chart_control_panel(request):
    return render(request, 'chart_control_panel.html')