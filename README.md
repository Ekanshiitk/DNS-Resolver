# ASSIGNMENT 2: DNS Resolver - Iterative and Recursive Lookup

## Authors: Ekansh Bajpai (220390), Pulkit Dhayal (220834)

## Course: CS425 - Computer Networks  
**Instructor:** Adithya Vadapalli  
---

## Overview
This project implements a **DNS resolution system** that supports both **iterative** and **recursive** lookups. It is built using Python and the `dnspython` library. The assignment demonstrates how DNS queries are resolved through the hierarchical DNS infrastructure.

### What is DNS Resolution?
- **Iterative Resolution**: The resolver queries root servers, then TLD servers, and finally authoritative servers to get the response.
- **Recursive Resolution**: The resolver delegates the entire resolution process to an external resolver, which retrieves the final result.

---

## Setup Instructions

### Prerequisites
- Python 3.x installed on your system.
- Install `dnspython` library using:
  ```
  pip install dnspython
  ```
---

## Usage
The script accepts command-line arguments to specify the resolution mode (iterative or recursive) and the domain to be resolved.

### Command Format:
```bash
python3 dns_resolver.py <mode> <domain>
```
Where:
- `<mode>` is either `iterative` or `recursive`.
- `<domain>` is the domain name to resolve.

### Example Usage:
#### Iterative Lookup:
```bash
python3 dns_resolver.py iterative google.com
```
**Expected Output:**
```
[Iterative DNS Lookup] Resolving google.com
[DEBUG] Querying ROOT server (198.41.0.4) - SUCCESS
Extracted NS hostname: l.gtld-servers.net.
Resolved l.gtld-servers.net. -> 192.41.162.30
[DEBUG] Querying TLD server (192.41.162.30) - SUCCESS
Extracted NS hostname: ns1.google.com.
Resolved ns1.google.com. -> 216.239.32.10
[DEBUG] Querying AUTH server (216.239.32.10) - SUCCESS
[SUCCESS] google.com -> 142.250.194.78
Time taken: 0.597 seconds
```

#### Recursive Lookup:
```bash
python3 dns_resolver.py recursive google.com
```
**Expected Output:**
```
[Recursive DNS Lookup] Resolving google.com
[SUCCESS] google.com -> ns1.google.com.
[SUCCESS] google.com -> ns2.google.com.
[SUCCESS] google.com -> 172.217.167.206
Time taken: 0.014 seconds
```

---

## Implementation Details
### **1. Iterative DNS Resolution**
- The script starts querying the **root DNS servers**.
- It extracts **next-level nameservers** (TLD or authoritative) and queries them until the IP is resolved.
- If no final answer is found, it moves to the next level until it reaches the authoritative server.

### **2. Recursive DNS Resolution**
- The system's DNS resolver performs the entire resolution process on its own.
- It fetches the result from authoritative servers directly.

### **3. Error Handling**
- Handles network timeouts and unreachable servers.
- Provides warnings if a nameserver cannot be resolved.
- Gracefully manages invalid domain names.

---

## File Structure
```
A2/
│── dns_resolver.py   # Main Python script
│── README.md         # Documentation (this file)
```

---

