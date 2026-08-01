import socket 
import sys
import time
from concurrent.futures import ThreadPoolExecutor

# Dictionary mapping common ports to their standard service names
COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    465: "SMTPS",
    587: "SMTP (Submission)",
    993: "IMAPS",
    995: "POP3S",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    8080: "HTTP-Proxy",
    8443: "HTTPS-Alt"
}

usage = "python3 port_scanner.py <target (ip or hostname)>"

print("-" * 100)
print("Python Port Scanner")
print("-" * 100)

if len(sys.argv) < 2:
    print(usage)
    sys.exit()
    
try:
    target = socket.gethostbyname(sys.argv[1])
except socket.gaierror:
    print("Name Resolution error") 
    sys.exit()

print("Scanning target:", target)

def scan_port(port):
    # Lookup the port name using socket module or fall back to the dictionary
    try:
        service_name = socket.getservbyport(port)
    except socket.error:
        service_name = COMMON_PORTS.get(port, "Unknown Service")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.5) 
    
    try:
        conn = s.connect_ex((target, port))
        if conn == 0:
            print(f"[+] Port {port:<5} ({service_name}) is OPEN")
        else:
            print(f"[-] Port {port:<5} ({service_name}) is CLOSED")
    except Exception:
        pass
    finally:
        s.close()

# Main Program Loop
while True:
    ports_to_scan = []

    print("\nChoose Scanning Option:")
    print("1. Custom Port Range")
    print("2. Common Ports Scan")
    print("3. Exit")
    choice = input("Enter choice (1, 2, or 3): ").strip()

    if choice == "1":
        try:
            start_port = int(input("Enter Start Port: "))
            end_port = int(input("Enter End Port: "))
            ports_to_scan = list(range(start_port, end_port + 1))
        except ValueError:
            print("[!] Please enter valid integer port numbers.")
            continue  

    elif choice == "2":
        ports_to_scan = list(COMMON_PORTS.keys())

    elif choice == "3":
        print("Exiting program.")
        sys.exit() 

    else:
        print("[!] Invalid choice. Please select 1, 2, or 3.")
        continue  
    
    scan_start_time = time.time()
    
    print(f"\n[i] Scanning {len(ports_to_scan)} ports with a safe thread pool...")

    # Maximum concurrent threads (100)
    MAX_THREADS = 100

    
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        executor.map(scan_port, ports_to_scan)

    scan_end_time = time.time()
    elapsed_time = round(scan_end_time - scan_start_time, 2)
    
    print(f"\nScan completed in {elapsed_time} seconds. Returning to main menu...")