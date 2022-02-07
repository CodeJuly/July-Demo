import json,requests,inspect

from common import *

def url_hijack(remote_addr):
    url = TARGET_ADDR+"url-hijack"
    payload = {"remote_addr":remote_addr}
    try:
        res=requests.post(url,json=payload)
    except:
        print("[FAIL][{}] request to {} payload:{} timeout".format(inspect.stack()[0][3],url,payload))
        return
    if res.status_code == 200:
        response = json.loads(res.content)
        if response.get("code") == 0:
            print("[SUCC][{}] request to {} payload:{} response_content:{}".format(inspect.stack()[0][3],url,payload,response))
        else:
            print("[FAIL][{}] request to {} payload:{} code:{}".format(inspect.stack()[0][3],url,payload,response.get("code")))
    else:
        print("[FAIL][{}] request to {} payload:{} httpcode:{}".format(inspect.stack()[0][3],url,payload,res.status_code))

url_hijack("https://www.baidu.com")