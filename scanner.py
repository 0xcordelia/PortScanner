#!/usr/bin/env python3

import socket
import sys
import argparse
import threading
from datetime import datetime
from queue import Queue

print_lock = threading.Lock()
open_ports = []

def scan_port(target, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))
        sock.close()
        return result == 0
    except socket.gaierror:
        return False

def threader(target, timeout):
    while True:
        port = q.get()
        if scan_port(target, port, timeout):
            with print_lock:
                open_ports.append(port)
                print(f"Port {port}: Open")
        q.task_done()

q = Queue()

def main():
    global q
    parser = argparse.ArgumentParser(description="Simple port scanner")
    parser.add_argument("host", help="Target host to scan")
    parser.add_argument("-p", "--ports", help="Port range (e.g., 1-1000)", default="common")
    parser.add_argument("-t", "--timeout", type=int, help="Connection timeout in seconds", default=1)
    parser.add_argument("--threads", type=int, help="Number of threads", default=50)
    
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
    
    # Start threads
    for _ in range(args.threads):
        t = threading.Thread(target=threader, args=(target, args.timeout))
        t.daemon = True
        t.start()
    
    # Add ports to queue
    for port in ports:
        q.put(port)
    
    q.join()
    
    print("-" * 50)
    print(f"Scan completed at: {datetime.now()}")
    print(f"Found {len(open_ports)} open ports")

if __name__ == "__main__":
    main()