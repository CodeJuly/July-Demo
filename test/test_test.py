import json,requests,inspect,dns.resolver
from xml import dom

from common import *

def test_test(remote_addr,expect_addr):
    url = TARGET_ADDR+"test"
    payload=""
    res=requests.post(url)
    print(res.content)
    # payload={"remote_addr":remote_addr,"expect_addr":expect_addr}
    # try:
        
    # except:
    #     print("[FAIL][{}] request to {} timeout".format(inspect.stack()[0][3],url))
    #     return
    # if res.status_code == 200:
    #     response = json.loads(res.content)
    #     print(res.content)
    #     if response.get("code") == 0:
    #         print("[SUCC][{}] request to {} payload:{} content:{}".format(inspect.stack()[0][3],url,payload,response.get("content")))
    #     else:
    #         print("[FAIL][{}] request to {} payload:{} code:{}".format(inspect.stack()[0][3],url,payload,response.get("code")))
    # else:
    #     print("[FAIL][{}] request to {} ".format(inspect.stack()[0][3],url))

    # return

test_test("www.baidu.com","180.101.49.12")