from django.db import models
from config import settings
import uuid
from django.utils import timezone
from datetime import datetime


class Customer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="کاربر")
    full_name = models.CharField(max_length=255, verbose_name="نام کامل")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="شماره تلفن")
    national_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="کد ملی")
    email = models.EmailField(blank=True, null=True, verbose_name="ایمیل")
    address = models.TextField(blank=True, null=True, verbose_name="آدرس")

    class Meta:
        verbose_name = "مشتری"
        verbose_name_plural = "مشتری‌ها"

    def __str__(self):
        return self.full_name


class Invoice(models.Model):
    STATUS_CHOICES = (
        ('draft', 'پیش‌نویس'),
        ('final', 'نهایی'),
        ('paid', 'پرداخت شده'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="کاربر")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='invoices', verbose_name="مشتری")
    invoice_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name="شناسه فاکتور")
    invoice_number = models.CharField(max_length=50, blank=True, verbose_name="شماره فاکتور")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ایجاد")
    due_date = models.DateField(blank=True, null=True, verbose_name="تاریخ سررسید")
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="تخفیف")
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="درصد مالیات")
    notes = models.TextField(blank=True, null=True, verbose_name="یادداشت")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="وضعیت")

    class Meta:
        verbose_name = "فاکتور"
        verbose_name_plural = "فاکتور‌ها"
        
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            date_str = self.created_at.strftime('%Y%m%d')

            today_invoices = Invoice.objects.filter(
                created_at__date=self.created_at.date()
            )
            count_today = today_invoices.count() + 1

            self.invoice_number = f"FAK-{date_str}-{count_today:04d}"

        super().save(*args, **kwargs)
    def subtotal(self):
        return sum(item.total_price for item in self.items.all())

    def tax_amount(self):
        return (self.subtotal() - self.discount) * (self.tax_percent / 100)

    def total(self):
        return self.subtotal() - self.discount + self.tax_amount()

    def __str__(self):
        return f"فاکتور {self.invoice_number or self.invoice_id} برای {self.customer.full_name}"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items', verbose_name="فاکتور")
    name = models.CharField(max_length=255, verbose_name="نام آیتم")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    quantity = models.PositiveIntegerField(default=1, verbose_name="تعداد")
    unit_price = models.PositiveIntegerField(verbose_name="قیمت واحد")

    class Meta:
        verbose_name = "آیتم فاکتور"
        verbose_name_plural = "آیتم‌های فاکتور"

    @property
    def total_price(self):
        if self.quantity is not None and self.unit_price is not None:
            return self.quantity * self.unit_price
        return 0

    def __str__(self):
        return f"{self.name} - {self.quantity} × {self.unit_price}"