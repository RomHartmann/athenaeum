# Kubernetes Scheduler

- User creates Pod
- Kubernetes Scheduler assigns pod to Node
    - k8s Scheduler monitors the Object Store
    - Task of Scheduler is to choose a placement.
        - Placement is a partial, non-injective assignment of a set of pods to a set of nodes.
            - Partial: Some pods may not be assigned to a node
            - Non-injective: Some pods may be assigned to the same node.
        - Scheduling is an optimisation problem
            1. find set of feasible placements
            1. find set of viable placements (feasible placements with highest score)
            
Binding = `PodObject.Spec.NodeName == NodeObject.Name`

Scheduler loop:
- monitor Object Store
- choose unbound Pod of highest priority
- perform scheduling step or preemption step.
    - Scheduling step: If there exists at least one node, such that the node is feasible to host the pod.
    - Preemption step: If node is feasible to host pod _if_ subset of pods with lower priorities bound to this node were to be deleted.
        - If preemption step enabled, scheduler will trigger deletion of subset of pods with lower priorities bound to _one_ node. (to inflict lowest possible casualties)
            - Not guaranteed that the pod which triggered the preemption step will be bound to that node in subsequent scheduling step.

Feasibility:
- Scheduler identifies the set of nodes which satisfy the constraintes of the pod
- Is a set of filter functions, where _all_ filters must yield true.
    - Schedulability and Lifecycle phase: Based on Node's schedulability and lifecycle phase.
    - Resource requirements and availability: "Does node have enough resources available to house pod?"
    - Node selector: Based on the Pod's node selector values and Node's label values.
    - Node Taints and Pod Tolerations: Pod cannot be scheduled on Node with taint unless it's tolerated.
    - Required Affinity: Node Affinity Terms, Pod Affinity Terms, and Pod Anti Affinity Terms
        - Node Affinity: Pod must be assigned to Node such that Node's labels match the Pod's Node Affinity Requirements.
        - Pod Affinity: Pod must be assigned to Node such that at least one Pod on a Node matches Pod's Pod Affinity Requirements.
        - Pod Anti-Affinity: Pod must be assigned to a Node such that no Pod on a Node matchest the Pod's Pod Anti-Affinity Requirements.

Viability:
- Is a linear combination rating of feasible nodes's scores.


