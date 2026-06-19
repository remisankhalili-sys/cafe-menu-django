from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.core.cache import cache
from . import utils
from .utils import phone_number, valid_phone, otp_key, OTP_TTL, check_rate_limit, send_sms, send_general_sms
import random

# Create your views here.
def otp_code(length=6):
    password = ''
    for i in range(length):
        number = random.randint(0, 9)
        password = password + str(number)
    return password

def send_otp_view(request):

    error = None
    if request.method == 'POST':
        phone_numbers = request.POST.get('phone')
        if not phone_numbers:
            error = 'شماره تلفن را وارد کنید'
        else:
            normalized_phone = phone_number(phone_numbers) 
            if not valid_phone(normalized_phone):
                error = 'شماره تلفن معتبر نیست'
            elif not check_rate_limit(normalized_phone):
                error = 'تعداد درخواست ها بیشتر از حد مجاز است'
            else:

                generated_otp = otp_code()
                cache_key = otp_key(normalized_phone)
                cache.set(cache_key, generated_otp, timeout=OTP_TTL)
                
                base_url = reverse('verify_otp')
                return redirect(f"{base_url}?phone={normalized_phone}")
    return render(request, 'menu/send_otp.html', {'error': error})

from django.contrib.auth import login
from django.contrib.auth.models import User

def verify_otp_view(request):
    error = None
    success = None
    
    phone = request.GET.get('phone', '')
    
    if request.method == 'POST':
        phone = request.POST.get('phone')
        otp_entered = request.POST.get('otp')
        
        if not phone or not otp_entered:
            error = 'لطفاً شماره تلفن و کد تأیید را وارد کنید'
        else:
            normalized_phone = phone_number(phone)
            cache_key = otp_key(normalized_phone)
            stored_otp = cache.get(cache_key)
            
            if not stored_otp:
                error = 'کد منقضی شده است. لطفاً مجدداً درخواست کد دهید'
            elif otp_entered != stored_otp:
                error = 'کد تأیید نادرست است'
            else:
                
                cache.delete(cache_key)
                
               
                try:
                    user = User.objects.get(username=normalized_phone)
                except User.DoesNotExist:
                    user = User.objects.create_user(username=normalized_phone)
                    user.set_unusable_password()  
                    user.save()
                login(request, user)
                
                return redirect('')  
    return render(request, 'menu/verify_otp.html', {
        'error': error,
        'success': success,
        'phone': phone
    })
def send_sms_view(request):
    if request.method == "POST":
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        normal_phone = phone_number(phone)
        if not valid_phone(normal_phone):
            error = 'شماره معتبر نیست'
            return render(request, 'send_sms.html', {'error': error})
        if not message:
            error = 'متن پیام نمی تواند خالی باشد'
            return render(request, 'send_sms.html', {'error': error})
        success_send = send_general_sms(normal_phone, message)
        if success_send:
            success_message = 'پیامک با موفقیت ارسال شد'
            return render(request, 'send_sms.html', {'success_message': success_message})
        else:
            error = 'لطفا دوباره تلاش کنید'
            return render(request, 'send_sms.html', {'error': error})
            
    else:
        
        return render(request, 'send_sms.html')
    