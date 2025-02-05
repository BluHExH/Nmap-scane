import os
import socket
from datetime import datetime
import threading

# Function to print the banner
def print_banner():
    os.system("clear")
    print("\033[1;32m")
    print("""
      ██████╗ ███████╗██╗  ██╗
      ██╔══██╗██╔════╝██║  ██║
      ██║  ██║███████╗███████║
      ██║  ██║╚════██║██╔══██║
      ██████╔╝███████║██║  ██║
      ╚═════╝ ╚══════╝╚═╝  ╚═╝
       HEX HACKER TOOL (MAX)
    """)
    print("\033[0m")

# Function to scan a single port
def scan_port(target, port, results):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(0.5)
        result = s.connect_ex((target, port))
        if result == 0:
            results.append(f"[OPEN] Port {port}")
        s.close()
    except:
        pass

# Function to scan a target with maximum port range
def scan_target(target, start_port, end_port, save_report):
    print(f"\n[+] Scanning Target: {target}")
    print(f"[+] Port Range: {start_port}-{end_port}")
    print(f"[+] Scan started at: {datetime.now()}\n")
   
    results = []  # To store scan results
    threads = []

    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(target, port, results))
        threads.append(t)
        t.start()

        # Limit threads to avoid resource overload
        if len(threads) > 1000:  # Max 1000 threads at once
            for t in threads:
                t.join()
            threads = []

    for t in threads:
        t.join()

    # Print and save results
    if results:
        for result in results:
            print(result)
        if save_report:
            with open("scan_report_max.txt", "a") as file:
                file.write(f"\nScan Report for {target} ({datetime.now()}):\n")
                file.write("\n".join(results) + "\n")
            print(f"\n[+] Scan results saved to 'scan_report_max.txt'.")
    else:
        print("[-] No open ports found.")

# Function to scan a large network range (CIDR)
def scan_network(cidr, save_report):
    print(f"\n[+] Scanning Network Range: {cidr}")
    print(f"[+] Scan started at: {datetime.now()}\n")
   
    try:
        network, subnet = cidr.split('/')
        subnet = int(subnet)
    except ValueError:
        print("[-] Invalid CIDR format.")
        return

    base_ip = network.split('.')
    base_ip = '.'.join(base_ip[:3])
    results = []

    for i in range(1, 256):
        target = f"{base_ip}.{i}"
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(0.5)
            result = s.connect_ex((target, 80))  # Checking HTTP port (80)
            if result == 0:
                results.append(f"[LIVE] {target}")
                print(f"[LIVE] {target}")
            s.close()
        except:
            pass

    # Save network scan report
    if save_report:
        with open("network_scan_report_max.txt", "a") as file:
            file.write(f"\nNetwork Scan Report for {cidr} ({datetime.now()}):\n")
            file.write("\n".join(results) + "\n")
        print(f"\n[+] Network scan results saved to 'network_scan_report_max.txt'.")

# Main menu
def main():
    print_banner()
    print("[1] Admin Panel")
    print("[2] Single Target Scan (Max Range)")
    print("[3] Network Range Scan (CIDR)\n")
    choice = input("[*] Select an option: ")

    if choice == "1":
        password = input("[*] Enter Admin Password: ")
        if password == "I am hacker hex":
            print("\n[+] Welcome to Admin Panel!")
            print("[*] Logs:\n")
            try:
                with open("user_logs.txt", "r") as file:
                    print(file.read())
            except FileNotFoundError:
                print("[-] No logs found.")
        else:
            print("[-] Incorrect Password!")
    elif choice == "2":
        target = input("[*] Enter Target IP: ")
        start_port = 1
        end_port = 65535
        save_report = input("[*] Save Scan Report? (y/n): ").lower() == 'y'
        scan_target(target, start_port, end_port, save_report)
    elif choice == "3":
        cidr = input("[*] Enter Network Range (CIDR, e.g., 192.168.1.0/24): ")
        save_report = input("[*] Save Network Scan Report? (y/n): ").lower() == 'y'
        scan_network(cidr, save_report)
    else:
        print("[-] Invalid Option!")

if __name__ == "__main__":
    main()
