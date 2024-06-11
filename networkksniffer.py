import scapy.all as scapy
import netifaces
import socket

# Colors for console outputs
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
WHITE = '\033[97m'
RESET = '\033[0m'


def get_interfaces():
    """Get a list of active network interfaces."""
    return netifaces.interfaces()


def select_interface(interfaces):
    """Prompt the user to select a network interface."""
    print(f"{BLUE}\nAvailable network interfaces:{RESET}")
    for index, interface in enumerate(interfaces):
        print(f"{WHITE}[{index}] {interface}{RESET}")

    try:
        selection = int(input("\nSelect an interface by its number: "))
        return interfaces[selection]
    except (ValueError, IndexError):
        print(f"{RED}Invalid selection.{RESET}")
        exit()


def get_filter():
    """Prompt the user to input a packet filter."""
    return input(f"\n{BLUE}Enter a BPF filter (or 'none' for no filter):{RESET} ").strip()


def get_capture_count():
    """Ask the user how many packets they want to capture."""
    try:
        return int(input(f"\n{BLUE}Enter number of packets to capture (0 for unlimited):{RESET} "))
    except ValueError:
        print(f"{RED}Invalid number.{RESET}")
        exit()


def get_save_option():
    """Check if the user wants to save packets to a file."""
    choice = input(f"\n{BLUE}Save packets to a file? (yes/no):{RESET} ").strip().lower()
    if choice == "yes":
        return input(f"{BLUE}Enter filename (e.g., capture.pcap):{RESET} ").strip()
    return None

def resolve_hostname(ip_address):
    """Resolve IP to hostname."""
    try:
        return socket.gethostbyaddr(ip_address)[0]
    except socket.herror:
        return ip_address

def packet_callback(packet):
    """Callback executed whenever a packet is captured."""
    protocol = packet.sprintf("%IP.proto%")
    if packet.haslayer(scapy.IP):
        ip_layer = packet[scapy.IP]
        src_host = resolve_hostname(ip_layer.src)
        dst_host = resolve_hostname(ip_layer.dst)

        transport_info = ""
        if packet.haslayer(scapy.TCP) or packet.haslayer(scapy.UDP):
            transport_layer = packet[scapy.TCP] if packet.haslayer(scapy.TCP) else packet[scapy.UDP]
            transport_info = f"PORT: {transport_layer.sport} --> {transport_layer.dport}"

        print(f"{WHITE}IP: {src_host} --> {dst_host} PROTOCOL: {protocol} {transport_info}{RESET}")


def main():
    interfaces = get_interfaces()
    selected_interface = select_interface(interfaces)
    packet_filter = None if get_filter().lower() == "none" else get_filter()
    capture_count = get_capture_count()
    save_file = get_save_option()

    print(f"\n{BLUE}[*] Sniffing on {selected_interface}{RESET}")

    packets = scapy.sniff(iface=selected_interface,
                          filter=packet_filter,
                          count=capture_count,
                          prn=packet_callback,
                          stop_filter=lambda x: x.haslayer(scapy.TCP) and x[scapy.TCP].flags == 'FA',
                          store=bool(save_file))
    
    if save_file:
        scapy.wrpcap(save_file, packets)

if __name__ == "__main__":
    main()
