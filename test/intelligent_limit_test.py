import json,requests,inspect

from common import *

def intelligent_limit(iperf_addr,port=5201):
    url = TARGET_ADDR+"intelligent-limit"
    payload = {"iperf_addr":iperf_addr,"iperf_port":port}
    try:
        res=requests.post(url,json=payload)
    except:
        print("[FAIL][{}] request to {} payload:{} timeout".format(inspect.stack()[0][3],url,payload))
        return
    if res.status_code == 200:
        response = json.loads(res.content)
        if response.get("code") == 0:
            print("[SUCC][{}] request to {} payload:{} content:{}".format(inspect.stack()[0][3],url,payload,response.get("content")))
        else:
            print("[FAIL][{}] request to {} payload:{} code:{}".format(inspect.stack()[0][3],url,payload,response.get("code")))
    else:
        print("[FAIL][{}] request to {} payload:{} httpcode:{}".format(inspect.stack()[0][3],url,payload,res.status_code))

intelligent_limit("10.168.1.1")