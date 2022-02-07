安装须知：
    1、Linux操作系统（需要提供ifconfig,ip,ping,pkill,dhclient,iperf3这些Linux命令命令）
    2、python3
安装步骤：
    python3 -m venv ob
    cd ob
    source bin/activate
    pip3 install requests
    pip3 install flask
    pip3 install dnspython
    bash observer/startup.sh
