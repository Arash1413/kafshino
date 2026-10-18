import requests
import json
from decouple import config

def send_otp_sms(mobile, code):
    url = "https://api.sms.ir/v1/send/verify"
    
    payload = json.dumps({
        "mobile": mobile,
        "templateId": 886831,  # شناسه قالبی که در عکس فرستادید
        "parameters": [
            {
                "name": "Code", # نام متغیری که در پنل sms.ir تعریف کردید
                "value": str(code)
            }
        ]
    })
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'text/plain',
       
        'x-api-key': config('x-api-key')
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.status_code == 200
    except:
        return False