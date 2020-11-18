


## Security groups

- instances belonged to a security group, that a SG is a sort of mapping with rules that instances refer to
- It is a mapping but also sort of a label with respect to when other SGs allow inbound from other SGs. They check if the resource connecting has the SG applied to it
- When we connect to office IP, and then to an EC2 instance, it does not see us connecting from a SG, but only from an IP
  - Because we are not connecting via an instance that has the SG label on it
- The simplest solution is to add the OfficeIP SG to your resources you want to connect to. Rather than putting the IP range on your SG directly. The advantage is we only have to update the CIDR range in one place if office IPs change and it’ll apply to all resources that need it. Given this is in sandbox, I wouldn’t worry about it. But for integration and production I’d take that approach














