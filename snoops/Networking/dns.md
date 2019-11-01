# DNS

Maps domain names to IPs


## A-record

- It is a type of DNS record.
- An `A` record points from a hostname to an IP address.
- Points from a single (static) ip to a hostname

## CNAME

CNAME = Canonical Name

- It's a type of DNS record that maps an alias name to a true (or _canonical_) domain name.
- Generally used to map a subdomain to the domain that is hosting that subdomain's content.
  - have `www.example.com` and `example.com`.  
    - `A record` for `example.com` to IP address
    - `CNAME record` for `www.example.com` to `example.com`
      - `www.example.com` >CNAME> `example.com` >A> `IP`
- A CNAME must always point to another domain name, never directly to an IP address.

- Introduces a performance penalty since at least one additional DNS lookup must be performed.
- Cannot be used at the zone apex
  - The zone apex is where the SOA and NS (and often MX) records for a DNS zone are placed. 
    - They are DNS records whose name are the same as the zone itself. 
      - For example in in zone mydomainname.org you might have: mydomainname.org. 3600 IN SOA dns1.mydomainname.org.
  - I.e. You cannot have a CNAME that points to itself.

## Alias

- Similar to a CNAME record
- Resolves final IP faster then a CNAME chain
- Looks like an A record, since it returns the final IP
  - This means it can be used anywhere an A record can be used, including zone apex


