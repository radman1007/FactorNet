from django.shortcuts import render, redirect
from .models import Contact

def index(request):
    return render(request, 'index.html')

def features(request):
    return render(request, 'features.html')

def help(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        Contact.objects.create(
            full_name=full_name,
            email=email,
            message=message
        )
        return redirect('index')
    return render(request, 'help.html')