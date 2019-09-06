# DNS

Maps domain names to IPs


## A-record

- It is a type of DNS record.
- An `A` record points from a hostname to an IP address.


## CNAME

CNAME = Canonical Name

- It's a type of DNS record that maps an alias name to a true (or _canonical_) domain name.
- Generally used to map a subdomain to the domain that is hosting that subdomain's content.
  - have `www.example.com` and `example.com`.  
    - `A record` for `example.com` to IP address
    - `CNAME record` for `www.example.com` to `example.com`
      - `www.example.com` >CNAME> `example.com` >A> `IP`
- A CNAME must always point to another domain name, never directly to an IP address.




