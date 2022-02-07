import json,requests,inspect

from common import *

def dns_test():
    url = TARGET_ADDR+"setdns"
    data={"dns1":"10.168.1.1"}
    try:
        res=requests.post(url,json=data)
    except:
        print("[FAIL][{}] request to {} timeout".format(inspect.stack()[0][3],url))
        return

    if res.status_code == 200:
        print("[SUCC][{}] request to {} ".format(inspect.stack()[0][3],url))
    else:
        print("[FAIL][{}] request to {} ".format(inspect.stack()[0][3],url))

    return

dns_test()