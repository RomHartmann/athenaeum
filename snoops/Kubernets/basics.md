# Kubernetes basics


## Objects

Every K8s object includes two nested object fields
- spec: must be provided.  Describes desired state.
- status: actual state of objec.  Supplied and updated by K8s system.
    - Actively managed by the Control Plane.  Tries to make state match spec.

Examples of Objects:  Pod, Deployment, Node

### Object lifecycle

- User/Controller
    - Creates a Pod
- Scheduler
    - Schedules the pod
- Kubelet
    - Executes pod
- Pod garbage collector
    - Deletes pod


## Components

### Master components

- Provide the cluster's control plane.
- Make global decisions about the cluster (eg scheduling)
- Detect and respond to cluster events.
- Can be run on any machine in the cluster, but typically all run on same machine.

**kube-apiserver**
- Exposes Kubernetes API.
- Is the front-end for the control plane
- Designed to scale horizontally.

**etcd**
- Key value store
- Consistent and highly-available
- used for storing all cluster data

**kube-scheduler**
- Watches newly created pods and assigns nodes.

**kube-controller-manager**
- Runs controllers
    - Controller:
        - Control loop that watches the shared state of the cluster through the api server
        - attempts to move the current state to the desired state.
    - Node Controller: Notice and respond when nodes go down
    - Replication Controller: Maintain the correct number of pods
    - Endpoints Controller: Populates the Endpoints object (Joins Services and Pods)
    - Service Account & Token Controller: Create default accounts and API access tokens for new namespaces.

**cloud-controller-manager**
- Runs controllers that interact with underlying cloud providers.
    - Allows vendor's and Kubernetes code evolve independently.
    - Controllers:
        - Node: checking the cloud provider to determine if a node has been deleted
        - Route: For setting up routes in the underlying infra
        - Service: Creating, Updating, Deleting load balancers
        - Volume: Creating, attaching, mounting volumes

### Node Components

- Run on every node
- Maintains pods and provides the K8s runtime environment

**kubelet**
- Runs on every node in the cluster
- Makes sure that containers are running in pod.
- Takes set of PodSpecs and ensures that containers in specs are running and healthy.
- Only manages containers created by Kubernetes

**kube-proxy**
- Network Proxy, runs on each node in cluster.
- Enables K8s service abstraction by maintaining network rules on the host and perform connection forwarding.
- Responsible for request forwarding.
- Allows TCP and UDP stream forwarding or round robin.

**Container Runtime**
- Software responsible for running containers.
    - Example Docker, containerd, cri-o, rklet


### Addons

- Kubernetes resources (eg DaemonSet, Deployment etc)
- Implement cluster features
- Provide cluxter-level features
- belong in the kube-system namespace

**DNS**
- Required (as most implementations rely on it)
- Every cluster requires Cluster DNS
- Containers started by Kubernetes automatically include DNS server
- Provides DNS records for Kubernetes services.

**Web UI (Dashboard)**
- Optional
- General purpose web-based UI for clusters.
- https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/

**Container Resource Monitoring**
- Optional
- Time series metrics about containers in a central database and provides UI for browsing that data
- Example: Prometheus, Sysdig
- https://kubernetes.io/docs/tasks/debug-application-cluster/resource-usage-monitoring/

**Cluster-level logging**
- Optional
- Mechanism responsible for saving container logs to central log store.
- https://kubernetes.io/docs/concepts/cluster-administration/logging/




