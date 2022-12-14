import re
import subprocess
from sys import platform

ICMP_HEADER_SIZE = 8
IP_HEADER_SIZE = 20


def ping(os_type, host, packet_size=1) -> bool:
    if not os_type:
        command = f'ping {host} -f -l {packet_size}'
    else:
        command = f'ping -M do -c 1 -s {packet_size} {host}'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    for line in iter(p.stdout.readline, b''):
        line = line.decode(encoding='utf-8')
        for error_message in ['message too long', '100.0% packet loss', 'packet size too large']:
            if error_message in line:
                return False
    code = p.wait()
    return code == 0


def mtu(os_type, host) -> int:
    l, r = 0, 10000
    while r - l > 1:
        m = (l + r) // 2
        if ping(os_type, host, m):
            l = m
        else:
            r = m
    return l + ICMP_HEADER_SIZE + IP_HEADER_SIZE


if __name__ == '__main__':
    try:
        os_type = 'win' not in platform.lower()

        host = ""
        host_regex = r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$"
        while not re.match(host_regex, host):
            host = input("Input host: ")

        if not ping(os_type, host, 0):
            print(host, " is not available or icmp is blocked")
            exit(0)

        print(f"MTU: {mtu(os_type, host)}")
    except Exception as e:
        print(f"Something wrong occurred: {e}")
