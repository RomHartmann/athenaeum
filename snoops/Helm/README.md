A cursary look into Helm
========================

- https://docs.helm.sh/chart_template_guide/
- https://github.com/technosophos/k8s-helm/blob/master/docs/charts_tips_and_tricks.md

## Installation

Kubernetes needs to be set up first.

https://docs.helm.sh/using_helm/#installing-helm

```bash
brew install kubernetes-helm
```

## Overview

Helm is an infrastructure as code application, and its deployments are organized in _Charts_.  A chart is a collection
of Kubernetes deployments/services/jobs etc, and those yaml files are defined as templates.

There is an example chart under `charts/example-chart`.  A nice thing here is that we can have a single source for
constants (`values.yaml` and `Chart.yaml`), and these constants can be shared among multiple templates.

Every chart must have `Chart.yaml`

Charts can be installed with values set at run-time:

```bash
helm install \
        --name my-chart \
        --set image.tag=$(SHA_TAG) \
	    --set image.repository=$(ECR_REPO) \
		--set environment=$(ENV) \
		--kube-context $(ENV) \
		--wait \
		charts/example-chart
```

Or via `helm update --install ...`

---

Here are some [best practices](https://docs.helm.sh/chart_best_practices/#the-chart-best-practices-guide), notably:

- chart names must be lower case and cant have underscores
- directory name must be consistent with name of chart


Helm can also be used to create RBAC resources. i.e create service accounts and roles etc.

## Thoughts

- A basic use for Helm is actually pretty simple, and is probably better than a uniquely defined yaml file for kubectl to ingest.
- Though one cannot just load a single item within the chart.  Its everything or nothing.  This may cause a bit of duplication if
that is needed.
- The templating language can get pretty complicated.  There are a lot of best practices and subtleties.
  - Fore more infor on templates, look at https://docs.helm.sh/chart_template_guide/
  - The templating languave is based off Go.

