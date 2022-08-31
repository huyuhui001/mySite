# Deployment

!!! Scenario
    * Modify Existing Deployment, e.g., add port number in below demo.

Demo:

Create Deployment `nginx`.
```
kubectl create deployment nginx --image=nginx
```

Execute command below to get yaml template with port number.
The option `--port=8080` specified the port that this container exposes.
```
kubectl create deployment nginx --image=nginx --port=8080 --dry-run=client -o yaml
```

Then we get to know the path to add port number, like below.
```
kubectl explain deployment.spec.template.spec.containers.ports.containerPort
```

Execute command below to edit the Deployemnt.
```
kubectl edit deployment nginx
```
Add below two lines to specify port number with `8080` and protocol is `TCP`.
```
spec:
  template:
    spec:
      containers:
      - image: nginx
        name: nginx
        ports:
        - containerPort: 8080
          protocol: TCP
```


Use command `kubectl describe deployment <deployment_name>`, we can see the port number was added.
```
Pod Template:
  Labels:  app=nginx
  Containers:
   nginx:
    Image:        nginx
    Port:         8080/TCP
    Host Port:    0/TCP
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
```

With command `kubectl describe pod <pod_name>`, we can see the port number was added.
```
Containers:
  nginx:
    Container ID:   containerd://af4a1243f981497074b5c006ac55fcf795688399871d1dfe91a095321f5c91aa
    Image:          nginx
    Image ID:       docker.io/library/nginx@sha256:1761fb5661e4d77e107427d8012ad3a5955007d997e0f4a3d41acc9ff20467c7
    Port:           8080/TCP
    Host Port:      0/TCP
    State:          Running
      Started:      Sun, 24 Jul 2022 22:50:12 +0800
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-hftdt (ro)
```


!!! Info
    Some key fields of deployment (use `kubectl explain deployment.`)
    * `.spec.revisionHistoryLimit`: The number of old ReplicaSets to retain to allow rollback. This is a pointer to distinguish between explicit zero and not specified. Defaults to `10`.
    * `.spec.strategy.type`: Type of deployment. Can be `Recreate` or `RollingUpdate`. Default is `RollingUpdate`.
        - `Recreate` Kill all existing pods before creating new ones.
        - `RollingUpdate` Replace the old ReplicaSets by new one using rolling update i.e gradually scale down the old ReplicaSets and scale up the new one.


