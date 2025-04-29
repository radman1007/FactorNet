from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def features(request):
    return render(request, 'features.html')

def help(request):
    return render(request, 'help.html')