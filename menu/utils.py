import secrets
import time
import re
from django.core.cache import cache

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
        ache.set(rl_key, 1, timeout=RATE_LIMIT_WINDOW)
        return True
    if attempts >= MAX_ATTEMPTS:
        return False 
    cache.incr(rl_key, delta=1)
    return True