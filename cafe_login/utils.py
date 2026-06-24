import requests
from django.conf import settings

def send_sms(phone, message):
    api_key = settings.KAVENEGAR_API_KEY
    URL = f"https://api.kavenegar.com/v1/{api_key}/sms/send.json"
    
    params = {
        'receptor' : phone,
        'message' : message,
        'sender' : "2000660110"
    }
    
    response = requests.post(URL, data=params)
    if response.status_code == 200:
        return response.json()
    else:
        return f"خطا در ارسال پیامک"