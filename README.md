Stresser (OPEN SOURCE)

Overview
Stresser is a powerful DDoS attack tool that sends multiple types of network traffic to overwhelm target sites. It features multi-vector attacks, automated IP resolution, and a simple terminal interface.

Features
- Multi-Vector Attacks: HTTP Flood, SYN Flood, UDP Flood, ICMP Flood, and Mixed Packet Flood.
- Automatic IP Retrieval: Resolves target IPs via DNS, socket, or external services.
- Parallel Execution: Uses multiprocessing to run attacks simultaneously.
- Terminal Interface: Enter the target URL, and attacks start immediately.

Usage
1. Run setup.bat: Installs dependencies and runs the tool.
2. Enter the Target URL: The tool retrieves the IP and starts the attack.

Requirements:
- Python
- Libraries: requests, scapy, dnspython
