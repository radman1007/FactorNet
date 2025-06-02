from accounts.models import User
from django.db.models import Q

def search_users(request):
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
    return context