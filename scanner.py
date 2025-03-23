#!/usr/bin/env python3

import socket
import sys
import argparse
from datetime import datetime

def scan_port(target, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))
        sock.close()
        return result == 0
    except socket.gaierror:
        return False

def main():
    parser = argparse.ArgumentParser(description="Simple port scanner")
    parser.add_argument("host", help="Target host to scan")
    parser.add_argument("-p", "--ports", help="Port range (e.g., 1-1000)", default="common")
    parser.add_argument("-t", "--timeout", type=int, help="Connection timeout in seconds", default=1)
    
    args = parser.parse_args()
    
    target = args.host
    print(f"Starting port scan on {target}")
    print(f"Time started: {datetime.now()}")
    print("-" * 50)
    
    # Determine ports to scan
    if args.ports == "common":
        ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995]
    elif "-" in args.ports:
        start, end = map(int, args.ports.split("-"))
        ports = range(start, end + 1)
    else:
        ports = [int(args.ports)]
    
    for port in ports:
        if scan_port(target, port, args.timeout):
            print(f"Port {port}: Open")

if __name__ == "__main__":
    main()