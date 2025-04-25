from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from datetime import timedelta


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('Phone number is required')
        user = self.model(phone=phone, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=15, unique=True, verbose_name='شماره تلفن')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_staff = models.BooleanField(default=False, verbose_name='کارمند')

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"


class OTP(models.Model):
    phone = models.CharField(max_length=11, verbose_name='شماره تلفن')
    code = models.CharField(max_length=6, verbose_name='کد تایید')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    def is_valid(self):
        return self.created_at >= timezone.now() - timedelta(minutes=2)

    def __str__(self):
        return f"{self.phone} - {self.code}"

    class Meta:
        verbose_name = "کد تایید"
        verbose_name_plural = "کدهای تایید"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profiles', verbose_name='کاربر')
    full_name = models.CharField(max_length=255, verbose_name='نام کامل')
    email = models.EmailField(blank=True, null=True, verbose_name='ایمیل')
    address = models.TextField(blank=True, null=True, verbose_name='آدرس')
    logo = models.ImageField(upload_to='logos/', blank=True, null=True, verbose_name='لوگوی فروشنده')
    signature = models.ImageField(upload_to='signatures/', blank=True, null=True, verbose_name='امضای دیجیتال')

    def __str__(self):
        return self.full_name or self.user.phone

    class Meta:
        verbose_name = "پروفایل"
        verbose_name_plural = "پروفایل‌ها"