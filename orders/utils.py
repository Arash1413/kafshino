import requests
import json

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
        'x-api-key': 'Rwa9Fc0qqhUyGvG1sl6f9h5IcCUOr38B4CJnH64g7SPRi0nd' # کلید عملیاتی (Production) خود را اینجا بگذارید
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.status_code == 200
    except:
        return False