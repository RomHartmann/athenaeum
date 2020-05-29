# kiam

## Overview
- A pod assumes a role directly via annotations:
  ```yaml
    kind: Pod
    metadata:
      name: foo
      namespace: iam-example
      annotations:
        iam.amazonaws.com/role: reportingdb-reader
    ```
- A pod _Must_ have corresponding namespace annotations, else it cannot assume roles:
  ```yaml
    kind: Namespace
    metadata:
      name: iam-example
      annotations:
        iam.amazonaws.com/permitted: ".*"
    ```
- kiam intercepts metadata requests and uses sts (Security Token Service) to retrieve temporary role credentials.
  - role credentials are like username and passwords for users.


## How it works

- kiam is split into two processes - Agent and Server.  This allows user workloads to run on nodes without `sts:AssumeRole`
  - Agent
    - Typically deployed as a DaemonSet
      - ensure that Pods have no access to AWS Metadata API
    - Agent runs HTTP proxy which intercepts credentials request and passes on anything else.
  - Server
    - Responsible for connecting to K8s API servers to watch pods and communicate with AWS sts to request credentials.
    - Also maintains a cache of credentials for roles currently in use by running pods
    - The server component is responsible for requesting credentials and thus needs to run on an EC2 instance that has 
      access to the AWS STS API. Given that the server can assume any IAM role, it should run on a node that does not run 
      user workloads (such as a Control Plane node)


## Iptables - How it really works

With the help of: https://medium.com/building-ibotta/moving-from-kube2iam-to-kiam-a000639b839e

- We can look at these IP tables: `kubectl --context outset -n unbounce-system exec -it kiam-agent-bdc8z sh`
    -   ```bash
        > iptables -t nat -n -L PREROUTING --line-numbers
        
        Chain PREROUTING (policy ACCEPT)
        num  target             prot opt source               destination
        1    KUBE-SERVICES      all  --  0.0.0.0/0            0.0.0.0/0            /* kubernetes service portals */
        2    CNI-HOSTPORT-DNAT  all  --  0.0.0.0/0            0.0.0.0/0            ADDRTYPE match dst-type LOCAL
        3    DNAT               tcp  --  0.0.0.0/0            169.254.169.254      tcp dpt:80 to:10.253.46.111:8181
        ```
    Here we see the following info:
        - PREROUTING: routes within the NAT table (Network Address Translation)
            - PREROUTING is traversed by before sending any packets going to inside or outside of network
                - FORWARD rules only apply to packets leaving network
            - This means that the packet is destined for the local machine but the destination address is changed
        - The rule forwards all tcp traffic from anywhere that _would have gone_ to `169.254.169.254`
            169.254.169.254: used in Amazon EC2 and other cloud computing platforms to distribute metadata to cloud instances.
                - https://serverfault.com/questions/427018/what-is-this-ip-address-169-254-169-254
                - https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html
            - From https://github.com/uswitch/kiam#how-it-works:
                - Agent: ensure that Pods have no access to the AWS Metadata API
                - agent runs an HTTP proxy which intercepts credentials requests and passes on anything else.
        - It then routes that packet through to `tcp dpt:80 to:10.253.46.111:8181` instead
    - Still from the kiam-agent, scanning IP addresses:
      ```sh
      > arp -a | grep 10.253.46`
      
      10-253-46-106.kiam-server.unbounce-system.svc.cluster.local (10.253.46.106) at 0e:01:ef:40:9e:c3 [ether]  on eth0
      ```
        - THe address doesn't quite match, so I'm missing something, but looks like that is the local address for the kiam-server.

Looking at Kiam server:
- https://github.com/uswitch/kiam#server
    - communicating with AWS STS to request credentials
    - maintains a cache of credentials for roles currently in use by running pods 
        - ensuring that credentials are refreshed every few minutes and stored in advance of Pods needing them



## Flow of permission:

- pod wants to access S3
- Role has been created in IAM that allows access to S3
- Pod has annotation that says this pod should use that role
- This pod is running on EC2 using another role
- If pod were to reach out to AWS to use S3 resource, it would be denied
- Kiam:
    - Request is redirected to kiam-server
    - Kiam-server running with role has power to assume any role. We assume s3 role
    - We reach out to AWS and permission granted via iptables
    - Other traffic runs as normal


We can't apply the role to the pod directly because:
- At this point a pod is not an IAM resource and can't assume roles
    - A EC2 instance is a IAM resource and can assume roles.
        - This is why the daemonset can intercept calls, because it acts for the IAM EC2 resource
    - Service accounts implementation will solve this.
- So a pod does not have credentials to access AWS
    - A pod wanting to access S3 would not be able to authenticate
    - We give authentication priviledges to kiam-server
    - Then when a pod wants access, we route the request to AWS metadata api through kiam-server via iptables
    - This way we are authenticated
- But the resource is still locked away via IAM rules
    - So then kiam-server AssumesRole for the role that we have annotated.
    - This way we are authorized.
- https://aws.amazon.com/blogs/opensource/introducing-fine-grained-iam-roles-service-accounts/
- https://alexbrand.dev/post/using-kiam-to-access-aws-resources-from-kubernetes-pods/
