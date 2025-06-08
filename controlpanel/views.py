from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from invoices.models import Invoice
from django.db.models import Q

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

@login_required
def invoices_control_panel(request):
    if not request.user.is_staff:
        return redirect('index')
    invoices = Invoice.objects.all()

    search_query = request.GET.get('search_query', '').strip()
    status = request.GET.get('status')
    created_at = request.GET.get('created_at')

    if search_query:
        invoices = invoices.filter(
            Q(invoice_number__icontains=search_query) |
            Q(customer__full_name__icontains=search_query)
        )

    if status:
        invoices = invoices.filter(status=status)

    if created_at:
        invoices = invoices.filter(created_at__date=created_at)

    context = {
        'invoices' : invoices
    }
    return render(request, 'invoices_control_panel.html', context)

@login_required
def messages_control_panel(request):
    return render(request, 'messages_control_panel.html')