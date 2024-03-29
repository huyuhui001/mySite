# Namespace

Scenario:

* Get namespace list
* Create new namespace
* Label a namespace
* Delete a namespace

Demo:

Get list of Namespace

```console
kubectl get namespace
```

Get list of Namespace with Label information.

```console
kubectl get ns --show-labels
```

Create a Namespace

```console
kubectl create namespace cka
```

Label the new created Namespace `cka`.

```console
kubectl label ns cka cka=true
```

Create Nginx Deployment in Namespace `cka`.

```console
kubectl create deploy nginx --image=nginx --namespace cka
```

Check Deployments and Pods running in namespace `cka`.

```console
kubectl get deploy,pod -n cka
```

Result is below.

```console
NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/nginx   1/1     1            1           2m14s

NAME                         READY   STATUS    RESTARTS   AGE
pod/nginx-85b98978db-bmkhf   1/1     Running   0          2m14s
```

Delete namespace `cka`. All resources in the namespaces will be gone.

```console
kubectl delete ns cka
```

Tip:

* Kubernetes Namespaces stuck in Terminating status.

```console
kubectl get namespace $NAMESPACE -o json | sed -e 's/"kubernetes"//' | kubectl replace --raw "/api/v1/namespaces/$NAMESPACE/finalize" -f -
```
