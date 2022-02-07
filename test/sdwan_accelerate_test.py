import json,requests,inspect

from common import *

def sdwan_accelerate(remote_addr):
    url = TARGET_ADDR+"sdwan-accelerate"
    payload = {"remote_addr":remote_addr}
    try:
        res=requests.post(url,json=payload)
    except:
        print("[FAIL][{}] request to {} payload:{} timeout".format(inspect.stack()[0][3],url,payload))
        return
    if res.status_code == 200:
        response = json.loads(res.content)
        if response.get("code") == 0:
            print("[SUCC][{}] request to {} payload:{}".format(inspect.stack()[0][3],url,payload))
        else:
            print("[FAIL][{}] request to {} payload:{} code:{}".format(inspect.stack()[0][3],url,payload,response.get("code")))
    else:
        print("[FAIL][{}] request to {} payload:{} httpcode:{}".format(inspect.stack()[0][3],url,payload,res.status_code))

sdwan_accelerate("8.8.8.8")