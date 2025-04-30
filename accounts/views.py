from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model, logout
from django.contrib import messages
from django.views import View
from random import randint
from .models import OTP, UserProfile
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required
from invoices.models import Invoice
from django.db.models import Q


# برای ارسال پیامک OTP به Ghasedak
import ghasedakpack
sms = ghasedakpack.Ghasedak('YOUR_API_KEY')
YOUR_TEMPLATE_NAME_ON_GHASEDAK = 'YOUR_TEMPLATE_NAME'
good_line_number_for_sending_otp = '30005088'

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        phone_number = request.POST.get('phone_number')
        sent_otp = request.POST.get('sent_otp')

        if phone_number and not sent_otp:
            otp = str(randint(100000, 999999))
            request.session['otp'] = otp
            request.session['phone_number'] = phone_number

            # ذخیره کد OTP در دیتابیس
            OTP.objects.create(phone=phone_number, code=otp)

            try:
                sms.verification({
                    'receptor': phone_number,
                    'linenumber': good_line_number_for_sending_otp,
                    'type': '1',
                    'template': YOUR_TEMPLATE_NAME_ON_GHASEDAK,
                    'param1': otp
                })
                messages.success(request, "کد تایید ارسال شد.")
            except Exception as e:
                messages.error(request, f"مشکلی رخ داد: {e}")
                return redirect('login')

            return render(request, 'login.html', {'phone_number': phone_number})

        if sent_otp:
            saved_otp = request.session.get('otp')
            saved_phone = request.session.get('phone_number')

            # چک کردن کد OTP وارد شده
            if sent_otp == saved_otp and saved_phone:
                # بررسی اینکه آیا کاربر قبلاً ثبت نام کرده یا نه
                user = get_user_model().objects.filter(phone=saved_phone).first()
                if not user:
                    user = get_user_model().objects.create(phone=saved_phone)
                
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                del request.session['otp']
                return redirect('profile')
            else:
                messages.error(request, "کد وارد شده صحیح نیست.")

        return render(request, 'login.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


@login_required
def profile(request):
    if len(request.user.profiles.full_name) > 1:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    return render(request, 'profile.html')


@login_required
def dashboard(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    form = UserProfileForm(request.POST or None, request.FILES or None, instance=profile)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    issued_invoices = Invoice.objects.filter(user=request.user)

    search_query = request.GET.get('search_query', '').strip()
    status = request.GET.get('status')
    created_at = request.GET.get('created_at')

    if search_query:
        issued_invoices = issued_invoices.filter(
            Q(invoice_number__icontains=search_query) |
            Q(customer__full_name__icontains=search_query)
        )

    if status:
        issued_invoices = issued_invoices.filter(status=status)

    if created_at:
        issued_invoices = issued_invoices.filter(created_at__date=created_at)

    received_invoices = Invoice.objects.filter(customer__user=request.user)

    context = {
        'form': form,
        'issued_invoices': issued_invoices,
        'received_invoices': received_invoices,
        'profile': profile
    }

    return render(request, 'dashboard.html', context)