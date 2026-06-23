from django.shortcuts import render, redirect
import re
import random
from .models import User
from .utils import send_sms
from django.contrib.auth import login
from django.contrib import messages
def login_code():
    return str(random.randint(100000, 999999))
def normal_phone(phone):
    digits = re.sub(r'\D', '', phone)
    if digits.startswith('0'):
        digits = '+98' + digits[1:]
    elif digits.startswith('98'):
        digits = '+' + digits
    else:
        digits = '+98' + digits
    return digits
    
def login_phone(request):
    if request.method == 'POST':
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password')
        action = request.POST.get('action')
        phone = normal_phone(phone)
        try:
            user = User.objects.get(phone=phone)
            user_exists = True
        except User.DoesNotExist:
            user_exists = False
            user = None
        if action == 'register':
            if user_exists:
                request.session['phone'] = phone
                messages.error(request,'این شماره قبلا ثبت نام کرده است')
                return render(request, cafe/login.html)
            if not user_exits:
                
                code = login_code()
                return code
                request.session['phone'] = phone
                request.session['code'] = code
                send_sms(phone, f"خوش آمدی به کافه ما❤️ کد فعالسازی شما:{code}")
                print(code)
                return redirect("request_code")
 
        elif action == 'password':
            return redirect("welcome")

    return render(request, 'cafe/login.html')
def verify_code(request):
    if request.method == 'POST':
        enter_code = request.POST.get('code', '')
        phone = request.session.get('phone')
        code_get = request.session.get('code')
        if enter_code == code_get:  
            user, created = User.objects.get_or_create(phone=phone)
            if created:
                return redirect("registry")
            login(request, user)
            return redirect("registry")
        else:
            messages.error(request, "کد وارد شده صحیح نمی باشد!")
            return redirect('verify_code')
    else:
        return render(request, 'cafe/verify_code.html')
def registry(request):
    phone = request.session.get("phone")
    if not phone:
        return redirect("login")
    if request.method == 'POST':
       
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        
        password = request.POST["password"]
        password_again = request.POST["password_again"]
        
        user = User.objects.get(phone=phone)
        user.first_name = first_name
        user.last_name = last_name
        if not(password == password_again):
            return redirect("registry")
        user.set_password(password)
        user.save()
        
        login(request, user)
        return redirect("welcome")
    return render(request, 'cafe/registry.html')
def welcome(request):
    return render(request, 'cafe/welcome.html')
        

