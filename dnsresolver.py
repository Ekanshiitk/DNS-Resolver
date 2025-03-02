"""Authors: Ekansh Bajpai (220390), Pulkit Dhayal (220834)"""

"""Iterative and recursive DNS resolution using dnspython."""
"""Install dnspython using pip install dnspython"""

import dns.message
import dns.query
import dns.rdatatype
import dns.resolver
import time
import sys

# List of root DNS servers to initiate the iterative resolution process
ROOT_SERVERS = {
    "198.41.0.4": "Root (a.root-servers.net)",
    "199.9.14.201": "Root (b.root-servers.net)",
    "192.33.4.12": "Root (c.root-servers.net)",
    "199.7.91.13": "Root (d.root-servers.net)",
    "192.203.230.10": "Root (e.root-servers.net)"
}

TIMEOUT = 3  # Timeout in seconds for each DNS query attempt

def send_dns_query(server, domain):
    """
    Sends a DNS query to the specified server for an A record of the given domain.
    Returns the response if successful, otherwise returns None.
    """
    try:
        query = dns.message.make_query(domain, dns.rdatatype.A)  # Create a query for an A record
        response = dns.query.udp(query, server, timeout=TIMEOUT)  # Send query via UDP
        return response  # Return the DNS response object
    except Exception:
        return None  # If query fails, return None

def extract_next_nameservers(response):
    """
    Extracts nameserver (NS) records from the authority section of a response.
    Resolves these NS hostnames into IP addresses.
    Returns a list of IP addresses for the next nameservers.
    """
    ns_ips = []  # List to store resolved nameserver IPs
    ns_names = []  # List to store nameserver hostnames
    
    # Extract NS records from the authority section
    for rrset in response.authority:
        if rrset.rdtype == dns.rdatatype.NS:
            for rr in rrset:
                ns_name = rr.to_text()
                ns_names.append(ns_name)
                print(f"Extracted NS hostname: {ns_name}")
    
    # Resolve each NS hostname to an IP address
    for ns_name in ns_names:
        try:
            ns_answer = dns.resolver.resolve(ns_name, "A")  # Resolve NS hostname to IP
            for ns_ip in ns_answer:
                ip_address = ns_ip.to_text()
                if ip_address not in ns_ips:
                    ns_ips.append(ip_address)
                    print(f"Resolved {ns_name} -> {ip_address}")
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.Timeout) as e:
            print(f"[WARNING] Could not resolve {ns_name}: {e}")
    
    return ns_ips  # Return list of resolved nameserver IPs

def iterative_dns_lookup(domain):
    """
    Performs an iterative DNS resolution process.
    Queries root servers, then TLD servers, then authoritative servers,
    until the final answer is found or resolution fails.
    """
    print(f"[Iterative DNS Lookup] Resolving {domain}")
    next_ns_list = list(ROOT_SERVERS.keys())  # Start with root servers
    stage = "ROOT"  # Track resolution stage (ROOT, TLD, AUTH)
    
    while next_ns_list:
        ns_ip = next_ns_list[0]  # Pick the first nameserver from the list
        response = send_dns_query(ns_ip, domain)
        
        if response:  # Check if response is not None
            print(f"[DEBUG] Querying {stage} server ({ns_ip}) - SUCCESS")
            
            # If an answer is found, print and return
            if response.answer:
                print(f"[SUCCESS] {domain} -> {response.answer[0][0]}")
                return
            
            # Extract the next nameservers if no final answer is found
            next_ns_list = extract_next_nameservers(response)
            stage = "TLD" if stage == "ROOT" else "AUTH"  # Move to next resolution stage
        else:
            print(f"[ERROR] Query failed for {stage} {ns_ip}")
            return  # Stop resolution if no response
    
    print("[ERROR] Resolution failed.")  # Print failure message

def recursive_dns_lookup(domain):
    """
    Performs recursive DNS resolution using the system's default resolver.
    The resolver automatically fetches results from authoritative nameservers.
    """
    print(f"[Recursive DNS Lookup] Resolving {domain}")
    try:
        # Perform recursive resolution using system resolver
        answer = dns.resolver.resolve(domain, "NS")
        for rdata in answer:
            print(f"[SUCCESS] {domain} -> {rdata}")
        
        answer = dns.resolver.resolve(domain, "A")
        for rdata in answer:
            print(f"[SUCCESS] {domain} -> {rdata}")
    except Exception as e:
        print(f"[ERROR] Recursive lookup failed: {e}")  # Handle resolution failure

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in {"iterative", "recursive"}:
        print("Usage: python3 dns_server.py <iterative|recursive> <domain>")
        sys.exit(1)
    
    mode = sys.argv[1]  # Get mode (iterative or recursive)
    domain = sys.argv[2]  # Get domain to resolve
    start_time = time.time()  # Record start time
    
    # Execute the selected DNS resolution mode
    if mode == "iterative":
        iterative_dns_lookup(domain)
    else:
        recursive_dns_lookup(domain)
    
    print(f"Time taken: {time.time() - start_time:.3f} seconds")  # Print execution time
