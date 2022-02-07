import os,re,requests,socket,fcntl,struct,ipaddress,dns.resolver


from flask import current_app

nic="enp2s0"

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s',bytes(nic,"utf-8")))[20:24])

def check_network_addr(local_ip,expect_network_addr):
    sub_network = ipaddress.ip_network(expect_network_addr,strict=False)
    ip_addr = ipaddress.ip_address(local_ip)
    if ip_addr in sub_network:
        return True
    else:
        return False


# 需要适配操作系统
def ping(remote_addr,count=4):
    # Linux下的特有实现
    res = os.popen("ping -c {} {}".format(count,remote_addr)).read()
    if re.search(" 0% packet loss",res):
        current_app.logger.info("ping {} count {} succ".format(remote_addr,count))
        return True
    current_app.logger.info("ping {} count {} fail".format(remote_addr,count))
    return False

# 需要适配操作系统
def change_ip(new_ip):
    try:
        os.popen("ip addr flush  dev {}".format({nic}))
        current_app.logger.info("ip addr flush  dev {}".format(nic))
        os.popen("ifconfig {} {}".format(nic,new_ip)).read()
        current_app.logger.info("ifconfig {} {}".format(nic,new_ip))
    except:
        return False
    return True

# 需要适配操作系统
def renew_ip():
    # Linux下的特有实现
    os.popen("pkill -9 -f {}".format(nic))
    os.popen("dhclient {}".format(nic))
    current_app.logger.info("dhclient {}".format(nic))

# 需要适配操作系统
def network_bench(iperf_addr):
    # Linux下的特有实现
    data=os.popen("iperf3 -t 5 -c {}".format(iperf_addr)).readlines()
    if list(filter(lambda x:"error" in x,data)):
        return None
    sender = list(filter(lambda x:"sender" in x, data))
    receiver = list(filter(lambda x:"receiver" in x, data))
    return (sender,receiver)

def curl(url):
    print(url)
    res = requests.get(url)
    echo = {"status_code":res.status_code,"response_content":res.content}
    return echo

def resolve_dns(d):
    domain = d
    qtype = 'A'
    answer = dns.resolver.query(domain,qtype, raise_on_no_answer=False)
    if answer.rrset is not None:
        return (str(i) for i in answer.rrset.items)
    return None

def trace_route():
    pass

def port_test():
    pass

def dns_test():
    pass

def valied_string(payload):
    return re.search(r'[a-zA-Z0-9\-\./]*',payload,re.I).group()

# 需要适配操作系统
def sdwan_ping(remote_addr,count=4):
    # Linux下的特有实现
    res = os.popen("ping -c {} {}".format(count,remote_addr)).readlines()
    current_app.logger.info("ping -c {} {}".format(count,remote_addr))
    return list(filter(lambda x: "bytes from" in x,res))

def get_ip():
    all_ips = []
    for i in range(0,4):
        res=str(requests.get("http://cip.cc",headers={"User-Agent":"curl/7.29.0"}).content).split("\n")
        if len(res) > 1:
            (current_ip,) = re.search(r'IP\t: ([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})',res[0]).groups()
            all_ips.append(current_ip)
    if len(set(all_ips)) > 1:
        return True
    else:
        return False