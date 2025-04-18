from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Invoice
from django.http import HttpResponseForbidden
from .forms import InvoiceForm, InvoiceItemFormSet
from django.core.mail import EmailMessage
from django.conf import settings
from .utils import *

@login_required
def invoice_list_view(request):
    invoices = Invoice.objects.filter(customer=request.user).order_by('-created_at')
    context = {
        'invoices' : invoices
    }
    return render(request, 'invoice_list.html', context)

@login_required
def invoice_create_or_update(request, pk=None):
    # تنظیم invoice بر اساس وجود pk
    if pk:
        invoice = get_object_or_404(Invoice, pk=pk, user=request.user)
    else:
        invoice = None

    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        formset = InvoiceItemFormSet(request.POST, instance=invoice)
        if form.is_valid() and formset.is_valid():
            invoice = form.save(commit=False)
            invoice.user = request.user
            invoice.save()
            formset.instance = invoice
            formset.save()

            if invoice.status == 'final':
                image_path = render_invoice_to_image(invoice)

                seller_email = request.user.email
                customer_email = invoice.customer.email if invoice.customer else None

                subject = f"Invoice {invoice.invoice_number}"
                message = "Dear Customer, please find attached the image of your invoice."
                email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL)
                
                email.attach_file(image_path)
                email.to = [seller_email]
                email.send()

                if customer_email:
                    email.to = [customer_email]
                    email.send()

            return redirect('invoice_list')
    else:
        form = InvoiceForm(instance=invoice)
        formset = InvoiceItemFormSet(instance=invoice)

    return render(request, 'invoice_create.html', {
        'form': form,
        'formset': formset,
        'is_edit': pk is not None
        })
    
@login_required
def invoice_delete_view(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, user=request.user)

    if invoice.status == 'final':
        return HttpResponseForbidden("حذف فاکتور نهایی مجاز نیست.")

    if request.method == 'POST':
        invoice.delete()
        return redirect('invoice_list')

    context = {
        'invoice': invoice
    }
    
    return render(request, 'invoice_confirm_delete.html', context)