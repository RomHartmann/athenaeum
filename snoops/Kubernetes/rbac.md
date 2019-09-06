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
apiVersion:
    rbac.authorization.k8s.io/v1
metadata:
    name: pod-read-create-role
    namespace: test
rules:
    - apiGroups: [""]
      resources: ["pods"]
      verbs: ["get", "list", "create"]
```

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


## Users and ServiceAccounts

Users:
- Global and meant for humans (or processes) living outside of the cluster
- Are not kubernetes objects

ServiceAccounts:
- Namespaced and meant for intra-cluster processes running inside pods.
- Are kubernetes objects
  - This means they can be `kubectl create serviceaccount` etc.




