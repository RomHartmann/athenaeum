# Metadata in manifests

## Labels

Used to select objects and to find collections of objects that satisfy certain conditions

- metadata.labels.key = "value"
- Do not mean anything to Kubernetes _core_, but is useful to tie user-defined objects together
- Useful such that users can map their own organisational structure
- Do not provide uniqueness
- Common labels:
  - app, environment, tier, release
- Can then do something like this:
  - `kubectl get pods -l app=ub-data-airflow`
- Can see what labels ware with `kubectl get pods --show-labels`
  - `kubectl get nodes --show-labels`


## Selector

- Used to define given object to target another object with the correct label
  - `Service` has `spec.selector.app = "myapp"` then there must
  exist a pod or deployment with `metadata.labels.app = "myapp"`
  - `Pod` has `spec.nodeSelelctor.key = "value"`:
    - Will only spawn the pod on the correct nodes with key=value.
  - `Deployment` can have `spec.selector.matchLabels.app = "value"`
    - Tells what pods the deployment will apply to.
    - Thus the Deployment must also have `spec.template.metadata.labels.app = "value"`
        - **Note:** `template` is a `podTemplate`
- Selectors can have multiple targets


#### Note on NodeSelector vs Taints

- The node selector affects only a single pod template, asking the scheduler to pllace it on a set of nodes.
- A taint tells scheduler to block all pods, except those with tolerations.


## Annotations

- Similar to labels, used to attach metadata to K8s objects
  - Are not used to identify and select objects like `Labels`
- `metadata.annotations.key = "valule"`
- Example Annotations:
  - build, release, image, git branch, PR etc info
  - pointers to logging, monitoring, analytics etc
  - `iam.amazonaws.com/role`
  - `imageregistry`
- Keys are of form `<prefix (optional)>/<name>`
  - name segment must be 63 characters or lelss
  - The prefix is optional, and must be a DNS subdomain, 253 characters or less.
    - if omitted, assumed to be private to the user.
    - Automated system components such as `kube-scheduler`, `kubectl` add annotations with prefix
    - `kubernetes.io/` and `k8s.io/` are reserved for Kubernetes core components









