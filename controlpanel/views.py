from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def index_control_panel(request):
    if not request.user.is_staff:
        return redirect('index')
    return render(request, 'index_control_panel.html')

@login_required
def chart_control_panel(request):
    if not request.user.is_staff:
        return redirect('index')
    return render(request, 'chart_control_panel.html')