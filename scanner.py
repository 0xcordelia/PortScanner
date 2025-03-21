#!/usr/bin/env python3

import socket
import sys
from datetime import datetime

def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        sock.close()
        return result == 0
    except socket.gaierror:
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 scanner.py <host>")
        sys.exit(1)
    
    target = sys.argv[1]
    print(f"Starting port scan on {target}")
    print(f"Time started: {datetime.now()}")
    print("-" * 50)
    
    # Common ports to scan
    common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995]
    
    for port in common_ports:
        if scan_port(target, port):
            print(f"Port {port}: Open")

if __name__ == "__main__":
    main()