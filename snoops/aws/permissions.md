AWS Permissions
===============

**I ran out of time a bit, this could use a lot more expansion**

---

This is a continious source of confusion to me.  Here I'm trying to dig into that confusion and extract some explicit questions.

Lets start with some definitions:

General:
- Authentication:  Who are you?
- Autherisation:  Are you allowed to be here?

Identities:
- Root User:  An identity created when creating a new AWS account that has access to all resources, including billing.
    - Single root use per account.  Should not be shared.
- User: An identity uniquely associated with one person that contains a set of permissions.
    - Multiple per account.  Set up access key to make API requests. (in `~/.aws/credentials`)
    - A "User" can also be an access key specifically for an application instead of person.
- Role: A set of permissions intended to be assumed by anyone who needs it.
- Policy: An object associated with an identity or resource that defines their permissions.



# How do permissions for users to assume a role work?

- The role/user that owns the resource is the _trusting_ account
- The user that needs to access the resource is the _trusted_ account.
- After creating a _trust relationship_, an IAM user from a trusted account can use `AssumeRole` operation
    - To modify who can assume role, must modify trust policy.

For example, the data role:
- role_arn: `arn:aws:iam::987654:role/data-role`
- How can my account access this role?  Because:
    - The policy looks like this (allow): `arn:aws:iam::334455:root`
    - And my personal arn is: `arn:aws:iam::334455:user/roman.hartmann`

So I can assume data-role because it has a policy that allows the account I am (and my team is) in.


# Lets do a run down of HTTPs and TSL again

Purpose of TSL is to create a secure connection and make sure it is not interrupted without knowing and that
the encrypted messages stay encrypted.

It has nothing to do with authentication or maintaining a connection.

**The handshake:**
1. Client sends first message `ClientHello`, which contains metadata on desired protocol version, cipher suites etc.
1. Server responds with `ServerHello`, which contains contains used protocol, session id, compression, cypher etc.
1. Serer sends over the certificate that contains the public key.
    - The client must trust this source or a party the client trusts (see certificate chain below)
    - Client also checks that current time is between certificate's `not before` and `not after`
1. The client verifies the certificate and extracts public key
    - Then uses public key to encrypt a new *pre-master key*
    - Then sends that to server
1. The server decrypts pre-master key using its private key.
1. Server + Client both use pre-master key to compute a *shared secret key*
1. Client sends server an encrypted message using shared key to server
    - everything the client sends from now on is encrypted using shared key
1. The server then decrypts and verifies this message using its private key
    - Server then encrypts and sends message back to client
    - Everything the server sends from now is encrypted
1. Client decrypts and verifies message
1. Handshake over, all data is encrypted using shared key from now on.


**In short:**
1. Client initiates
1. Server responds with certificate + public key
1. Client encrypts some message with public key and sends to server
1. Server decrypts with private key and verify its the right message
1. Happy handshake complete!


**The certificate chain:**
1. Every operating system has a list of Certificate Authorities that it trusts
    - This list can easily be modified
1. During a handshake, the client wants to check if the server's certificate can be trusted.
    - Usually the server's certificate was signed by someone else, going up a chain until you end up at one of the trusted CAs.
        - If I am a trusted root CA, I can 'sign' some certificate using my own public key (`cert.pem`).
        - A root CA signs its own certificate, and keeps its private key very secure (`key.pem`)
    - How do we verify the certificate chain?
        - A certificate contains the following:
            - hostname
            - public key
            - Issuer's name
            - Issuer's signature
        - A CA signs a certificate using its public key
            - so we can verify if that certificate is valid by looking at the issuer's public key
        - So we go up the chain of issuer's by validating that each certificate was created via the publik key of its parent.
        - [This is a nice image](https://en.wikipedia.org/wiki/Chain_of_trust#/media/File:Chain_of_trust.svg)



# Lets go through oAuth again

oAuth is about authorization and not authentication.  I.e. *are you allowed to be here* and not *who are you*

We 4 main players in an oAuth process:
1. Resource owner:  Owner who can grant access to resource.
2. Resource Server: This is some service we want access to.
3. Client:  This is either us, or an application that does somethign for us.
4. Authentication server:  Hosts the protected user accounts and verifies the identity of the resource owner and issues access tokens to the client.

In short, here is how it works:
1. Client asks Resource for something
1. Resource redirects to authentication server
    - resource must be registered with authentication server
1. Authentications server responds to client with bearer token
1. Client then auths with resource using token
    - there is some bearer access token complexity here
1. Resource authenticates token and grants access.


From https://tools.ietf.org/html/rfc6750:
```text
     +--------+                               +---------------+
     |        |--(A)- Authorization Request ->|   Resource    |
     |        |                               |     Owner     |
     |        |<-(B)-- Authorization Grant ---|               |
     |        |                               +---------------+
     |        |
     |        |                               +---------------+
     |        |--(C)-- Authorization Grant -->| Authorization |
     | Client |                               |     Server    |
     |        |<-(D)----- Access Token -------|               |
     |        |                               +---------------+
     |        |
     |        |                               +---------------+
     |        |--(E)----- Access Token ------>|    Resource   |
     |        |                               |     Server    |
     |        |<-(F)--- Protected Resource ---|               |
     +--------+                               +---------------+
```


# So how does AWS Kubernetes live in this ecosystem?

https://github.com/kubernetes-sigs/aws-iam-authenticator



## What does a healthy configuration look like?

**~/.aws**

`config` for multiple profiles:
```text
[default]
region = us-east-1
output = json

[profile data]
role_arn = arn:aws:iam::123:role/data-role
source_profile = default
region = us-east-1
mfa_serial = arn:aws:iam::890:mfa/roman.hartmann
duration_seconds = 14400

```
`/credentials` come from IAM users -> access keys page.  And then `aws configure`
```text
[default]
aws_access_key_id = ABC
aws_secret_access_key = abc

```

**~/.kube**

personal `/config`
```text
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: TOKEN=
    server: https://EA0AF39F611F87CC51EE923B68A05477.gr7.us-east-1.eks.amazonaws.com
  name: arn:aws:eks:us-east-1:514588561872:cluster/unicorn
- cluster:
    certificate-authority-data: TOKEN=
    server: https://C9C34CCCA7BD324259970F133B0EC535.sk1.us-east-1.eks.amazonaws.com
  name: arn:aws:eks:us-east-1:514588561872:cluster/outset
contexts:
- context:
    cluster: arn:aws:eks:us-east-1:514588561872:cluster/unicorn
    user: arn:aws:eks:us-east-1:514588561872:cluster/unicorn
  name: unicorn
- context:
    cluster: arn:aws:eks:us-east-1:514588561872:cluster/outset
    user: arn:aws:eks:us-east-1:514588561872:cluster/outset
  name: outset
current-context: outset
kind: Config
preferences: {}
users:
- name: arn:aws:eks:us-east-1:514588561872:cluster/unicorn
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1alpha1
      args:
      - --region
      - us-east-1
      - eks
      - get-token
      - --cluster-name
      - unicorn
      command: aws
      env:
      - name: AWS_PROFILE
        value: data
- name: arn:aws:eks:us-east-1:514588561872:cluster/outset
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1alpha1
      args:
      - --region
      - us-east-1
      - eks
      - get-token
      - --cluster-name
      - outset
      command: aws
      env:
      - name: AWS_PROFILE
        value: data

```

eks config: 

```text
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: ABC=
    server: https://XXX.yl4.us-east-1.eks.amazonaws.com
  name: arn:aws:eks:us-east-1:123:cluster/cluster_name
contexts:
- context:
    cluster: arn:aws:eks:us-east-1:123:cluster/cluster_name
    user: arn:aws:eks:us-east-1:123:cluster/cluster_name
  name: arn:aws:eks:us-east-1:123:cluster/cluster_name
current-context: arn:aws:eks:us-east-1:123:cluster/cluster_name
kind: Config
preferences: {}
users:
- name: arn:aws:eks:us-east-1:123:cluster/cluster_name
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1alpha1
      args:
      - token
      - -i
      - cluster_name
      - -r
      - arn:aws:iam::123:role/eks-cluster-admin-development
      command: aws-iam-authenticator
```
