
# DNS - Resolver

This Python script implements both **iterative** and **recursive** DNS resolution. It allows querying a domain name to obtain its IP address using either method.

## Features

-   **Iterative DNS Resolution**: Queries root servers --> TLD servers --> finally authoritative servers to resolve the domain.
-   **Recursive DNS Resolution**: Uses the system's DNS resolver to fetch the result directly.
-   **Handles Failures**: Implements exception handling for timeouts and unreachable servers.
-   **Uses dnspython Library**: Leverages `dnspython` to construct and send DNS queries.

## Prerequisites

Ensure you have Python3 installed. You also need to install the `dnspython` library:

```bash
pip install dnspython
```

## How to run

Run the script from the command line with the following syntax:

- For Iterative DNS resolution
```bash
python3 dnsresolver.py iterative <domain>
```
- For Recursive DNS resolution
```bash
python3 dnsresolver.py recursive <domain>
```

## How It Works

### Iterative Mode

1.  Starts with a predefined set of root DNS servers.
2.  Sends a DNS query to a root server.
3.  Extracts nameservers from the response and queries them iteratively.
4.  Continues this process until it finds the authoritative nameserver that returns the domain's IP address.

### Recursive Mode

1.  Uses the system's DNS resolver to handle the query.
2.  Directly retrieves the resolved IP without manually iterating through DNS hierarchy.

## Code Structure

-   `send_dns_query(server, domain)`: Sends a DNS query to a specified server.
-   `extract_next_nameservers(response)`: Extracts the next set of nameservers from the response.
-   `iterative_dns_lookup(domain)`: Performs iterative DNS resolution.
-   `recursive_dns_lookup(domain)`: Performs recursive DNS resolution using the system's resolver.
-   `ROOT_SERVERS`: List of root DNS server IPs used for iterative resolution.

## Error Handling

The script uses Python's `try` and `except` blocks for exception handling to manage common errors and unexpected behavior like:

-   **Timeouts**: If a DNS server is unresponsive.
-   **NXDOMAIN**: If the domain does not exist.
-   **NoAnswer**: If no answer is returned by the nameserver.

## Example Output

```bash
[Iterative DNS Lookup] Resolving example.com
[DEBUG] Querying ROOT server (198.41.0.4) - SUCCESS
Extracted NS hostname: a.iana-servers.net.
Resolved a.iana-servers.net -> 199.43.135.53
[DEBUG] Querying TLD server (199.43.135.53) - SUCCESS
[DEBUG] Querying AUTH server (93.184.216.34) - SUCCESS
[SUCCESS] example.com -> 93.184.216.34
Time taken: 0.532 seconds

```

## Author

Ekansh Bajpai 220390
Pulkit Dhayal 220834
