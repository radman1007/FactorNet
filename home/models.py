from django.db import models


class Contact(models.Model):
    full_name = models.CharField(max_length=255, verbose_name='نام کامل')
    email = models.EmailField(verbose_name='ایمیل')
    message = models.TextField(verbose_name='پیام')
    
    def __str__(self):
        return f"{self.full_name : {self.message}}"
    
    class Meta:
        verbose_name = "پیام"
        verbose_name_plural = "پیام ها"