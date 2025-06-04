from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def chat(request):
    return render(request, 'chat.html')