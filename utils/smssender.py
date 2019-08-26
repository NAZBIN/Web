import requests

def send(mobile,captcha):
    url = "http://v.juhe.cn/sms/send"
    #参数
    params = {
        "mobile":mobile,
        "tpl_id": "178954",
        "tpl_value": "#code#="+captcha,
        "key": "6eeae359ea78a0733d04ec509e76c561",
    }
    response = requests.get(url,params=params)
    result = response.json()
    if result['error_code']==0:
        return True
    else:
        return False