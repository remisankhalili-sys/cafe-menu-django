import secrets
import time
import re
from django.core.cache import cache
from kavenegar import KavenegarAPI, APIException, HTTPException
from django.conf import settings
import logging

logger = logging.getLogger(__name__)
OTP_LENGTH = 6
OTP_TTL = 120  
MAX_ATTEMPTS = 3
RATE_LIMIT_COUNT = 3
RATE_LIMIT_WINDOW = 600 
RL_CACHE_PREFIX = "rl_" 

def phone_number(phone):
    
    digits = re.sub(r'\D', '', phone)
    if digits.startswith('0'):
        digits = '+98' + digits[1:]
    elif digits.startswith('98'):
        digits = '+' + digits
    else:
        digits = '+98' + digits
        
    return digits

def valid_phone(phone):
    
    try:
        normal_phone_number = phone_number(phone)
    except Exception:
        return False
        
    result = re.match(r'^\+?[0-9]+$', normal_phone_number)
    phone_length = len(normal_phone_number.lstrip('+'))
    
    if not result:
        return False
    if 10 <= phone_length <= 15:
        return True
    return False
def otp_key(phone):
    return 'otp_' + phone

def rate_limiting(phone):
    return f"{RL_CACHE_PREFIX}{phone}"
def check_rate_limit(phone):
    rl_key = rate_limiting(phone)
    result = cache.get(rl_key)
    if result is None:
        create = cache.set(rl_key, 1, timeout=RATE_LIMIT_WINDOW)
        return True
    try:
        attempts = int(result)
    except (ValueError, TypeError):
        cache.set(rl_key, 1, timeout=RATE_LIMIT_WINDOW)
        return True
    if attempts >= MAX_ATTEMPTS:
        return False 
    cache.incr(rl_key, delta=1)
    return True

def send_sms(phone_number, otp_code):
    try:
        api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
        message = f"کد تایید شما:{otp_code}"
        params = {'sender':settings.KAVENEGAR_SENDER, 'receptor':phone_number, 'message':message}
        response = api.sms_send(params)
        logger.info(f"پیام با موفقیت به شماره{phone_number} ارسال شد")
        return True
    except APIException as error:
        print("APIException:", error)
        return False
    except HTTPException as error:
        logger.error(f"خطا سرور{error}")
        print("HTTPException:", error)
        return False
def send_general_sms(phone_number, message):
    pass
    