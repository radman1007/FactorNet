from django.shortcuts import render

def index_control_panel(request):
    return render(request, 'index_control_panel.html')