# Kubernetes RBAC

Given a _user_, which _operations_ can be executed over a set of _resources_.
  - user === subjects: users and processes that want access to K8s API.
  - operations === verbs for resources: list, get, create, delete etc.
  - resources === set of K8s API objects such as pods, deployments, services, nodes etc.


Thus we need RBAC objects:
- Roles + ClusterRoles: Connect api resource and verbs.  "Who can do what to what"
- RoleBindings + ClusterRoleBindings: Which subjects can use which roles - Connect entity-subjects.

## example:

This role can read and create pods:

```yaml
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: pod-read-create-role
  namespace: test
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list", "create"]
```

- `apiGroups` are the namespace for the target resources `apiVersion`.
  - If a role were to have `rules.resources = Role`, then `apiGroups` (from above)
  would have to be `rbac.authorization.k8s.io`

It just lives in isolation now, and no subject has access to it.  
To do that, the RoleBinding:

```yaml
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: roman-pods-binding
  namespace: test
subjects: 
  - kind: User
    name: romanhartmann
    apiGroup: rbac.authorization.k8s.io
roleRef:
    kind: ClusterRole
    name: pod-read-create-role
    apiGroup: rbac.authorization.k8s.io
```


## Service Account

- Human is authenticated by the apiserver as a particulalr User Account
  - Namespaced and meant for intra-cluster processes running inside pods.
  - Are kubernetes objects
    - This means they can be `kubectl create serviceaccount` etc.
- Processes in containers are authenticated by apiserver as a Service Account
  - If no service account is specified, `default` service account is assigned.
- define a non-default service account in `spec.serviceAccountName`
- to see all of them, `kubectl get serviceaccounts --all-namespaces`
  - Each namespaces has a `default` serviceaccount.
- A token is automatically created and assigned for service accounts.
- The service account has to exist at the time the pod is created, or it will be rejected
  - _You cannot update the service account of an already created pod._
- You can create Secrets and assign them to service accounts 
  - via `Secret.metadata.annotations."kubernetes.io/service-account.name" = "name"`

### Service Accounts within Kubernetes RBAC

https://kubernetes.io/docs/reference/access-authn-authz/rbac/#service-account-permissions

Best practice (but hardest to administer):
- Grant role to every service account
- Every application has a service account
  - Every Pod must have `spec.serviceAccountName`
- I think good to do this for cluster services

```yaml
# Here I have something that does work.  Its 'owner' is myapp-sa service account
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  serviceAccountName: myapp-sa
  containers:
    - name: "myapp-pod"
      image: myappimage:latest
---
# This is a machine user that exists in my namespace 'test'.  I own the above work
# It doesn't really do anything except define an owner.  It has no inherent permissions.
kind: ServiceAccount
apiVersion: v1
metadata:
  name: myapp-sa
  namespace: test
---
# I am a permission set.
# A ClusterRole would step outside of the namespace.
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: pod-read-create-role
  namespace: test
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list", "watch"]
---
# I am a binding between the service account (or user) and a Role
# This means that a service account is now allowed to do something
# In this case, myapp is allowed to read pods in this namespace.
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: myapp-binding
  namespace: test
subjects: 
  - kind: ServiceAccount
    name: myapp-sa
    apiGroup: rbac.authorization.k8s.io
roleRef:
    kind: ClusterRole
    name: pod-read-create-role
    apiGroup: rbac.authorization.k8s.io
```

For dynamic services:
- Grant role to the `default` service account in relevant namespace
  - If an application does not specify a `serviceAccountName`, it uses `default`



## Users

Users:
- Global and meant for humans (or processes) living outside of the cluster
- Are not kubernetes objects
