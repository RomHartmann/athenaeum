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









