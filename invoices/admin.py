from django.contrib import admin
from .models import Customer, Invoice, InvoiceItem

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1  # تعداد آیتم‌های جدید قابل اضافه شدن
    readonly_fields = ('total_price',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'email')
    search_fields = ('full_name', 'phone_number', 'email')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'customer', 'status', 'created_at', 'due_date', 'total_display')
    list_filter = ('status', 'created_at', 'due_date')
    search_fields = ('invoice_number', 'customer__full_name')
    readonly_fields = ('subtotal_display', 'tax_amount_display', 'total_display')
    inlines = [InvoiceItemInline]

    def subtotal_display(self, obj):
        return obj.subtotal()
    subtotal_display.short_description = "مبلغ خام"

    def tax_amount_display(self, obj):
        return obj.tax_amount()
    tax_amount_display.short_description = "مالیات"

    def total_display(self, obj):
        return obj.total()
    total_display.short_description = "مبلغ نهایی"