DNS Subdomain Enumerator
A lightweight Python script that performs fast subdomain enumeration using the dnspython library. It reads from a built-in list of common subdomains and checks for active A records to help automate reconnaissance during security assessments.

Features
Fast Discovery: Iterates through a comprehensive list of standard subdomains.

Error Handling: Gracefully handles non-existent domains (NXDOMAIN), empty answers (NoAnswer), and user interruptions (KeyboardInterrupt).

Clean Output: Instantly prints valid and active subdomains as they are discovered.

Prerequisites
Requires Python 3 and the dnspython library. Install the required dependency using pip:

Bash
pip install dnspython
