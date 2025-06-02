from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import User
from django.db.models import Q

@login_required
def index_control_panel(request):
    users = User.objects.all()
    search_user = request.GET.get('search_user', '').strip()
    if search_user:
        users = User.objects.filter(
            Q(phone__icontains=search_user)|Q(profiles__full_name__icontains=search_user)
        )
    context = {
        'users' : users,
        'search_user' : search_user,
    }
    return render(request, 'index_control_panel.html', context)

@login_required
def chart_control_panel(request):
    return render(request, 'chart_control_panel.html')