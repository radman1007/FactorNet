from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def features(request):
    return render(request, 'features.html')

def guide(request):
    return render(request, 'guide.html')