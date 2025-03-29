#!/usr/bin/env python3

import socket
import sys
import argparse
import threading
import json
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

def threader(target, timeout, quiet=False):
    while True:
        port = q.get()
        if scan_port(target, port, timeout):
            with print_lock:
                open_ports.append(port)
                if not quiet:
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
    parser.add_argument("-o", "--output", choices=["text", "json"], help="Output format", default="text")
    parser.add_argument("-q", "--quiet", action="store_true", help="Quiet mode - only show final results")
    
    args = parser.parse_args()
    
    target = args.host
    start_time = datetime.now()
    
    if not args.quiet:
        print(f"Starting port scan on {target}")
        print(f"Time started: {start_time}")
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
        t = threading.Thread(target=threader, args=(target, args.timeout, args.quiet))
        t.daemon = True
        t.start()
    
    # Add ports to queue
    for port in ports:
        q.put(port)
    
    q.join()
    
    end_time = datetime.now()
    duration = end_time - start_time
    
    if args.output == "json":
        result = {
            "target": target,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_seconds": duration.total_seconds(),
            "open_ports": sorted(open_ports),
            "total_open_ports": len(open_ports)
        }
        print(json.dumps(result, indent=2))
    else:
        if not args.quiet:
            print("-" * 50)
        print(f"Scan completed at: {end_time}")
        print(f"Duration: {duration}")
        print(f"Found {len(open_ports)} open ports")
        if open_ports:
            print(f"Open ports: {sorted(open_ports)}")

if __name__ == "__main__":
    main()