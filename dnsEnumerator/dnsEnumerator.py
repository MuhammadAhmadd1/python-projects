import dns.resolver
import sys

record_types = ['A', 'AAAA', 'CNAME', 'MX', 'TXT', 'NS','SOA', 'SRV', 'PTR']
try:
    domain = sys.argv[1]
except IndexError:
    print('Syntax error: python3 dnsEnumerator <domainname>')
    quit()
for records in record_types:
    try:
        answer = dns.resolver.resolve(domain, records)
        print(f'\n{records} Records')
        print('-'*30)
        for server in answer:
            print(server.to_text() + '\n')
    except dns.resolver.NoAnswer:
        pass
    except KeyboardInterrupt:
        print('You do not have to finger in between everything.')
        quit()
    except dns.resolver.NXDOMAIN: 
        print(f'{domain} does not exist. Big Brain!')
        quit()
        