from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index_control_panel(request):
    return render(request, 'index_control_panel.html')