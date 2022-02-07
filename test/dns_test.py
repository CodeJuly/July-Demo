import json,requests,inspect,dns.resolver
from xml import dom

from common import *

def dns_test(remote_addr,expect_addr):
    url = TARGET_ADDR+"dns"
    payload={"remote_addr":remote_addr,"expect_addr":expect_addr}
    try:
        res=requests.post(url,json=payload)
    except:
        print("[FAIL][{}] request to {} timeout".format(inspect.stack()[0][3],url))
        return
    if res.status_code == 200:
        response = json.loads(res.content)
        print(res.content)
        if response.get("code") == 0:
            print("[SUCC][{}] request to {} payload:{} content:{}".format(inspect.stack()[0][3],url,payload,response.get("content")))
        else:
            print("[FAIL][{}] request to {} payload:{} code:{}".format(inspect.stack()[0][3],url,payload,response.get("code")))
    else:
        print("[FAIL][{}] request to {} ".format(inspect.stack()[0][3],url))

    return

dns_test("www.baidu.com","180.101.49.12")


def resolve_dns(d):
    domain = d
    qtype = 'A'
    answer = dns.resolver.query(domain,qtype, raise_on_no_answer=False)
    if answer.rrset is not None:
        return (str(i) for i in answer.rrset.items)
    return None

def local_dns_test(domain,expect_addr):
    result = resolve_dns(domain)
    if expect_addr in list(result):
        print(True)
    else:
        print(False)

# local_dns_test("www.baidu.com","180.101.49.12")