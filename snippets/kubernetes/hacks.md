


```bash
kubectl --context my_cluster -n my_namespace run -i --tty testpod \
  --image=<repo>:<hash> \
  --overrides='{ "spec": { "serviceAccount": "sc-name" }  }' \
  -- bash

```


