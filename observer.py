from flask import Flask,jsonify,request

import os,json

from url_action import *
from common import *

app = Flask(__name__)

#DNS全局设置
@app.route("/setdns",methods=["GET","POST"])
def setdns():
    res = {"code":1,"msg":"unknow","action":SET_DNS}
    if request.method == "POST":
        req=json.loads(request.get_data())
        dns1=req.get("dns1")
        dns2=req.get("dns2")
        conditions= []
        if dns1:
            conditions.append(len(list(filter(lambda x:"nameserver {}\n".format(dns1) in x,open("/etc/resolv.conf").readlines())))) 
        if dns2:
            conditions.append(len(list(filter(lambda x:"nameserver {}\n".format(dns2) in x,open("/etc/resolv.conf").readlines()))))
        if not filter(lambda x: x==0,conditions):
            res["msg"]="succ" 
        res["msg"]="fail" 
        res["code"]=0
        return jsonify(res)
    else:
        return jsonify(res)
    
#网络配置
@app.route("/wan-setting",methods=["POST"])
def wan_setting():
    res = {"code":1,"msg":"unknow","action":WAN_SETTING}
    renew_ip()
    if ping("8.8.8.8"):
        res["msg"] = "succ"
        res["code"]=0
        return jsonify(res)
    else:
        res["msg"] = "fail"
        return jsonify(res)

@app.route("/vlan-list",methods=["POST"])
def vlan_list():
    res = {"code":1,"msg":"unknow","action":VLAN_LIST}
    if request.method == "POST":
        req=json.loads(request.get_data())
        expect_network_addr=req.get("network_addr")
        renew_ip()
        local_ip = get_local_ip()
        ok = check_network_addr(local_ip,expect_network_addr)
        if not ok:
            res["code"] = 2
            res["msg"] = "fail"
            return jsonify(res)
    if ping("8.8.8.8"):
        res["code"]=0
        res["msg"] = "succ"
        return jsonify(res)
    else:
        res["msg"] = "fail"
        return jsonify(res)

@app.route("/arp",methods=["POST"])
def arp_binding():
    res = {"code":1,"msg":"unknow","action":ARP}
    if request.method == "POST":
        req=json.loads(request.get_data())
        new_ip=req.get("new_ip")
        safe_addr = valied_string(new_ip)
        if safe_addr != new_ip:
            res["code"]=2
            return jsonify(res)
        if not change_ip(new_ip):
            res["code"]=3
            return jsonify(res)
        if ping("8.8.8.8"):
            res["msg"] = "succ"
            res["code"]=0
        else:
            res["code"]=4
            res["msg"] = "fail"
        return jsonify(res)
    else:
        return jsonify(res)


@app.route("/gre",methods=["POST"])
def gre():
    res = {"code":1,"msg":"unknow","action":GRE}
    if request.method == "POST":
        req=json.loads(request.get_data())
        remote_addr=req.get("remote_addr")
        safe_addr = valied_string(remote_addr)
        if safe_addr != remote_addr:
            res["code"]=2
            return jsonify(res)
        if ping(safe_addr):
            res["code"]=0
            res["msg"] = "succ"
        else:
            res["code"]=3
            res["msg"] = "fail"
        return jsonify(res)
    else:
        return jsonify(res)

@app.route("/ipsec",methods=["POST"])
def ipsec():
    res = {"code":1,"msg":"unknow","action":IPSEC}
    if request.method == "POST":
        req=json.loads(request.get_data())
        remote_addr=req.get("remote_addr")
        safe_addr = valied_string(remote_addr)
        if safe_addr != remote_addr:
            res["code"]=2
            return jsonify(res)
        if ping(safe_addr):
            res["code"]=0
            res["msg"] = "succ"
        else:
            res["code"]=3
            res["msg"] = "fail"
        return jsonify(res)
    else:
        return jsonify(res)

#加速管理
@app.route("/sdwan-accelerate",methods=["POST"])
def sdwan_accelerate():
    res = {"code":1,"msg":"unknow","action":IPSEC}
    if request.method == "POST":
        req=json.loads(request.get_data())
        remote_addr=req.get("remote_addr")
        safe_addr = valied_string(remote_addr)
        if safe_addr != remote_addr:
            res["code"]=2
            return jsonify(res)
        content = sdwan_ping(safe_addr)
        if content:
            res["code"]=0
            res["content"]= content
            res["msg"] = "succ"
        else:
            res["code"]=3
            res["msg"] = "fail"
        return jsonify(res)
    else:
        return jsonify(res)
    # network_bench()

@app.route("/sdwan-accelerate-enable",methods=["POST"])
def sdwan_accelerate_enable():
    res = {"code":1,"msg":"unknow","action":IPSEC}
    if request.method == "POST":
        req=json.loads(request.get_data())
        remote_addr=req.get("remote_addr")
        safe_addr = valied_string(remote_addr)
        if safe_addr != remote_addr:
            res["code"]=2
            return jsonify(res)
        content = sdwan_ping(safe_addr) 
        if content:
            res["code"]=0
            res["content"] = content
            res["msg"] = "succ"
        else:
            res["code"]=3
            res["msg"] = "fail"
        return jsonify(res)
    else:
        return jsonify(res)

#路由管理
@app.route("/bgp",methods=["POST"])
def bgp():
    res = {"code":1,"msg":"unknow","action":BGP}
    if request.method == "POST":
        req=json.loads(request.get_data())
        remote_addr=req.get("remote_addr")
        safe_addr = valied_string(remote_addr)
        if safe_addr != remote_addr:
            res["code"]=2
            return jsonify(res)
        if ping(safe_addr):
            res["code"]=0
            res["msg"] = "succ"
        else:
            res["code"]=3
            res["msg"] = "fail"
        return jsonify(res)
    else:
        return jsonify(res)

@app.route("/static-route",methods=["POST"])
def static_route():
    res = {"code":1,"msg":"unknow","action":STATIC_ROUTE}
    if request.method == "POST":
        req=json.loads(request.get_data())
        remote_addr=req.get("remote_addr")
        safe_addr = valied_string(remote_addr)
        if safe_addr != remote_addr:
            res["code"]=2
            return jsonify(res)
        if ping(safe_addr):
            res["code"]=0
            res["msg"] = "succ"
        else:
            res["code"]=3
            res["msg"] = "fail"
        return jsonify(res)
    else:
        return jsonify(res)

@app.route("/ospf",methods=["POST"])
def ospf():
    res = {"code":1,"msg":"unknow","action":OSPF}
    if request.method == "POST":
        req=json.loads(request.get_data())
        remote_addr=req.get("remote_addr")
        safe_addr = valied_string(remote_addr)
        if safe_addr != remote_addr:
            res["code"]=2
            return jsonify(res)
        if ping(safe_addr):
            res["code"]=0
            res["msg"] = "succ"
        else:
            res["code"]=3
            res["msg"] = "fail"
        return jsonify(res)
    else:
        return jsonify(res)

#防火墙
@app.route("/snat",methods=["POST"])
def snat():
    res = {"code":1,"msg":"unknow","action":SNAT}
    if request.method == "POST":
        req=json.loads(request.get_data())
        remote_addr=req.get("remote_addr")
        safe_addr = valied_string(remote_addr)
        if safe_addr != remote_addr:
            res["code"]=2
            return jsonify(res)
        if ping(safe_addr):
            res["code"]=0
            res["msg"] = "succ"
        else:
            res["code"]=3
            res["msg"] = "fail"
        return jsonify(res)
    else:
        return jsonify(res)

@app.route("/dnat",methods=["GET"])
def dnat():
    res = {"code":0,"msg":"now you are access the dnat web page!","action":DNAT}
    return jsonify(res)

#行为管理
@app.route("/basic-security",methods=["POST"])
def basic_security():
    res = {"code":1,"msg":"unknow","action":BASIC_SECURITY}
    if request.method == "POST":
        req=json.loads(request.get_data())
        remote_addr=req.get("remote_addr")
        safe_addr = valied_string(remote_addr)
        if safe_addr != remote_addr:
            res["code"]=2
            return jsonify(res)
        if ping(safe_addr):
            res["code"]=0
            res["msg"] = "succ"
        else:
            res["code"]=3
            res["msg"] = "fail"
        return jsonify(res)
    else:
        return jsonify(res)

@app.route("/url-hijack",methods=["POST"])
def url_hijack():
    res = {"code":1,"msg":"unknow","action":URL_HIJACK}
    if request.method == "POST":
        req=json.loads(request.get_data())
        remote_addr=req.get("remote_addr")
        content = curl(remote_addr)
        # print(content)
        if content:
            res["code"]=0
            res["msg"] = "succ"
            # res["content"] = content
        else:
            res["code"]=2
            res["msg"] = "fail"
        return jsonify(res)
    else:
        return jsonify(res)

@app.route("/l7-security",methods=["POST"])
def l7_security():
    # curl()
    # dingtalk这些怎么测？
    pass

#智能流控
@app.route("/qos",methods=["POST"])
def qos():
    dingtalk()
    ftp()
    # 其他协议
    pass

@app.route("/wan-policy",methods=["POST"])
def wan_policy():
    res = {"code":0,"msg":"SUCC","action":WAN_POLICY}
    if get_ip():
        return jsonify(res)
    else:
        res["msg"] = "FAIL"
        return jsonify(res)

@app.route("/intelligent-limit",methods=["POST"])
def intelligent_limit():
    res = {"code":1,"msg":"unknow","action":INTELLIGENT_LIMIT}
    if request.method == "POST":
        req=json.loads(request.get_data())
        iperf_addr=req.get("iperf_addr")
        if not iperf_addr:
            res["code"]=2
            return jsonify(res)
        safe_addr = valied_string(iperf_addr)
        result = network_bench(safe_addr)
        if result:
            res["code"]=0
            res["msg"] = "succ"
            res["content"] = result
        else:
            res["code"]=3
            res["msg"] = "fail"
        return jsonify(res)
    else:
        return jsonify(res)

#高级功能
@app.route("/dns",methods=["POST"])
def dns():
    res = {"code":1,"msg":"unknow","action":DNS}
    if request.method == "POST":
        req=json.loads(request.get_data())
        remote_addr=req.get("remote_addr")
        expect_addr=req.get("expect_addr")
        result = resolve_dns(remote_addr)
        result = list(result)
        if expect_addr in result:
            res["code"]=0
            res["msg"] = "succ"
        else:
            res["code"]=2
            res["msg"] = "fail"
        return jsonify(res)
    else:
        return jsonify(res)

@app.route("/network-security",methods=["POST"])
def network_security():
    # 未知功能(需要配合wifi来测试相关功能)
    curl()

@app.route("/d-dns",methods=["POST"])
def d_dns():
    # 未知功能，本质是反向代理
    pass

@app.route("/sase",methods=["POST"])
def sase():
    res = {"code":0,"msg":"now you are access the sase web page!","action":SASE}
    return jsonify(res)


@app.route("/test",methods=["POST"])
def t():
    l=['180.101.49.11', '180.101.49.12']
    a="180.101.49.12"
    if a in l:
        return "match"
    else:
        return "not match"