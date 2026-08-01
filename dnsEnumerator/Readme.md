# DNS Enumerator

A lightweight Python script that queries a domain for common DNS record types using `dnspython`. It automates domain recon during security assessments by resolving standard DNS records in one clean pass.

##  Supported Record Types

Queries and displays the following DNS records for any given domain:
- `A` & `AAAA` (IPv4 / IPv6 addresses)
- `CNAME` (Canonical names)
- `MX` (Mail servers)
- `TXT` (Text records, SPF, verification tokens)
- `NS` (Name servers)
- `SOA` (Start of Authority)
- `SRV` (Service records)
- `PTR` (Pointer records)

## Prerequisites

Requires **Python 3** and the `dnspython` library:

```bash
pip install dnspython
