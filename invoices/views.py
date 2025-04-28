from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Customer, Invoice, InvoiceItem
from .forms import InvoiceForm, InvoiceItemFormSet
from django.core.mail import EmailMessage
from django.conf import settings
from .utils import *
from accounts.models import UserProfile
from django.db.models import Q
from rest_framework import viewsets
from .serializers import CustomerSerializer, InvoiceSerializer, InvoiceItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

@login_required
def invoice_list_view(request):
    invoices = Invoice.objects.filter(customer=request.user).order_by('-created_at')
    context = {
        'invoices' : invoices
    }
    return render(request, 'invoice_list.html', context)

@login_required
def invoice_create_or_update(request, pk=None):
    if pk:
        invoice = get_object_or_404(Invoice, pk=pk, user=request.user)
        profile = get_object_or_404(UserProfile, user=request.user)
    else:
        invoice = None
        profile = None

    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        formset = InvoiceItemFormSet(request.POST, instance=invoice)
        if form.is_valid() and formset.is_valid():
            invoice = form.save(commit=False)
            invoice.user = request.user
            invoice.save()
            formset.instance = invoice
            formset.save()
            form.save()

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
        
    context = {
        'invoice' : invoice,
        'profile' : profile,
        'form': form,
        'formset': formset,
        'is_edit': pk is not None
    }

    return render(request, 'invoice_create.html', context)
    
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


@login_required
def invoice_detail_view(request, pk):
    invoice = get_object_or_404(
        Invoice.objects.select_related('customer'),
        Q(pk=pk) & (Q(user=request.user) | Q(customer__user=request.user))
    )
    
    signature_url = None
    try:
        profile = UserProfile.objects.get(user=invoice.user)
        if profile.signature:
            signature_url = profile.signature.url
    except UserProfile.DoesNotExist:
        pass
    
    context = {
        'invoice': invoice,
        'signature_url': signature_url,
    }

    return render(request, 'invoice_detail.html', context)


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("شما اجازه ویرایش این مشتری را ندارید.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("شما اجازه حذف این مشتری را ندارید.")
        instance.delete()


class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("شما اجازه ویرایش این فاکتور را ندارید.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("شما اجازه حذف این فاکتور را ندارید.")
        instance.delete()


class InvoiceItemViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InvoiceItem.objects.filter(invoice__user=self.request.user)

    def perform_create(self, serializer):
        invoice = serializer.validated_data.get('invoice')
        if invoice.user != self.request.user:
            raise PermissionDenied("شما اجازه افزودن آیتم به این فاکتور را ندارید.")
        serializer.save()

    def perform_update(self, serializer):
        if serializer.instance.invoice.user != self.request.user:
            raise PermissionDenied("شما اجازه ویرایش این آیتم فاکتور را ندارید.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.invoice.user != self.request.user:
            raise PermissionDenied("شما اجازه حذف این آیتم فاکتور را ندارید.")
        instance.delete()