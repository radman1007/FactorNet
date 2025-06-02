from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import User

@login_required
def index_control_panel(request):
    users = User.objects.all()
    context = {
        'users' : users,
    }
    return render(request, 'index_control_panel.html', context)