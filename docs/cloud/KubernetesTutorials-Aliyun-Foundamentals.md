# Kubernetes Tutourials: Ubuntu@Aliyun

Refer to "Installation on Aliyun Ubuntu" in file [Kubernetes-Installation.md](./Kubernetes-Installation.md)

## 1.Cluster Overview

### Container Layer

We are using Containerd service to manage our images and containers via command `nerdctl`, which is same concept with Docker.

Tasks:

* Get namespace.
* Get containers.
* Get images.
* Get volumes.
* Get overall status.
* Get network status.

#### namespace.

Get namespaces.
```
nerdctl namespace ls
```
Result
```
NAME      CONTAINERS    IMAGES    VOLUMES    LABELS
k8s.io    21            30        0      
```

#### containers.

Get containers under specific namespace with `-n` option.
```
nerdctl -n k8s.io ps
```
Result
```
CONTAINER ID    IMAGE                                                                      COMMAND                   CREATED           STATUS    PORTS    NAMES
0965b195f41a    registry.aliyuncs.com/google_containers/etcd:3.5.1-0                       "etcd --advertise-cl…"    44 minutes ago    Up                 k8s://kube-system/etcd-cka001/etcd
0c5e69118f1b    registry.aliyuncs.com/google_containers/kube-apiserver:v1.24.0             "kube-apiserver --ad…"    44 minutes ago    Up                 k8s://kube-system/kube-apiserver-cka001/kube-apiserver
1285b6814c3b    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  44 minutes ago    Up                 k8s://kube-system/kube-scheduler-cka001
29a1ef016b43    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  24 minutes ago    Up                 k8s://kube-system/calico-kube-controllers-5c64b68895-jr4nl
2aab1a388a4a    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  25 minutes ago    Up                 k8s://kube-system/calico-node-dsx76
2f09aa56c83a    registry.aliyuncs.com/google_containers/coredns:v1.8.6                     "/coredns -conf /etc…"    24 minutes ago    Up                 k8s://kube-system/coredns-6d8c4cb4d-g4jxc/coredns
49ca8fcbee2d    docker.io/calico/node:v3.23.3                                              "start_runit"             24 minutes ago    Up                 k8s://kube-system/calico-node-dsx76/calico-node
4ed8183581b5    registry.aliyuncs.com/google_containers/coredns:v1.8.6                     "/coredns -conf /etc…"    24 minutes ago    Up                 k8s://kube-system/coredns-6d8c4cb4d-sqcvj/coredns
545b4ad4e448    docker.io/calico/kube-controllers:v3.23.3                                  "/usr/bin/kube-contr…"    24 minutes ago    Up                 k8s://kube-system/calico-kube-controllers-5c64b68895-jr4nl/calico-kube-controllers
638bb602c310    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  44 minutes ago    Up                 k8s://kube-system/kube-apiserver-cka001
9e1bea9f25d1    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  44 minutes ago    Up                 k8s://kube-system/etcd-cka001
ad6f45ec7cd8    registry.aliyuncs.com/google_containers/kube-controller-manager:v1.24.0    "kube-controller-man…"    44 minutes ago    Up                 k8s://kube-system/kube-controller-manager-cka001/kube-controller-manager
b95c81350937    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  24 minutes ago    Up                 k8s://kube-system/coredns-6d8c4cb4d-g4jxc
d655d2b02af3    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  44 minutes ago    Up                 k8s://kube-system/kube-proxy-cm4hc
df5e4d68acae    registry.aliyuncs.com/google_containers/kube-proxy:v1.24.0                 "/usr/local/bin/kube…"    44 minutes ago    Up                 k8s://kube-system/kube-proxy-cm4hc/kube-proxy
edb274666e48    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  44 minutes ago    Up                 k8s://kube-system/kube-controller-manager-cka001
ee2a0b3713f5    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  24 minutes ago    Up                 k8s://kube-system/coredns-6d8c4cb4d-sqcvj
f9ff812d8e07    registry.aliyuncs.com/google_containers/kube-scheduler:v1.24.0             "kube-scheduler --au…"    44 minutes ago    Up                 k8s://kube-system/kube-scheduler-cka001/kube-scheduler
```

```
nerdctl -n default ps
```
Result
```
CONTAINER ID    IMAGE    COMMAND    CREATED    STATUS    PORTS    NAMES
```

#### images.

Get images.
```
nerdctl image ls -a
nerdctl -n k8s.io image ls -a
```

#### volumes.

Get volumes. After inintial installation, no volume within namespaces.
```
nerdctl -n default volume ls
nerdctl -n k8s.io volume ls
```

#### overall status.

Get overall status
```
nerdctl stats
```
Result
```
CONTAINER ID   NAME      CPU %     MEM USAGE / LIMIT   MEM %     NET I/O           BLOCK I/O     PIDS
```

#### network status.

Get network status.
```
nerdctl network ls
nerdctl network inspect bridge
nerdctl network inspect k8s-pod-network
```
Result
```
NETWORK ID    NAME               FILE
              k8s-pod-network    /etc/cni/net.d/10-calico.conflist
0             bridge             /etc/cni/net.d/nerdctl-bridge.conflist
              host               
              none
```

Get network interface in host `cka001` with command `ip addr list`.

IP pool of `10.4.0.1/24` is `ipam` and defined in `/etc/cni/net.d/nerdctl-bridge.conflist`.
```
lo                   : inet 127.0.0.1/8 qlen 1000
eth0                 : inet 172.16.18.170/24 brd 172.16.18.255 scope global dynamic eth0
tunl0@NONE           : inet 10.244.228.192/32 scope global tunl0
calid100479d885@if4  :
cali01418e9b2c2@if4  :
cali24f48a34a33@if4  :
```





### Kubernetes Layer

Kubernetes is beyond container layer. 

Summary: 

* Nodes
* Namespaces
* System Pods

#### Node

In Kubernetes layer, we have three nodes here, `cka001`, `cka002`, and `cka003`.

Get nodes status.
```
kubectl get node -o wide
```
Result
```
NAME     STATUS   ROLES                  AGE   VERSION   INTERNAL-IP     EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION      CONTAINER-RUNTIME
cka001   Ready    control-plane,master   56m   v1.24.0   172.16.18.170   <none>        Ubuntu 20.04.4 LTS   5.4.0-122-generic   containerd://1.5.9
cka002   Ready    <none>                 52m   v1.24.0   172.16.18.169   <none>        Ubuntu 20.04.4 LTS   5.4.0-122-generic   containerd://1.5.9
cka003   Ready    <none>                 52m   v1.24.0   172.16.18.168   <none>        Ubuntu 20.04.4 LTS   5.4.0-122-generic   containerd://1.5.9
```

#### Namespaces

We have four initial namespaces across three nodes.
```
kubectl get namespace -A
```
Result
```
NAME              STATUS   AGE
default           Active   56m
dev               Active   22m
kube-node-lease   Active   56m
kube-public       Active   56m
kube-system       Active   56m
```

#### System Pods

We have some initial pods. 
```
kubectl get pod -A -o wide
```
Result
```
NAMESPACE     NAME                                       READY   STATUS    RESTARTS   AGE   IP               NODE     NOMINATED NODE   READINESS GATES
kube-system   calico-kube-controllers-5c64b68895-jr4nl   1/1     Running   0          37m   10.244.228.194   cka001   <none>           <none>
kube-system   calico-node-dsx76                          1/1     Running   0          37m   172.16.18.170    cka001   <none>           <none>
kube-system   calico-node-p5rf2                          1/1     Running   0          37m   172.16.18.169    cka002   <none>           <none>
kube-system   calico-node-tr22l                          1/1     Running   0          37m   172.16.18.168    cka003   <none>           <none>
kube-system   coredns-6d8c4cb4d-g4jxc                    1/1     Running   0          56m   10.244.228.195   cka001   <none>           <none>
kube-system   coredns-6d8c4cb4d-sqcvj                    1/1     Running   0          56m   10.244.228.193   cka001   <none>           <none>
kube-system   etcd-cka001                                1/1     Running   0          56m   172.16.18.170    cka001   <none>           <none>
kube-system   kube-apiserver-cka001                      1/1     Running   0          56m   172.16.18.170    cka001   <none>           <none>
kube-system   kube-controller-manager-cka001             1/1     Running   0          56m   172.16.18.170    cka001   <none>           <none>
kube-system   kube-proxy-5cdbj                           1/1     Running   0          52m   172.16.18.169    cka002   <none>           <none>
kube-system   kube-proxy-cm4hc                           1/1     Running   0          56m   172.16.18.170    cka001   <none>           <none>
kube-system   kube-proxy-g4w52                           1/1     Running   0          52m   172.16.18.168    cka003   <none>           <none>
kube-system   kube-scheduler-cka001                      1/1     Running   0          56m   172.16.18.170    cka001   <none>           <none>
```

Summary below shows the relationship between containers and pods. 

Good references about container pause: [article](https://zhuanlan.zhihu.com/p/464712164) and [artical](https://cloud.tencent.com/developer/article/1583919).

* Master node:
    * CoreDNS: 2 Pod
    * etcd: 1 Pod
    * apiserver: 1 Pod
    * controller-manager: 1 Pod
    * scheduler: 1 Pod
    * Calico Controller: 1 Pod
* All nodes:
    * Calico Node: 1 Pod each
    * Proxy: 1 Pod each








## 4.Kubernetes API and Resource

### kubectl

Three approach to operate Kubernetes cluster:

* via [API](https://kubernetes.io/docs/reference/kubernetes-api/)
* via kubectl
* via Dashboard


Remember the link of `kubectl`: https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands


1. Get a complete list of supported resources

```
kubectl api-resources
```

2. Get cluster status.

```
kubectl cluster-info
kubectl cluster-info dump
```

* Kubernetes control plane is running at `https://<control_plane_ip>:6443`
* CoreDNS is running at `https://<control_plane_ip>:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy`


3. Display resources

Use `kubectl get --help` to get examples of displaying one or many resources.

Get health status of control plane.
```
kubectl get componentstatuses
kubectl get cs
```
Result
```
NAME                 STATUS    MESSAGE                         ERROR
etcd-0               Healthy   {"health":"true","reason":""}   
scheduler            Healthy   ok                              
controller-manager   Healthy   ok 
```

Get node status.
```
kubectl get nodes
kubectl get nodes -o wide
```
Result
```
NAME     STATUS   ROLES                  AGE   VERSION   INTERNAL-IP     EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION      CONTAINER-RUNTIME
cka001   Ready    control-plane,master   74m   v1.24.0   172.16.18.170   <none>        Ubuntu 20.04.4 LTS   5.4.0-122-generic   containerd://1.5.9
cka002   Ready    <none>                 70m   v1.24.0   172.16.18.169   <none>        Ubuntu 20.04.4 LTS   5.4.0-122-generic   containerd://1.5.9
cka003   Ready    <none>                 69m   v1.24.0   172.16.18.168   <none>        Ubuntu 20.04.4 LTS   5.4.0-122-generic   containerd://1.5.9
```


4. Create resources

Use command `kubectl create --help` to get examples of creating resources.


Create namespace.
```
kubectl create namespace --help
kubectl create namespace my-namespace
```

Create Deployment on the namespace.
```
kubectl -n my-namespace create deployment my-busybox --image=busybox --replicas=3 --port=5701
```

Create ClusterRole.
```
kubectl create clusterrole --help
kubectl -n my-namespace create clusterrole pod-creater --verb=create --resource=deployment --resource-name=my-busybox
```

Create ServiceAccount
```
kubectl create serviceaccount --help
kubectl -n my-namespace create serviceaccount my-service-account
```

Create RoleBinding
Note: `RoleBinding` can reference a Role in the same namespace or a ClusterRole in the global namespace.
```
kubectl create rolebinding --help
kubectl create rolebinding NAME --clusterrole=NAME|--role=NAME [--user=username] [--group=groupname] [--serviceaccount=namespace:serviceaccountname] [--dry-run=server|client|none]
kubectl create rolebinding my-admin --clusterrole=pod-creater --serviceaccount=my-namespace:my-service-account
```



### Static Pod

`kubectl` will automatically check yaml file in `/etc/kubernetes/manifests/` and create the static pod once it's detected.

Some system static Pods are already in place.
```
ll /etc/kubernetes/manifests/
```
Result
```
-rw------- 1 root root 2292 Jul 23 10:45 etcd.yaml
-rw------- 1 root root 3889 Jul 23 10:45 kube-apiserver.yaml
-rw------- 1 root root 3395 Jul 23 10:45 kube-controller-manager.yaml
-rw------- 1 root root 1464 Jul 23 10:45 kube-scheduler.yaml
```

Create yaml file in directory `/etc/kubernetes/manifests/`.
```
kubectl run my-nginx --image=nginx:mainline --dry-run=client -n dev -oyaml > /etc/kubernetes/manifests/my-nginx.yaml
```

Check status of the Pod `my-nginx`.
```
kubectl get pod -o wide
```

The node name `cka001` is part of the Pod name, which means the Pod is running on node `cka001`.
```
NAME              READY   STATUS    RESTARTS   AGE   IP               NODE     NOMINATED NODE   READINESS GATES
my-nginx-cka001   1/1     Running   0          20s   10.244.228.196   cka001   <none>           <none>
```

Delete the yaml file `/etc/kubernetes/manifests/my-nginx.yaml`, the static pod will be deleted automatically.
```
rm /etc/kubernetes/manifests/my-nginx.yaml 
```





### Multi-Container Pod

Summary:

* Create Multi-Container Pod
* Describe the Pod
* Check the log of Pod
* Check the log of Containers


Create a Pod `multi-container-pod` with multiple container `container-1-nginx` and `container-2-alpine`.
```
kubectl apply -f - << EOF
apiVersion: v1
kind: Pod
metadata:
  name: multi-container-pod
spec:
  containers:
  - name: container-1-nginx
    image: nginx
    ports:
    - containerPort: 80  
  - name: container-2-alpine
    image: alpine
    command: ["watch", "wget", "-qO-", "localhost"]
EOF
```

Get the status.
```
kubectl get pod multi-container-pod
```
Result
```
NAME                  READY   STATUS    RESTARTS   AGE
multi-container-pod   2/2     Running   0          81s
```

Get details of the pod.
```
kubectl describe pod multi-container-pod
```
Result
```
.......
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  41s   default-scheduler  Successfully assigned dev/multi-container-pod to cka002
  Normal  Pulling    40s   kubelet            Pulling image "nginx"
  Normal  Pulled     23s   kubelet            Successfully pulled image "nginx" in 16.767129903s
  Normal  Created    22s   kubelet            Created container container-1-nginx
  Normal  Started    22s   kubelet            Started container container-1-nginx
  Normal  Pulling    22s   kubelet            Pulling image "alpine"
  Normal  Pulled     14s   kubelet            Successfully pulled image "alpine" in 7.776104353s
  Normal  Created    14s   kubelet            Created container container-2-alpine
  Normal  Started    14s   kubelet            Started container container-2-alpine
```

For multi-container pod, container name is needed if we want to get log of pod via command `kubectl logs <pod_name> <container_name>`.

Without the container name, we receive error.
```
kubectl logs multi-container-pod
```
```
error: a container name must be specified for pod multi-container-pod, choose one of: [container-1-nginx container-2-alpine]
```

With specified container name, we get the log info.
```
kubectl logs multi-container-pod container-1-nginx
```
Result
```
......
::1 - - [23/Jul/2022:04:06:37 +0000] "GET / HTTP/1.1" 200 615 "-" "Wget" "-"
```

Same if we need specify container name to login into the pod via command `kubectl exec -it <pod_name> -c <container_name> -- <commands>`.
```
kubectl exec -it multi-container-pod -c container-1-nginx -- /bin/bash
root@multi-container-pod:/# ls
bin  boot  dev  docker-entrypoint.d  docker-entrypoint.sh  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
```

Clean up
```
kubectl delete pod multi-container-pod
```





### initContainer Pod

Summary: 

* Create Pod `myapp-pod` that has two init containers. 
    * `myapp-container`
    * `init-mydb`
* Create two Services.
    * `myservice`
    * `mydb`

Conclusion:

* `myapp-container` waits for Service `myservice` up in order to resolve the name `myservice.dev.svc.cluster.local`
* `init-mydb` waits for Service `mydb` up in order to resolve the name `mydb.dev.svc.cluster.local`.

Demo: 

Create Pod `myapp-pod` with below yaml file.

Create yaml file `myapp-pod.yaml`.
```
vi myapp-pod.yaml
```

Add below content. 
Due to the command `$(cat /var/.....` will be treated as host variable, we can not use echo to generate the file. It's the variabel in container itself.
```
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: myapp-container
    image: busybox:1.28
    command: ['sh', '-c', 'echo The app is running! && sleep 3600']
  initContainers:
  - name: init-myservice
    image: busybox:1.28
    command: ['sh', '-c', "until nslookup myservice.$(cat /var/run/secrets/kubernetes.io/serviceaccount/namespace).svc.cluster.local; do echo waiting for myservice; sleep 2; done"]
  - name: init-mydb
    image: busybox:1.28
    command: ['sh', '-c', "until nslookup mydb.$(cat /var/run/secrets/kubernetes.io/serviceaccount/namespace).svc.cluster.local; do echo waiting for mydb; sleep 2; done"]

```

Apply the yaml file to create the Pod.
```
kubectl apply -f myapp-pod.yaml
```

Check Pod status.
```
kubectl get pod myapp-pod
```
Result
```
NAME        READY   STATUS     RESTARTS   AGE
myapp-pod   0/1     Init:0/2   0          12m
```

Inspect Pods. Get two errors:

* nslookup: can't resolve 'myservice.dev.svc.cluster.local'
* container "init-mydb" in pod "myapp-pod" is waiting to start: PodInitializing

```
kubectl logs myapp-pod -c init-myservice # Inspect the first init container
kubectl logs myapp-pod -c init-mydb      # Inspect the second init container
```

At this point, those init containers will be waiting to discover Services named mydb and myservice.

Create the `mydb` and `myservice` services:
```
kubectl apply -f - << EOF
apiVersion: v1
kind: Service
metadata:
  name: myservice
spec:
  ports:
  - protocol: TCP
    port: 80
    targetPort: 9376
---
apiVersion: v1
kind: Service
metadata:
  name: mydb
spec:
  ports:
  - protocol: TCP
    port: 80
    targetPort: 9377
EOF
```

Get current status of Services.
```
kubectl get service
```
Both of Services are up.
```
NAME        TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
mydb        ClusterIP   11.244.239.149   <none>        80/TCP    6s
myservice   ClusterIP   11.244.116.126   <none>        80/TCP    6s
```

Get current Pod status.
```
kubectl get pod myapp-pod -o wide
```
The Pod is up.
```
NAME        READY   STATUS     RESTARTS   AGE     IP             NODE     NOMINATED NODE   READINESS GATES
myapp-pod   0/1     Init:0/2   0          2m40s   10.244.112.2   cka002   <none>           <none>
```

We now see that those init containers complete, and that the myapp-pod Pod moves into the Running state.



Clean up.
```
kubectl delete service mydb myservice 
kubectl delete pod myapp-pod 
```





### StatefulSet

Summary: 

* Create Headless Service `nginx` and StatefulSet `web`
* Scale out StatefulSet `web`


#### Create Headless Service and StatefulSet

Create Headless Service `nginx` and StatefulSet `web`.
```
kubectl apply -f - << EOF
---
apiVersion: v1
kind: Service
metadata:
  name: nginx
  labels:
    app: nginx
spec:
  ports:
  - port: 80
    name: web
  clusterIP: None
  selector:
    app: nginx
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  serviceName: "nginx"
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
          name: web
EOF
```

Get details of StatefulSet Pod created just now.
```
kubectl get pod | grep web
```
Result
```
NAME    READY   STATUS    RESTARTS   AGE
web-0   1/1     Running   0          27s
web-1   1/1     Running   0          10s
```

Use command `kubectl edit sts web` to update an existing StatefulSet.
ONLY these fields can be updated: `replicas`、`image`、`rolling updates`、`labels`、`resource request/limit` and `annotations`.

Note: 
Copy of StatefulSet Pod will not be created automatically in other node when it's dead in current node.  




#### Scale out StatefulSet

Scale StatefulSet `web` to `5` Replicas.
```
kubectl scale sts web --replicas=5
```


Clean up.
```
kubectl delete sts web
kubectl delete service nginx
```




### DaemonSet

Create DaemonSet `daemonset-busybox`.
```
kubectl apply -f - << EOF
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: daemonset-busybox
  labels:
    app: daemonset-busybox
spec:
  selector:
    matchLabels:
      app: daemonset-busybox
  template:
    metadata:
      labels:
        app: daemonset-busybox
    spec:
      tolerations:
      - key: node-role.kubernetes.io/control-plane
        effect: NoSchedule
      - key: node-role.kubernetes.io/master
        effect: NoSchedule
      containers:
      - name: busybox
        image: busybox:1.28
        args:
        - sleep
        - "10000"
EOF

```

Get status of DaemonSet.
```
kubectl get daemonsets daemonset-busybox
```
```
NAME                DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
daemonset-busybox   3         3         3       3            3           <none>          5m33s
```

Get DaemonSet Pod status. It's deployed on each node.
```
kubectl get pod -o wide
```
Result
```
NAME                      READY   STATUS    RESTARTS   AGE   IP               NODE     NOMINATED NODE   READINESS GATES
daemonset-busybox-54cj5   1/1     Running   0          44s   10.244.102.4     cka003   <none>           <none>
daemonset-busybox-5tl55   1/1     Running   0          44s   10.244.228.197   cka001   <none>           <none>
daemonset-busybox-wg225   1/1     Running   0          44s   10.244.112.5     cka002   <none>           <none>
```


Clean up.
```
kubectl delete daemonset daemonset-busybox 
```




### Job

Create Job `pi`.
```
kubectl apply -f - << EOF
apiVersion: batch/v1
kind: Job
metadata:
  name: pi
spec:
  template:
    spec:
      containers:
      - name: pi
        image: perl:5.34
        command: ["perl",  "-Mbignum=bpi", "-wle", "print bpi(2000)"]
      restartPolicy: Never
  backoffLimit: 4
EOF

```

Get details of Job.
```
kubectl get jobs
```

Get details of Job Pod. The status `Completed` means the job was done successfully.
```
kubectl get pod
```

Get log info of the Job Pod.
```
kubectl pi-2s74d
3.141592653589793..............
```


Clean up
```
kubectl delete job pi
```




### Cronjob

Create Cronjob `hello`.
```
kubectl apply -f - << EOF
apiVersion: batch/v1
kind: CronJob
metadata:
 name: hello
spec:
  schedule: "*/1 * * * *"
  jobTemplate:
   spec:
    template:
     spec:
      containers:
      - name: hello
        image: busybox
        args:
        - /bin/sh
        - -c
        - date ; echo Hello from the kubernetes cluster
      restartPolicy: OnFailure
EOF

```

Get detail of Cronjob
```
kubectl get cronjobs -o wide
```
```
NAME    SCHEDULE      SUSPEND   ACTIVE   LAST SCHEDULE   AGE   CONTAINERS   IMAGES    SELECTOR
hello   */1 * * * *   False     0        <none>          25s   hello        busybox   <none>
```

Monitor Jobs. Every 1 minute a new job will be created. 
```
kubectl get jobs -w
```

Clean up
```
kubectl delete cronjob hello
```



### Demo: Operations on Resources

Summary:

* Node Label
* Namespace
* ServiceAccount Authorization
    * Grant API access authorization to default ServiceAccount
* Deployment
* Expose Service
* Scale out the Deployment
* Rolling update
* Rolling back update
* Event
* Logging


#### Node Label

Add/update/remove node Label.
```
# Update node label
kubectl label node cka002 node=demonode

# Get node info with label info
kubectl get node --show-labels

# Search node by label
kubectl get node -l node=demonode

# Remove a lable of node
kubectl label node cka002 node-
```



#### Namespace

Get current available namespaces.
```
kubectl get namespace
```
Result
```
NAME              STATUS   AGE
default           Active   3h45m
dev               Active   3h11m
kube-node-lease   Active   3h45m
kube-public       Active   3h45m
kube-system       Active   3h45m
```

Get Pod under a specific namespace.
```
kubectl get pod -n kube-system
```
Result
```
NAME                                       READY   STATUS    RESTARTS   AGE
calico-kube-controllers-5c64b68895-jr4nl   1/1     Running   0          3h25m
calico-node-dsx76                          1/1     Running   0          3h25m
calico-node-p5rf2                          1/1     Running   0          3h25m
calico-node-tr22l                          1/1     Running   0          3h25m
coredns-6d8c4cb4d-g4jxc                    1/1     Running   0          3h45m
coredns-6d8c4cb4d-sqcvj                    1/1     Running   0          3h45m
etcd-cka001                                1/1     Running   0          3h45m
kube-apiserver-cka001                      1/1     Running   0          3h45m
kube-controller-manager-cka001             1/1     Running   0          3h45m
kube-proxy-5cdbj                           1/1     Running   0          3h41m
kube-proxy-cm4hc                           1/1     Running   0          3h45m
kube-proxy-g4w52                           1/1     Running   0          3h41m
kube-scheduler-cka001                      1/1     Running   0          3h45m
```

Get Pods in all namespaces.
```
kubectl get pod --all-namespaces
kubectl get pod -A
```



#### ServiceAccount Authorization

With Kubernetes 1.23 and lower version, when we create a new namespace, Kubernetes will automatically create a ServiceAccount `default` and a token `default-token-xxxxx`.

We can say that the ServiceAccount `default` is an account under the namespace.

Here is an example of new namespace `dev`.

* ServiceAcccount: `default`
* Token: `default-token-8vrsc`

Get current ServiceAccount on Namespace `dev`.
```
kubectl get serviceaccount -n dev
```
Result
```
NAME      SECRETS   AGE
default   1         3h12m
```

Get current Token for ServiceAccount `default` on Namespace `dev`.
```
kubectl get secrets -n dev
```
Result
```
NAME                  TYPE                                  DATA   AGE
default-token-qd68h   kubernetes.io/service-account-token   3      3h12m
```

There is a default cluster role `admin`.
```
kubectl get clusterrole admin
```
Result
```
NAME    CREATED AT
admin   2022-07-23T02:45:51Z
```

But there is no clusterrole binding to the cluster role `admin`.
```
kubectl get clusterrolebinding | grep ClusterRole/admin
```

Role and rolebinding is namespaces based. On Namespace `dev`, there is no role and rolebinding after fresh installation.
```
kubectl get role -n dev
kubectl get rolebinding -n dev
```

Get token of the service account `default`.
```
TOKEN=$(kubectl describe secret $(kubectl get secrets | grep default | cut -f1 -d ' ') | grep -E '^token' | cut -f2 -d':' | tr -d ' ')
echo $TOKEN
```

Get API Service address.
```
APISERVER=$(kubectl config view | grep https | cut -f 2- -d ":" | tr -d " ")
echo $APISERVER
```

Get Pod resources in namespace `dev` via API server with JSON layout.
```
curl $APISERVER/api/v1/namespaces/dev/pods --header "Authorization: Bearer $TOKEN" --insecure
```

We will receive `430 forbidden` error message. The ServiceAccount `default` does not have authorization to access pod.

Let's create a rolebinding `rolebinding-admin` to bind cluster role `admin` to service account `default` in namespapce `dev`.
Hence service account `default` is granted adminstrator authorization in namespace `dev`.
```
# Usage:
kubectl create rolebinding <rule> --clusterrole=<clusterrule> --serviceaccount=<namespace>:<name> --namespace=<namespace>

# Crate rolebinding:
kubectl create rolebinding rolebinding-admin --clusterrole=admin --serviceaccount=dev:default --namespace=dev
```

Result looks like below by executing `kubectl get rolebinding -n dev`.
```
NAME                ROLE                AGE
rolebinding-admin   ClusterRole/admin   10s
```

Try again, get pod resources in namespace `dev` via API server with JSON layout.
```
curl $APISERVER/api/v1/namespaces/dev/pods --header "Authorization: Bearer $TOKEN" --insecure
```




#### Deployment

Create a Ubuntu Pod for operation. And attach to the running Pod. 
```
kubectl create -f - << EOF
apiVersion: v1
kind: Pod
metadata:
  name: ubuntu
  labels:
    app: ubuntu
spec:
  containers:
  - name: ubuntu
    image: ubuntu:latest
    command: ["/bin/sleep", "3650d"]
    imagePullPolicy: IfNotPresent
  restartPolicy: Always
EOF

kubectl exec --stdin --tty ubuntu -- /bin/bash
```

Create a deployment, option `--image` specifies a image，option `--port` specifies port for external access. 
A pod is also created when deployment is created.
```
kubectl create deployment myapp --image=docker.io/jocatalin/kubernetes-bootcamp:v1 --replicas=1 --port=8080
```

Get deployment status
```
kubectl get deployment myapp -o wide
```
Result
```
NAME    READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS            IMAGES                                       SELECTOR
myapp   1/1     1            1           79s   kubernetes-bootcamp   docker.io/jocatalin/kubernetes-bootcamp:v1   app=myapp
```

Get detail information of deployment.
```
kubectl describe deployment myapp
```
Result
```
Name:                   myapp
Namespace:              dev
CreationTimestamp:      Sat, 23 Jul 2022 14:36:43 +0800
Labels:                 app=myapp
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=myapp
Replicas:               1 desired | 1 updated | 1 total | 1 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=myapp
  Containers:
   kubernetes-bootcamp:
    Image:        docker.io/jocatalin/kubernetes-bootcamp:v1
    Port:         8080/TCP
    Host Port:    0/TCP
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  <none>
NewReplicaSet:   myapp-b5d775f5d (1/1 replicas created)
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  95s   deployment-controller  Scaled up replica set myapp-b5d775f5d to 1
```




#### Expose Service

Get the Pod and Deployment we created just now.
```
kubectl get deployment myapp -o wide
kubectl get pod -o wide
```
Result
```
NAME                    READY   STATUS    RESTARTS   AGE     IP             NODE     NOMINATED NODE   READINESS GATES
myapp-b5d775f5d-cx8dx   1/1     Running   0          2m34s   10.244.102.7   cka003   <none>           <none>
```

Send http request to the Pod `curl 10.244.102.7:8080` with below result.
```
Hello Kubernetes bootcamp! | Running on: myapp-b5d775f5d-6jtgs | v=1
```

To make pod be accessed outside, we need expose port `8080` to a node port. A related service will be created. 
```
kubectl expose deployment myapp --type=NodePort --port=8080
```

Get details of service `myapp` by executing `kubectl get svc myapp -o wide`.
```
NAME    TYPE       CLUSTER-IP    EXTERNAL-IP   PORT(S)          AGE   SELECTOR
myapp   NodePort   11.244.74.3   <none>        8080:30514/TCP   7s    app=myapp
```

Send http request to service port.
```
curl 11.244.74.3:8080
Hello Kubernetes bootcamp! | Running on: myapp-b5d775f5d-cx8dx | v=1
```

Get more details of the service.
```
kubectl get svc myapp -o yaml
kubectl describe svc myapp
```

Get details of related endpoint `myapp` by executing `kubectl get endpoints myapp -o wide`.
```
NAME    ENDPOINTS           AGE
myapp   10.244.102.7:8080   43s
```

Send http request to the service and node sucessfully. Pod port `8080` is mapped to node port `32566`.

Send http request to node port on `cka003`.
```
curl 172.16.18.168:30514
Hello Kubernetes bootcamp! | Running on: myapp-b5d775f5d-6jtgs | v=1
```

Attach to Ubuntu Pod we created and send http request to the Service and Pod and Node of `myapp`.
```
kubectl exec --stdin --tty ubuntu -- /bin/bash
curl 10.244.102.7:8080
curl 11.244.74.3:8080
curl 172.16.18.168:30514
Hello Kubernetes bootcamp! | Running on: myapp-b5d775f5d-6jtgs | v=1
```




#### Scale out Deployment

Scale out by replicaset. We set three replicasets to scale out deployment `myapp`. The number of deployment `myapp` is now three.
```
kubectl scale deployment myapp --replicas=3
```

Get status of deployment
```
kubectl get deployment myapp
```

Get status of replicaset
```
kubectl get replicaset
```


#### Rolling update

Command usage: `kubectl set image (-f FILENAME | TYPE NAME) CONTAINER_NAME_1=CONTAINER_IMAGE_1 ... CONTAINER_NAME_N=CONTAINER_IMAGE_N`.

With the command `kubectl get deployment`, we will get deployment name `myapp` and related container name `kubernetes-bootcamp`.
```
kubectl get deployment myapp -o wide
```

With the command `kubectl set image` to update image to many versions and log the change under deployment's annotations with option `--record`.
```
kubectl set image deployment/myapp kubernetes-bootcamp=docker.io/jocatalin/kubernetes-bootcamp:v2 --record
```

Current replicas status
```
kubectl get replicaset -o wide -l app=myapp
```
Result. Pods are running on new Replicas.
```
NAME               DESIRED   CURRENT   READY   AGE   CONTAINERS            IMAGES                                       SELECTOR
myapp-5dbd68cc99   1         1         0       8s    kubernetes-bootcamp   docker.io/jocatalin/kubernetes-bootcamp:v2   app=myapp,pod-template-hash=5dbd68cc99
myapp-b5d775f5d    3         3         3       14m   kubernetes-bootcamp   docker.io/jocatalin/kubernetes-bootcamp:v1   app=myapp,pod-template-hash=b5d775f5d
```

We can get the change history under `metadata.annotations`.
```
kubectl get deployment myapp -o yaml
```
Result
```
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    deployment.kubernetes.io/revision: "2"
    kubernetes.io/change-cause: kubectl set image deployment/myapp kubernetes-bootcamp=docker.io/jocatalin/kubernetes-bootcamp:v2
      --record=true
  ......
```

We can also get the change history by command `kubectl rollout history`, and show details with specific revision `--revision=<revision_number>`.
```
kubectl rollout history deployment/myapp
```
Result
```
deployment.apps/myapp 
REVISION  CHANGE-CAUSE
1         <none>
2         kubectl set image deployment/myapp kubernetes-bootcamp=docker.io/jocatalin/kubernetes-bootcamp:v2 --record=true
```

Get rollout history with specific revision.
```
kubectl rollout history deployment/myapp --revision=2
```

Roll back to previous revision with command `kubectl rollout undo `, or roll back to specific revision with option `--to-revision=<revision_number>`.
```
kubectl rollout undo deployment/myapp --to-revision=1
```

Revision `1` was replaced by new revision `3` now.
```
kubectl rollout history deployment/myapp
```
Result
```
deployment.apps/myapp 
REVISION  CHANGE-CAUSE
2         kubectl set image deployment/myapp kubernetes-bootcamp=docker.io/jocatalin/kubernetes-bootcamp:v2 --record=true
3         <none>
```



#### Event

Get detail event info of related Pod.
```
kubectl describe pod myapp-b5d775f5d-jlx6g
```

Result looks like below.
```
......
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  54s   default-scheduler  Successfully assigned dev/myapp-b5d775f5d-jlx6g to cka003
  Normal  Pulled     53s   kubelet            Container image "docker.io/jocatalin/kubernetes-bootcamp:v1" already present on machine
  Normal  Created    53s   kubelet            Created container kubernetes-bootcamp
  Normal  Started    53s   kubelet            Started container kubernetes-bootcamp
```

Get detail event info of entire cluster.
```
kubectl get event
```




#### Logging

Get log info of Pod.
```
kubectl logs -f <pod_name>
kubectl logs -f <pod_name> -c <container_name> 
```

Get a Pod logs
```
kubectl logs -f myapp-b5d775f5d-jlx6g
```
```
Kubernetes Bootcamp App Started At: 2022-07-23T06:54:18.532Z | Running On:  myapp-b5d775f5d-jlx6g

```

Get log info of K8s components. 
```
kubectl logs kube-apiserver-cka001 -n kube-system
kubectl logs kube-controller-manager-cka001 -n kube-system
kubectl logs kube-scheduler-cka001 -n kube-system
kubectl logs etcd-cka001 -n kube-system
systemctl status kubelet
journalctl -fu kubelet
kubectl logs kube-proxy-5cdbj -n kube-system
```


Clean up.
```
kubectl delete service myapp
kubectl delete deployment myapp
```










## 5.Label and Annotation

### Label and Annotation

#### Label

Set Label `disktype=ssd` for node `cka003`.
```
kubectl label node cka003 disktype=ssd
```

Get Label info
```
kubectl get node --show-labels
kubectl describe node cka003
kubectl get node cka003 -oyaml
```

Overwrite Label with `disktype=hdd` for node `cka003`.
```
kubectl label node cka003 disktype=hdd --overwrite
```

Remove Label for node `cka003`
```
kubectl label node cka003 disktype-
```



#### Annotation

Create Nginx deployment
```
kubectl create deploy nginx --image=nginx:mainline
```

Get Annotation info.
```
kubectl describe deployment/nginx
```
Result
```
......
Labels:                 app=nginx
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=nginx
......
```

Add new Annotation.
```
kubectl annotate deployment nginx owner=James.H
```

Now annotation looks like below.
```
......
Labels:                 app=nginx
Annotations:            deployment.kubernetes.io/revision: 1
                        owner: James.H
Selector:               app=nginx
......
```

Update/Overwrite Annotation.
```
kubectl annotate deployment/nginx owner=K8s --overwrite
```
Now annotation looks like below.
```
......
Annotations:            deployment.kubernetes.io/revision: 1
                        owner: K8s
Selector:               app=nginx
......
```

Remove Annotation
```
kubectl annotate deployment/nginx owner-
```
```
......
Labels:                 app=nginx
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=nginx
......
```

Clean up
```
kubectl delete deployment nginx
```




## 6.Health Check

### Status of Pod and Container

Create a Pod `multi-pods` with two containers `nginx` and `busybox`. 
```
kubectl apply -f - << EOF
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: multi-pods
  name: multi-pods
spec:
  containers:
  - image: nginx
    name: nginx
  - image: busybox
    name: busybox
  dnsPolicy: ClusterFirst
  restartPolicy: Always
EOF
```

Minotor the status with option `--watch`. The status of Pod was changed from `ContainerCreating` to `NotReady` to `CrashLoopBackOff`.
```
kubectl get pod multi-pods --watch
```

Get details of the Pod `multi-pods`, focus on Container's state under segment `Containers` and Conditions of Pod under segment `Conditions`.
```
kubectl describe pod multi-pods
```
Result
```
......
Containers:
  nginx:
    ......
    State:          Running
      Started:      Sat, 23 Jul 2022 15:06:56 +0800
    Ready:          True
    Restart Count:  0
    ......
  busybox:
    ......
    State:          Terminated
      Reason:       Completed
      Exit Code:    0
......
Conditions:
  Type              Status
  Initialized       True 
  Ready             False 
  ContainersReady   False 
  PodScheduled      True 
...... 
```





### LivenessProbe

Detail description of the demo can be found on the [Kubernetes document](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/).

Create a yaml file `liveness.yaml` with `livenessProbe` setting and apply it.
```
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  labels:
    test: liveness
  name: liveness-exec
spec:
  containers:
  - name: liveness
    image: busybox
    args:
    - /bin/sh
    - -c
    - touch /tmp/healthy; sleep 30; rm -rf /tmp/healthy; sleep 600
    livenessProbe:
      exec:
        command:
        - cat
        - /tmp/healthy
      initialDelaySeconds: 5
      periodSeconds: 5
EOF

```

Let's see what happened in the Pod `liveness-exec`.

* Create a folder `/tmp/healthy`.
* Execute the the command `cat /tmp/healthy` and return successful code.
* After `35` seconds, execute command `rm -rf /tmp/healthy` to delete the folder. The probe `livenessProbe` detects the failure and return error message.
* The kubelet kills the container and restarts it. The folder is created again `touch /tmp/healthy`.

By command `kubectl describe pod liveness-exec`, wec can see below event message. 
Once failure detected, image will be pulled again and the folder `/tmp/healthy` is in place again.
```
......
Events:
  Type     Reason     Age                From               Message
  ----     ------     ----               ----               -------
  Normal   Scheduled  63s                default-scheduler  Successfully assigned dev/liveness-exec to cka002
  Normal   Pulling    62s                kubelet            Pulling image "busybox"
  Normal   Pulled     53s                kubelet            Successfully pulled image "busybox" in 9.153404392s
  Normal   Created    53s                kubelet            Created container liveness
  Normal   Started    53s                kubelet            Started container liveness
  Warning  Unhealthy  12s (x3 over 22s)  kubelet            Liveness probe failed: cat: can't open '/tmp/healthy': No such file or directory
  Normal   Killing    12s                kubelet            Container liveness failed liveness probe, will be restarted
```




### ReadinessProbe

Readiness probes are configured similarly to liveness probes. 
The only difference is that you use the readinessProbe field instead of the livenessProbe field.

Create a yaml file `readiness.yaml` with `readinessProbe` setting and apply it.
```
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: readiness
spec:
    containers:
    - name: readiness
      image: busybox
      args:
      - /bin/sh
      - -c
      - touch /tmp/healthy; sleep 5;rm -rf /tmp/healthy; sleep 600
      readinessProbe:
        exec:
          command:
          - cat
          - /tmp/healthy
        initialDelaySeconds: 10
        periodSeconds: 5
EOF

```

The ready status of the Pod is 0/1, that is, the Pod is not up successfully.
```
kubectl get pod readiness --watch
```
Result
```
NAME        READY   STATUS    RESTARTS   AGE
readiness   0/1     Running   0          15s
```

Execute command `kubectl describe pod readiness` to check status of Pod. 
We see failure message `Readiness probe failed`.
```
......
Events:
  Type     Reason     Age               From               Message
  ----     ------     ----              ----               -------
  Normal   Scheduled  46s               default-scheduler  Successfully assigned dev/readiness to cka002
  Normal   Pulling    45s               kubelet            Pulling image "busybox"
  Normal   Pulled     43s               kubelet            Successfully pulled image "busybox" in 2.244369424s
  Normal   Created    43s               kubelet            Created container readiness
  Normal   Started    43s               kubelet            Started container readiness
  Warning  Unhealthy  1s (x7 over 31s)  kubelet            Readiness probe failed: cat: can't open '/tmp/healthy': No such file or directory
```


Liveness probes do not wait for readiness probes to succeed. 
If we want to wait before executing a liveness probe you should use initialDelaySeconds or a startupProbe.


Clean up.
```
kubectl delete pod liveness-exec
kubectl delete pod multi-pods 
kubectl delete pod readiness
```






### Demo: Health Check

Summary:

* Create Deployment and Service
* Simulate an error (delete index.html)
* Pod is in unhealth status and is removed from endpoint list
* Fix the error (revert the index.html)
* Pod is back to normal and in endpoint list


#### Create Deployment and Service

Create Deployment `nginx-healthcheck` and Service `nginx-healthcheck`.
```
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-healthcheck
spec:
  replicas: 2
  selector:
    matchLabels:
      name: nginx-healthcheck
  template:
    metadata:
      labels:
        name: nginx-healthcheck
    spec:
      containers:
        - name: nginx-healthcheck
          image: nginx:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 80  
          livenessProbe:
            initialDelaySeconds: 5
            periodSeconds: 5
            tcpSocket:
              port: 80
            timeoutSeconds: 5   
          readinessProbe:
            httpGet:
              path: /
              port: 80
              scheme: HTTP
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-healthcheck
spec:
  ports:
    - port: 80
      targetPort: 80
      protocol: TCP
  type: NodePort
  selector:
    name: nginx-healthcheck
EOF

```

Check Pod `nginx-healthcheck`.
```
kubectl get pod -owide
```
Result
```
NAME                                 READY   STATUS    RESTARTS   AGE   IP              NODE     NOMINATED NODE   READINESS GATES
nginx-healthcheck-79fc55d944-jw887   1/1     Running   0          9s    10.244.102.14   cka003   <none>           <none>
nginx-healthcheck-79fc55d944-nwwjc   1/1     Running   0          9s    10.244.112.13   cka002   <none>           <none>
```

Access Pod IP via `curl` command, e.g., above example.
```
curl 10.244.102.14
curl 10.244.112.13
```
We see a successful `index.html` content of Nginx below with above example.

Check details of Service craeted in above example.
```
kubectl describe svc nginx-healthcheck
```
We will see below output. There are two Pods information listed in `Endpoints`.
```
Name:                     nginx-healthcheck
Namespace:                dev
Labels:                   <none>
Annotations:              <none>
Selector:                 name=nginx-healthcheck
Type:                     NodePort
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       11.244.238.20
IPs:                      11.244.238.20
Port:                     <unset>  80/TCP
TargetPort:               80/TCP
NodePort:                 <unset>  31795/TCP
Endpoints:                10.244.102.14:80,10.244.112.13:80
Session Affinity:         None
External Traffic Policy:  Cluster
Events:                   <none>
```

We can also get information of Endpoints.
```
kubectl get endpoints nginx-healthcheck
```
Result
```
NAME                ENDPOINTS                           AGE
nginx-healthcheck   10.244.102.14:80,10.244.112.13:80   72s
```

Till now, two `nginx-healthcheck` Pods are working and providing service as expected. 


#### Simulate readinessProbe Failure

Let's simulate an error by deleting and `index.html` file in on of `nginx-healthcheck` Pod and see what's readinessProbe will do.

First, execute `kubectl exec -it <your_pod_name> -- bash` to log into `nginx-healthcheck` Pod, and delete the `index.html` file.
```
kubectl exec -it nginx-healthcheck-79fc55d944-jw887 -- bash
cd /usr/share/nginx/html/
rm -rf index.html
exit
```

After that, let's check the status of above Pod that `index.html` file was deleted.
```
kubectl describe pod nginx-healthcheck-79fc55d944-jw887
```
We can now see `Readiness probe failed` error event message.
```
......
Events:
  Type     Reason     Age              From               Message
  ----     ------     ----             ----               -------
  Normal   Scheduled  2m8s             default-scheduler  Successfully assigned dev/nginx-healthcheck-79fc55d944-jw887 to cka003
  Normal   Pulled     2m7s             kubelet            Container image "nginx:latest" already present on machine
  Normal   Created    2m7s             kubelet            Created container nginx-healthcheck
  Normal   Started    2m7s             kubelet            Started container nginx-healthcheck
  Warning  Unhealthy  2s (x2 over 7s)  kubelet            Readiness probe failed: HTTP probe failed with statuscode: 403
```

Let's check another Pod. 
```
kubectl describe pod nginx-healthcheck-79fc55d944-nwwjc
```
There is no error info.
```
......
Events:
  Type    Reason     Age    From               Message
  ----    ------     ----   ----               -------
  Normal  Scheduled  3m46s  default-scheduler  Successfully assigned dev/nginx-healthcheck-79fc55d944-nwwjc to cka002
  Normal  Pulled     3m45s  kubelet            Container image "nginx:latest" already present on machine
  Normal  Created    3m45s  kubelet            Created container nginx-healthcheck
  Normal  Started    3m45s  kubelet            Started container nginx-healthcheck
```

Now, access Pod IP via `curl` command and see what the result of each Pod.
```
curl 10.244.102.14
curl 10.244.112.13
```

`curl 10.244.102.14` failed with `403 Forbidden` error below. 
`curl 10.244.112.13` works well.


Let's check current status of Nginx Service after one of Pods runs into failure. 
```
kubectl describe svc nginx-healthcheck
```

In below output, there is only one Pod information listed in Endpoint.
```
Name:                     nginx-healthcheck
Namespace:                dev
Labels:                   <none>
Annotations:              <none>
Selector:                 name=nginx-healthcheck
Type:                     NodePort
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       11.244.238.20
IPs:                      11.244.238.20
Port:                     <unset>  80/TCP
TargetPort:               80/TCP
NodePort:                 <unset>  31795/TCP
Endpoints:                10.244.112.13:80
Session Affinity:         None
External Traffic Policy:  Cluster
Events:                   <none>
```

Same result we can get by checking information of Endpoints, which is only Pod is running.
```
kubectl get endpoints nginx-healthcheck 
```
Output:
```
NAME                ENDPOINTS          AGE
nginx-healthcheck   10.244.112.13:80   6m5s
```


#### Fix readinessProbe Failure

Let's re-create the `index.html` file again in the Pod. 
```
kubectl exec -it nginx-healthcheck-79fc55d944-jw887 -- bash

cd /usr/share/nginx/html/

cat > index.html << EOF 
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
EOF

exit
```

We now can see that two Pods are back to Endpoints to provide service now.
```
kubectl describe svc nginx-healthcheck

kubectl get endpoints nginx-healthcheck
```

Re-access Pod IP via `curl` command and we can see both are back to normal status.
```
curl 10.244.102.14
curl 10.244.112.13
```

Verify the Pod status again. 
```
kubectl describe pod nginx-healthcheck-79fc55d944-jw887
```

#### Conclusion

By delete the `index.html` file, the Pod is in unhealth status and is removed from endpoint list. 
One one health Pod can provide normal service.


Clean up
```
kubectl delete service nginx-healthcheck
kubectl delete deployment nginx-healthcheck
```


#### Simulate livenessProbe Failure

Re-create Deployment `nginx-healthcheck` and Service `nginx-healthcheck`.

Deployment:
```
NAME                     READY   UP-TO-DATE   AVAILABLE   AGE
nginx-healthcheck        0/2     2            0           7s
```

Pods:
```
NAME                                      READY   STATUS    RESTARTS   AGE
nginx-healthcheck-79fc55d944-lknp9        1/1     Running   0          96s
nginx-healthcheck-79fc55d944-wntmg        1/1     Running   0          96s
```

Change nginx default listening port from `80` to `90` to simulate livenessProbe Failure. livenessProbe check the live status via port `80`. 
```
kubectl exec -it nginx-healthcheck-79fc55d944-lknp9 -- bash
root@nginx-healthcheck-79fc55d944-lknp9:/# cd /etc/nginx/conf.d
root@nginx-healthcheck-79fc55d944-lknp9:/etc/nginx/conf.d# sed -i 's/80/90/g' default.conf
root@nginx-healthcheck-79fc55d944-lknp9:/etc/nginx/conf.d# nginx -s reload
2022/07/24 12:59:45 [notice] 79#79: signal process started
```

The Pod runs into failure.
```
kubectl describe pod nginx-healthcheck-79fc55d944-lknp9
```
We can see `livenessProbe` failed error event message.
```
Events:
  Type     Reason     Age                    From               Message
  ----     ------     ----                   ----               -------
  Normal   Scheduled  17m                    default-scheduler  Successfully assigned dev/nginx-healthcheck-79fc55d944-lknp9 to cka003
  Normal   Pulled     2m47s (x2 over 17m)    kubelet            Container image "nginx:latest" already present on machine
  Normal   Created    2m47s (x2 over 17m)    kubelet            Created container nginx-healthcheck
  Normal   Started    2m47s (x2 over 17m)    kubelet            Started container nginx-healthcheck
  Warning  Unhealthy  2m47s (x4 over 2m57s)  kubelet            Readiness probe failed: Get "http://10.244.102.46:80/": dial tcp 10.244.102.46:80: connect: connection refused
  Warning  Unhealthy  2m47s (x3 over 2m57s)  kubelet            Liveness probe failed: dial tcp 10.244.102.46:80: connect: connection refused
  Normal   Killing    2m47s                  kubelet            Container nginx-healthcheck failed liveness probe, will be restarted
```

Once failure detected by `livenessProbe`, the container will restarted again automatically. 
The `default.conf` we modified will be replaced by default file and the container status is up and normal.




## 7.Namespace

Get list of Namespace
```
kubectl get namespace
```

Get list of Namespace with Label information.
```
kubectl get ns --show-labels
```

Create a Namespace
```
kubectl create namespace cka
```

Label the new created Namespace `cka`.
```
kubectl label ns cka cka=true
```

Create Nginx Deployment in Namespace `cka`. 
```
kubectl create deploy nginx --image=nginx --namespace cka
```

Check Deployments and Pods running in namespace `cka`.
```
kubectl get deploy,pod -n cka
```
Result is below.
```
NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/nginx   1/1     1            1           2m14s

NAME                         READY   STATUS    RESTARTS   AGE
pod/nginx-85b98978db-bmkhf   1/1     Running   0          2m14s
```

Delete namespace `cka`. All resources in the namespaces will be gone.
```
kubectl delete ns cka
```





## 8.Horizontal Pod Autoscaling (HPA)

Summary:

* Install Metrics Server component
* Create Deployment `podinfo` and Service `podinfo` for stress testing
* Create HPA `nginx`
* Stress Testing



### Install Metrics Server component

Download yaml file for Metrics Server component
```
wget https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

Replace Google image by Aliyun image `image: registry.aliyuncs.com/google_containers/metrics-server:v0.6.1`.
```
sed -i 's/k8s\.gcr\.io\/metrics-server\/metrics-server\:v0\.6\.1/registry\.aliyuncs\.com\/google_containers\/metrics-server\:v0\.6\.1/g' components.yaml
```

Change `arg` of `metrics-server` by adding `--kubelet-insecure-tls` to disable tls certificate validation. 
```
vi components.yaml
```
Updated `arg` of `metrics-server` is below.
```
......
  template:
    metadata:
      labels:
        k8s-app: metrics-server
    spec:
      containers:
      - args:
        - --cert-dir=/tmp
        - --secure-port=4443
        - --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
        - --kubelet-use-node-status-port
        - --metric-resolution=15s
        - --kubelet-insecure-tls
        image: registry.aliyuncs.com/google_containers/metrics-server:v0.6.1
......
```

Appy the yaml file `components.yaml` to deploy `metrics-server`.
```
kubectl apply -f components.yaml
```
Below resources were crested. 
```
serviceaccount/metrics-server created
clusterrole.rbac.authorization.k8s.io/system:aggregated-metrics-reader created
clusterrole.rbac.authorization.k8s.io/system:metrics-server created
rolebinding.rbac.authorization.k8s.io/metrics-server-auth-reader created
clusterrolebinding.rbac.authorization.k8s.io/metrics-server:system:auth-delegator created
clusterrolebinding.rbac.authorization.k8s.io/system:metrics-server created
service/metrics-server created
deployment.apps/metrics-server created
apiservice.apiregistration.k8s.io/v1beta1.metrics.k8s.io created
```

Verify if `metrics-server` Pod is running as expected (`1/1` running)
```
kubectl get pod -n kube-system -owide | grep metrics-server
```
Result
```
NAME                                       READY   STATUS    RESTARTS   AGE     IP               NODE     NOMINATED NODE   READINESS GATES
metrics-server-7fd564dc66-sdhdc            1/1     Running   0          61s     10.244.102.15    cka003   <none>           <none>
```


Get current usage of CPU, memory of each node.
```
kubectl top node
```
Result:
```
NAME     CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%   
cka001   595m         29%    1937Mi          50%       
cka002   75m          3%     1081Mi          28%       
cka003   79m          3%     1026Mi          26% 
```


### Deploy a Service `podinfo`

Create Deployment `podinfo` and Service `podinfo` for further stress testing.
```
kubectl apply -f - << EOF
apiVersion: v1
kind: Service
metadata:
  name: podinfo
  labels:
    app: podinfo
spec:
  type: NodePort
  ports:
    - port: 9898
      targetPort: 9898
      nodePort: 31198
      protocol: TCP
  selector:
    app: podinfo
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: podinfo
  labels:
    app: podinfo
spec:
  replicas: 2
  selector:
    matchLabels:
      app: podinfo
  template:
    metadata:
      labels:
        app: podinfo
    spec:
      containers:
      - name: podinfod
        image: stefanprodan/podinfo:0.0.1
        imagePullPolicy: Always
        command:
          - ./podinfo
          - -port=9898
          - -logtostderr=true
          - -v=2
        ports:
        - containerPort: 9898
          protocol: TCP
        resources:
          requests:
            memory: "32Mi"
            cpu: "10m"
          limits:
            memory: "256Mi"
            cpu: "100m"
EOF

```



### Config HPA
 
Create HPA `nginx` by setting CPU threshold `50%` to trigger auto-scalling with minimal `2` and maximal `10` Replicas.
```
kubectl apply -f - <<EOF
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: nginx
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: podinfo
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 50
EOF
```

For `autoscaling/v2` version, we can either use below template to create HPA. 
And add memory resource in the matrics.
```
kubectl apply -f - <<EOF
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: nginx
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: podinfo
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
  - type: Resource
    resource:
      name: memory
      target:
        type: AverageValue
        averageValue: 100Mi
EOF
```

Memo: 

> `metrics.resource` The values will be averaged together before being compared to the target. 在与目标值比较之前，这些指标值将被平均。
> 
> `metrics.resource.target.type` represents whether the metric type is Utilization, Value, or AverageValue
> 
> `metrics.resource.target.averageUtilization` is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type. 是跨所有相关 Pod 得出的资源指标均值的目标值。
> 
> `metrics.resource.target.averageValue` (Quantity) is the target value of the average of the metric across all relevant pods (as a quantity). 跨所有 Pod 得出的指标均值的目标值（以数量形式给出）。
> 
> `metrics.resource.target.value` (Quantity) is the target value of the metric (as a quantity). 是指标的目标值（以数量形式给出）。



Get status of HPA.
```
kubectl get hpa
```
Result:
```
NAME    REFERENCE            TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
nginx   Deployment/podinfo   5%/50%    2         10        2          21s
```




### Stress Testing

Install ab

Here we will use `ab` tool to simulate 1000 concurrency.

The `ab` command is a command line load testing and benchmarking tool for web servers that allows you to simulate high traffic to a website. 

The short definition form apache.org is: The acronym `ab` stands for Apache Bench where bench is short for benchmarking.

Execute below command to install `ab` tool.
```
apt install apache2-utils -y
```

Most common options of `ab` are `-n` and `-c`：
```
-n requests     Number of requests to perform
-c concurrency  Number of multiple requests to make at a time
-t timelimit    Seconds to max. to spend on benchmarking. This implies -n 50000
-p postfile     File containing data to POST. Remember also to set -T      
-T content-type Content-type header to use for POST/PUT data, eg. 'application/x-www-form-urlencoded'. Default is 'text/plain'
-k              Use HTTP KeepAlive feature
```

Example: 
```
ab -n 1000 -c 100 http://www.baidu.com/
```

Concurrency Stres Test 

Simulate 1000 concurrency request to current node running command `ab`. Node port `31198` is the for the service `podinfo`.
```
ab -c 1000 -t 60 http://127.0.0.1:31198/
```

By command `kubectl get hpa -w` we can see that CPU workload has been increasing.
```
NAME    REFERENCE            TARGETS     MINPODS   MAXPODS   REPLICAS   AGE
......
nginx   Deployment/podinfo   199%/50%    2         10        10         14m
nginx   Deployment/podinfo   934%/50%    2         10        10         14m
nginx   Deployment/podinfo   964%/50%    2         10        10         14m
nginx   Deployment/podinfo   992%/50%    2         10        10         15m
nginx   Deployment/podinfo   728%/50%    2         10        10         15m
nginx   Deployment/podinfo   119%/50%    2         10        10         15m
......
```
And see auto-scalling automically triggered for Deployment `podinfo`.
```
kubectl get pod
kubectl get deployment
```

Please be noted the scale up is a phased process rather than a sudden event to scale to max. 
And it'll be scaled down to a balanced status when CPU workload is down.
```
kubectl get hpa -w
```
After several hours, we can see below result with above command.
```
NAME    REFERENCE            TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
nginx   Deployment/podinfo   0%/50%    2         10        2          8h 
```

Clean up.
```
kubectl delete service podinfo
kubectl delete deployment podinfo
```





## 9.Service

Summary:

* Create Deployment `httpd-app`.
* Create Service `httpd-app` with type `ClusterIP`, which is default type and accessable internally.
* Verify the access to Pod IP and Service ClusterIP.
* Update Service `httpd-app` with type `NodePort`. No change to the Deployment `httpd-app`.
* Verify the access to Node. The access will route to Pod. The service is now accesable from outside.
* Create Headless Service `web` and StatefulSet `web`.


### ClusterIP

#### Create Service

Create a Deployment `http-app`.
Create a Service `httpd-app` link to Development `http-app` by Label Selector. 

Service type is `ClusterIP`, which is default type and accessable internally. 

```
kubectl apply -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  name: httpd-app
spec:
  type: ClusterIP
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  selector:
    app: httpd
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: httpd-app
spec:
  selector:
    matchLabels:
      app: httpd
  replicas: 2
  template:
    metadata:
      labels:
        app: httpd
    spec:
      containers:
      - name: httpd
        image: httpd
        ports:
        - containerPort: 80
EOF
```

Execute command `kubectl get deployment,service,pod -o wide` to check resources we created. 
```
NAME                        READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES   SELECTOR
deployment.apps/httpd-app   0/2     2            0           14s   httpd        httpd    app=httpd

NAME                TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE   SELECTOR
service/httpd-app   ClusterIP   11.244.247.7   <none>        80/TCP    14s   app=httpd

NAME                             READY   STATUS    RESTARTS   AGE    IP              NODE     NOMINATED NODE   READINESS GATES
pod/httpd-app-6496d888c9-4nb6z   1/1     Running   0          77s    10.244.102.21   cka003   <none>           <none>
pod/httpd-app-6496d888c9-b7xht   1/1     Running   0          77s    10.244.112.19   cka002   <none>           <none>
```

Verify the access to Pod IPs.
```
curl 10.244.102.21
curl 10.244.112.19
```
And receive below successful information.
```
<html><body><h1>It works!</h1></body></html>
```

Verify the access via ClusterIP with Port.
```
curl 11.244.247.7:80
```
And receive below successful information.
```
<html><body><h1>It works!</h1></body></html>
```



#### Expose Service

Create and attach to a temporary Pod `nslookup` and to verify DNS resolution. The option `--rm` means delete the Pod after exit.
```
kubectl run -it nslookup --rm --image=busybox:1.28
```

After attach to the Pod, run command `nslookup httpd-app`. We receive the ClusterIP of Service `httpd-app` and full domain name.
```
/ # nslookup httpd-app
Server:    11.244.0.10
Address 1: 11.244.0.10 kube-dns.kube-system.svc.cluster.local

Name:      httpd-app
Address 1: 11.244.247.7 httpd-app.dev.svc.cluster.local
```

We can check the IP of temporary Pod `nslookup` in a new terminal by executing command `kubectl get pod -o wide`. 
The Pod `nslookup` has Pod IP `10.244.112.20`.
```
kubectl get pod nslookup
```
Result
```
NAME       READY   STATUS    RESTARTS   AGE     IP              NODE     NOMINATED NODE   READINESS GATES
nslookup   1/1     Running   0          2m44s   10.244.112.20   cka002   <none>           <none>
```




### NodePort

Create and apply yaml file `svc-nodeport.yaml` to create a Service `httpd-app`.
```
kubectl apply -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  name: httpd-app
spec:
  type: NodePort
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30080
  selector:
     app: httpd
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: httpd-app
spec:
  selector:
    matchLabels:
      app: httpd
  replicas: 2
  template:
    metadata:
      labels:
        app: httpd
    spec:
      containers:
      - name: httpd
        image: httpd
        ports:
        - containerPort: 80
EOF
```

We will receive below output. The command `kubectl apply -f <yaml_file>` will update configuration to existing resources.
Here the Service `httpd-app` is changed from `ClusterIP` to `NodePort` type. No change to the Deployment `httpd-app`.
```
service/httpd-app configured
deployment.apps/httpd-app unchanged
```

Check the Service `httpd-app` via `kubectl get svc`. 
IP is the same.
Type is changed to NodePort.
Port numbers is changed from `80/TCP` to `80:30080/TCP`.
```
NAME        TYPE       CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
httpd-app   NodePort   11.244.247.7   <none>        80:30080/TCP   18m
```

Test the connection to the Service `httpd-app` via command `curl <your_node_ip>:30080` to each node.
```
curl 172.16.18.170:30080
curl 172.16.18.169:30080
curl 172.16.18.168:30080
```
We will receive below successful information.
```
<html><body><h1>It works!</h1></body></html>
```





### Special Service

#### Headless Service

Create Headless Service `web` and StatefulSet `web`.
```
kubectl apply -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  name: web
  labels:
    app: web
spec:
  ports:
  - port: 80
    name: web
  clusterIP: None
  selector:
    app: web
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  serviceName: "web"
  replicas: 2
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: web
        image: nginx
        ports:
        - containerPort: 80
          name: web
EOF
```

Check Pos by command `kubectl get pod -owide -l app=web`.
```
NAME    READY   STATUS    RESTARTS   AGE   IP              NODE     NOMINATED NODE   READINESS GATES
web-0   1/1     Running   0          9s    10.244.102.22   cka003   <none>           <none>
web-1   1/1     Running   0          6s    10.244.112.21   cka002   <none>           <none>
```

Get details of the Service by command `kubectl describe svc -l app=web`.
```
Name:              web
Namespace:         dev
Labels:            app=web
Annotations:       <none>
Selector:          app=web
Type:              ClusterIP
IP Family Policy:  SingleStack
IP Families:       IPv4
IP:                None
IPs:               None
Port:              web  80/TCP
TargetPort:        80/TCP
Endpoints:         10.244.102.22:80,10.244.112.21:80
Session Affinity:  None
Events:            <none>
```

Attach to the temporary Pod `nslookup` and use `nslookup` to verify DNS resolution.
```
kubectl run -it nslookup --rm --image=busybox:1.28
```

With `nslookup` command for Headless Service `web`, we received two Pod IPs, not ClusterIP due to Headless Service. 
```
/ # nslookup web
Server:    11.244.0.10
Address 1: 11.244.0.10 kube-dns.kube-system.svc.cluster.local

Name:      web
Address 1: 10.244.112.21 web-1.web.dev.svc.cluster.local
Address 2: 10.244.102.22 web-0.web.dev.svc.cluster.local
```

We can also use `nslookup` for `web-0.web` and `web-1.web`. Every Pod of Headless Service has own Service Name for DNS lookup.
```
/ # nslookup web-0.web
Server:    11.244.0.10
Address 1: 11.244.0.10 kube-dns.kube-system.svc.cluster.local

Name:      web-0.web
Address 1: 10.244.102.22 web-0.web.dev.svc.cluster.local

/ # nslookup web-1.web
Server:    11.244.0.10
Address 1: 11.244.0.10 kube-dns.kube-system.svc.cluster.local

Name:      web-1.web
Address 1: 10.244.112.21 web-1.web.dev.svc.cluster.local
```

Clean up.
```
kubectl delete sts web
kubectl delete service httpd-app web
kubectl delete deployment httpd-app 
```





## 10.Ingress

Summary:

* Deploy Ingress Controller.
* Create two deployment `nginx-app-1` and `nginx-app-2`.
    * Host directory `/root/html-1` and `/root/html-2` will be created and mounted to two Deployments on running host.
* Create Service.
    * Create Service `nginx-app-1` and `nginx-app-2` and map to related Deployment `nginx-app-1` and `nginx-app-2`.
* Create Ingress.
    * Create Ingress resource `nginx-app` and map to two Services `nginx-app-1` and `nginx-app-1`.
* Test Accessibility.
    * Send HTTP request to two hosts defined in Ingress


### Deploy Ingress Controller

Get Ingress Controller yaml file. Choose one of below two files to deploy Ingress Controller.
```
wget https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.2.1/deploy/static/provider/cloud/deploy.yaml
wget https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.2.1/deploy/static/provider/cloud/1.23/deploy.yaml
```

Replace two images's sources to Aliyun.
```
image: k8s.gcr.io/ingress-nginx/controller:v1.2.1@sha256:5516d103a9c2ecc4f026efbd4b40662ce22dc1f824fb129ed121460aaa5c47f8
image: k8s.gcr.io/ingress-nginx/kube-webhook-certgen:v1.1.1@sha256:64d8c73dca984af206adf9d6d7e46aa550362b1d7a01f3a0a91b20cc67868660
```
From grc.io to Aliyun.
```
k8s.gcr.io/ingress-nginx/kube-webhook-certgen` to `registry.aliyuncs.com/google_containers/kube-webhook-certgen
k8s.gcr.io/ingress-nginx/controller` to `registry.aliyuncs.com/google_containers/nginx-ingress-controller
```
Commands:
```
sed -i 's/k8s.gcr.io\/ingress-nginx\/kube-webhook-certgen/registry.aliyuncs.com\/google\_containers\/kube-webhook-certgen/g' deploy.yaml
sed -i 's/k8s.gcr.io\/ingress-nginx\/controller/registry.aliyuncs.com\/google\_containers\/nginx-ingress-controller/g' deploy.yaml
```




Apply the yaml file `deploy.yaml` to create Ingress Nginx.

A new namespace `ingress-nginx` was created and Ingress Nginx resources are running under the new namespace.
```
kubectl apply -f deploy.yaml
```

Check the status of Pod.
```
kubectl get pod -n ingress-nginx
```
The result is below.
```
NAME                                        READY   STATUS      RESTARTS   AGE
ingress-nginx-admission-create-lgtdj        0/1     Completed   0          49s
ingress-nginx-admission-patch-nk9fv         0/1     Completed   0          49s
ingress-nginx-controller-556fbd6d6f-6jl4x   1/1     Running     0          49s
```




### Create Deployments

Create two deployment `nginx-app-1` and `nginx-app-2`.
```
kubectl apply -f - << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-app-1
spec:
  selector:
    matchLabels:
      app: nginx-app-1
  replicas: 1 
  template:
    metadata:
      labels:
        app: nginx-app-1
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
        volumeMounts:
          - name: html
            mountPath: /usr/share/nginx/html
      volumes:
       - name: html
         hostPath:
           path: /root/html-1
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-app-2
spec:
  selector:
    matchLabels:
      app: nginx-app-2
  replicas: 1 
  template:
    metadata:
      labels:
        app: nginx-app-2
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
        volumeMounts:
          - name: html
            mountPath: /usr/share/nginx/html
      volumes:
       - name: html
         hostPath:
           path: /root/html-2
EOF
```

Get status of Pods by executing `kubectl get pod -o wide`. Two Pods are running on node `cka002` with two different Pod IPs.
```
NAME                           READY   STATUS    RESTARTS   AGE     IP              NODE     NOMINATED NODE   READINESS GATES
nginx-app-1-695b7b647d-fp249   1/1     Running   0          68s     10.244.112.24   cka002   <none>           <none>
nginx-app-2-7f6bf6f4d4-5jkp6   1/1     Running   0          68s     10.244.112.25   cka002   <none>           <none>
```

Access to two Pod via curl. We get `403 Forbidden` error.
```
curl 10.244.112.24
curl 10.244.112.25
```

Log onto node `cka002`. 

* Directory `/root/html-1/` and `/root/html-2/` are in place on node `cka002`.
* Create `index.html` file in path `/root/html-1/` and `/root/html-2/`, and add below content to each file.

         echo 'This is test 1 !!' > /root/html-1/index.html
         echo 'This is test 2 !!' > /root/html-2/index.html


Check Pods status again by executing `kubectl get pod -o wide`.
```
NAME                           READY   STATUS    RESTARTS   AGE     IP              NODE     NOMINATED NODE   READINESS GATES
nginx-app-1-695b7b647d-fp249   1/1     Running   0          62m     10.244.112.24   cka002   <none>           <none>
nginx-app-2-7f6bf6f4d4-5jkp6   1/1     Running   0          62m     10.244.112.25   cka002   <none>           <none>
```

Now access to two Pod via curl is reachable. 
```
curl 10.244.112.24
curl 10.244.112.25
```
We get correct information now.
```
This is test 1 !!
This is test 2 !!
```



### Create Service

Create Service `nginx-app-1` and `nginx-app-2` and map to related deployment `nginx-app-1` and `nginx-app-2`.
```
kubectl apply -f - << EOF
apiVersion: v1
kind: Service
metadata:
 name: nginx-app-1
spec:
 ports:
 - protocol: TCP
   port: 80
   targetPort: 80
 selector:
   app: nginx-app-1
---
kind: Service
apiVersion: v1
metadata:
 name: nginx-app-2
spec:
 ports:
 - protocol: TCP
   port: 80
   targetPort: 80
 selector:
   app: nginx-app-2
EOF
```

Check the status by executing `kubectl get svc -o wide`.
```
NAME          TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE   SELECTOR
nginx-app-1   ClusterIP   11.244.51.241    <none>        80/TCP    12s   app=nginx-app-1
nginx-app-2   ClusterIP   11.244.123.249   <none>        80/TCP    12s   app=nginx-app-2
```

Access to two Service via curl. 
```
curl 11.244.51.241
curl 11.244.123.249
```
We get correct information.
```
This is test 1 !!
This is test 2 !!
```





### Create Ingress

Create Ingress resource `nginx-app` and map to two Services `nginx-app-1` and `nginx-app-1` we created.
Change the namespace to `dev`. 
```
kubectl apply -f - << EOF
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: nginx-app
  namespace: dev
spec:
  ingressClassName: "nginx"
  rules:
  - host: app1.com
    http:
      paths:
      - pathType: Prefix
        path: "/"
        backend:
          service:
            name: nginx-app-1
            port: 
              number: 80
  - host: app2.com
    http:
      paths:
      - pathType: Prefix
        path: "/"
        backend:
          service:
            name: nginx-app-2
            port:
              number: 80
EOF
```

Get Ingress status by executing command `kubectl get ingress`.
```  
NAME        CLASS   HOSTS               ADDRESS   PORTS   AGE
nginx-app   nginx   app1.com,app2.com             80      64s
```



### Test Accessiblity

By executing `kubectl get pod -n ingress-nginx -o wide`, we know Ingress Controllers are running on node `cka003`.
```
NAME                                        READY   STATUS      RESTARTS   AGE    IP              NODE     NOMINATED NODE   READINESS GATES
ingress-nginx-admission-create-lgtdj        0/1     Completed   0          117m   10.244.112.22   cka002   <none>           <none>
ingress-nginx-admission-patch-nk9fv         0/1     Completed   0          117m   10.244.112.23   cka002   <none>           <none>
ingress-nginx-controller-556fbd6d6f-6jl4x   1/1     Running     0          117m   10.244.102.23   cka003   <none>           <none>
```

cka001  172.16.18.170
cka002  172.16.18.169
cka003  172.16.18.168


Update `/etc/hosts file` in current node. 
Add mapping between node `cka003` IP and two host names `app1.com` and `app1.com` which present Services `nginx-app-1` and `nginx-app-2`. 
Ingress Controllers are running on node `cka003`
```
cat >> /etc/hosts << EOF
172.16.18.168   app1.com
172.16.18.168   app2.com
EOF
```

By executing `kubectl -n ingress-nginx get svc` to get NodePort of Ingress Controller. 
```
NAME                                 TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
ingress-nginx-controller             LoadBalancer   11.244.89.106    <pending>     80:31396/TCP,443:31464/TCP   123m
ingress-nginx-controller-admission   ClusterIP      11.244.104.136   <none>        443/TCP                      123m
```

Two files `index.html` are in two Pods, the web services are exposed to outside via node IP. 
The `ingress-nginx-controller` plays a central entry point for outside access, and provide two ports for different backend services from Pods.

Send HTTP request to two hosts defined in Ingress.
```
curl http://app1.com:31396
curl http://app2.com:31396
curl app1.com:31396
curl app2.com:31396
```
Get below successful information.
```
This is test 1 !!
This is test 2 !!
```








## 11.Storage

Summary: 

* Creat Pod with `emptyDir` type Volume. Container in the Pod will mount default directory `/var/lib/kubelet/pods/` on running node.

* Create Deployment `Deployment` with `hostPath` type volume. Container in the Deployment will mount directory defined in `hostPath:` on running node.

* PV and PVC.
    * Set up NFS Server and share folder `/nfsdata/`.
    * Create PV `mysql-pv` to link to the share folder `/nfsdata/` and set StorageClassName `nfs`.
    * Create PVC `mysql-pvc` mapped with StorageClassName `nfs`.
    * Create Deployment `mysql` to consume PVC `mysql-pvc`.

* StorageClass
    * Create ServiceAccount `nfs-client-provisioner`.
    * Create ClusterRole `nfs-client-provisioner-runner` and Role `leader-locking-nfs-client-provisioner` and bind them to the ServiceAccount so the ServiceAccount has authorization to operate the Deployment created in next step.
    * Create Deployment `nfs-client-provisioner` to to add connection information for your NFS server, e.g, `PROVISIONER_NAME` is `k8s-sigs.io/nfs-subdir-external-provisioner`
    * Create StorageClass `nfs-client` link to `provisioner: k8s-sigs.io/nfs-subdir-external-provisioner`. Releated PV is created automatically.
    * Create PVC `nfs-pvc-from-sc` mapped to PV and StorageClass `nfs-client`.

* Configuration
    * Create a ConfigMap for content of a file, and mount this ConfigMap to a specific file in a Pod.
    * Create a ConfigMap for username and password, and consume them within a Pod.
    * Use ConfigMap as environment variables in Pod. 



Tips:

* Delete PVC first, then delete PV.
* If facing `Terminating` status when delete a PVC, use `kubectl edit pvc <your_pvc_name>` and remove `finalize: <your_value>`.


### emptyDir

Create a Pod `hello-producer` with `emptyDir` type Volume.
```
cat > pod-emptydir.yaml <<EOF
apiVersion: v1
kind: Pod
metadata:
 name: hello-producer
spec:
 containers:
 - image: busybox
   name: producer
   volumeMounts:
   - mountPath: /producer_dir
     name: shared-volume
   args:
   - /bin/sh
   - -c
   - echo "hello world" > /producer_dir/hello; sleep 30000
 volumes:
 - name: shared-volume
   emptyDir: {}
EOF


kubectl apply -f pod-emptydir.yaml
```

The Pod `hello-producer` is running on node `cka003`. 
```
kubectl get pod hello-producer -owide
```
The Pod is running on node `cka003`.
```
NAME             READY   STATUS    RESTARTS   AGE   IP              NODE     NOMINATED NODE   READINESS GATES
hello-producer   1/1     Running   0          6s    10.244.102.24   cka003   <none>           <none>
```

Log onto `cka003` because the Pod `hello-producer` is running on the node.

Set up the environment `CONTAINER_RUNTIME_ENDPOINT` for command `crictl`. Suggest to do the same for all nodes.
```
export CONTAINER_RUNTIME_ENDPOINT=unix:///run/containerd/containerd.sock
```

Run command `crictl ps` to get the container ID of Pod `hello-producer`.
```
crictl ps |grep hello-producer
```

The ID of container `producer` is `05f5e1bb6a1bb`.
```
CONTAINER           IMAGE               CREATED             STATE               NAME                ATTEMPT             POD ID              POD
50058afb3cba5       62aedd01bd852       About an hour ago   Running             producer            0                   e6953bd4833a7       hello-producer
```

Run command `crictl inspect` to get the path of mounted `shared-volume`, which is `emptyDir`.
```
crictl inspect 50058afb3cba5 | grep source | grep empty
```
The result is below.
```
"source": "/var/lib/kubelet/pods/d7424f86-534a-48f9-9001-9d2a6e822b12/volumes/kubernetes.io~empty-dir/shared-volume",
```

Change the path to the path of mounted `shared-volume` we get above. We will see the content `hello world` of file `hello`. 
```
cd /var/lib/kubelet/pods/d7424f86-534a-48f9-9001-9d2a6e822b12/volumes/kubernetes.io~empty-dir/shared-volume
cat hello
```

The path `/producer_dir` inside the Pod is mounted to the local host path `/var/lib/kubelet/pods/d7424f86-534a-48f9-9001-9d2a6e822b12/volumes/kubernetes.io~empty-dir/shared-volume`.

The file `/producer_dir/hello` we created inside the Pod is actually in the host local path.

Let's delete the container `producer`, the container `producer` will be started again with new container ID and the file `hello` is still there.
```
crictl ps
crictl stop <your_container_id>
crictl rm <your_container_id>
```

Let's delete the Pod `hello-producer`, the container `producer` is deleted, file `hello` is deleted.
```
kubectl delete pod hello-producer 
```









### hostPath

Apply below yaml file to create a MySQL Pod and mount a `hostPath`.
It'll mount host directory `/tmp/mysql` to Pod directory `/var/lib/mysql`.
Check locally if directory `/tmp/mysql` is in place. If not, create it using `mkdir /tmp/mysql`.
```
cat > mysql-hostpath.yaml <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
 name: mysql
spec:
 selector:
   matchLabels:
     app: mysql
 template:
   metadata:
     labels:
       app: mysql
   spec:
     containers:
     - image: mysql:8.0
       name: mysql
       env:
       - name: MYSQL_ROOT_PASSWORD
         value: password
       ports:
       - containerPort: 3306
         name: mysql
       volumeMounts:
       - name: mysql-vol
         mountPath: /var/lib/mysql
     volumes:
     - hostPath:
         path: /tmp/mysql
       name: mysql-vol
EOF

kubectl apply -f mysql-hostpath.yaml
```


Verify MySQL Availability

Check status of MySQL Pod. Need document the Pod name and node it's running on.
```
kubectl get pod -l app=mysql -o wide
```
Result
```
NAME                     READY   STATUS              RESTARTS   AGE   IP       NODE     NOMINATED NODE   READINESS GATES
mysql-749c8ddd67-h2rgs   0/1     ContainerCreating   0          28s   <none>   cka003   <none>           <none>
```

Attach into the MySQL Pod on the running node.
```
kubectl exec -it <your_pod_name> -- bash
```

Within the Pod, go to directory `/var/lib/mysql`, all files in the directory are same with all files in directory `/tmp/mysql` on node `cka003`.

Connect to the database in the Pod.
```
mysql -h 127.0.0.1 -uroot -ppassword
```

Operate the database.
```
mysql> show databases;
mysql> connect mysql;
mysql> show tables;
mysql> exit
```



### PV and PVC

Here we will use NFS as backend storage to demo how to deploy PV and PVC.

#### Set up NFS Share

1. Install nfs-kernel-server

Log onto `cka002`.

Choose one Worker `cka002` to build NFS server. 
```
sudo apt-get install -y nfs-kernel-server
```

2. Configure Share Folder

Create share folder.  
```
mkdir /nfsdata
```

Append one line in file `/etc/exports`.
```
cat >> /etc/exports << EOF
/nfsdata *(rw,sync,no_root_squash)
EOF
```

There are many different NFS sharing options, including these:

* `*`: accessable to all IPs, or specific IPs.
* `rw`: Share as read-write. Keep in mind that normal Linux permissions still apply. (Note that this is a default option.)
* `ro`: Share as read-only.
* `sync`: File data changes are made to disk immediately, which has an impact on performance, but is less likely to result in data loss. On som* `distributions this is the default.
* `async`: The opposite of sync; file data changes are made initially to memory. This speeds up performance but is more likely to result in data loss. O* `some distributions this is the default.
* `root_squash`: Map the root user and group account from the NFS client to the anonymous accounts, typically either the nobody account or the nfsnobod* `account. See the next section, “User ID Mapping,” for more details. (Note that this is a default option.)
* `no_root_squash`: Map the root user and group account from the NFS client to the local root and group accounts.


We will use password-free remote mount based on `nfs` and `rpcbind` services between Linux servers, not based on `smb` service. 
The two servers must first grant credit, install and set up nfs and rpcbind services on the server side, set the common directory, start the service, and mount it on the client

Start `rpcbind` service.
```
sudo systemctl enable rpcbind
sudo systemctl restart rpcbind
```

Start `nfs` service.
```
sudo systemctl enable nfs-server
sudo systemctl start nfs-server
```

Once `/etc/exports` is changed, we need run below command to make change effected.
```
exportfs -ra
```
Result
```
exportfs: /etc/exports [1]: Neither 'subtree_check' or 'no_subtree_check' specified for export "*:/nfsdata".
  Assuming default behaviour ('no_subtree_check').
  NOTE: this default has changed since nfs-utils version 1.0.x
```

Check whether sharefolder is configured. 
```
showmount -e
```
And see below output.
```
Export list for cka002:
/nfsdata *
```



3. Install NFS Client

Install NFS client on all nodes.
```
sudo apt-get install -y nfs-common
```



4. Verify NFS Server

Log onto any nodes to verify NFS service and sharefolder list.

Log onto `cka001` and check sharefolder status on `cka002`.
```
showmount -e cka002
```
Below result will be shown if no issues.
```
Export list for cka002:
/nfsdata *
```



5. Mount NFS

Execute below command to mount remote NFS folder on any other non-NFS-server node, e.g., `cka001` or `cka003`.
```
mkdir /remote-nfs-dir
mount -t nfs cka002:/nfsdata /remote-nfs-dir/
```

Use command `df -h` to verify mount point. Below is the sample output.
```
Filesystem       Size  Used Avail Use% Mounted on
cka002:/nfsdata   40G  5.8G   32G  16% /remote-nfs-dir
```



#### Create PV

Create a PV `mysql-pv`. 
Replace the NFS Server IP with actual IP (here is `172.16.18.169`) that NFS server `cka002` is running on.
```
kubectl apply -f - <<EOF
apiVersion: v1
kind: PersistentVolume
metadata:
 name: mysql-pv
spec:
 accessModes:
     - ReadWriteOnce
 capacity:
   storage: 1Gi
 persistentVolumeReclaimPolicy: Retain
 storageClassName: nfs
 nfs:
   path: /nfsdata/
   server: 172.16.18.169
EOF
```

Check the PV.
```
kubectl get pv
```
The result:
```
NAME       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM   STORAGECLASS   REASON   AGE
mysql-pv   1Gi        RWO            Retain           Available           nfs                     19s
```


#### Create PVC

Create a PVC `mysql-pvc` and specify storage size, access mode, and storage class. 
The PVC `mysql-pvc` will be binded with PV automatically via storage class name. 
```
kubectl apply -f - <<EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  storageClassName: nfs
EOF
```



#### Consume PVC

Update the Deployment `mysql` to consume the PVC created.
```
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
 name: mysql
spec:
 selector:
   matchLabels:
     app: mysql
 template:
   metadata:
     labels:
       app: mysql
   spec:
     containers:
     - image: mysql:8.0
       name: mysql
       env:
       - name: MYSQL_ROOT_PASSWORD
         value: password
       ports:
       - containerPort: 3306
         name: mysql
       volumeMounts:
       - name: mysql-persistent-storage
         mountPath: /var/lib/mysql
         subPath: mysqldata
     volumes:
     - name: mysql-persistent-storage
       persistentVolumeClaim:
        claimName: mysql-pvc
EOF
```

Now we can see MySQL files were moved to directory `/nfsdata` on `cka002`




### StorageClass

#### Configure RBAC Authorization

RBAC authorization uses the rbac.authorization.k8s.io API group to drive authorization decisions, allowing you to dynamically configure policies through the Kubernetes API.

* ServiceAccount: `nfs-client-provisioner`
* namespace: `dev`

* ClusterRole: `nfs-client-provisioner-runner`. Grant authorization on node, pv, pvc, sc, event.
* ClusterRoleBinding: `run-nfs-client-provisioner`, bind above ClusterRole to above ServiceAccount.

* Role: `leader-locking-nfs-client-provisioner`. Grant authorization on endpoint.
* RoleBinding: `leader-locking-nfs-client-provisioner`, bind above Role to above ServiceAccount.


Create RBAC Authorization.
```
cat > nfs-provisioner-rbac.yaml <<EOF
apiVersion: v1
kind: ServiceAccount
metadata:
  name: nfs-client-provisioner
  # replace with namespace where provisioner is deployed
  namespace: dev
---
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: nfs-client-provisioner-runner
rules:
  - apiGroups: [""]
    resources: ["nodes"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["persistentvolumes"]
    verbs: ["get", "list", "watch", "create", "delete"]
  - apiGroups: [""]
    resources: ["persistentvolumeclaims"]
    verbs: ["get", "list", "watch", "update"]
  - apiGroups: ["storage.k8s.io"]
    resources: ["storageclasses"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["events"]
    verbs: ["create", "update", "patch"]
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: run-nfs-client-provisioner
subjects:
  - kind: ServiceAccount
    name: nfs-client-provisioner
    # replace with namespace where provisioner is deployed
    namespace: dev
roleRef:
  kind: ClusterRole
  name: nfs-client-provisioner-runner
  apiGroup: rbac.authorization.k8s.io
---
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: leader-locking-nfs-client-provisioner
  # replace with namespace where provisioner is deployed
  namespace: dev
rules:
  - apiGroups: [""]
    resources: ["endpoints"]
    verbs: ["get", "list", "watch", "create", "update", "patch"]
---
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: leader-locking-nfs-client-provisioner
  # replace with namespace where provisioner is deployed
  namespace: dev
subjects:
  - kind: ServiceAccount
    name: nfs-client-provisioner
    # replace with namespace where provisioner is deployed
    namespace: dev
roleRef:
  kind: Role
  name: leader-locking-nfs-client-provisioner
  apiGroup: rbac.authorization.k8s.io
EOF


kubectl apply -f nfs-provisioner-rbac.yaml
```


#### Create Provisioner's Deloyment

Create Deloyment `nfs-client-provisioner` by consuming volume `nfs-client-root` mapped to `/nfsdata` on `172.16.18.169`(`cka002`). 
Replace NFS server IP with actual IP (here is `172.16.18.169`)
```
cat > nfs-provisioner-deployment.yaml <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nfs-client-provisioner
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nfs-client-provisioner
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app: nfs-client-provisioner
    spec:
      serviceAccountName: nfs-client-provisioner
      containers:
        - name: nfs-client-provisioner
          image: liyinlin/nfs-subdir-external-provisioner:v4.0.2
          volumeMounts:
            - name: nfs-client-root
              mountPath: /persistentvolumes
          env:
            - name: PROVISIONER_NAME
              value: k8s-sigs.io/nfs-subdir-external-provisioner
            - name: NFS_SERVER
              value: 172.16.18.169
            - name: NFS_PATH
              value: /nfsdata
      volumes:
        - name: nfs-client-root
          nfs:
            server: 172.16.18.169
            path: /nfsdata
EOF

kubectl apply -f nfs-provisioner-deployment.yaml
```


#### Create NFS StorageClass

Create StorageClass `nfs-client`. Define the NFS subdir external provisioner's Kubernetes Storage Class.
```
vi nfs-storageclass.yaml
```
And add below info to create NFS StorageClass.
```
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: nfs-client
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: k8s-sigs.io/nfs-subdir-external-provisioner
parameters:
  pathPattern: "${.PVC.namespace}/${.PVC.annotations.nfs.io/storage-path}"
  onDelete: delete
```

Apply the yaml file.
```
kubectl apply -f nfs-storageclass.yaml
```


#### Create PVC

Create PVC `nfs-pvc-from-sc`.
```
kubectl apply -f - <<EOF
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: nfs-pvc-from-sc
spec:
  storageClassName: nfs-client
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 1Gi
EOF
```

Check the PVC status we ceated.
```
kubectl get pvc nfs-pvc-from-sc
```
The status is `Pending`.
```
NAME              STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
nfs-pvc-from-sc   Pending                                      nfs-client     112s
```

Check pending reason
```
kubectl describe pvc nfs-pvc-from-sc
```
It's pending on waiting for a volume to be created.
```
Events:
  Type    Reason                Age               From                         Message
  ----    ------                ----              ----                         -------
  Normal  ExternalProvisioning  9s (x6 over 84s)  persistentvolume-controller  waiting for a volume to be created, either by external provisioner "k8s-sigs.io/nfs-subdir-external-provisioner" or manually created by system administrator
```




#### Consume PVC

Create Deployment `mysql-with-sc-pvc` to consume the PVC `nfs-pvc-from-sc`.
```
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql-with-sc-pvc
spec:
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - image: mysql:8.0
        name: mysql
        env:
        - name: MYSQL_ROOT_PASSWORD
          value: password
        ports:
        - containerPort: 3306
          name: mysql
        volumeMounts:
        - name: mysql-pv
          mountPath: /var/lib/mysql
      volumes:
      - name: mysql-pv
        persistentVolumeClaim:
          claimName: nfs-pvc-from-sc
EOF
```


Check the Deployment status.
```
kubectl get deployment mysql-with-sc-pvc -o wide
```
Result
```
NAME                READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES      SELECTOR
mysql-with-sc-pvc   1/1     1            1           16s   mysql        mysql:8.0   app=mysql
```

With the comsumption from Deployment `mysql-with-sc-pvc`, the status of PVC `nfs-pvc-from-sc` is now status `Bound` from `Pending`.
```
kubectl get pvc nfs-pvc-from-sc
```
Result
```
NAME              STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
nfs-pvc-from-sc   Bound    pvc-edf70dff-7407-4b38-aac9-9c2dd6a84316   1Gi        RWX            nfs-client     52m
```

Check related Pods status. Be noted that the Pod `mysql-with-sc-pvc-7c97d875f8-dwfkc` is running on `cka003`.
```
kubectl get pod -o wide -l app=mysql
```
Result
```
NAME                                 READY   STATUS    RESTARTS   AGE     IP              NODE     NOMINATED NODE   READINESS GATES
mysql-774db46945-h82kk               1/1     Running   0          69m     10.244.112.26   cka002   <none>           <none>
mysql-with-sc-pvc-7c97d875f8-wkvr9   1/1     Running   0          3m37s   10.244.102.27   cka003   <none>           <none>
```

Let's check directory `/nfsdata/` on NFS server `cka002`. 
```
ll /nfsdata/
```
Two folders were created. Same content of `/remote-nfs-dir/` on other nodes.
```
drwxrwxrwx  6 systemd-coredump root 4096 Jul 23 23:35 dev/
drwxr-xr-x  6 systemd-coredump root 4096 Jul 23 22:29 mysqldata/
```

Namespace name is used as folder name under directory `/nfsdata/` and it is mounted to Pod.
By default, namespace name will be used at mount point. 
If we want to use customized folder for that purpose, we need claim an annotation `nfs.io/storage-path`, e.g., below example.

Create PVC test-claim on Namespace `kube-system` and consume volume `nfs-client`.
```
kubectl apply -f - <<EOF
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: test-claim
  namespace: kube-system
  annotations:
    nfs.io/storage-path: "test-path"
spec:
  storageClassName: nfs-client
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 1Gi
EOF
```

In above case, the PVC was created in `kube-system` Namespace, hence we can see directory `test-path` is under directory`kube-system` on node `cka002`. 

Overall directory structure of folder `/nfsdata/` looks like below.
```
tree -L 1 /nfsdata/ 
```
Result
```
/nfsdata/
├── dev
├── kube-system
└── mysqldata
```

Please be noted that above rule is following `nfs-subdir-external-provisioner` implementation. It's may be different with other `provisioner`.

Detail about `nfs-subdir-external-provisioner` project is [here](https://github.com/kubernetes-sigs/nfs-subdir-external-provisioner)



### Configuration

#### ConfigMap

Create ConfigMap `cm-nginx` to define content of `nginx.conf`.
```
vi configmap.yaml
```
Paste below content.
```
apiVersion: v1
kind: ConfigMap
metadata:
  labels:
    cattle.io/creator: norman
  name: cm-nginx
  namespace: dev
data:
  nginx.conf: |-
    user  nginx;
    worker_processes  2;

    error_log  /var/log/nginx/error.log warn;
    pid        /var/run/nginx.pid;


    events {
        worker_connections  1024;
    }


    http {
        include       /etc/nginx/mime.types;
        default_type  application/octet-stream;

        log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                          '$status $body_bytes_sent "$http_referer" '
                          '"$http_user_agent" "$http_x_forwarded_for"';

        access_log  /var/log/nginx/access.log  main;

        sendfile        on;
        #tcp_nopush     on;

        keepalive_timeout  65;

        #gzip  on;

        include /etc/nginx/conf.d/*.conf;
    }
```

Apply the ConfigMap.
```
kubectl apply -f configmap.yaml
```

Create Pod `nginx-with-cm`.
```
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: nginx-with-cm
spec:
 containers:
 - name: nginx
   image: nginx
   volumeMounts:
   - name: foo
     mountPath: "/etc/nginx/nginx.conf"
     subPath:  nginx.conf
 volumes:
 - name: foo
   configMap:
     name: cm-nginx
EOF
```

Be noted:

* By default to mount ConfigMap, Kubernetes will overwrite all content of the mount point. We can use `volumeMounts.subPath` to specify that only overwrite the file `nginx.conf` defined in `mountPath`.
* Is we use `volumeMounts.subPath` to mount a Container Volume, Kubernetes won't do hot update to reflect real-time update.


Verify if the `nginx.conf` mounted from outside is in the Container by comparing with above file.
```
kubectl exec -it nginx-with-cm -- sh 
cat /etc/nginx/nginx.conf
```




#### Secret

Encode password with base64  
```
echo -n admin | base64  
YWRtaW4=

echo -n 123456 | base64
MTIzNDU2
```

Create Secret `mysecret`.
```
kubectl apply -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
data:
  username: YWRtaW4=
  password: MTIzNDU2
EOF
```

Using Volume to mount (injection) Secret to a Pod.
```
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: busybox-with-secret
spec:
 containers:
 - name: mypod
   image: busybox
   args:
    - /bin/sh
    - -c
    - sleep 1000000;
   volumeMounts:
   - name: foo
     mountPath: "/tmp/secret"
 volumes:
 - name: foo
   secret:
    secretName: mysecret
EOF
```

Let's attach to the Pod `busybox-with-secret` to verify if two data elements of `mysecret` are successfully mounted to the path `/tmp/secret` within the Pod.
```
kubectl exec -it busybox-with-secret -- sh
```
By executing below command, we can see two data elements are in the directory `/tmp/secret` as file type. 
```
/ # ls -l /tmp/secret/
lrwxrwxrwx    1 root     root            15 Jul 23 16:30 password -> ..data/password
lrwxrwxrwx    1 root     root            15 Jul 23 16:30 username -> ..data/username
```
And we can get the content of each element, which are predefined before.
```
/ # cat /tmp/secret/username
admin

/ # cat /tmp/secret/password
123456
```



#### Additional Cases

##### Various way to create ConfigMap

ConfigMap can be created by file, directory, or value. 

Let's create a ConfigMap `colors` includes:

* Four files with four color names.
* One file with favorite color name.

```
mkdir configmap
cd configmap
mkdir primary

echo c > primary/cyan
echo m > primary/magenta
echo y > primary/yellow
echo k > primary/black
echo "known as key" >> primary/black
echo blue > favorite
```
Final structure looks like below via command `tree configmap`.
```
configmap
├── favorite
└── primary
    ├── black
    ├── cyan
    ├── magenta
    └── yellow
```

Create ConfigMap referring above files we created. Make sure we are now in the path `~/configmap`.
```
kubectl create configmap colors \
--from-literal=text=black  \
--from-file=./favorite  \
--from-file=./primary/
```

Check content of the ConfigMap `colors`.
```
kubectl get configmap colors -o yaml
```
```
apiVersion: v1
data:
  black: |
    k
    known as key
  cyan: |
    c
  favorite: |
    blue
  magenta: |
    m
  text: black
  yellow: |
    y
kind: ConfigMap
metadata:
  creationTimestamp: "2022-07-12T16:38:27Z"
  name: colors
  namespace: dev
  resourceVersion: "2377258"
  uid: d5ab133f-5e4d-41d4-bc9e-2bbb22a872a1
```




##### Set environment variable via ConfigMap

Here we will create a Pod `pod-configmap-env` and set the environment variable `ilike` and assign value of `favorite` from ConfigMap `colors`.
```
kubectl apply -f - << EOF
apiVersion: v1
kind: Pod
metadata:
  name: pod-configmap-env
spec:
  containers:
  - name: nginx
    image: nginx
    env:
    - name: ilike
      valueFrom:
        configMapKeyRef:
          name: colors
          key: favorite
EOF
```

Attach to the Pod `pod-configmap-env`.
```
kubectl exec -it pod-configmap-env -- bash
```

Verify the value of env variable `ilike` is `blue`, which is the value of `favorite` of ConfigMap `colors`.
```
root@pod-configmap-env:/# echo $ilike
blue
```

We can also use all key-value of ConfigMap to set up environment variables of Pod.
```
kubectl apply -f - << EOF
apiVersion: v1
kind: Pod
metadata:
 name: pod-configmap-env-2
spec:
 containers:
 - name: nginx
   image: nginx
   envFrom:
    - configMapRef:
        name: colors
EOF
```

Attach to the Pod `pod-configmap-env-2`.
```
kubectl exec -it pod-configmap-env-2 -- bash
```

Verify the value of env variables based on key-values we defined in ConfigMap `colors`.
```
root@pod-configmap-env-2:/# echo $black
k known as key
root@pod-configmap-env-2:/# echo $cyan
c
root@pod-configmap-env-2:/# echo $favorite
blue
```






## 12.Scheduling

Summary:

* Configure nodeSelector for Pod.
* Configure nodeName for Node.
* Use `podAffinity` to group Pods.

* Taints & Tolerations
    * Set Taints
    * Set Tolerations
    * Remove Taints



### nodeSelector

Let's assume the scenario below.

* We have a group of high performance servers.
* Some applications require high performance computing.
* These applicaiton need to be scheduled and running on those high performance servers.

We can leverage Kubernetes attributes node `label` and `nodeSelector` to group resources as a whole for scheduling to meet above requirement.




1. Label Node

Let's label `cka002` with `Configuration=hight`.
```
kubectl label node cka002 configuration=hight
```

Verify. We wil see the label `configuration=hight` on `cka002`.
```
kubectl get node --show-labels
```


2. Configure nodeSelector for Pod

Create a Pod and use `nodeSelector` to schedule the Pod running on specified node.
```
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
 name: mysql-nodeselector
spec:
 selector:
   matchLabels:
     app: mysql
 template:
   metadata:
     labels:
       app: mysql
   spec:
     containers:
     - image: mysql:8.0
       name: mysql
       env:
       - name: MYSQL_ROOT_PASSWORD
         value: password
       ports:
       - containerPort: 3306
         name: mysql
     nodeSelector:
       configuration: hight
EOF
```

Let's check with node the Pod `mysql-nodeselector` is running.
```
kubectl get pod -l app=mysql -o wide |  grep mysql-nodeselector
```

With below result, Pod `mysql-nodeselector` is running on `cka002` node.
```
NAME                                  READY   STATUS    RESTARTS   AGE     IP             NODE     NOMINATED NODE   READINESS GATES
mysql-nodeselector-6b7d9c875d-vs8mk   1/1     Running   0          7s     10.244.112.29   cka002   <none>           <none>
```



### nodeName

Be noted, `nodeName` has hightest priority as it's not scheduled by `Scheduler`.

Create a Pod `nginx-nodename` with `nodeName=cka003`.
```
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: nginx-nodename
spec:
  containers:
  - name: nginx
    image: nginx
  nodeName: cka003
EOF
```

Verify if Pod `nginx-nodename` is running on `ckc003 node.
```
kubectl get pod -owide |grep nginx-nodename
```
Result
```
NAME                                      READY   STATUS    RESTARTS   AGE     IP             NODE     NOMINATED NODE   READINESS GATES
nginx-nodename                            1/1     Running   0          8s     10.244.102.29   cka003   <none>           <none>
```




### Affinity

In Kubernetes cluster, some Pods have frequent interaction with other Pods. With that situation, it's suggested to schedule these Pods running on same node. 
For example, Two Pods Nginx and Mysql, we need deploy them on one node if they frequently communicate.

We can use `podAffinity` to select Pods based on their relationship. 

There are two scheduling type of `podAffinity`.

* `requiredDuringSchedulingIgnoredDuringExecution`(硬亲和)
* `preferredDuringSchedulingIgnoredDuringExecution`(软亲和)

`topologyKey` could be set by below types:

* `kubernetes.io/hostname` ＃NodeName
* `failure-domain.beta.kubernetes.io/zone` ＃Zone 
* `failure-domain.beta.kubernetes.io/region` # Region 

We can set node Label to classify Name/Zone/Region of node, which can be used by `podAffinity`.

Create a Pod Nginx.
```
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    app: nginx
spec:
  containers:
  - name: nginx
    image: nginx
EOF
```

Create a Pod MySql.
```
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: mysql
  labels:
    app: mysql
spec:
  containers:
  - name: mysql
    image: mysql
    env:
     - name: "MYSQL_ROOT_PASSWORD"
       value: "123456"
  affinity:
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: app
            operator: In
            values:
            - nginx
        topologyKey: kubernetes.io/hostname
EOF
```

As we configured `podAffinity`, so Pod `mysql` will be scheduled to the same node with Pod `nginx` by Label `app:nginx`.

Via the command `kubectl get pod -o wide` we can get two Pods are running on node `cka002`.









### Taints & Tolerations

#### Concept

Node affinity is a property of Pods that attracts them to a set of nodes (either as a preference or a hard requirement). 
Taints are the opposite -- they allow a node to repel a set of pods.

Tolerations are applied to pods. 
Tolerations allow the scheduler to schedule pods with matching taints. 
Tolerations allow scheduling but don't guarantee scheduling: the scheduler also evaluates other parameters as part of its function.

Taints and tolerations work together to ensure that pods are not scheduled onto inappropriate nodes. 
One or more taints are applied to a node; this marks that the node should not accept any pods that do not tolerate the taints.

In the production environment, we generally configure Taints for Control Plane nodes (in fact, most K8s installation tools automatically add Taints to Control Plane nodes), because Control Plane only runs Kubernetes system components. 
If it is used to run application Pods, it is easy to consume resources. In the end, the Control Plane node will crash. 
If we need to add additional system components to the Control Plane node later, we can configure Tolerations for the corresponding system component Pod to tolerate taints.


#### Set Taints

Set `cka003` node to taint node. Set status to `NoSchedule`, which won't impact existing Pods running on `cka003`.
```
kubectl taint nodes cka003 key=value:NoSchedule
```

#### Set Tolerations

We can use Tolerations to let Pods schedule to a taint node. 
```
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
 name: mysql-tolerations
spec:
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - image: mysql:8.0
        name: mysql
        env:
        - name: MYSQL_ROOT_PASSWORD
          value: password
        ports:
        - containerPort: 3306
          name: mysql
      tolerations:
      - key: "key"
        operator: "Equal"
        value: "value"
        effect: "NoSchedule"
EOF
```

The Pod of Deployment `mysql-tolerations` is scheduled and running on node `cka003` with `tolerations` setting, which is a taint node.
```
kubectl get pod -o wide | grep mysql-tolerations
```





#### Remove Taints

```
kubectl taint nodes cka003 key-
```



## 13.ResourceQuota

Summary:

* Create ResourceQuota `object-quota-demo` for namespace `quota-object-example`.
* Test ResourceQuota `object-quota-demo` for NodePort
* Test ResourceQuota `object-quota-demo` for PVC


1. Create Namespace

Ceate a Namespace
```
kubectl create ns quota-object-example
```

2. Create ResourceQuota for Namespace

Create ResourceQuota `object-quota-demo` for namespace `quota-object-example`.
Within the namespace, we can only create 1 PVC, 1 LoadBalancer Service, can not create NodePort Service.
```
kubectl apply -f - <<EOF
apiVersion: v1
kind: ResourceQuota
metadata:
  name: object-quota-demo
  namespace: quota-object-example
spec:
  hard:
    persistentvolumeclaims: "1"
    services.loadbalancers: "2"
    services.nodeports: "0"
EOF
```


3. Check Quota status

```
kubectl get resourcequota object-quota-demo --namespace=quota-object-example --output=yaml
```
Key information is below. 
```
spec:
  hard:
    persistentvolumeclaims: "1"
    services.loadbalancers: "2"
    services.nodeports: "0"
status:
  hard:
    persistentvolumeclaims: "1"
    services.loadbalancers: "2"
    services.nodeports: "0"
  used:
    persistentvolumeclaims: "0"
    services.loadbalancers: "0"
    services.nodeports: "0"
```

4. Test Quota for NodePort

Create a Deployment `ns-quota-test` on namespace `quota-object-example`.
```
kubectl create deployment ns-quota-test --image nginx --namespace=quota-object-example
```

Expose the Deployment via NodePort    
```
kubectl expose deployment ns-quota-test --port=80 --type=NodePort --namespace=quota-object-example
```

We receive below error, which is expected because we set Quota `services.nodeports: 0`.
```
Error from server (Forbidden): services "ns-quota-test" is forbidden: exceeded quota: object-quota-demo, requested: services.nodeports=1, used: services.nodeports=0, limited: services.nodeports=0
```
  

5. Test Quota for PVC

Create a PVC `pvc-quota-demo` on namespace `quota-object-example`.
```
kubectl applly -f - << EOF
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: pvc-quota-demo
  namespace: quota-object-example
spec:
  storageClassName: nfs-client
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 3Gi
EOF
```

Check the Quota status.
```
kubectl get resourcequota object-quota-demo --namespace=quota-object-example --output=yaml
```
Here `persistentvolumeclaims` is used `1`, and the quota is also `1`. If we create PVC again, will receive 403 error.
```
spec:
  hard:
    persistentvolumeclaims: "1"
    services.loadbalancers: "2"
    services.nodeports: "0"
status:
  hard:
    persistentvolumeclaims: "1"
    services.loadbalancers: "2"
    services.nodeports: "0"
  used:
    persistentvolumeclaims: "1"
    services.loadbalancers: "0"
    services.nodeports: "0"
```




## 14.LimitRange

Summary:

* Create LimitRange `cpu-limit-range` to define range of CPU Request and CPU Limit for a Container. 
* Test LimitRange `cpu-limit-range` via Pod.
    * Scenario 1: Pod without specified limits
    * Scenario 2: Pod with CPU limit, without CPU Request
    * Scenario 3: Pod with CPU Request onlyl, without CPU Limits




A *LimitRange* provides constraints that can:

* Enforce minimum and maximum compute resources usage per Pod or Container in a namespace.
* Enforce minimum and maximum storage request per PersistentVolumeClaim in a namespace.
* Enforce a ratio between request and limit for a resource in a namespace.
* Set default request/limit for compute resources in a namespace and automatically inject them to Containers at runtime.


### Set LimitRange

Create a Namespace `default-cpu-example` for demo.
```
kubectl create namespace default-cpu-example
```

Create LimitRange `cpu-limit-range` to define range of CPU Request and CPU Limit for a Container.
After apply LimitRange resource, the CPU limitation will affect all new created Pods.
```
kubectl apply -f - << EOF
apiVersion: v1
kind: LimitRange
metadata:
  name: cpu-limit-range
  namespace: default-cpu-example
spec:
  limits:
  - default:
      cpu: 1
    defaultRequest:
      cpu: 0.5
    type: Container
EOF
```



### Test via Pod

#### Scenario 1: Pod without specified limits

Create a Pod without any specified limits.
```
kubectl apply -f - << EOF
apiVersion: v1
kind: Pod
metadata:
  name: default-cpu-demo
  namespace: default-cpu-example
spec:
  containers:
  - name: default-cpu-demo-ctr
    image: nginx
EOF
```

Verify details of the Pod we created. The Pod inherits the both CPU Limits and CPU Requests from namespace as its default.
```
kubectl get pod default-cpu-demo --output=yaml --namespace=default-cpu-example
```
```
spec:
  containers:
  - image: nginx
    imagePullPolicy: Always
    name: default-cpu-demo-ctr
    resources:
      limits:
        cpu: "1"
      requests:
        cpu: 500m
```



#### Scenario 2: Pod with CPU limit, without CPU Request

Create Pod with specified CPU limits only.  
```
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: default-cpu-demo-limit
  namespace: default-cpu-example
spec:
  containers:
  - name: default-cpu-demo-limit-ctr
    image: nginx
    resources:
      limits:
        cpu: "1"
EOF

kubectl apply -f default-cpu-demo-limit.yaml
```

Verify details of the Pod we created. The Pod inherits the CPU Request from namespace as its default and specifies own CPU Limits.
```
kubectl get pod default-cpu-demo-limit --output=yaml --namespace=default-cpu-example
```
```
spec:
  containers:
  - image: nginx
    imagePullPolicy: Always
    name: default-cpu-demo-limit-ctr
    resources:
      limits:
        cpu: "1"
      requests:
        cpu: "1"
```

#### Scenario 3: Pod with CPU Request onlyl, without CPU Limits

Create Pod with specified CPU Request only. 
```
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: default-cpu-demo-request
  namespace: default-cpu-example
spec:
  containers:
  - name: default-cpu-demo-request-ctr
    image: nginx
    resources:
      requests:
        cpu: "0.75"
EOF
```

Verify details of the Pod we created. The Pod inherits the CPU Limits from namespace as its default and specifies own CPU Requests.
```
kubectl get pod default-cpu-demo-request --output=yaml --namespace=default-cpu-example
```
```
spec:
  containers:
  - image: nginx
    imagePullPolicy: Always
    name: default-cpu-demo-request-ctr
    resources:
      limits:
        cpu: "1"
      requests:
        cpu: 750m
```






## 15.Troubleshooting

### Event

Usage:
```
kubectl describe <resource_type> <resource_name> --namespace=<namespace_name>
```

Get event information of a Pod

Create a Tomcat Pod.
```
kubectl run tomcat --image=tomcat
```

Check event of above deplyment.
```
kubectl describe pod/tomcat
```
Get below event information.
```
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  55s   default-scheduler  Successfully assigned dev/tomcat to cka002
  Normal  Pulling    54s   kubelet            Pulling image "tomcat"
  Normal  Pulled     21s   kubelet            Successfully pulled image "tomcat" in 33.134162692s
  Normal  Created    19s   kubelet            Created container tomcat
  Normal  Started    19s   kubelet            Started container tomcat
```

Get event information for a Namespace.
```
kubectl get events -n <your_namespace_name>
```
Get current default namespace event information.
```
LAST SEEN   TYPE      REASON           OBJECT                          MESSAGE
70s         Warning   FailedGetScale   horizontalpodautoscaler/nginx   deployments/scale.apps "podinfo" not found
2m16s       Normal    Scheduled        pod/tomcat                      Successfully assigned dev/tomcat to cka002
2m15s       Normal    Pulling          pod/tomcat                      Pulling image "tomcat"
102s        Normal    Pulled           pod/tomcat                      Successfully pulled image "tomcat" in 33.134162692s
100s        Normal    Created          pod/tomcat                      Created container tomcat
100s        Normal    Started          pod/tomcat                      Started container tomcat
```

Get event information for all Namespace.
```
kubectl get events -A
```




### Logs

Usage:
```
kubectl logs <pod_name> -n <namespace_name>
```

Options:

* `--tail <n>`: display only the most recent `<n>` lines of output
* `-f`: streaming the output

Get the most recent 100 lines of output.
```
kubectl logs -f tomcat --tail 100
```

If it's multipPod, use `-c` to specify Container.
```
kubectl logs -f tomcat --tail 100 -c tomcat
```




### Monitoring Indicators

Get node monitoring information
```
kubectl top node
```
Output:
```
NAME     CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
cka001   147m         7%     1940Mi          50%
cka002   62m          3%     2151Mi          56%
cka003   63m          3%     1825Mi          47%
```

Get Pod monitoring information
```
kubectl top pod
```
Output:
```
root@cka001:~# kubectl top pod
NAME                                      CPU(cores)   MEMORY(bytes)   
busybox-with-secret                       0m           0Mi
mysql                                     2m           366Mi
mysql-774db46945-sztrp                    2m           349Mi
mysql-nodeselector-6b7d9c875d-227t6       2m           365Mi
mysql-tolerations-5c5986944b-cg9bs        2m           366Mi
mysql-with-sc-pvc-7c97d875f8-dwfkc        2m           349Mi
nfs-client-provisioner-699db7fd58-bccqs   2m           7Mi
nginx                                     0m           3Mi
nginx-app-1-695b7b647d-l76bh              0m           3Mi
nginx-app-2-7f6bf6f4d4-lvbz8              0m           3Mi
nginx-nodename                            0m           3Mi
nginx-with-cm                             0m           3Mi
pod-configmap-env                         0m           3Mi
pod-configmap-env-2                       0m           3Mi
tomcat                                    1m           58Mi
```

Sort output by CPU or Memory using option `--sort-by`, the field can be either 'cpu' or 'memory'.
```
kubectl top pod --sort-by=cpu
kubectl top pod --sort-by=memory
```
Output:
```
NAME                                      CPU(cores)   MEMORY(bytes)   
nfs-client-provisioner-699db7fd58-bccqs   2m           7Mi
mysql                                     2m           366Mi
mysql-774db46945-sztrp                    2m           349Mi
mysql-nodeselector-6b7d9c875d-227t6       2m           365Mi
mysql-tolerations-5c5986944b-cg9bs        2m           366Mi
mysql-with-sc-pvc-7c97d875f8-dwfkc        2m           349Mi
tomcat                                    1m           58Mi
nginx                                     0m           3Mi
nginx-app-1-695b7b647d-l76bh              0m           3Mi
nginx-app-2-7f6bf6f4d4-lvbz8              0m           3Mi
nginx-nodename                            0m           3Mi
nginx-with-cm                             0m           3Mi
pod-configmap-env                         0m           3Mi
pod-configmap-env-2                       0m           3Mi
busybox-with-secret                       0m           0Mi
```







### Node Eviction

Disable scheduling for a Node.
```
kubectl cordon <node_name>
```
Example:
```
kubectl cordon cka003
```
Node status:
```
NAME     STATUS                     ROLES                  AGE   VERSION
cka001   Ready                      control-plane,master   18d   v1.24.0
cka002   Ready                      <none>                 18d   v1.24.0
cka003   Ready,SchedulingDisabled   <none>                 18d   v1.24.0
```

Enable scheduling for a Node.
```
kubectl uncordon <node_name>
```
Example:
```
kubectl uncordon cka003
```
Node status:
```
NAME     STATUS   ROLES                  AGE   VERSION
cka001   Ready    control-plane,master   18d   v1.24.0
cka002   Ready    <none>                 18d   v1.24.0
cka003   Ready    <none>                 18d   v1.24.0
```

Evict Pods on a Node.
```
kubectl drain <node_name>
kubectl drain <node_name> --ignore-daemonsets
kubectl drain <node_name> --ignore-daemonsets --delete-emptydir-data
```



## 16.RBAC

Summary:

1. Create differnet profiles for one cluster.
2. Use `cfssl` generate certificates for each profile.
3. Create new kubeconfig file with all profiles and associated users.
4. Merge old and new kubeconfig files into new kubeconfig file. We can switch different context for further demo.


Role-based access control (RBAC) is a method of regulating access to computer or network resources based on the roles of individual users within the organization.

When using client certificate authentication, we can generate certificates manually through `easyrsa`, `openssl` or `cfssl`.

Best pracice: 

The purpose of kubeconfig is to grant different authorizations to different users for different clusters. 
Different contexts will link to different clusters.

It's not recommended to put multiple users' contexts for one cluster in one kubeconfig. 
It's recommended to use one kubeconfig file for one user.



### Install cfssl

Install `cfssl` tool
```
apt install golang-cfssl
```

### Set Multiple Contexts

#### Current Context

Execute command `kubectl config` to get current contenxt.
```
kubectl config get-contexts
```
We get below key information of the cluster.

* Cluster Name: kubernetes
* System account: kubenetes-admin
* Current context name: kubernetes-admin@kubernetes (format: `<system_account>@<cluster_name>`)
```
CURRENT   NAME                          CLUSTER      AUTHINFO           NAMESPACE
*         kubernetes-admin@kubernetes   kubernetes   kubernetes-admin   dev
```


#### Create CA Config File


Get overview of directory `/etc/kubernetes/pki`.
```
tree /etc/kubernetes/pki
```
Result
```
/etc/kubernetes/pki
├── apiserver.crt
├── apiserver-etcd-client.crt
├── apiserver-etcd-client.key
├── apiserver.key
├── apiserver-kubelet-client.crt
├── apiserver-kubelet-client.key
├── ca.crt
├── ca.key
├── etcd
│   ├── ca.crt
│   ├── ca.key
│   ├── healthcheck-client.crt
│   ├── healthcheck-client.key
│   ├── peer.crt
│   ├── peer.key
│   ├── server.crt
│   └── server.key
├── front-proxy-ca.crt
├── front-proxy-ca.key
├── front-proxy-client.crt
├── front-proxy-client.key
├── sa.key
└── sa.pub
```


Change to directory `/etc/kubernetes/pki`.
```
cd /etc/kubernetes/pki
```

Check if file `ca-config.json` is in place in current directory.
```
ll ca-config.json
```

If not, create it.

* We can add multiple profiles to specify different expiry date, scenario, parameters, etc.. 
* Profile will be used to sign certificate.
* `87600` hours are about 10 years.


Here we will create 1 additional profile `dev`.
```
cat > ca-config.json <<EOF
{
  "signing": {
    "default": {
      "expiry": "87600h"
    },
    "profiles": {
      "dev": {
        "usages": [
            "signing",
            "key encipherment",
            "server auth",
            "client auth"
        ],
        "expiry": "87600h"
      }
    }
  }
}
EOF
```



#### Create CSR file for signature

A CertificateSigningRequest (CSR) resource is used to request that a certificate be signed by a denoted signer, after which the request may be approved or denied before finally being signed.


It is important to set `CN` and `O` attribute of the CSR. 

* The `CN` is the *name of the user* to request CSR.
* The `O` is the *group* that this user will belong to. We can refer to RBAC for standard groups.

Stay in the directory `/etc/kubernetes/pki`.

Create csr file `cka-dev-csr.json`. 
`CN` is `cka-dev`.
`O` is `k8s`.
```
cat > cka-dev-csr.json <<EOF
{
  "CN": "cka-dev",
  "hosts": [],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "Shanghai",
      "L": "Shanghai",
      "O": "k8s",
      "OU": "System"
    }
  ]
}
EOF
```

Generate certifcate and key for the profile we defined above.
`cfssljson -bare cka-dev` will generate two files, `cka-dev.pem` as public key and `cka-dev-key.pem` as private key.
```
cfssl gencert -ca=ca.crt -ca-key=ca.key -config=ca-config.json -profile=dev cka-dev-csr.json | cfssljson -bare cka-dev
```

Get below files.
```
ll -tr | grep cka-dev
```
```
-rw-r--r-- 1 root root  222 Jul 24 08:49 cka-dev-csr.json
-rw-r--r-- 1 root root 1281 Jul 24 09:14 cka-dev.pem
-rw------- 1 root root 1675 Jul 24 09:14 cka-dev-key.pem
-rw-r--r-- 1 root root 1001 Jul 24 09:14 cka-dev.csr
```







#### Create file kubeconfig

Get the IP of Control Plane (e.g., `172.16.18.170` here) to composite evn variable `APISERVER` (`https://<control_plane_ip>:<port>`).
```
kubectl get node -owide
```
```
NAME     STATUS   ROLES                  AGE   VERSION   INTERNAL-IP     EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION      CONTAINER-RUNTIME
cka001   Ready    control-plane,master   14h   v1.24.0   172.16.18.170   <none>        Ubuntu 20.04.4 LTS   5.4.0-122-generic   containerd://1.5.9
cka002   Ready    <none>                 14h   v1.24.0   172.16.18.169   <none>        Ubuntu 20.04.4 LTS   5.4.0-122-generic   containerd://1.5.9
cka003   Ready    <none>                 14h   v1.24.0   172.16.18.168   <none>        Ubuntu 20.04.4 LTS   5.4.0-122-generic   containerd://1.5.9
```

Export env `APISERVER`.
```
echo "export APISERVER=\"https://172.16.18.170:6443\"" >> ~/.bashrc
source ~/.bashrc
```

Verify the setting.
```
echo $APISERVER
```
Output:
```
https://172.16.18.170:6443
```


1. Set up cluster

Stay in the directory `/etc/kubernetes/pki`.

Generate kubeconfig file.
```
kubectl config set-cluster kubernetes \
  --certificate-authority=/etc/kubernetes/pki/ca.crt \
  --embed-certs=true \
  --server=${APISERVER} \
  --kubeconfig=cka-dev.kubeconfig
```

Now we get the new config file `cka-dev.kubeconfig`
```
ll -tr | grep cka-dev
```
Output:
```
-rw-r--r-- 1 root root  222 Jul 24 08:49 cka-dev-csr.json
-rw-r--r-- 1 root root 1281 Jul 24 09:14 cka-dev.pem
-rw------- 1 root root 1675 Jul 24 09:14 cka-dev-key.pem
-rw-r--r-- 1 root root 1001 Jul 24 09:14 cka-dev.csr
-rw------- 1 root root 1671 Jul 24 09:16 cka-dev.kubeconfig
```

Get content of file `cka-dev.kubeconfig`.
```
cat cka-dev.kubeconfig
```
```
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: <your_key>
    server: https://172.16.18.170:6443
  name: kubernetes
contexts: null
current-context: ""
kind: Config
preferences: {}
users: null
```




2. Set up user

In file `cka-dev.kubeconfig`, user info is null. 

Set up user `cka-dev`.
```
kubectl config set-credentials cka-dev \
  --client-certificate=/etc/kubernetes/pki/cka-dev.pem \
  --client-key=/etc/kubernetes/pki/cka-dev-key.pem \
  --embed-certs=true \
  --kubeconfig=cka-dev.kubeconfig
```

Now file `cka-dev.kubeconfig` was updated and user information was added.
```
cat cka-dev.kubeconfig
```
```
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: <your_key>
    server: https://172.16.18.170:6443
  name: kubernetes
contexts: null
current-context: ""
kind: Config
preferences: {}
users:
- name: cka-dev
  user:
    client-certificate-data: <your_key>
    client-key-data: <your_key>
```

Now we have a complete kubeconfig file `cka-dev.kubeconfig`.
When we use it to get node information, receive error below because we did not set up current-context in kubeconfig file.
```
kubectl --kubeconfig=cka-dev.kubeconfig get nodes
```
```
The connection to the server localhost:8080 was refused - did you specify the right host or port?
```

Current contents is empty.
```
kubectl --kubeconfig=cka-dev.kubeconfig config get-contexts
```
```
CURRENT   NAME   CLUSTER   AUTHINFO   NAMESPACE
```



3. Set up Context

Set up context. 
```
kubectl config set-context dev --cluster=kubernetes --user=cka-dev  --kubeconfig=cka-dev.kubeconfig
```

Now we have context now but the `CURRENT` flag is empty.
```
kubectl --kubeconfig=cka-dev.kubeconfig config get-contexts
```
Output:
```
CURRENT   NAME   CLUSTER      AUTHINFO   NAMESPACE
          dev    kubernetes   cka-dev 
```

Set up default context. The context will link clusters and users for multiple clusters environment and we can switch to different cluster.
```
kubectl --kubeconfig=cka-dev.kubeconfig config use-context dev
```


4. Verify

Now `CURRENT` is marked with `*`, that is, current-context is set up.
```
kubectl --kubeconfig=cka-dev.kubeconfig config get-contexts
```
```
CURRENT   NAME   CLUSTER      AUTHINFO   NAMESPACE
*         dev    kubernetes   cka-dev      
```

Because user `cka-dev` does not have authorization in the cluster, we will receive `forbidden` error when we try to get information of Pods or Nodes.
```
kubectl --kubeconfig=/etc/kubernetes/pki/cka-dev.kubeconfig get pod 
kubectl --kubeconfig=/etc/kubernetes/pki/cka-dev.kubeconfig get node
```


#### Merge kubeconfig files

Make a copy of your existing config
```
cp ~/.kube/config ~/.kube/config.old 
```

Merge the two config files together into a new config file `/tmp/config`.
```
KUBECONFIG=~/.kube/config:/etc/kubernetes/pki/cka-dev.kubeconfig  kubectl config view --flatten > /tmp/config
```

Replace the old config with the new merged config
```
mv /tmp/config ~/.kube/config
```

Now the new `~/.kube/config` looks like below.
```
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: <your_key>
    server: https://172.16.18.170:6443
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    user: cka-dev
  name: dev
- context:
    cluster: kubernetes
    user: kubernetes-admin
  name: kubernetes-admin@kubernetes
current-context: kubernetes-admin@kubernetes
kind: Config
preferences: {}
users:
- name: cka-dev
  user:
    client-certificate-data: <your_key>
    client-key-data: <your_key>
- name: kubernetes-admin
  user:
    client-certificate-data: <your_key>
    client-key-data: <your_key>
```



Verify contexts after kubeconfig merged.
```
kubectl config get-contexts
```
Current context is the system default `kubernetes-admin@kubernetes`.
```
CURRENT   NAME                          CLUSTER      AUTHINFO           NAMESPACE
          dev                           kubernetes   cka-dev            
*         kubernetes-admin@kubernetes   kubernetes   kubernetes-admin   dev
```



### Namespaces & Contexts

Get list of Namespace with Label information.
```
kubectl get ns --show-labels
```

Create Namespace `cka`.
```
kubectl create namespace cka
```

Use below command to set a context with new update, e.g, update default namespace, etc..
```
kubectl config set-context <context name> --cluster=<cluster name> --namespace=<namespace name> --user=<user name> 
```

Let's set default namespace to each context.
```
kubectl config set-context kubernetes-admin@kubernetes --cluster=kubernetes --namespace=default --user=kubernetes-admin
kubectl config set-context dev --cluster=kubernetes --namespace=cka --user=cka-dev
```

Let's check current context information.
```
kubectl config get-contexts
```
Output:
```
CURRENT   NAME                          CLUSTER      AUTHINFO           NAMESPACE
          dev                           kubernetes   cka-dev            cka
*         kubernetes-admin@kubernetes   kubernetes   kubernetes-admin   dev
```

To switch to a new context, use below command.
```
kubectl config use-contexts <context name>
```

For example.
```
kubectl config use-context dev
```
Verify if it's changed as expected.
```
kubectl config get-contexts
```
```
CURRENT   NAME                          CLUSTER      AUTHINFO           NAMESPACE
*         dev            kubernetes   cka-dev            cka
          kubernetes-admin@kubernetes   kubernetes   kubernetes-admin   dev
```

Be noted, four users beginning with `cka-dev` created don't have any authorizations, e.g., access namespaces, get pods, etc..
Referring RBAC to grant their authorizations. 






### Role & RoleBinding


Switch to context `kubernetes-admin@kubernetes`.
```
kubectl config use-context kubernetes-admin@kubernetes
```


Use `kubectl create role` command  with option `--dry-run=client` and `-o yaml` to generate yaml template for customizing. 
```
kubectl create role admin-dev --resource=pods --verb=get --verb=list --verb=watch --dry-run=client -o yaml
```

Create role `admin-dev` on namespace `cka`.
```
kubectl apply -f - << EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: cka
  name: admin-dev
rules:
- apiGroups:
  - ""
  resources:
  - pods
  verbs:
  - get
  - watch
  - list
EOF
```

Use `kubectl create rolebinding` command  with option `--dry-run=client` and `-o yaml` to generate yaml template for customizing.
```
kubectl create rolebinding admin --role=admin-dev --user=cka-dev --dry-run=client -o yaml
```

Create rolebinding `admin` on namespace `cka`.
```
kubectl apply -f - << EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: admin
  namespace: cka
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: admin-dev
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: User
  name: cka-dev
EOF
```

Verify authorzation of user `cka-dev` on Namespace `cka`.

Switch to context `dev`.
```
kubectl config use-context dev
```



Get Pods status in Namespace `cka`. Success!
```
kubectl get pod -n cka
```

Get Pods status in Namespace `kube-system`. Failed, because the authorzation is only for Namespace `cka`.
```
kubectl get pod -n kube-system
```

Get Nodes status. Failed, because the role we defined is only for Pod resource.
```
kubectl get node
```

Create a Pod in Namespace `dev`. Failed because we only have `get`,`watch`,`list` for Pod, no `create` authorization.
```
kubectl run nginx --image=nginx -n cka
```





### ClusterRole & ClusterRoleBinding

Switch to context `kubernetes-admin@kubernetes`.
```
kubectl config use-context kubernetes-admin@kubernetes
```

Create a ClusterRole `nodes-admin` with authorization `get`,`watch`,`list` for `nodes` resource.
```
kubectl apply -f - <<EOF
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: nodes-admin
rules:
- apiGroups:
  - ""
  resources: 
  - nodes
  verbs:
  - get
  - watch
  - list
EOF
```

Bind ClusterRole `nodes-admin` to user `cka-dev`.

```
kubectl apply -f - << EOF
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: admin
subjects:
- kind: User
  name: cka-dev
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: nodes-admin
  apiGroup: rbac.authorization.k8s.io
EOF
```

Verify Authorization

Switch to context `dev`.
```
kubectl config use-context dev
```

Get node information. Success!
```
kubectl get node
```

Switch to system context.
```
kubectl config use-context kubernetes-admin@kubernetes 
```



## 17.Network Policy

### Replace Flannel by Calico

If Calico was installed at the installation phase, ignore this section.

Delete Flannel
```
kubectl delete -f https://raw.githubusercontent.com/coreos/flannel/v0.18.1/Documentation/kube-flannel.yml
```
or
```
kubectl delete -f kube-flannel.yml
```
Output:
```
Warning: policy/v1beta1 PodSecurityPolicy is deprecated in v1.21+, unavailable in v1.25+
podsecuritypolicy.policy "psp.flannel.unprivileged" deleted
clusterrole.rbac.authorization.k8s.io "flannel" deleted
clusterrolebinding.rbac.authorization.k8s.io "flannel" deleted
serviceaccount "flannel" deleted
configmap "kube-flannel-cfg" deleted
daemonset.apps "kube-flannel-ds" deleted
```


Clean up iptables for all nodes.
```
rm -rf /var/run/flannel /opt/cni /etc/cni /var/lib/cni
iptables -F && iptables -t nat -F && iptables -t mangle -F && iptables -X
```

Log out and log on to host (e.g., cka001) again. Install Calico.
```
curl https://docs.projectcalico.org/manifests/calico.yaml -O

kubectl apply -f calico.yaml
```
Output:
```
configmap/calico-config created
customresourcedefinition.apiextensions.k8s.io/bgpconfigurations.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/bgppeers.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/blockaffinities.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/caliconodestatuses.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/clusterinformations.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/felixconfigurations.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/globalnetworkpolicies.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/globalnetworksets.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/hostendpoints.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/ipamblocks.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/ipamconfigs.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/ipamhandles.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/ippools.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/ipreservations.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/kubecontrollersconfigurations.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/networkpolicies.crd.projectcalico.org created
customresourcedefinition.apiextensions.k8s.io/networksets.crd.projectcalico.org created
clusterrole.rbac.authorization.k8s.io/calico-kube-controllers created
clusterrolebinding.rbac.authorization.k8s.io/calico-kube-controllers created
clusterrole.rbac.authorization.k8s.io/calico-node created
clusterrolebinding.rbac.authorization.k8s.io/calico-node created
daemonset.apps/calico-node created
serviceaccount/calico-node created
deployment.apps/calico-kube-controllers created
serviceaccount/calico-kube-controllers created
poddisruptionbudget.policy/calico-kube-controllers created
```

Verify status of Calico. Make sure all Pods are running
```
kubectl get pod -n kube-system | grep calico
```
Output:
```
NAME                                       READY   STATUS        RESTARTS   AGE
calico-kube-controllers-7bc6547ffb-tjfcg   1/1     Running       0          30m
calico-node-7x8jm                          1/1     Running       0          30m
calico-node-cwxj5                          1/1     Running       0          30m
calico-node-rq978                          1/1     Running       0          30m
```

If facing any error, check log in the Container.
```
# Get Container ID
crictl ps

# Get log info
crictl logs <your_container_id>
```


As we change CNI from Flannel to Calico, we need delete all Pods. All of Pods will be created automatically again. 
```
kubectl delete pod -A --all
```

Make sure all Pods are up and running successfully.
```
kubectl get pod -A
```







### Inbound Rules

1. Create workload for test.

Create three Deployments `pod-netpol-1`,`pod-netpol-2`,`pod-netpol-3` based on image `busybox`.
```
kubectl apply -f - << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: pod-netpol-1
  name: pod-netpol-1
spec:
  replicas: 1
  selector:
    matchLabels:
      app: pod-netpol-1
  template:
    metadata:
      labels:
        app: pod-netpol-1
    spec:
      containers:
      - image: busybox
        name: busybox
        command: ["sh", "-c", "sleep 1h"]
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: pod-netpol-2
  name: pod-netpol-2
spec:
  replicas: 1
  selector:
    matchLabels:
      app: pod-netpol-2
  template:
    metadata:
      labels:
        app: pod-netpol-2
    spec:
      containers:
      - image: busybox
        name: busybox
        command: ["sh", "-c", "sleep 1h"]
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: pod-netpol-3
  name: pod-netpol-3
spec:
  replicas: 1
  selector:
    matchLabels:
      app: pod-netpol-3
  template:
    metadata:
      labels:
        app: pod-netpol-3
    spec:
      containers:
      - image: busybox
        name: busybox
        command: ["sh", "-c", "sleep 1h"]       
EOF
```

Check Pods IP.
```
kubectl get pod -owide
```
Output:
```
NAME                                      READY   STATUS    RESTARTS   AGE   IP              NODE     NOMINATED NODE   READINESS GATES
pod-netpol-1-6494f6bf8b-n58r9             1/1     Running   0          29s   10.244.102.30   cka003   <none>           <none>
pod-netpol-2-77478d77ff-l6rzm             1/1     Running   0          29s   10.244.112.30   cka002   <none>           <none>
pod-netpol-3-68977dcb48-ql5s6             1/1     Running   0          29s   10.244.102.31   cka003   <none>           <none>
```

Attach to Pod `pod-netpol-1`
```
kubectl exec -it pod-netpol-1-6494f6bf8b-n58r9 -- sh
```

Execute command `ping` that `pod-netpol-2` and `pod-netpol-3` are both reachable. 
```
/ # ping 10.244.112.30 
3 packets transmitted, 3 packets received, 0% packet loss

/ # ping 10.244.102.31
3 packets transmitted, 3 packets received, 0% packet loss
```



2. Deny For All Ingress

Create deny policy for all ingress.
```
kubectl apply -f - << EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
spec:
  podSelector: {}
  policyTypes:
  - Ingress
EOF
```

Attach to Pod `pod-netpol-1` again
```
kubectl exec -it pod-netpol-1-6494f6bf8b-n58r9 -- sh
```

Execute command `ping` that `pod-netpol-2` and `pod-netpol-3` are both unreachable as expected.
```
/ # ping 10.244.112.30
3 packets transmitted, 0 packets received, 100% packet loss

/ # ping 10.244.102.31
3 packets transmitted, 0 packets received, 100% packet loss
```



3. Allow For Specific Ingress

Create NetworkPlicy to allow ingress from `pod-netpol-1` to `pod-netpol-2`.
```
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-pod-netpol-1-to-pod-netpol-2
spec:
  podSelector:
    matchLabels:
      app: pod-netpol-2
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: pod-netpol-1
EOF
```

4. Verify NetworkPolicy

Attach to Pod `pod-netpol-1` again
```
kubectl exec -it pod-netpol-1-6494f6bf8b-n58r9 -- sh
```

Execute command `ping` to check if `pod-netpol-2` and `pod-netpol-3` are reachable. 
As expected, `pod-netpol-2` is reachable and `pod-netpol-3` is still unreachable. 
```
/ # ping 10.244.112.30
3 packets transmitted, 3 packets received, 0% packet loss

/ # ping 10.244.102.8
3 packets transmitted, 0 packets received, 100% packet loss
```



### Inbound Across Namespace

1. Create workload and namespace for test

Create Namespace `ns-netpol`.
```
kubectl create ns ns-netpol
```

Create Deployment `pod-netpol`.
```
kubectl apply -f - << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: pod-netpol
  name: pod-netpol
  namespace: ns-netpol
spec:
  replicas: 1
  selector:
    matchLabels:
      app: pod-netpol
  template:
    metadata:
      labels:
        app: pod-netpol
    spec:
      containers:
      - image: busybox
        name: busybox
        command: ["sh", "-c", "sleep 1h"]
EOF
```

Check Pod status on new namespace.
```
kubectl get pod -n ns-netpol
```
Output:
```
NAME                          READY   STATUS    RESTARTS   AGE
pod-netpol-5b67b6b496-2cgnw   1/1     Running   0          9s
```

Attach into `pod-netpol` Pod.
```
kubectl exec -it pod-netpol-5b67b6b496-2cgnw -n ns-netpol -- sh
```

Try to ping pod-netpol-2 (`10.244.112.30`) in Namespace `dev`. It's unreachable. 
```
ping 10.244.112.30
3 packets transmitted, 0 packets received, 100% packet loss
```



2. Create Allow Ingress

Create NetworkPolicy to allow access to pod-netpol-2 in namespace `dev` from all Pods in namespace `pod-netpol`.
```
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-ns-netpol-to-pod-netpol-2
spec:
  podSelector:
    matchLabels:
      app: pod-netpol-2
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          allow: to-pod-netpol-2
EOF
```



3. Verify Policy

Attach into `pod-netpol` Pod.
```
kubectl exec -it pod-netpol-5b67b6b496-2cgnw -n ns-netpol -- sh
```

Try to ping pod-netpol-2 (`10.244.112.30`) in Namespace `dev`. It's still unreachable. 
```
ping 10.244.112.30
3 packets transmitted, 0 packets received, 100% packet loss
```

What we allowed ingress is from namespace with label `allow: to-pod-netpol-2`, but namespace `ns-netpol` does not have it and we need label it.
```
kubectl label ns ns-netpol allow=to-pod-netpol-2
```

Attach into `pod-netpol` Pod.
```
kubectl exec -it pod-netpol-5b67b6b496-2cgnw -n ns-netpol -- sh
```

Try to ping pod-netpol-2 (`10.244.112.30`) in Namespace `dev`. It's now reachable. 
```
ping 10.244.112.30
3 packets transmitted, 3 packets received, 0% packet loss
```

Be noted that we can use namespace default label as well.








## 18.Cluster Management

### `etcd` Backup and Restore

1. Install `etcdctl`

Download `etcd` package from Github.
```
wget https://github.com/etcd-io/etcd/releases/download/v3.5.3/etcd-v3.5.3-linux-amd64.tar.gz
```

Unzip and grant execute permission.
```
tar -zxvf etcd-v3.5.3-linux-amd64.tar.gz
cp etcd-v3.5.3-linux-amd64/etcdctl /usr/local/bin/
sudo chmod u+x /usr/local/bin/etcdctl
```

Verify
```
etcdctl --help
```

2. Create Deployment Before Backup

Create Deployment before backup.
```
kubectl create deployment app-before-backup --image=nginx
```


3. Backup `etcd`

Command usage: 

* `<CONTROL_PLANE_IP_ADDRESS>` is the actual IP address of Control Plane.
* `--endpoints`: specify where to save backup of etcd, 2379 is etcd port.
* `--cert`: sepcify etcd certificate, which was generated by `kubeadm` and saved in `/etc/kubernetes/pki/etcd/`.
* `--key`: specify etcd certificate key, which was generated by `kubeadm` and saved in `/etc/kubernetes/pki/etcd/`.
* `--cacert`: specify etcd certificate CA, which was generated by `kubeadm` and saved in `/etc/kubernetes/pki/etcd/`.

```
etcdctl \
  --endpoints=https://<CONTROL_PLANE_IP_ADDRESS>:2379 \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  snapshot save snapshot-$(date +"%Y%m%d%H%M%S").db
```

```
etcdctl \
  --endpoints=https://172.16.18.170:2379 \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  snapshot save snapshot-$(date +"%Y%m%d%H%M%S").db
```
Output:
```
{"level":"info","ts":"2022-07-24T18:51:21.328+0800","caller":"snapshot/v3_snapshot.go:65","msg":"created temporary db file","path":"snapshot-20220724185121.db.part"}
{"level":"info","ts":"2022-07-24T18:51:21.337+0800","logger":"client","caller":"v3/maintenance.go:211","msg":"opened snapshot stream; downloading"}
{"level":"info","ts":"2022-07-24T18:51:21.337+0800","caller":"snapshot/v3_snapshot.go:73","msg":"fetching snapshot","endpoint":"https://172.16.18.170:2379"}
{"level":"info","ts":"2022-07-24T18:51:21.415+0800","logger":"client","caller":"v3/maintenance.go:219","msg":"completed snapshot read; closing"}
{"level":"info","ts":"2022-07-24T18:51:21.477+0800","caller":"snapshot/v3_snapshot.go:88","msg":"fetched snapshot","endpoint":"https://172.16.18.170:2379","size":"3.6 MB","took":"now"}
{"level":"info","ts":"2022-07-24T18:51:21.477+0800","caller":"snapshot/v3_snapshot.go:97","msg":"saved","path":"snapshot-20220724185121.db"}
Snapshot saved at snapshot-20220724185121.db
```

We can get the backup file in current directory with `ls -al` command.
```
-rw-------  1 root root 3616800 Jul 24 18:51 snapshot-20220724185121.db
```



4. Create Deployment After Backup

Create Deployment after backup.
```
kubectl create deployment app-after-backup --image=nginx
```

Delete Deployment we created before backup.
```
kubectl delete deployment app-before-backup
```

Check Deployment status
```
kubectl get deploy
```
```
NAME                     READY   UP-TO-DATE   AVAILABLE   AGE
app-after-backup         1/1     1            1           108s
```




5. Stop Services

Delete `etcd` directory.
```
mv /var/lib/etcd/ /var/lib/etcd.bak
```

Stop `kubelet`
```
systemctl stop kubelet
```

Stop kube-apiserver
```
nerdctl -n k8s.io ps -a | grep apiserver
```
```
0c5e69118f1b    registry.aliyuncs.com/google_containers/kube-apiserver:v1.24.0             "kube-apiserver --ad…"    32 hours ago    Up                  k8s://kube-system/kube-apiserver-cka001/kube-apiserver
638bb602c310    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  32 hours ago    Up                  k8s://kube-system/kube-apiserver-cka001
```

Stop those `up` status containers.
```
nerdctl -n k8s.io stop <container_id>

nerdctl -n k8s.io stop 0c5e69118f1b
nerdctl -n k8s.io stop 638bb602c310
```
No `up` status `kube-apiserver` now.
```
nerdctl -n k8s.io ps -a | grep apiserver
```
```
0c5e69118f1b    registry.aliyuncs.com/google_containers/kube-apiserver:v1.24.0             "kube-apiserver --ad…"    32 hours ago    Created             k8s://kube-system/kube-apiserver-cka001/kube-apiserver
638bb602c310    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  32 hours ago    Created             k8s://kube-system/kube-apiserver-cka001
```



6. Stop etcd
```
nerdctl -n k8s.io ps -a | grep etcd
```
```
0965b195f41a    registry.aliyuncs.com/google_containers/etcd:3.5.1-0                       "etcd --advertise-cl…"    32 hours ago    Up                  k8s://kube-system/etcd-cka001/etcd
9e1bea9f25d1    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  32 hours ago    Up                  k8s://kube-system/etcd-cka001
```

Stop those `up` status containers.
```
nerdctl -n k8s.io stop <container_id>
```
```
nerdctl -n k8s.io stop 0965b195f41a
nerdctl -n k8s.io stop 9e1bea9f25d1
```
No `up` status `etcd` now.
```
nerdctl -n k8s.io ps -a | grep etcd
```
```
0965b195f41a    registry.aliyuncs.com/google_containers/etcd:3.5.1-0                       "etcd --advertise-cl…"    32 hours ago    Created             k8s://kube-system/etcd-cka001/etcd
9e1bea9f25d1    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  32 hours ago    Created             k8s://kube-system/etcd-cka001
```


7. Restore `etcd`

Execute the restore operation on Control Plane node with actual backup file, here it's file `snapshot-20220724185121.db`.
```
etcdctl snapshot restore snapshot-20220724185121.db \
    --endpoints=172.16.18.170:2379 \
    --cert=/etc/kubernetes/pki/etcd/server.crt \
    --key=/etc/kubernetes/pki/etcd/server.key \
    --cacert=/etc/kubernetes/pki/etcd/ca.crt\
    --data-dir=/var/lib/etcd
```
Output:
```
Deprecated: Use `etcdutl snapshot restore` instead.

2022-07-24T18:57:49+08:00       info    snapshot/v3_snapshot.go:248     restoring snapshot      {"path": "snapshot-20220724185121.db", "wal-dir": "/var/lib/etcd/member/wal", "data-dir": "/var/lib/etcd", "snap-dir": "/var/lib/etcd/member/snap", "stack": "go.etcd.io/etcd/etcdutl/v3/snapshot.(*v3Manager).Restore\n\t/go/src/go.etcd.io/etcd/release/etcd/etcdutl/snapshot/v3_snapshot.go:254\ngo.etcd.io/etcd/etcdutl/v3/etcdutl.SnapshotRestoreCommandFunc\n\t/go/src/go.etcd.io/etcd/release/etcd/etcdutl/etcdutl/snapshot_command.go:147\ngo.etcd.io/etcd/etcdctl/v3/ctlv3/command.snapshotRestoreCommandFunc\n\t/go/src/go.etcd.io/etcd/release/etcd/etcdctl/ctlv3/command/snapshot_command.go:129\ngithub.com/spf13/cobra.(*Command).execute\n\t/go/pkg/mod/github.com/spf13/cobra@v1.1.3/command.go:856\ngithub.com/spf13/cobra.(*Command).ExecuteC\n\t/go/pkg/mod/github.com/spf13/cobra@v1.1.3/command.go:960\ngithub.com/spf13/cobra.(*Command).Execute\n\t/go/pkg/mod/github.com/spf13/cobra@v1.1.3/command.go:897\ngo.etcd.io/etcd/etcdctl/v3/ctlv3.Start\n\t/go/src/go.etcd.io/etcd/release/etcd/etcdctl/ctlv3/ctl.go:107\ngo.etcd.io/etcd/etcdctl/v3/ctlv3.MustStart\n\t/go/src/go.etcd.io/etcd/release/etcd/etcdctl/ctlv3/ctl.go:111\nmain.main\n\t/go/src/go.etcd.io/etcd/release/etcd/etcdctl/main.go:59\nruntime.main\n\t/go/gos/go1.16.15/src/runtime/proc.go:225"}
2022-07-24T18:57:49+08:00       info    membership/store.go:141 Trimming membership information from the backend...
2022-07-24T18:57:49+08:00       info    membership/cluster.go:421       added member    {"cluster-id": "cdf818194e3a8c32", "local-member-id": "0", "added-peer-id": "8e9e05c52164694d", "added-peer-peer-urls": ["http://localhost:2380"]}
2022-07-24T18:57:49+08:00       info    snapshot/v3_snapshot.go:269     restored snapshot       {"path": "snapshot-20220724185121.db", "wal-dir": "/var/lib/etcd/member/wal", "data-dir": "/var/lib/etcd", "snap-dir": "/var/lib/etcd/member/snap"}
```

Check if `etcd` folder is back from restore. 
```
tree /var/lib/etcd
```
```
/var/lib/etcd
└── member
    ├── snap
    │   ├── 0000000000000001-0000000000000001.snap
    │   └── db
    └── wal
        └── 0000000000000000-0000000000000000.wal
```



8. Start Services

Start `kubelet`. The `kube-apiserver` and `etcd` will be started automatically by `kubelet`.
```
systemctl start kubelet
```

Execute below comamnds to make sure services are all up.
```
systemctl status kubelet.service
nerdctl -n k8s.io ps -a | grep etcd
nerdctl -n k8s.io ps -a | grep apiserver
```

The current status of `etcd`.
```
0965b195f41a    registry.aliyuncs.com/google_containers/etcd:3.5.1-0                       "etcd --advertise-cl…"    32 hours ago     Created             k8s://kube-system/etcd-cka001/etcd
3b8f37c87782    registry.aliyuncs.com/google_containers/etcd:3.5.1-0                       "etcd --advertise-cl…"    6 seconds ago    Up                  k8s://kube-system/etcd-cka001/etcd
9e1bea9f25d1    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  32 hours ago     Created             k8s://kube-system/etcd-cka001
fbbbb628a945    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  6 seconds ago    Up                  k8s://kube-system/etcd-cka001
```

The current status of `apiserver`.
```
0c5e69118f1b    registry.aliyuncs.com/google_containers/kube-apiserver:v1.24.0             "kube-apiserver --ad…"    32 hours ago      Created             k8s://kube-system/kube-apiserver-cka001/kube-apiserver
281cf4c6670d    registry.aliyuncs.com/google_containers/kube-apiserver:v1.24.0             "kube-apiserver --ad…"    14 seconds ago    Up                  k8s://kube-system/kube-apiserver-cka001/kube-apiserver
5ed8295d92da    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  15 seconds ago    Up                  k8s://kube-system/kube-apiserver-cka001
638bb602c310    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  32 hours ago      Created             k8s://kube-system/kube-apiserver-cka001
```


9. Verify

Check cluster status, if the Pod `app-before-backup` is there.
```
kubectl get deploy
```
Result
```
NAME                     READY   UP-TO-DATE   AVAILABLE   AGE
app-before-backup        1/1     1            1           11m
```




### Upgrade

#### Upgrade `Control Plane`

1. Preparation

Evict Control Plane node.
```
kubectl drain <control_plane_node_name> --ignore-daemonsets 
```
```
kubectl drain cka001 --ignore-daemonsets 
```
```
node/cka001 cordoned
WARNING: ignoring DaemonSet-managed Pods: kube-system/calico-node-dsx76, kube-system/kube-proxy-cm4hc
evicting pod kube-system/calico-kube-controllers-5c64b68895-jr4nl
evicting pod kube-system/coredns-6d8c4cb4d-g4jxc
evicting pod kube-system/coredns-6d8c4cb4d-sqcvj
pod/calico-kube-controllers-5c64b68895-jr4nl evicted
pod/coredns-6d8c4cb4d-g4jxc evicted
pod/coredns-6d8c4cb4d-sqcvj evicted
node/cka001 drained
```

The Control Plane node is now in `SchedulingDisabled` status.
```
kubectl get node -owide
```
Result
```
NAME     STATUS                     ROLES                  AGE   VERSION   INTERNAL-IP     EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION      CONTAINER-RUNTIME
cka001   Ready,SchedulingDisabled   control-plane,master   32h   v1.24.0   172.16.18.170   <none>        Ubuntu 20.04.4 LTS   5.4.0-122-generic   containerd://1.5.9
cka002   Ready                      <none>                 32h   v1.24.0   172.16.18.169   <none>        Ubuntu 20.04.4 LTS   5.4.0-122-generic   containerd://1.5.9
cka003   Ready                      <none>                 32h   v1.24.0   172.16.18.168   <none>        Ubuntu 20.04.4 LTS   5.4.0-122-generic   containerd://1.5.9
```

Check current available version of `kubeadm`.
```
apt policy kubeadm
```
```
kubeadm:
  Installed: 1.24.0-00
  Candidate: 1.24.3-00
  Version table:
     1.24.3-00 500
        500 https://mirrors.aliyun.com/kubernetes/apt kubernetes-xenial/main amd64 Packages
     1.24.2-00 500
        500 https://mirrors.aliyun.com/kubernetes/apt kubernetes-xenial/main amd64 Packages
     1.24.1-00 500
        500 https://mirrors.aliyun.com/kubernetes/apt kubernetes-xenial/main amd64 Packages
     1.24.0-00 500
        500 https://mirrors.aliyun.com/kubernetes/apt kubernetes-xenial/main amd64 Packages
     1.24.2-00 500
        500 https://mirrors.aliyun.com/kubernetes/apt kubernetes-xenial/main amd64 Packages
 *** 1.24.0-00 500
        500 https://mirrors.aliyun.com/kubernetes/apt kubernetes-xenial/main amd64 Packages
        100 /var/lib/dpkg/status
     1.23.7-00 500
        500 https://mirrors.aliyun.com/kubernetes/apt kubernetes-xenial/main amd64 Packages
......
```

Upgrade `kubeadm` to `Candidate: 1.24.2-00` version.
```
sudo apt-get -y install kubeadm=1.24.2-00 --allow-downgrades
```

Check upgrade plan.
```
kubeadm upgrade plan
```

Get below guideline of upgrade.
```
[upgrade/config] Making sure the configuration is correct:
[upgrade/config] Reading configuration from the cluster...
[upgrade/config] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -o yaml'
[preflight] Running pre-flight checks.
[upgrade] Running cluster health checks
[upgrade] Fetching available versions to upgrade to
[upgrade/versions] Cluster version: v1.24.0
[upgrade/versions] kubeadm version: v1.24.2
I0724 19:05:00.111855 1142460 version.go:255] remote version is much newer: v1.24.3; falling back to: stable-1.23
[upgrade/versions] Target version: v1.24.2
[upgrade/versions] Latest version in the v1.23 series: v1.24.2

Components that must be upgraded manually after you have upgraded the control plane with 'kubeadm upgrade apply':
COMPONENT   CURRENT       TARGET
kubelet     3 x v1.24.0   v1.24.2

Upgrade to the latest version in the v1.23 series:

COMPONENT                 CURRENT   TARGET
kube-apiserver            v1.24.0   v1.24.2
kube-controller-manager   v1.24.0   v1.24.2
kube-scheduler            v1.24.0   v1.24.2
kube-proxy                v1.24.0   v1.24.2
CoreDNS                   v1.8.6    v1.8.6
etcd                      3.5.1-0   3.5.1-0

You can now apply the upgrade by executing the following command:

        kubeadm upgrade apply v1.24.2

_____________________________________________________________________


The table below shows the current state of component configs as understood by this version of kubeadm.
Configs that have a "yes" mark in the "MANUAL UPGRADE REQUIRED" column require manual config upgrade or
resetting to kubeadm defaults before a successful upgrade can be performed. The version to manually
upgrade to is denoted in the "PREFERRED VERSION" column.

API GROUP                 CURRENT VERSION   PREFERRED VERSION   MANUAL UPGRADE REQUIRED
kubeproxy.config.k8s.io   v1alpha1          v1alpha1            no
kubelet.config.k8s.io     v1beta1           v1beta1             no
_____________________________________________________________________
```





2. Upgrade

Refer to upgrade plan, let's upgrade to v1.24.2 version.
```
kubeadm upgrade apply v1.24.2
```

With option `--etcd-upgrade=false`, the `etcd` can be excluded from the upgrade.
```
kubeadm upgrade apply v1.24.2 --etcd-upgrade=false
```

It's successful when receiving below message.
```
[upgrade/successful] SUCCESS! Your cluster was upgraded to "v1.24.2". Enjoy!

[upgrade/kubelet] Now that your control plane is upgraded, please proceed with upgrading your kubelets if you haven't already done so.
```

Upgrade `kubelet` and `kubectl`.
```
sudo apt-get -y install kubelet=1.24.2-00 kubectl=1.24.2-00 --allow-downgrades
sudo systemctl daemon-reload
sudo systemctl restart kubelet
```

Get current node status.
```
kubectl get node
```
```
NAME     STATUS                     ROLES                  AGE   VERSION
cka001   Ready,SchedulingDisabled   control-plane,master   32h   v1.24.2
cka002   Ready                      <none>                 32h   v1.24.0
cka003   Ready                      <none>                 32h   v1.24.0
```

After verify that each node is in Ready status, enable node scheduling.
```
kubectl uncordon <control_plane_node_name>
```
```
kubectl uncordon cka001
```
Output:
```
node/cka001 uncordoned
```

Check node status again. Make sure all nodes are in Ready status.
```
kubectl get node
```
Output:
```
NAME     STATUS   ROLES                  AGE   VERSION
cka001   Ready    control-plane,master   32h   v1.24.2
cka002   Ready    <none>                 32h   v1.24.0
cka003   Ready    <none>                 32h   v1.24.0
```





#### Upgrade Worker

1. Preparation

Log on to `cka001`

Evict Worker nodes, explicitly specify to remove local storage if needed.
```
kubectl drain <worker_node_name> --ignore-daemonsets --force
kubectl drain <worker_node_name> --ignore-daemonsets --delete-emptydir-data --force
```
If have error on dependency of `emptydir`, use the 2nd command.
```
kubectl drain cka002 --ignore-daemonsets --force
kubectl drain cka002 --ignore-daemonsets --delete-emptydir-data --force
```
```
node/cka002 cordoned
WARNING: deleting Pods not managed by ReplicationController, ReplicaSet, Job, DaemonSet or StatefulSet: dev/ubuntu; ignoring DaemonSet-managed Pods: kube-system/calico-node-p5rf2, kube-system/kube-proxy-zvs68
evicting pod ns-netpol/pod-netpol-5b67b6b496-2cgnw
evicting pod dev/ubuntu
evicting pod dev/app-before-backup-66dc9d5cb-6xc8c
evicting pod dev/nfs-client-provisioner-86d7fb78b6-2f5dx
evicting pod dev/pod-netpol-2-77478d77ff-l6rzm
evicting pod ingress-nginx/ingress-nginx-admission-patch-nk9fv
evicting pod ingress-nginx/ingress-nginx-admission-create-lgtdj
evicting pod kube-system/coredns-6d8c4cb4d-l4kx4
pod/ingress-nginx-admission-create-lgtdj evicted
pod/ingress-nginx-admission-patch-nk9fv evicted
pod/nfs-client-provisioner-86d7fb78b6-2f5dx evicted
pod/app-before-backup-66dc9d5cb-6xc8c evicted
pod/coredns-6d8c4cb4d-l4kx4 evicted
pod/pod-netpol-5b67b6b496-2cgnw evicted
pod/pod-netpol-2-77478d77ff-l6rzm evicted
pod/ubuntu evicted
node/cka002 drained
```

2. Upgrade

Log on to `cka002`.

Download `kubeadm` with version `v1.24.2`.
```
sudo apt-get -y install kubeadm=1.24.2-00 --allow-downgrades
```

Upgrade `kubeadm`.
```
sudo kubeadm upgrade node
```

Upgrade `kubelet`.
```
sudo apt-get -y install kubelet=1.24.2-00 --allow-downgrades
sudo systemctl daemon-reload
sudo systemctl restart kubelet
```

Make sure all nodes are in Ready status, then, enable node scheduling.
```
kubectl uncordon <worker_node_name>
```
```
kubectl uncordon cka002
```

3. Verify

Check node status. 
```
kubectl get node
```
Result
```
NAME     STATUS   ROLES                  AGE   VERSION
cka001   Ready    control-plane,master   32h   v1.24.2
cka002   Ready    <none>                 32h   v1.24.2
cka003   Ready    <none>                 32h   v1.24.0
```




Repeat the same on node `cka003`.

Log onto `cka001`. If have error on dependency of `emptydir`, use the 2nd command.
```
kubectl drain cka003 --ignore-daemonsets --ignore-daemonsets --force
kubectl drain cka003 --ignore-daemonsets --ignore-daemonsets --delete-emptydir-data --force
```

Log onto `cka003` and perform below commands.
```
sudo apt-get -y install kubeadm=1.24.2-00 --allow-downgrades

sudo kubeadm upgrade node

sudo apt-get -y install kubelet=1.24.2-00 --allow-downgrades
sudo systemctl daemon-reload
sudo systemctl restart kubelet

kubectl get node
kubectl uncordon cka003
```

Get final status of all nodes.
```
kubectl get node
```
```
NAME     STATUS   ROLES                  AGE   VERSION
cka001   Ready    control-plane,master   32h   v1.24.2
cka002   Ready    <none>                 32h   v1.24.2
cka003   Ready    <none>                 32h   v1.24.2
```







## 19.Helm Chart

### Install Helm

Install Helm on `cka001`. 
```
# https://github.com/helm/helm/releases
wget https://get.helm.sh/helm-v3.8.2-linux-amd64.tar.gz
tar -zxvf helm-v3.8.2-linux-amd64.tar.gz
cp linux-amd64/helm /usr/bin/
rm -rf linux-amd64 helm-v3.8.2-linux-amd64.tar.gz
```

Or manually download the file via link `https://get.helm.sh/helm-v3.8.2-linux-amd64.tar.gz`, and remote copy to `cka001`.
```
scp -i cka-key-pair.pem ./Package/helm-v3.8.2-linux-amd64.tar.gz root@cka001:/root/
```
```
ssh -i cka-key-pair.pem root@cka001
tar -zxvf helm-v3.8.2-linux-amd64.tar.gz
cp linux-amd64/helm /usr/bin/
rm -rf linux-amd64 helm-v3.8.2-linux-amd64.tar.gz
```



### Usage of Helm

Check `helm` version
```
helm version
```
```
version.BuildInfo{Version:"v3.8.2", GitCommit:"6e3701edea09e5d55a8ca2aae03a68917630e91b", GitTreeState:"clean", GoVersion:"go1.17.5"}
```

Get help of `helm`.
```
helm help
```

Configure auto-completion for `helm`.
```
echo "source <(helm completion bash)" >> ~/.bashrc
source <(helm completion bash)
```



### Install MySQL from Helm

Add bitnami Chartes Repository.
```
helm repo add bitnami https://charts.bitnami.com/bitnami
```

Get current Charts repositories.
```
helm repo list
```
```
NAME    URL
bitnami https://charts.bitnami.com/bitnami
```

Sync up local Charts repositories.
```
helm repo update
```

Search bitnami Charts in repositories.
```
helm search repo bitnami
```

Search bitnami/mysql Charts in repositories.
```
helm search repo bitnami/mysql
```

Install MySQL Chart on namespace `dev`：
```
helm install mysql bitnami/mysql -n dev
```
Output
```
NAME: mysql
LAST DEPLOYED: Sun Jul 24 19:37:20 2022
NAMESPACE: dev
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: mysql
CHART VERSION: 9.2.1
APP VERSION: 8.0.29

** Please be patient while the chart is being deployed **

Tip:

  Watch the deployment status using the command: kubectl get pods -w --namespace dev

Services:

  echo Primary: mysql.dev.svc.cluster.local:3306

Execute the following to get the administrator credentials:

  echo Username: root
  MYSQL_ROOT_PASSWORD=$(kubectl get secret --namespace dev mysql -o jsonpath="{.data.mysql-root-password}" | base64 -d)

To connect to your database:

  1. Run a pod that you can use as a client:

      kubectl run mysql-client --rm --tty -i --restart='Never' --image  docker.io/bitnami/mysql:8.0.29-debian-11-r9 --namespace dev --env MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD --command -- bash

  2. To connect to primary service (read/write):

      mysql -h mysql.dev.svc.cluster.local -uroot -p"$MYSQL_ROOT_PASSWORD"
```

Check installed release：
```
helm list
```
Result
```
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
mysql   dev             1               2022-07-24 19:37:20.710988009 +0800 CST deployed        mysql-9.2.1     8.0.29 
```

Check installed mysql release information.
```
helm status mysql
```

Check mysql Pod status.
```
kubectl get pod
```
Result
```
NAME                                      READY   STATUS    RESTARTS   AGE
mysql-0                                   1/1     Running   0          72s
```


### Develop a Chart

Below is a demo on how to develop a Chart.

Execute `helm create` to initiate a Chart：

```
# Naming conventions of Chart: lowercase a~z and -(minus sign)
helm create cka-demo
```

A folder `cka-demo` was created. Check the folder structure.
```
tree cka-demo/
```
Output
```
cka-demo/
├── charts
├── Chart.yaml
├── templates
│   ├── deployment.yaml
│   ├── _helpers.tpl
│   ├── hpa.yaml
│   ├── ingress.yaml
│   ├── NOTES.txt
│   ├── serviceaccount.yaml
│   ├── service.yaml
│   └── tests
│       └── test-connection.yaml
└── values.yaml
```

Delete or empty some files, which will be re-created later.
```
cd cka-demo
rm -rf charts
rm -rf templates/tests 
rm -rf templates/*.yaml
echo "" > values.yaml
echo "" > templates/NOTES.txt
echo "" > templates/_helpers.tpl
cd ..
```

Now new structure looks like below.
```
tree cka-demo/
```
Output
```
cka-demo/
├── Chart.yaml
├── templates
│   ├── _helpers.tpl
│   └── NOTES.txt
└── values.yaml
```


### NOTES.txt

NOTES.txt is used to provide summary information to Chart users. 
In the demo, we will use NOTES.txt to privide summary info about whether the user passed CKA certificate or not.
```
cd cka-demo/
vi templates/NOTES.txt
```
Add below info.
```
{{- if .Values.passExam }}
Congratulations!

You have successfully completed Certified Kubernetes Administrator China Exam (CKA-CN). 

Your CKA score is: {{ .Values.ckaScore }}

Click the link below to view and download your certificate.

https://trainingportal.linuxfoundation.org/learn/dashboard
{{- else }}
Come on! you can do it next time!
{{- end }}
```



### Deployment Template

Let's use Busybox service to generate information. 
We use `kubectl create deployment --dry-run=client -oyaml` to generate Deployment yaml file and write it the yaml file content into file `templates/deployment.yaml`.
```
kubectl create deployment cka-demo-busybox --image=busybox:latest --dry-run=client -oyaml > templates/deployment.yaml
```

Check content of deployment yaml file `templates/deployment.yaml`.
```
cat templates/deployment.yaml
```
```
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: cka-demo-busybox
  name: cka-demo-busybox
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cka-demo-busybox
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: cka-demo-busybox
    spec:
      containers:
      - image: busybox:latest
        name: busybox
        resources: {}
status: {}
```

Edit file `templates/deployment.yaml`.
```
vi templates/deployment.yaml
```
Let's replace value of `.spec.replicas` from `1` to a variable `{{ .Values.replicaCount }}`, so we can dynamicly assign replicas number for other Deployment.
```
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: cka-demo-busybox
  name: cka-demo-busybox
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: cka-demo-busybox
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: cka-demo-busybox
    spec:
      containers:
      - image: busybox:latest
        name: busybox
        resources: {}
status: {}
```

The `.spec.replicas` will be replaced by actula value of `.Values.replicaCount` during deployment. 

Let's create another file `values.yaml` and add a variable `replicaCount` with default value 1 into the file.
Strong recommended to add comments for each value we defined in file `values.yaml`.
```
vi values.yaml
```
```
# Number of deployment replicas
replicaCount: 1
```

Let's add more variables into file `templates/deployment.yaml`.

* Replace Release name `.metadata.name` by `{{ .Release.Name }}` and filled with variable defined in file `values.yaml`.
* Replace label name `.metadata.labels` by `{{- include "cka-demo.labels" . | nindent 4 }}`, and filled with labels name `cka-demo.labels` defined in file `_helpers.tpl`.
* Replace `.spec.replicas` by `{{ .Values.replicaCount }}` and filled with variable defined in file `values.yaml`.
* Replace `.spec.selector.matchLabels` by `{{- include "cka-demo.selectorLabels" . | nindent 6 }}` and filled with `cka-demo.selectorLabels` defined in file `_helpers.tpl`.
* Replace `.spec.template.metadata.labels` by `{{- include "cka-demo.selectorLabels" . | nindent 8 }}` and filled with `cka-demo.selectorLabels` defined in file `_helpers.tpl`.
* Replace `.spec.template.spec.containers[0].image` by `{{ .Values.image.repository }}` and `{{ .Values.image.tag }}` and filled with variables defined in `values.yaml` for image name and image tag.
* Replace `.spec.template.spec.containers[0].command` and add `if-else` statement, if `.Values.passExam` is true, execute commands defined in `.Values.passCommand`, if false, execute commands defined in `.Values.lostCommand`.
* Use `key` from `ConfigMap` from `.spec.template.spec.containers[0].env` as prefix of ConfigMap name and filled with `{{ .Values.studentName }}` defined in file `values.yaml`.
* Replace `.spec.template.spec.containers[0].resources` by `{{ .Values.resources }}` and filled with variable defined in file `values.yaml`.

The `.Release.Name` is built-in object, no need to be specified in file `values.yaml`. It's generated by Release by `helm install`.


Remove unused lines and final one looks like below.
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}
  labels:
    {{- include "cka-demo.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "cka-demo.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "cka-demo.selectorLabels" . | nindent 8 }}
    spec:
      containers:
      - name: id-generator
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        {{- if .Values.passExam }}
        {{- with .Values.passCommand }}
        command: {{ range . }}
          - {{ . | quote }}
          {{- end }}
          {{- end }}
        {{- else }}
        {{- with .Values.lostCommand }}
        command: {{ range . }}
          - {{ . | quote }}
          {{- end }}
          {{- end }}
        {{- end }}
        env:
        - name: CKA_SCORE
          valueFrom:
            configMapKeyRef:
              name: {{ .Values.studentName }}-cka-score
              key: cka_score
        {{- with .Values.resources }}
        resources:
            {{- toYaml . | nindent 12 }}
          {{- end}}
      restartPolicy: Always
```



Update file `values.yaml` with variables default values.
Suggestions：add variables one and test one, don't add all at one time.
```
vi values.yaml
```
```
# Number of deployment replicas	
replicaCount: 1

# Image repository and tag
image:
  repository: busybox
  tag: latest

# Container start command
passCommand:
  - '/bin/sh'
  - '-c'
  - "echo Your CKA score is $(CKA_SCORE) and your CKA certificate ID number is $(tr -dc 'A-Za-z0-9' < /dev/urandom | head -c 13; echo) ; sleep 86400"
lostCommand:
  - '/bin/sh'
  - '-c'
  - "echo Your CKA score is $(CKA_SCORE), Come on! you can do it next time! ; sleep 86400"

# Container resources
resources:
  limits:
    cpu: 200m
    memory: 256Mi
  requests:
    cpu: 100m
    memory: 128Mi
    
# Student Name
studentName: whoareyou

# Student pass CKA exam or not
passExam: true
```





### ConfigMap Template

ConfigMap is referred in the Deployment, hence we need define the ConfigMap template.
We will combine name of ConfigMap and `cka_score` as a variable, like `name-cka-score`.

```
vi templates/configmap.yaml
```
```
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Values.studentName }}-cka-score
  labels:
    {{- include "cka-demo.labels" . | nindent 4 }}
data:
  cka_score: {{ .Values.ckaScore | quote }}
```

The `studentName` was already defined in file `values.yaml`, we just need add `ckaScore` with default value.
```
vi values.yaml
```
```
# Student CKA Score
ckaScore: 100
```



### _helpers.tpl

Define a common template `_helpers.tpl` to add labels and labels of Selector for labels of Deployment and ConfigMap.
```
vi templates/_helpers.tpl
```
```
{{/*
Common labels
*/}}
{{- define "cka-demo.labels" -}}
{{ include "cka-demo.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}


{{/*
Selector labels
*/}}
{{- define "cka-demo.selectorLabels" -}}
app: {{ .Chart.Name }}
release: {{ .Release.Name }}
{{- end -}}
```



### Chart.yaml

We use CKA logo as the icon of Chart
```
wget https://www.cncf.io/wp-content/uploads/2021/09/kubernetes-cka-color.svg
```

Edit Chart.yaml file.
```
vi Chart.yaml
```
Append icon info in the file.
```
icon: file://./kubernetes-cka-color.svg
```

Add author info for the Chart
```
vi Chart.yaml
```
```
maintainers:
  - name: James.H
```

Final `Chart.yaml` looks like below. Don't forget to update `appVersion: "v1.23"` to current Kubernetes API version.
```
apiVersion: v2
name: cka-demo
description: A Helm chart for CKA demo.
type: application
version: 0.1.0
appVersion: "v1.23"
maintainers:
  - name: James.H
icon: file://./kubernetes-cka-color.svg
```



### Chart Debug

Use `helm lint` to verify above change.
```
helm lint
```
```
1 chart(s) linted, 0 chart(s) failed
```

`helm lint` only check format of Chart, won't check Manifest file.

We can use `helm install --debug --dry-run` or `helm template` to check Manifest output in order to verify all yaml files are correct or not.
```
helm template cka-demo ./
```

Use `helm install --debug --dry-run` to simulate the installation. We can get expected results from two different options (passed or failed the CKA certificate).
```
helm install --debug --dry-run cka-demo ./ --create-namespace \
  -n cka \
  --set studentName=kubernetes \
  --set ckaScore=99 \
  --set passExam=true
  
helm install --debug --dry-run cka-demo ./ --create-namespace \
  -n cka \
  --set studentName=kubernetes \
  --set ckaScore=0 \
  --set passExam=false
```

Package Chart to .tgz file, and upload to repository, e.g., Chart Museum or OCI Repo.
```
cd ../
helm package cka-demo
```
```
Successfully packaged chart and saved it to: /root/cka-demo-0.1.0.tgz
```

Till now, we have done our task to develop a Chart. Let's install the Chart.
```
helm install cka-demo cka-demo-0.1.0.tgz --create-namespace \
  -n cka \
  --set studentName=kubernetes \
  --set ckaScore=0 \
  --set passExam=false
```
Result
```
NAME: cka-demo
LAST DEPLOYED: Sun Jul 24 19:58:36 2022
NAMESPACE: cka
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
Come on! you can do it next time!
```

Check the deployment
```
helm list --all-namespaces
```
Result
```
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
cka-demo        cka             1               2022-07-24 19:58:36.272093383 +0800 CST deployed        cka-demo-0.1.0  v1.23      
mysql           dev             1               2022-07-24 19:37:20.710988009 +0800 CST deployed        mysql-9.2.1     8.0.29  
```

If any error, need to unstall `cka-demo` and reinstall it.
```
helm uninstall cka-demo -n <your_namespace>
```

Check log of `cka-demo `.
```
kubectl logs -n cka -l app=cka-demo
```
Result
```
Your CKA score is 0, Come on! you can do it next time!
```

Install `cka-demo` with different options.
```
helm uninstall cka-demo -n cka

helm install cka-demo cka-demo-0.1.0.tgz --create-namespace \
  -n cka \
  --set studentName=kubernetes \
  --set ckaScore=100 \
  --set passExam=true
```
```
NAME: cka-demo
LAST DEPLOYED: Sun Jul 24 20:01:34 2022
NAMESPACE: cka
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
Congratulations!

You have successfully completed Certified Kubernetes Administrator China Exam (CKA-CN).

Your CKA score is: 100

Click the link below to view and download your certificate.

https://trainingportal.linuxfoundation.org/learn/dashboard
```

Check log of `cka-demo `.
```
kubectl logs -n cka -l app=cka-demo
```
```
Your CKA score is 100 and your CKA certificate ID number is BQKoVYVhjzl3G
```




**Built-in Objects**
```
Release.Name                 # 发布名称
Release.Namespace            # 发布Namespace
Release.Service              # 渲染模板的服务，在Helm中默认值为"Helm"
Release.IsUpgrade            # 如果当前是升级或回滚，设置为true
Release.IsInstall            # 如果当前是安装，设置为true
Release.Revision             # 发布版本号
Values                       # 从values.yaml和--set传入，默认为空
Chart                        # 所有Chart.yaml中的内容
Chart.Version                # 例如
Chart.Maintainers            # 例如
Files                        # 在chart中访问非特殊文件
Capabilities                 # 提供关于支持能力的信息（K8s API版本、K8s版本、Helm版本）
Capabilities.KubeVersion     # Kubernetes的版本号
Capabilities.APIVersions.Has "batch/v1" # K8s API版本包含"batch/v1"
Template                     # 当前模板信息
Template.Name                # 当前模板文件路径
Template.BasePath            # 当前模板目录路径
```



### Reference

[Helm 官网](https://helm.sh/)

[Helm 版本支持策略](https://helm.sh/zh/docs/topics/version_skew/)

[Helm Chart 资源对象安装顺序](https://github.com/helm/helm/blob/484d43913f97292648c867b56768775a55e4bba6/pkg/releaseutil/kind_sorter.go)





## Case Study

### Install Calico

[End-to-end Calico installation](https://projectcalico.docs.tigera.io/getting-started/kubernetes/hardway/)


#### The Calico Datastore

In order to use Kubernetes as the Calico datastore, we need to define the custom resources Calico uses.

Download and examine the list of Calico custom resource definitions, and open it in a file editor.
```
wget https://projectcalico.docs.tigera.io/manifests/crds.yaml
```

Create the custom resource definitions in Kubernetes.
```
kubectl apply -f crds.yaml
```

Install `calicoctl`. To interact directly with the Calico datastore, use the `calicoctl` client tool.

Download the calicoctl binary to a Linux host with access to Kubernetes. 
The latest release of calicoctl can be found in the [git page](https://github.com/projectcalico/calico/releases) and replace below `v3.23.2` by actual release number.
```
wget https://github.com/projectcalico/calico/releases/download/v3.23.3/calicoctl-linux-amd64
chmod +x calicoctl-linux-amd64
sudo cp calicoctl-linux-amd64 /usr/local/bin/calicoctl
```

Configure calicoctl to access Kubernetes
```
echo "export KUBECONFIG=/root/.kube/config" >> ~/.bashrc
echo "export DATASTORE_TYPE=kubernetes" >> ~/.bashrc

echo $KUBECONFIG
echo $DATASTORE_TYPE
```

Verify `calicoctl` can reach the datastore by running：
```
calicoctl get nodes -o wide
```
Output similar to below:
```
NAME     ASN   IPV4   IPV6   
cka001                       
cka002                       
cka003  
```

Nodes are backed by the Kubernetes node object, so we should see names that match `kubectl get nodes`.
```
kubectl get nodes -o wide
```
```
NAME     STATUS     ROLES                  AGE   VERSION   INTERNAL-IP     EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION      CONTAINER-RUNTIME
cka001   NotReady   control-plane,master   23m   v1.24.0   172.16.18.170   <none>        Ubuntu 20.04.4 LTS   5.4.0-113-generic   containerd://1.5.9
cka002   NotReady   <none>                 22m   v1.24.0   172.16.18.169   <none>        Ubuntu 20.04.4 LTS   5.4.0-113-generic   containerd://1.5.9
cka003   NotReady   <none>                 21m   v1.24.0   172.16.18.159   <none>        Ubuntu 20.04.4 LTS   5.4.0-113-generic   containerd://1.5.9
```



#### Configure IP Pools

A workload is a container or VM that Calico handles the virtual networking for. 
In Kubernetes, workloads are pods. 
A workload endpoint is the virtual network interface a workload uses to connect to the Calico network.

IP pools are ranges of IP addresses that Calico uses for workload endpoints.

Get current IP pools in the cluster. So far, it's empty after fresh installation.
```
calicoctl get ippools
```
```
NAME   CIDR   SELECTOR 
```

The Pod CIDR is `10.244.0.0/16` we specified via `kubeadm init`.

Let's create two IP pools for use in the cluster. Each pool can not have any overlaps.

* ipv4-ippool-1: `10.244.0.0/18`
* ipv4-ippool-2: `10.244.192.0/19`

```
calicoctl apply -f - <<EOF
apiVersion: projectcalico.org/v3
kind: IPPool
metadata:
  name: ipv4-ippool-1
spec:
  cidr: 10.244.0.0/18
  ipipMode: Never
  natOutgoing: true
  disabled: false
  nodeSelector: all()
EOF
```
```
calicoctl apply -f - <<EOF
apiVersion: projectcalico.org/v3
kind: IPPool
metadata:
  name: ipv4-ippool-2
spec:
  cidr: 10.244.192.0/19
  ipipMode: Never
  natOutgoing: true
  disabled: true
  nodeSelector: all()
EOF
```

IP pool now looks like below.
```
calicoctl get ippools -o wide
```
```
NAME            CIDR              NAT    IPIPMODE   VXLANMODE   DISABLED   DISABLEBGPEXPORT   SELECTOR   
ipv4-ippool-1   10.244.0.0/18     true   Never      Never       false      false              all()      
ipv4-ippool-2   10.244.192.0/19   true   Never      Never       true       false              all()     
```


#### Install CNI plugin

* Provision Kubernetes user account for the plugin.

Kubernetes uses the Container Network Interface (CNI) to interact with networking providers like Calico. 
The Calico binary that presents this API to Kubernetes is called the CNI plugin and must be installed on every node in the Kubernetes cluster.

The CNI plugin interacts with the Kubernetes API server while creating pods, both to obtain additional information and to update the datastore with information about the pod.

On the Kubernetes *master* node, create a key for the CNI plugin to authenticate with and certificate signing request.

Change to directory `/etc/kubernetes/pki/`.
```
cd /etc/kubernetes/pki/
```
```
openssl req -newkey rsa:4096 \
  -keyout cni.key \
  -nodes \
  -out cni.csr \
  -subj "/CN=calico-cni"
```

We will sign this certificate using the main Kubernetes CA.
```
sudo openssl x509 -req -in cni.csr \
  -CA /etc/kubernetes/pki/ca.crt \
  -CAkey /etc/kubernetes/pki/ca.key \
  -CAcreateserial \
  -out cni.crt \
  -days 3650
```
Output looks like below. User is `calico-cni`.
```
Signature ok
subject=CN = calico-cni
Getting CA Private Key
```
```
sudo chown $(id -u):$(id -g) cni.crt
```

Next, we create a kubeconfig file for the CNI plugin to use to access Kubernetes. 
Copy this `cni.kubeconfig` file to every node in the cluster.

Stay in directory `/etc/kubernetes/pki/`.
```
APISERVER=$(kubectl config view -o jsonpath='{.clusters[0].cluster.server}')

echo $APISERVER

kubectl config set-cluster kubernetes \
  --certificate-authority=/etc/kubernetes/pki/ca.crt \
  --embed-certs=true \
  --server=$APISERVER \
  --kubeconfig=cni.kubeconfig

kubectl config set-credentials calico-cni \
  --client-certificate=cni.crt \
  --client-key=cni.key \
  --embed-certs=true \
  --kubeconfig=cni.kubeconfig

kubectl config set-context cni@kubernetes \
  --cluster=kubernetes \
  --user=calico-cni \
  --kubeconfig=cni.kubeconfig

kubectl config use-context cni@kubernetes --kubeconfig=cni.kubeconfig
```

The context for CNI looks like below.
```
kubectl config get-contexts --kubeconfig=cni.kubeconfig
```
```
CURRENT   NAME             CLUSTER      AUTHINFO     NAMESPACE
*         cni@kubernetes   kubernetes   calico-cni 
```



* Provision RBAC

Change to home directory
```
cd ~
```

Define a cluster role the CNI plugin will use to access Kubernetes.

```
kubectl apply -f - <<EOF
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: calico-cni
rules:
  # The CNI plugin needs to get pods, nodes, and namespaces.
  - apiGroups: [""]
    resources:
      - pods
      - nodes
      - namespaces
    verbs:
      - get
  # The CNI plugin patches pods/status.
  - apiGroups: [""]
    resources:
      - pods/status
    verbs:
      - patch
 # These permissions are required for Calico CNI to perform IPAM allocations.
  - apiGroups: ["crd.projectcalico.org"]
    resources:
      - blockaffinities
      - ipamblocks
      - ipamhandles
    verbs:
      - get
      - list
      - create
      - update
      - delete
  - apiGroups: ["crd.projectcalico.org"]
    resources:
      - ipamconfigs
      - clusterinformations
      - ippools
    verbs:
      - get
      - list
EOF
```

Bind the cluster role to the `calico-cni` account.
```
kubectl create clusterrolebinding calico-cni --clusterrole=calico-cni --user=calico-cni
```



* Install the plugin

Do these steps on **each node** in your cluster.

Installation on `cka001`.

Run these commands as **root**.
```
sudo su
```

Install the CNI plugin Binaries. 
Get right release in the link `https://github.com/projectcalico/cni-plugin/releases`, and link `https://github.com/containernetworking/plugins/releases`.
```
mkdir -p /opt/cni/bin

curl -L -o /opt/cni/bin/calico https://github.com/projectcalico/cni-plugin/releases/download/v3.20.5/calico-amd64
chmod 755 /opt/cni/bin/calico

curl -L -o /opt/cni/bin/calico-ipam https://github.com/projectcalico/cni-plugin/releases/download/v3.20.5/calico-ipam-amd64
chmod 755 /opt/cni/bin/calico-ipam
```
```
wget https://github.com/containernetworking/plugins/releases/download/v1.1.1/cni-plugins-linux-amd64-v1.1.1.tgz
tar xvf cni-plugins-linux-amd64-v1.1.1.tgz -C /opt/cni/bin
```

Create the config directory
```
mkdir -p /etc/cni/net.d/
```

Copy the kubeconfig from the previous section
```
cp /etc/kubernetes/pki/cni.kubeconfig /etc/cni/net.d/calico-kubeconfig

chmod 600 /etc/cni/net.d/calico-kubeconfig
```

Write the CNI configuration
```
cat > /etc/cni/net.d/10-calico.conflist <<EOF
{
  "name": "k8s-pod-network",
  "cniVersion": "0.3.1",
  "plugins": [
    {
      "type": "calico",
      "log_level": "info",
      "datastore_type": "kubernetes",
      "mtu": 1500,
      "ipam": {
          "type": "calico-ipam"
      },
      "policy": {
          "type": "k8s"
      },
      "kubernetes": {
          "kubeconfig": "/etc/cni/net.d/calico-kubeconfig"
      }
    },
    {
      "type": "portmap",
      "snat": true,
      "capabilities": {"portMappings": true}
    }
  ]
}
EOF
```
```
cp /etc/cni/net.d/calico-kubeconfig ~
```

Exit from su and go back to the logged in user.
```
exit
```


Installation on `cka002`.

```
sftp -i cka-key-pair.pem cka002
```
```
put calico-amd64
put calicoctl-linux-amd64
put calico-ipam-amd64
put calico-kubeconfig
put cni-plugins-linux-amd64-v1.1.1.tgz
```
```
ssh -i cka-key-pair.pem cka002
```
```
mkdir -p /opt/cni/bin

cp calico-amd64 /opt/cni/bin/calico
cp calico-ipam-amd64 /opt/cni/bin/calico-ipam

tar xvf cni-plugins-linux-amd64-v1.1.1.tgz -C /opt/cni/bin

mkdir -p /etc/cni/net.d/

cp calico-kubeconfig /etc/cni/net.d/calico-kubeconfig

chmod 600 /etc/cni/net.d/calico-kubeconfig
```
```
cat > /etc/cni/net.d/10-calico.conflist <<EOF
{
  "name": "k8s-pod-network",
  "cniVersion": "0.3.1",
  "plugins": [
    {
      "type": "calico",
      "log_level": "info",
      "datastore_type": "kubernetes",
      "mtu": 1500,
      "ipam": {
          "type": "calico-ipam"
      },
      "policy": {
          "type": "k8s"
      },
      "kubernetes": {
          "kubeconfig": "/etc/cni/net.d/calico-kubeconfig"
      }
    },
    {
      "type": "portmap",
      "snat": true,
      "capabilities": {"portMappings": true}
    }
  ]
}
EOF
```

Back to `cka001`.
```
exit
```


Installation on `cka003`.

```
sftp -i cka-key-pair.pem cka003
```
```
put calico-amd64
put calicoctl-linux-amd64
put calico-ipam-amd64
put calico-kubeconfig
put cni-plugins-linux-amd64-v1.1.1.tgz
```

```
ssh -i cka-key-pair.pem cka003
```
```
mkdir -p /opt/cni/bin

cp calico-amd64 /opt/cni/bin/calico
cp calico-ipam-amd64 /opt/cni/bin/calico-ipam

tar xvf cni-plugins-linux-amd64-v1.1.1.tgz -C /opt/cni/bin

mkdir -p /etc/cni/net.d/

cp calico-kubeconfig /etc/cni/net.d/calico-kubeconfig

chmod 600 /etc/cni/net.d/calico-kubeconfig
```
```
cat > /etc/cni/net.d/10-calico.conflist <<EOF
{
  "name": "k8s-pod-network",
  "cniVersion": "0.3.1",
  "plugins": [
    {
      "type": "calico",
      "log_level": "info",
      "datastore_type": "kubernetes",
      "mtu": 1500,
      "ipam": {
          "type": "calico-ipam"
      },
      "policy": {
          "type": "k8s"
      },
      "kubernetes": {
          "kubeconfig": "/etc/cni/net.d/calico-kubeconfig"
      }
    },
    {
      "type": "portmap",
      "snat": true,
      "capabilities": {"portMappings": true}
    }
  ]
}
EOF
```

Back to `cka001`.
```
exit
```

Stay in home directory in node `cka001`.

At this point Kubernetes nodes will become Ready because Kubernetes has a networking provider and configuration installed.
```
kubectl get nodes
```
Result
```
NAME     STATUS   ROLES                  AGE     VERSION
cka001   Ready    control-plane,master   4h50m   v1.24.0
cka002   Ready    <none>                 4h49m   v1.24.0
cka003   Ready    <none>                 4h49m   v1.24.0
```






#### Install Typha

Typha sits between the Kubernetes API server and per-node daemons like Felix and confd (running in calico/node). 
It watches the Kubernetes resources and Calico custom resources used by these daemons, and whenever a resource changes it fans out the update to the daemons. 
This reduces the number of watches the Kubernetes API server needs to serve and improves scalability of the cluster.

* Provision Certificates

We will use mutually authenticated TLS to ensure that calico/node and Typha communicate securely. 
We generate a certificate authority (CA) and use it to sign a certificate for Typha.

Change to directory `/etc/kubernetes/pki/`.
```
cd /etc/kubernetes/pki/
```

Create the CA certificate and key
```
openssl req -x509 -newkey rsa:4096 \
  -keyout typhaca.key \
  -nodes \
  -out typhaca.crt \
  -subj "/CN=Calico Typha CA" \
  -days 365
```

Store the CA certificate in a ConfigMap that Typha & calico/node will access.
```
kubectl create configmap -n kube-system calico-typha-ca --from-file=typhaca.crt
```

Create the Typha key and certificate signing request (CSR).
```
openssl req -newkey rsa:4096 \
  -keyout typha.key \
  -nodes \
  -out typha.csr \
  -subj "/CN=calico-typha"
```

The certificate presents the Common Name (CN) as `calico-typha`. `calico/node` will be configured to verify this name.

Sign the Typha certificate with the CA.
```
openssl x509 -req -in typha.csr \
  -CA typhaca.crt \
  -CAkey typhaca.key \
  -CAcreateserial \
  -out typha.crt \
  -days 365
```
```
Signature ok
subject=CN = calico-typha
Getting CA Private Key
```

Store the Typha key and certificate in a secret that Typha will access
```
kubectl create secret generic -n kube-system calico-typha-certs --from-file=typha.key --from-file=typha.crt
```


* Provision RBAC

Change to home directory.
```
cd ~
```

Create a ServiceAccount that will be used to run Typha.
```
kubectl create serviceaccount -n kube-system calico-typha
```

Define a cluster role for Typha with permission to watch Calico datastore objects.
```
kubectl apply -f - <<EOF
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: calico-typha
rules:
  - apiGroups: [""]
    resources:
      - pods
      - namespaces
      - serviceaccounts
      - endpoints
      - services
      - nodes
    verbs:
      # Used to discover service IPs for advertisement.
      - watch
      - list
  - apiGroups: ["networking.k8s.io"]
    resources:
      - networkpolicies
    verbs:
      - watch
      - list
  - apiGroups: ["crd.projectcalico.org"]
    resources:
      - globalfelixconfigs
      - felixconfigurations
      - bgppeers
      - globalbgpconfigs
      - bgpconfigurations
      - ippools
      - ipamblocks
      - globalnetworkpolicies
      - globalnetworksets
      - networkpolicies
      - clusterinformations
      - hostendpoints
      - blockaffinities
      - networksets
    verbs:
      - get
      - list
      - watch
  - apiGroups: ["crd.projectcalico.org"]
    resources:
      #- ippools
      #- felixconfigurations
      - clusterinformations
    verbs:
      - get
      - create
      - update
EOF
```

Bind the cluster role to the calico-typha ServiceAccount.
```
kubectl create clusterrolebinding calico-typha --clusterrole=calico-typha --serviceaccount=kube-system:calico-typha
```



* Install Deployment

Since Typha is required by `calico/node`, and `calico/node` establishes the pod network, we run Typha as a host networked pod to avoid a chicken-and-egg problem. 
We run 3 replicas of Typha so that even during a rolling update, a single failure does not make Typha unavailable.
```
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: calico-typha
  namespace: kube-system
  labels:
    k8s-app: calico-typha
spec:
  replicas: 3
  revisionHistoryLimit: 2
  selector:
    matchLabels:
      k8s-app: calico-typha
  template:
    metadata:
      labels:
        k8s-app: calico-typha
      annotations:
        cluster-autoscaler.kubernetes.io/safe-to-evict: 'true'
    spec:
      hostNetwork: true
      tolerations:
        # Mark the pod as a critical add-on for rescheduling.
        - key: CriticalAddonsOnly
          operator: Exists
      serviceAccountName: calico-typha
      priorityClassName: system-cluster-critical
      containers:
      - image: calico/typha:v3.8.0
        name: calico-typha
        ports:
        - containerPort: 5473
          name: calico-typha
          protocol: TCP
        env:
          # Disable logging to file and syslog since those don't make sense in Kubernetes.
          - name: TYPHA_LOGFILEPATH
            value: "none"
          - name: TYPHA_LOGSEVERITYSYS
            value: "none"
          # Monitor the Kubernetes API to find the number of running instances and rebalance
          # connections.
          - name: TYPHA_CONNECTIONREBALANCINGMODE
            value: "kubernetes"
          - name: TYPHA_DATASTORETYPE
            value: "kubernetes"
          - name: TYPHA_HEALTHENABLED
            value: "true"
          # Location of the CA bundle Typha uses to authenticate calico/node; volume mount
          - name: TYPHA_CAFILE
            value: /calico-typha-ca/typhaca.crt
          # Common name on the calico/node certificate
          - name: TYPHA_CLIENTCN
            value: calico-node
          # Location of the server certificate for Typha; volume mount
          - name: TYPHA_SERVERCERTFILE
            value: /calico-typha-certs/typha.crt
          # Location of the server certificate key for Typha; volume mount
          - name: TYPHA_SERVERKEYFILE
            value: /calico-typha-certs/typha.key
        livenessProbe:
          httpGet:
            path: /liveness
            port: 9098
            host: localhost
          periodSeconds: 30
          initialDelaySeconds: 30
        readinessProbe:
          httpGet:
            path: /readiness
            port: 9098
            host: localhost
          periodSeconds: 10
        volumeMounts:
        - name: calico-typha-ca
          mountPath: "/calico-typha-ca"
          readOnly: true
        - name: calico-typha-certs
          mountPath: "/calico-typha-certs"
          readOnly: true
      volumes:
      - name: calico-typha-ca
        configMap:
          name: calico-typha-ca
      - name: calico-typha-certs
        secret:
          secretName: calico-typha-certs
EOF
```

We set `TYPHA_CLIENTCN` to calico-node which is the common name we will use on the certificate `calico/node` will use late.

Verify Typha is up an running with three instances
```
kubectl get pods -l k8s-app=calico-typha -n kube-system
```
Result looks like below.
```
NAME                           READY   STATUS    RESTARTS   AGE
calico-typha-5b8669646-b2xnq   1/1     Running   0          20s
calico-typha-5b8669646-q5glk   0/1     Pending   0          20s
calico-typha-5b8669646-rvv86   1/1     Running   0          20s
```

Here is an error message received:
```
0/3 nodes are available: 1 node(s) had taint {node-role.kubernetes.io/master: }, that the pod didn't tolerate, 2 node(s) didn't have free ports for the requested pod ports.
```




* Install Service

`calico/node` uses a Kubernetes Service to get load-balanced access to Typha.
```
kubectl apply -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  name: calico-typha
  namespace: kube-system
  labels:
    k8s-app: calico-typha
spec:
  ports:
    - port: 5473
      protocol: TCP
      targetPort: calico-typha
      name: calico-typha
  selector:
    k8s-app: calico-typha
EOF
```

Validate that Typha is using TLS.
```
TYPHA_CLUSTERIP=$(kubectl get svc -n kube-system calico-typha -o jsonpath='{.spec.clusterIP}')
```
```
curl https://$TYPHA_CLUSTERIP:5473 -v --cacert /etc/kubernetes/pki/typhaca.crt
```
Result
```
*   Trying 11.244.91.165:5473...
* TCP_NODELAY set
* Connected to 11.244.91.165 (11.244.91.165) port 5473 (#0)
* ALPN, offering h2
* ALPN, offering http/1.1
* successfully set certificate verify locations:
*   CAfile: /etc/kubernetes/pki/typhaca.crt
  CApath: /etc/ssl/certs
* TLSv1.3 (OUT), TLS handshake, Client hello (1):
* TLSv1.3 (IN), TLS handshake, Server hello (2):
* TLSv1.2 (IN), TLS handshake, Certificate (11):
* TLSv1.2 (IN), TLS handshake, Server key exchange (12):
* TLSv1.2 (IN), TLS handshake, Request CERT (13):
* TLSv1.2 (IN), TLS handshake, Server finished (14):
* TLSv1.2 (OUT), TLS handshake, Certificate (11):
* TLSv1.2 (OUT), TLS handshake, Client key exchange (16):
* TLSv1.2 (OUT), TLS change cipher, Change cipher spec (1):
* TLSv1.2 (OUT), TLS handshake, Finished (20):
* TLSv1.2 (IN), TLS alert, bad certificate (554):
* error:14094412:SSL routines:ssl3_read_bytes:sslv3 alert bad certificate
* Closing connection 0
curl: (35) error:14094412:SSL routines:ssl3_read_bytes:sslv3 alert bad certificate
```

This demonstrates that Typha is presenting its TLS certificate and rejecting our connection because we do not present a certificate. 
We will later deploy calico/node with a certificate Typha will accept.





#### Install calico/node

`calico/node` runs three daemons:

* Felix, the Calico per-node daemon
* BIRD, a daemon that speaks the BGP protocol to distribute routing information to other nodes
* confd, a daemon that watches the Calico datastore for config changes and updates BIRD’s config files


* Provision Certificates

Change to directory `/etc/kubernetes/pki/`.
```
cd /etc/kubernetes/pki/
```

Create the key `calico/node` will use to authenticate with Typha and the certificate signing request (CSR)
```
openssl req -newkey rsa:4096 \
  -keyout calico-node.key \
  -nodes \
  -out calico-node.csr \
  -subj "/CN=calico-node"
```

The certificate presents the Common Name (CN) as `calico-node`, which is what we configured Typha to accept in the last lab.

Sign the Felix certificate with the CA we created earlier.
```
openssl x509 -req -in calico-node.csr \
  -CA typhaca.crt \
  -CAkey typhaca.key \
  -CAcreateserial \
  -out calico-node.crt \
  -days 365
```
```
Signature ok
subject=CN = calico-node
Getting CA Private Key
```

Store the key and certificate in a Secret that calico/node will access.
```
kubectl create secret generic -n kube-system calico-node-certs --from-file=calico-node.key --from-file=calico-node.crt
```


* Provision RBAC

Change to home directory.
```
cd ~
```

Create the ServiceAccount that calico/node will run as.
```
kubectl create serviceaccount -n kube-system calico-node
```

Provision a cluster role with permissions to read and modify Calico datastore objects
```
kubectl apply -f - <<EOF
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: calico-node
rules:
  # The CNI plugin needs to get pods, nodes, and namespaces.
  - apiGroups: [""]
    resources:
      - pods
      - nodes
      - namespaces
    verbs:
      - get
  # EndpointSlices are used for Service-based network policy rule
  # enforcement.
  - apiGroups: ["discovery.k8s.io"]
    resources:
      - endpointslices
    verbs:
      - watch
      - list
  - apiGroups: [""]
    resources:
      - endpoints
      - services
    verbs:
      # Used to discover service IPs for advertisement.
      - watch
      - list
      # Used to discover Typhas.
      - get
  # Pod CIDR auto-detection on kubeadm needs access to config maps.
  - apiGroups: [""]
    resources:
      - configmaps
    verbs:
      - get
  - apiGroups: [""]
    resources:
      - nodes/status
    verbs:
      # Needed for clearing NodeNetworkUnavailable flag.
      - patch
      # Calico stores some configuration information in node annotations.
      - update
  # Watch for changes to Kubernetes NetworkPolicies.
  - apiGroups: ["networking.k8s.io"]
    resources:
      - networkpolicies
    verbs:
      - watch
      - list
  # Used by Calico for policy information.
  - apiGroups: [""]
    resources:
      - pods
      - namespaces
      - serviceaccounts
    verbs:
      - list
      - watch
  # The CNI plugin patches pods/status.
  - apiGroups: [""]
    resources:
      - pods/status
    verbs:
      - patch
  # Used for creating service account tokens to be used by the CNI plugin
  - apiGroups: [""]
    resources:
      - serviceaccounts/token
    resourceNames:
      - calico-node
    verbs:
      - create
  # Calico monitors various CRDs for config.
  - apiGroups: ["crd.projectcalico.org"]
    resources:
      - globalfelixconfigs
      - felixconfigurations
      - bgppeers
      - globalbgpconfigs
      - bgpconfigurations
      - ippools
      - ipamblocks
      - globalnetworkpolicies
      - globalnetworksets
      - networkpolicies
      - networksets
      - clusterinformations
      - hostendpoints
      - blockaffinities
    verbs:
      - get
      - list
      - watch
  # Calico must create and update some CRDs on startup.
  - apiGroups: ["crd.projectcalico.org"]
    resources:
      - ippools
      - felixconfigurations
      - clusterinformations
    verbs:
      - create
      - update
  # Calico stores some configuration information on the node.
  - apiGroups: [""]
    resources:
      - nodes
    verbs:
      - get
      - list
      - watch
  # These permissions are required for Calico CNI to perform IPAM allocations.
  - apiGroups: ["crd.projectcalico.org"]
    resources:
      - blockaffinities
      - ipamblocks
      - ipamhandles
    verbs:
      - get
      - list
      - create
      - update
      - delete
  - apiGroups: ["crd.projectcalico.org"]
    resources:
      - ipamconfigs
    verbs:
      - get
  # Block affinities must also be watchable by confd for route aggregation.
  - apiGroups: ["crd.projectcalico.org"]
    resources:
      - blockaffinities
    verbs:
      - watch
EOF
```

Bind the cluster role to the calico-node ServiceAccount
```
kubectl create clusterrolebinding calico-node --clusterrole=calico-node --serviceaccount=kube-system:calico-node
```



* Install daemon set

Change to home directory.
```
cd ~
```

`calico/node` runs as a daemon set so that it is installed on every node in the cluster.

Change `image: calico/node:v3.20.0` to right version. 

Create the daemon set
```
kubectl apply -f - <<EOF
kind: DaemonSet
apiVersion: apps/v1
metadata:
  name: calico-node
  namespace: kube-system
  labels:
    k8s-app: calico-node
spec:
  selector:
    matchLabels:
      k8s-app: calico-node
  updateStrategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
  template:
    metadata:
      labels:
        k8s-app: calico-node
    spec:
      nodeSelector:
        kubernetes.io/os: linux
      hostNetwork: true
      tolerations:
        # Make sure calico-node gets scheduled on all nodes.
        - effect: NoSchedule
          operator: Exists
        # Mark the pod as a critical add-on for rescheduling.
        - key: CriticalAddonsOnly
          operator: Exists
        - effect: NoExecute
          operator: Exists
      serviceAccountName: calico-node
      # Minimize downtime during a rolling upgrade or deletion; tell Kubernetes to do a "force
      # deletion": https://kubernetes.io/docs/concepts/workloads/pods/pod/#termination-of-pods.
      terminationGracePeriodSeconds: 0
      priorityClassName: system-node-critical
      containers:
        # Runs calico-node container on each Kubernetes node.  This
        # container programs network policy and routes on each
        # host.
        - name: calico-node
          image: calico/node:v3.20.0
          env:
            # Use Kubernetes API as the backing datastore.
            - name: DATASTORE_TYPE
              value: "kubernetes"
            - name: FELIX_TYPHAK8SSERVICENAME
              value: calico-typha
            # Wait for the datastore.
            - name: WAIT_FOR_DATASTORE
              value: "true"
            # Set based on the k8s node name.
            - name: NODENAME
              valueFrom:
                fieldRef:
                  fieldPath: spec.nodeName
            # Choose the backend to use.
            - name: CALICO_NETWORKING_BACKEND
              value: bird
            # Cluster type to identify the deployment type
            - name: CLUSTER_TYPE
              value: "k8s,bgp"
            # Auto-detect the BGP IP address.
            - name: IP
              value: "autodetect"
            # Disable file logging so kubectl logs works.
            - name: CALICO_DISABLE_FILE_LOGGING
              value: "true"
            # Set Felix endpoint to host default action to ACCEPT.
            - name: FELIX_DEFAULTENDPOINTTOHOSTACTION
              value: "ACCEPT"
            # Disable IPv6 on Kubernetes.
            - name: FELIX_IPV6SUPPORT
              value: "false"
            # Set Felix logging to "info"
            - name: FELIX_LOGSEVERITYSCREEN
              value: "info"
            - name: FELIX_HEALTHENABLED
              value: "true"
            # Location of the CA bundle Felix uses to authenticate Typha; volume mount
            - name: FELIX_TYPHACAFILE
              value: /calico-typha-ca/typhaca.crt
            # Common name on the Typha certificate; used to verify we are talking to an authentic typha
            - name: FELIX_TYPHACN
              value: calico-typha
            # Location of the client certificate for connecting to Typha; volume mount
            - name: FELIX_TYPHACERTFILE
              value: /calico-node-certs/calico-node.crt
            # Location of the client certificate key for connecting to Typha; volume mount
            - name: FELIX_TYPHAKEYFILE
              value: /calico-node-certs/calico-node.key
          securityContext:
            privileged: true
          resources:
            requests:
              cpu: 250m
          lifecycle:
            preStop:
              exec:
                command:
                - /bin/calico-node
                - -shutdown
          livenessProbe:
            httpGet:
              path: /liveness
              port: 9099
              host: localhost
            periodSeconds: 10
            initialDelaySeconds: 10
            failureThreshold: 6
          readinessProbe:
            exec:
              command:
              - /bin/calico-node
              - -bird-ready
              - -felix-ready
            periodSeconds: 10
          volumeMounts:
            - mountPath: /lib/modules
              name: lib-modules
              readOnly: true
            - mountPath: /run/xtables.lock
              name: xtables-lock
              readOnly: false
            - mountPath: /var/run/calico
              name: var-run-calico
              readOnly: false
            - mountPath: /var/lib/calico
              name: var-lib-calico
              readOnly: false
            - mountPath: /var/run/nodeagent
              name: policysync
            - mountPath: "/calico-typha-ca"
              name: calico-typha-ca
              readOnly: true
            - mountPath: /calico-node-certs
              name: calico-node-certs
              readOnly: true
      volumes:
        # Used by calico-node.
        - name: lib-modules
          hostPath:
            path: /lib/modules
        - name: var-run-calico
          hostPath:
            path: /var/run/calico
        - name: var-lib-calico
          hostPath:
            path: /var/lib/calico
        - name: xtables-lock
          hostPath:
            path: /run/xtables.lock
            type: FileOrCreate
        # Used to create per-pod Unix Domain Sockets
        - name: policysync
          hostPath:
            type: DirectoryOrCreate
            path: /var/run/nodeagent
        - name: calico-typha-ca
          configMap:
            name: calico-typha-ca
        - name: calico-node-certs
          secret:
            secretName: calico-node-certs
EOF
```

Verify that calico/node is running on each node in your cluster, and goes to Running within a few minutes.
```
kubectl get pod -l k8s-app=calico-node -n kube-system
```
Result looks like below.
```
NAME                READY   STATUS    RESTARTS   AGE
calico-node-4c4sp   1/1     Running   0          40s
calico-node-j2z6v   1/1     Running   0          40s
calico-node-vgm9n   1/1     Running   0          40s
```


#### Test networking

* Pod to pod pings

Create three busybox instances
```
kubectl create deployment pingtest --image=busybox --replicas=3 -- sleep infinity
```

Check their IP addresses
```
kubectl get pods --selector=app=pingtest --output=wide
```
Result
```
NAME                        READY   STATUS    RESTARTS   AGE   IP             NODE     NOMINATED NODE   READINESS GATES
pingtest-585b76c894-chwjq   1/1     Running   0          7s    10.244.31.1    cka002   <none>           <none>
pingtest-585b76c894-s2tbs   1/1     Running   0          7s    10.244.31.0    cka002   <none>           <none>
pingtest-585b76c894-vm9wn   1/1     Running   0          7s    10.244.28.64   cka003   <none>           <none>
```

Note the IP addresses of the second two pods, then exec into the first one. 
From inside the pod, ping the other two pod IP addresses. 
For example:
```
kubectl exec -ti pingtest-585b76c894-chwjq -- sh
/ # ping 10.244.31.1 -c 4
4 packets transmitted, 4 packets received, 0% packet loss

/ # ping 10.244.31.0 -c 4
4 packets transmitted, 4 packets received, 0% packet loss

/ # ping 10.244.28.64 -c 4
4 packets transmitted, 0 packets received, 100% packet loss
```


* Check routes

From one of the nodes, verify that routes exist to each of the pingtest pods’ IP addresses. For example
```
ip route get 10.244.31.1
ip route get 10.244.31.0
ip route get 10.244.28.64
```
Result
```
10.244.31.1 via 172.16.18.253 dev eth0 src 172.16.18.170 uid 0 
    cache 

10.244.31.0 via 172.16.18.253 dev eth0 src 172.16.18.170 uid 0 
    cache 

10.244.28.64 via 172.16.18.253 dev eth0 src 172.16.18.170 uid 0 
    cache 
```

The via `172.16.18.170`(it's control-plane) in this example indicates the next-hop for this pod IP, which matches the IP address of the node the pod is scheduled on, as expected.
IPAM allocations from different pools.

Recall that we created two IP pools, but left one disabled.
```
calicoctl get ippools -o wide
```
Result
```
NAME            CIDR              NAT    IPIPMODE   VXLANMODE   DISABLED   DISABLEBGPEXPORT   SELECTOR   
ipv4-ippool-1   10.244.0.0/18     true   Never      Never       false      false              all()      
ipv4-ippool-2   10.244.192.0/19   true   Never      Never       true       false              all()   
```

Enable the second pool.
```
calicoctl --allow-version-mismatch apply -f - <<EOF
apiVersion: projectcalico.org/v3
kind: IPPool
metadata:
  name: ipv4-ippool-2
spec:
  cidr: 10.244.192.0/19
  ipipMode: Never
  natOutgoing: true
  disabled: false
  nodeSelector: all()
EOF
```

```
calicoctl get ippools -o wide
```
Result
```
NAME            CIDR              NAT    IPIPMODE   VXLANMODE   DISABLED   DISABLEBGPEXPORT   SELECTOR   
ipv4-ippool-1   10.244.0.0/18     true   Never      Never       false      false              all()      
ipv4-ippool-2   10.244.192.0/19   true   Never      Never       false      false              all()      
```


Create a pod, explicitly requesting an address from pool2
```
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: pingtest-ippool-2
  annotations:
    cni.projectcalico.org/ipv4pools: "[\"ipv4-ippool-2\"]"
spec:
  containers:
  - args:
    - sleep
    - infinity
    image: busybox
    imagePullPolicy: Always
    name: pingtest
EOF
```

Verify it has an IP address from pool2
```
kubectl get pod pingtest-ippool-2 -o wide
```
Result
```
NAME                READY   STATUS    RESTARTS   AGE   IP               NODE     NOMINATED NODE   READINESS GATES
pingtest-ippool-2   1/1     Running   0          18s   10.244.203.192   cka003   <none>           <none>
```

Let's attach to the Pod `pingtest-585b76c894-chwjq` again.
```
kubectl exec -ti pingtest-585b76c894-chwjq -- sh
/ # 10.244.203.192 -c 4
4 packets transmitted, 0 packets received, 100% packet loss
```

!! Mark here. it's failed. Need further check why the route does not work.



Clean up
```
kubectl delete deployments.apps pingtest
kubectl delete pod pingtest-ippool-2
```





## Mini-practice


### Modify Existing Deployment

Scenario: 
> Update existing Deployment, e.g., add port number

Demo:

Create Deployment `nginx`.
```
kubectl create deployment nginx --image=nginx
```

Execute command below to get yaml template with port number.
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
Add below two lines to specify port number with `80` and protocol is `TCP`.
```
    spec:
      containers:
      - image: nginx
        imagePullPolicy: Always
        name: nginx
        ports:
        - containerPort: 80
          protocol: TCP
```


Use command `kubectl describe deployment <deployment_name>`, we can see the port number was added.
```
Pod Template:
  Labels:  app=nginx
  Containers:
   nginx:
    Image:        nginx
    Port:         80/TCP
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
    Port:           80/TCP
    Host Port:      0/TCP
    State:          Running
      Started:      Sun, 24 Jul 2022 22:50:12 +0800
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-hftdt (ro)
```




### Service Internal Traffic Policy

Scenario: 
> * Simulate how Service Internal Traffic Policy works.
> * Expected result:
>     * With setting Service `internalTrafficPolicy: Local`, the Service only route internal traffic within the nodes that Pods are running. 

Backgroud:

Service Internal Traffic Policy enables internal traffic restrictions to only route internal traffic to endpoints within the node the traffic originated from. 

The "internal" traffic here refers to traffic originated from Pods in the current cluster.

By setting its `.spec.internalTrafficPolicy` to Local. This tells kube-proxy to only use node local endpoints for cluster internal traffic.

For pods on nodes with no endpoints for a given Service, the Service behaves as if it has zero endpoints (for Pods on this node) even if the service does have endpoints on other nodes.

Demo:

Create Deployment `my-nginx` and Service `my-nginx`.
```
kubectl apply -f - << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-nginx
spec:
  selector:
    matchLabels:
      run: my-nginx
  replicas: 1
  template:
    metadata:
      labels:
        run: my-nginx
    spec:
      containers:
      - name: my-nginx
        image: nginx
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: my-nginx
  labels:
    run: my-nginx
spec:
  ports:
  - port: 80
    protocol: TCP
  selector:
    run: my-nginx
EOF
```

With command `kubectl get pod -o wide`, we know the Pod of Deployment `my-nginx` is running on node `cka003`.
```
NAME                                      READY   STATUS    RESTARTS   AGE     IP              NODE     NOMINATED NODE   READINESS GATES
my-nginx-cf54cdbf7-bscf8                  1/1     Running   0          9h      10.244.112.63   cka002   <none>           <none>
```

Let's send http request from `cka001` to the Pod on `cka002`. 
We will receive `Welcome to nginx!` information, which means the Pod is accessable from other nodes.
```
curl 11.244.163.60
```

Let's modify the Serivce `my-nginx` and specify `internalTrafficPolicy: Local`. 
```
kubectl apply -f - << EOF
apiVersion: v1
kind: Service
metadata:
  name: my-nginx
  labels:
    run: my-nginx
spec:
  ports:
  - port: 80
    protocol: TCP
  selector:
    run: my-nginx
  internalTrafficPolicy: Local
EOF
```

Let's send http request from `cka001` to the http request to the Pod again. 
We will receive `curl: (7) Failed to connect to 11.244.163.60 port 80: Connection refused` error information.
```
curl 11.244.163.60
```

Let's log onto `cka002` and the http request to the Pod again. 
We will receive `Welcome to nginx!` information, 
```
curl 11.244.163.60
```

Conclution:

With setting Service `internalTrafficPolicy: Local`, the Service only route internal traffic within the nodes that Pods are running. 






### ClusterRole and ServiceAccount

Scenario: 
> * Create a ClusterRole, which is authorized to create Deployment, StatefulSet, DaemonSet.
> * Bind the ClusterRole to a ServiceAccount.

Demo:

```
kubectl create namespace my-namespace

kubectl -n my-namespace create serviceaccount my-sa

kubectl create clusterrole my-clusterrole --verb=create --resource=deployments,statefulsets,daemonsets

kubectl -n my-namespace create rolebinding my-clusterrolebinding --clusterrole=my-clusterrole --serviceaccount=my-namespace:my-sa
```

Hints:

    1. A RoleBinding may reference any Role in the same namespace. 
    2. A RoleBinding can reference a ClusterRole and bind that ClusterRole to the namespace of the RoleBinding. 
    3. If you want to bind a ClusterRole to all the namespaces in your cluster, you use a ClusterRoleBinding.
    4. Use RoleBinding to bind ClusterRole is to reuse the ClusterRole for namespaced resources, avoid duplicated namespaced roles for same authorization.
    

Clean up.
```
kubectl delete namespace my-namespace 
kubectl delete clusterrole my-clusterrole
```


### Drain a Node

Scenario:
> Drain the node `cka003`

Demo:

Get list of Pods running.
```
kubectl get pod -o wide
```

We know that a Pod is running on `cka003`.
```
NAME                                      READY   STATUS    RESTARTS   AGE   IP             NODE     NOMINATED NODE   READINESS GATES
nfs-client-provisioner-86d7fb78b6-xk8nw   1/1     Running   0          22h   10.244.102.3   cka003   <none>           <none>
```

Evict node `cka003`.
```
kubectl drain cka003 --ignore-daemonsets --delete-emptydir-data --force
```
Output looks like below.
```
node/cka003 cordoned
WARNING: ignoring DaemonSet-managed Pods: kube-system/calico-node-tr22l, kube-system/kube-proxy-g76kg
evicting pod dev/nfs-client-provisioner-86d7fb78b6-xk8nw
evicting pod cka/cka-demo-64f88f7f46-dkxmk
pod/nfs-client-provisioner-86d7fb78b6-xk8nw evicted
pod/cka-demo-64f88f7f46-dkxmk evicted
node/cka003 drained
```

Check pod status again.
```
kubectl get pod -o wide
```
The pod is running on `cka002` now.
```
NAME                                      READY   STATUS    RESTARTS   AGE     IP             NODE     NOMINATED NODE   READINESS GATES
nfs-client-provisioner-86d7fb78b6-k8xnl   1/1     Running   0          2m20s   10.244.112.4   cka002   <none>           <none>
```


Notes:
> * `cordon` is included in `drain`, no need additional step to `cordon` node before `drain` node. 




### Upgrade

Scenario:
> Upgrade `kubeadm`, `kubectl`, `kubelet`.

Demo:

Reference link: `https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/`.

Control Plane
```
kubectl get node -owide
kubectl drain cka001 --ignore-daemonsets 
kubectl get node -owide
apt policy kubeadm
apt-get -y install kubeadm=1.24.0-00 --allow-downgrades
kubeadm upgrade plan
kubeadm upgrade apply v1.24.0
# kubeadm upgrade apply v1.24.0 --etcd-upgrade=false
apt-get -y install kubelet=1.24.0-00 kubectl=1.24.0-00 --allow-downgrades
systemctl daemon-reload
systemctl restart kubelet
kubectl get node
kubectl uncordon cka001
```

Worker Node
```
# On Control Plane
kubectl drain cka002 --ignore-daemonsets

$ On Workder Node
apt-get -y install kubeadm=1.24.1-00 --allow-downgrades
kubeadm upgrade node
apt-get -y install kubelet=1.24.1-00 --allow-downgrades
systemctl daemon-reload
systemctl restart kubelet
kubectl uncordon cka002
```

Worker Node
```
# On Control Plane
kubectl drain cka003 --ignore-daemonsets

$ On Workder Node
apt-get -y install kubeadm=1.24.1-00 --allow-downgrades
kubeadm upgrade node
apt-get -y install kubelet=1.24.1-00 --allow-downgrades
systemctl daemon-reload
systemctl restart kubelet
kubectl uncordon cka003
```


### etcd Snapshot

Scenario:
> * Backup etcd to `/opt/backup/snapshot-backup.db`.
> * Restore etcd from `/opt/backup/snapshot-backup.db`.

Demo:

Get Control Plan Node information.
```
kubectl get node -o wide
```

Backup
```
etcdctl \
--endpoints=172.16.18.170:2379 \
--cert=/etc/kubernetes/pki/etcd/server.crt \
--key=/etc/kubernetes/pki/etcd/server.key \
--cacert=/etc/kubernetes/pki/etcd/ca.crt \
snapshot save /opt/backup/snapshot-backup.db
```

Restore
```
etcdctl  \
--endpoints=172.16.18.170:2379 \
--cert=/etc/kubernetes/pki/etcd/server.crt \
--key=/etc/kubernetes/pki/etcd/server.key \
--cacert=/etc/kubernetes/pki/etcd/ca.crt \
snapshot restore /opt/backup/snapshot-backup.db
```





### NetworkPolicy

Scenario: Ingress:
> * Create two namespaces `my-ns-1`, `my-ns-2`.
> * Create two deployments on `my-ns-1`, `nginx` listens to port `80` and `tomcat` listens to port `8080`.
> * Create NetworkPolicy `my-networkpolicy-1` on namespace `my-ns-1` to allow access to port 8080 from namespace `my-ns-1`.
> * Verify the access to `nginx` port `80` and `tomcat` port `8080`.
> * Edit the NetworkPolicy to allow access to port 8080 from namespace `my-ns-2`.
> * Verify the access to `nginx` port `80` and `tomcat` port `8080`.

Demo:

Create namespaces
```
kubectl create namespace my-ns-1
kubectl create namespace my-ns-2
```

Create deployment on `my-ns-1`
```
kubectl create deployment my-nginx --image=nginx --namespace=my-ns-1 --port=80
kubectl create deployment my-tomcat --image=tomcat --namespace=my-ns-1 --port=8080
```

Get the label: e.g., `kubernetes.io/metadata.name=my-ns-1`, `kubernetes.io/metadata.name=my-ns-2`.
```
kubectl get namespace my-ns-1 --show-labels  
kubectl get namespace my-ns-2 --show-labels   
```

Create NetworkPolicy to allow access from my-ns-2 to Pod with port 8080 on my-ns-1.
Refer to yaml template from the link https://kubernetes.io/docs/concepts/services-networking/network-policies/.
```
kubectl apply -f - << EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: my-networkpolicy-1
  namespace: my-ns-1
spec:
  podSelector:
    matchLabels: {}
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: my-ns-1
      ports:
        - protocol: TCP
          port: 8080
EOF
```

Check Deployment and Pod status
```
kubectl get deployment,pod -n my-ns-1 -o wide
```

Create temp pod on namespace `my-ns-1`.
Attach to the pod and verify the access. 
Command `curl <nginx_ip>:80` failed. 
Command `curl <tomcat_ip>:80` succeed. 
```
kubectl run centos --image=centos -n my-ns-1 -- "/bin/sh" "-c" "sleep 3600"
kubectl exec -it mycentos -n my-ns-1 -- bash
```

Create temp pod on namespace `my-ns-2`.
Attach to the pod and verify the access. 
Command `curl <nginx_ip>:80` failed. 
Command `curl <tomcat_ip>:80` failed. 
```
kubectl run centos --image=centos -n my-ns-2 -- "/bin/sh" "-c" "sleep 3600"
kubectl exec -it mycentos -n my-ns-2 -- bash
```

Edit `my-networkpolicy-1` to change `ingress.from.namespaceSelector.matchLabels` to `my-ns-2`.

Attach to temp pod on namespace `my-ns-2`.
Verify the access. 
Command `curl <nginx_ip>:80` failed. 
Command `curl <tomcat_ip>:80` succeed. 
```
kubectl exec -it mycentos -n my-ns-2 -- bash
```


Clean up:
```
kubectl delete namespace my-ns-1
kubectl delete namespace my-ns-2
```





### Expose Service

Scenario:
> * Create a `nginx` deployment
> * Add port number and alias name of the `nginx` Pod.
> * Expose the deployment with internal traffic to local only.


Demo:

Create deployment `my-nginx` with port number `80`.
```
kubectl create deployment my-nginx --image=nginx --port=80
```

Edit deployment.
```
kubectl edit deployment my-nginx
```
Add port alias name `http`.
Refer to the link for deployment yaml template https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
```
    spec:
      containers:
      - image: nginx
        imagePullPolicy: Always
        name: nginx
        ports:
        - containerPort: 80
          protocol: TCP
          name: http
```

Expose the deployment with `NodePort` type.
```
kubectl expose deployment my-nginx --port=80 --target-port=http --name=my-nginx-svc --type=NodePort
```

Edit the service. Change `internalTrafficPolicy` from `Cluster` to `Local`.
```
kubectl edit svc my-nginx-svc 
```

Verify the access. Note, the pod is running on node `cka003`. We will see below expected results.
```
curl <deployment_pod_ip>:80    # succeed on node cka003. internalTrafficPolicy is effective.
curl <service_cluster_ip>:80   # succeed on all nodes.
curl <node_ip>:<ext_port>      # succeed on all nodes.
```




### Ingress

Scenario:
> * Create Deployment `nginx` on new namespace `my-ns`.
> * Expose the deployment with Service name `my-nginx-svc` and service port `3456`
> * Create Ingress with to expose the service on path `/test`.
> * Verify the http access to `<ingress_ip><your_path>` instead of `<ip><port>`.


Demo:

Create namespace, deployment, and service.
```
kubectl create namespace my-ns
kubectl create deployment my-nginx --image=nginx --port=80 --namespace=my-ns
kubectl expose deployment my-nginx --name=my-nginx-svc --port=3456 --target-port=80 --namespace=my-ns
```

```
kubectl patch ingressclass nginx -p '{"metadata": {"annotations":{"ingressclass.kubernetes.io/is-default-class": "true"}}}'
```

Create Ingress on new namespace.
Refer to the Ingress yaml template via link https://kubernetes.io/zh-cn/docs/concepts/services-networking/ingress/
```
kubectl apply -f - << EOF
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
  namespace: my-ns
  annotations:
    kubernetes.io/ingressclass: nginx
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  # ingressClassName: nginx
  rules:
  - http:
      paths:
      - path: /test
        pathType: Prefix
        backend:
          service:
            name: my-nginx-svc
            port:
              number: 3456
EOF
```

Get the IP address via and test the access.
```
kubectl get ingress -n my-ns
curl 10.110.175.39/test
```



Clean up.
```
kubectl delete namespace my-ns
```



### Schedule Pod to Node

Scenario:
> * Label a node
> * Create a Pod and assign it to the node by nodeSelector


Demo:

Label node.
```
kubectl label node cka003 disk=ssd
```

Create Pod with name `my-nginx` and set `nodeSelector` as `disk=ssd` and set container name `my-nginx`.
Get Pod template via the link https://kubernetes.io/docs/tasks/configure-pod-container/assign-pods-nodes/
```
kubectl apply -f - << EOF
apiVersion: v1
kind: Pod
metadata:
  name: my-nginx
  labels:
    env: demo
spec:
  containers:
  - name: my-nginx
    image: nginx
    imagePullPolicy: IfNotPresent
  nodeSelector:
    disk: ssd
EOF
```


Clean up
```
kubectl label node cka003 disk-
kubectl delete pod my-nginx
```







### Check Available Node

Scenario:
> * Check available Node

Option 1:
```
kubectl describe node | grep -i taint
```
Manual check the result, here it's `2` nodes are available
```
Taints:             node-role.kubernetes.io/control-plane:NoSchedule
Taints:             <none>
Taints:             <none>
```

Option 2:
```
kubectl describe node | grep -i taint |grep -vc NoSchedule
```
We will get same result `2`. Here `-v` means exclude, `-c` count numbers.





### Multiple Containers

Scenario:
> * Create multiple container Pod.


Get yaml template with below command.
```
kubectl run my-pod --image=nginx --dry-run=client -o yaml
```

Add more containers in the template we get from above command.
```
kubectl apply -f - << EOF
apiVersion: v1
kind: Pod
metadata:
  name: my-multi-pod
spec:
  containers:
  - image: nginx
    name: nginx
  - image: memcached
    name: memcached
  - image: redis
    name: redis
EOF
```




### PV+SC+PVC+Pod

Scenario: 
> Refer to sample codes from [Kubernetes Documentation](https://kubernetes.io/docs/home/) to complete below tasks:
>   
> * Create PV
>>    * name is `my-pv-volume`
>>    * `hostPath` type
>>    * location is `/my-data`
>>    * size 1Gi
>>    * AccessMode `ReadWriteMany`
>>    * StorageClass is `my-sc`
> * Create PVC and bind it to the PV
>>    * name is `my-pv-claim`
>>    * capacity 10Mi
>>    * consume StorageClass `my-sc`
>>    * AccessMode `ReadWriteOnce`
> * Create Pod to mount the PVC.
>>    * name `my-pv-storage`
>>    * consume PVC `my-pv-claim`
> * Mount new volume with emptyDir type to the Pod.

Demo: 

Search `Create a PersistentVolume` in [Kubernetes Documentation](https://kubernetes.io/docs/home/).

Choose [Configure a Pod to Use a PersistentVolume for Storage](https://kubernetes.io/docs/tasks/configure-pod-container/configure-persistent-volume-storage/)

With sample codes we get from above link, let's complete these demo tasks.

Task 1: create a PV.
```
kubectl apply -f - << EOF
apiVersion: v1
kind: PersistentVolume
metadata:
  name: my-pv-volume
spec:
  storageClassName: my-sc
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/my-data"
EOF
```

Task 2: create PVC.
```
kubectl apply -f - << EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pv-claim
spec:
  storageClassName: my-sc
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Mi
EOF
```


Task 3: create Pod.
```
kubectl apply -f - << EOF
apiVersion: v1
kind: Pod
metadata:
  name: my-pv-pod
spec:
  volumes:
    - name: my-pv-storage
      persistentVolumeClaim:
        claimName: my-pv-claim
  containers:
    - name: my-pv-container
      image: nginx
      ports:
        - containerPort: 80
          name: "http-server"
      volumeMounts:
        - mountPath: "/usr/share/nginx/html"
          name: my-pv-storage
EOF
```

Attach to the Pod and create `index.html` file in directory `/usr/share/nginx/html/`.
```
kubectl exec -it my-pv-pod -- bash
root@task-pv-pod:/usr/share/nginx/html# echo "Hello Nginx" > index.html
```

We can see the file `index.html` in directory `/cka-data/` on node `cka003`, which the Pod is running on.


Task 4: Update Pod to mount new volume with emptyDir type.

Search `Create a PersistentVolume` in [Kubernetes Documentation](https://kubernetes.io/docs/home/).

Get sampe code of [emptydir](https://kubernetes.io/docs/concepts/storage/volumes/#emptydir).

Update the Pod `task-pv-pod` and mount new volume `mnt-volume` with emptyDir type.
```
kubectl apply -f - << EOF
apiVersion: v1
kind: Pod
metadata:
  name: my-pv-pod
spec:
  volumes:
    - name: my-pv-storage
      persistentVolumeClaim:
        claimName: my-pv-claim
    - name: mnt-volume
      emptyDir: {}
  containers:
    - name: my-pv-container
      image: nginx
      ports:
        - containerPort: 80
          name: "http-server"
      volumeMounts:
        - mountPath: "/usr/share/nginx/html"
          name: my-pv-storage
        - mountPath: "/mnt"
          name: mnt-volume
EOF
```


Clean up.
```
kubectl delete pod my-pv-pod 
kubectl delete pvc 
kubectl delete pvc my-pv-claim  
kubectl delete pv my-pv-volume 
rm -rf my-data/
```



### Sidecar

Scenario: 



Create a Pod `my-busybox` with multiple container `container-1-busybox`.
```
kubectl apply -f - << EOF
apiVersion: v1
kind: Pod
metadata:
  name: my-busybox
spec:
  containers:
  - name: container-1-busybox
    image: busybox
    args:
    - /bin/sh
    - -c
    - >
      i=0;
      while true;
      do
        echo "Hello message from container-1: $i" >> /var/log/my-pod-busybox.log;
        i=$((i+1));
        sleep 1;
      done
EOF
```

Search `emptyDir` in the Kubernetes documetation.
Refer to below template for emptyDir via https://kubernetes.io/zh-cn/docs/concepts/storage/volumes/

Add below new features into the Pod

* Volume:
    * volume name: `logfile`
    * type: `emptyDir`
* Update existing container:
    * name: `container-1-busybox`
    * volumeMounts
        * name: `logfile`
        * mounthPath: `/var/log`
* Add new container:
    * name: `container-2-busybox`
    * image: busybox
    * args: ['/bin/sh', '-c', 'tail -n+1 -f /var/log/my-pod-busybox.log']
    * volumeMounts:
        * name: `logfile`
        * mountPath: `/var/log`
```
kubectl get pod my-busybox -o yaml > my-busybox.yaml
vi my-busybox.yaml
kubectl delete pod my-busybox 
kubectl apply -f my-busybox.yaml
kubectl logs my-busybox -c container-2-busybox
```


The final file `my-busybox.yaml` looks like below.
```
apiVersion: v1
kind: Pod
metadata:
  annotations:
    cni.projectcalico.org/containerID: 89644b6b073cd152f94b4cae7bdea6bbc3292cf59afd4f28102bd74f0205c9e4
    cni.projectcalico.org/podIP: 10.244.102.20/32
    cni.projectcalico.org/podIPs: 10.244.102.20/32
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"v1","kind":"Pod","metadata":{"annotations":{},"name":"my-busybox","namespace":"dev"},"spec":{"containers":[{"args":["/bin/sh","-c","i=0; while true; do\n  echo \"Hello message from container-1: \" \u003e\u003e /var/log/my-pod-busybox.log;\n  i=1;\n  sleep 1;\ndone\n"],"image":"busybox","name":"container-1-busybox"}]}}
  creationTimestamp: "2022-07-29T22:58:27Z"
  name: my-busybox
  namespace: dev
  resourceVersion: "1185720"
  uid: c5e62a16-4459-4828-a441-7d1471b89a56
spec:
  containers:
  - name: container-2-busybox
    image: busybox
    args: ['/bin/sh', '-c', 'tail -n+1 -f /var/log/my-pod-busybox.log']
    volumeMounts:
    - name: logfile
      mountPath: /var/log
  - args:
    - /bin/sh
    - -c
    - |
      i=0; while true; do
        echo "Hello message from container-1: $i" >> /var/log/my-pod-busybox.log;
        i=1;
        sleep 1;
      done
    image: busybox
    imagePullPolicy: Always
    name: container-1-busybox
    resources: {}
    terminationMessagePath: /dev/termination-log
    terminationMessagePolicy: File
    volumeMounts:
    - name: logfile
      mountPath: /var/log
    - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
      name: kube-api-access-mhxlf
      readOnly: true
  dnsPolicy: ClusterFirst
  enableServiceLinks: true
  nodeName: cka003
  preemptionPolicy: PreemptLowerPriority
  priority: 0
  restartPolicy: Always
  schedulerName: default-scheduler
  securityContext: {}
  serviceAccount: default
  serviceAccountName: default
  terminationGracePeriodSeconds: 30
  tolerations:
  - effect: NoExecute
    key: node.kubernetes.io/not-ready
    operator: Exists
    tolerationSeconds: 300
  - effect: NoExecute
    key: node.kubernetes.io/unreachable
    operator: Exists
    tolerationSeconds: 300
  volumes:
  - name: logfile
    emptyDir: {}
  - name: kube-api-access-mhxlf
    projected:
      defaultMode: 420
      sources:
      - serviceAccountToken:
          expirationSeconds: 3607
          path: token
      - configMap:
          items:
          - key: ca.crt
            path: ca.crt
          name: kube-root-ca.crt
      - downwardAPI:
          items:
          - fieldRef:
              apiVersion: v1
              fieldPath: metadata.namespace
            path: namespace
status:
  conditions:
  - lastProbeTime: null
    lastTransitionTime: "2022-07-29T22:58:27Z"
    status: "True"
    type: Initialized
  - lastProbeTime: null
    lastTransitionTime: "2022-07-29T22:58:30Z"
    status: "True"
    type: Ready
  - lastProbeTime: null
    lastTransitionTime: "2022-07-29T22:58:30Z"
    status: "True"
    type: ContainersReady
  - lastProbeTime: null
    lastTransitionTime: "2022-07-29T22:58:27Z"
    status: "True"
    type: PodScheduled
  containerStatuses:
  - containerID: containerd://fd42d4ba4d94d8918d8846327b1db2328be13c5f93f381877ff0228ed7b5468d
    image: docker.io/library/busybox:latest
    imageID: docker.io/library/busybox@sha256:0e97a8ca6955f22dbc7db9e9dbe970971f423541e52c34b8cb96ccc88d6a3883
    lastState: {}
    name: container-1-busybox
    ready: true
    restartCount: 0
    started: true
    state:
      running:
        startedAt: "2022-07-29T22:58:30Z"
  hostIP: 172.16.18.168
  phase: Running
  podIP: 10.244.102.20
  podIPs:
  - ip: 10.244.102.20
  qosClass: BestEffort
  startTime: "2022-07-29T22:58:27Z"
```


Clean up:
```
kubectl delete pod my-busybox
```






### Monitoring

Scenario: 
> * Find out top pod consuming CPU


Use option `--sort-by` to get top CPU workload
```
kubectl top pod --sort-by cpu -A
```






### Node NotReady

Scenario: 
> When we stop `kubelet` service on worker node `cka002`,

> * What's the status of each node?
> * What's containers changed via command `nerdctl`?
> * What's pods status via command `kubectl get pod -owide -A`? 

Demo:

Execute command `systemctl stop kubelet.service` on `cka002`.

Execute command `kubectl get node` on either `cka001` or `cka003`, the status of `cka002` is `NotReady`.

Execute command `nerdctl -n k8s.io container ls` on `cka002` and we can observe all containers are still up and running, including the pod `my-first-pod`.

Execute command `systemctl start kubelet.service` on `cka002`.


Conclusion:

* The node status is changed to `NotReady` from `Ready`.
* For those DaemonSet pods, like `calico`、`kube-proxy`, are exclusively running on each node. They won't be terminated after `kubelet` is down.
* The status of pod `my-first-pod` keeps showing `Terminating` on each node because status can not be synced to other nodes via `apiserver` from `cka002` because `kubelet` is down.
* The status of pod is marked by `controller` and recycled by `kubelet`.
* When we start kubelet service on `cka003`, the pod `my-first-pod` will be termiated completely on `cka002`.

In addition, let's create a deployment with 3 replicas. Two are running on `cka003` and one is running on `cka002`.
```
root@cka001:~# kubectl get pod -o wide -w
NAME                               READY   STATUS    RESTARTS   AGE    IP           NODE     NOMINATED NODE   READINESS GATES
nginx-deployment-9d745469b-2xdk4   1/1     Running   0          2m8s   10.244.2.3   cka003   <none>           <none>
nginx-deployment-9d745469b-4gvmr   1/1     Running   0          2m8s   10.244.2.4   cka003   <none>           <none>
nginx-deployment-9d745469b-5j927   1/1     Running   0          2m8s   10.244.1.3   cka002   <none>           <none>
```
After we stop kubelet service on `cka003`, the two running on `cka003` are terminated and another two are created and running on `cka002` automatically. 











