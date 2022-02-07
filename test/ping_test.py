import json,requests,inspect

from common import *

def ping_test(url,remote_addr):
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


def bpg_test(remote_addr):
    url = TARGET_ADDR+"bgp"
    ping_test(url,remote_addr)


bpg_test("8.8.4.4")