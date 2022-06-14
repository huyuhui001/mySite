# Tutorials: SAP BTP trail account

## kubectl basics

Register account of [SAP BTP trail system](https://account.hanatrial.ondemand.com/). I am using BTP Kyma runtime for the demo.

Choose the entitlements for `k8sdev` subdomain:

* Alert Notification: Standard plan
* Continuous Integration & Delivery: default (Application) or the trial (Application) or free (Application) plans which are not charged
* Kyma runtime: any available plan in the list (trial and free are not charged)
* Launchpad Service: standard (Application) or free (Application)
* SAP HANA Cloud: hana
* SAP HANA Schemas & HDI Containers: hdi-shared

Enable Kyma runtime in `k8sdev` subdomain, and download kubeconfig file to local directory `~/.kube/` and rename it to `~/.kube/config-btp-kyma.yaml`. 
If the directory `~/.kube/` does not exist, create it.

Add below line into file `/etc/profile.local` and make it effected by command `source /etc/profile.local`.
```
export KUBECONFIG=$HOME/.kube/config-btp-kyma.yaml
```

### Check current kubeconfig file.

Use the `kubectl config` command to get current context of configuration file.
```
james@lizard:~> echo $KUBECONFIG
/home/james/.kube/config-btp-kyma.yaml

james@lizard:~> kubectl config view

james@lizard:~> kubectl config get-contexts
CURRENT   NAME                   CLUSTER                AUTHINFO               NAMESPACE
*         shoot--kyma--eb68ebe   shoot--kyma--eb68ebe   shoot--kyma--eb68ebe  
```

Using SAP BTP, `brew` and `oidc-login` need to be installed.

Install `krew` (https://krew.sigs.k8s.io/docs/user-guide/setup/install/)

james@lizard:~> (
  set -x; cd "$(mktemp -d)" &&
  OS="$(uname | tr '[:upper:]' '[:lower:]')" &&
  ARCH="$(uname -m | sed -e 's/x86_64/amd64/' -e 's/\(arm\)\(64\)\?.*/\1\2/' -e 's/aarch64$/arm64/')" &&
  KREW="krew-${OS}_${ARCH}" &&
  curl -fsSLO "https://github.com/kubernetes-sigs/krew/releases/latest/download/${KREW}.tar.gz" &&
  tar zxvf "${KREW}.tar.gz" &&
  ./"${KREW}" install krew
)

Append below two lines to file `/etc/profile.local` make it effected by command `source /etc/profile.local`
```
export PATH=$HOME/.krew/bin:$PATH
```

Install oidc-login (https://github.com/int128/kubelogin#setup) . 
```
james@lizard:~> kubectl krew install oidc-login
```

### Check the nodes

Use the `kubectl get nodes` command to get the basic information about the clusters' nodes. 
There will be a pop-up web page for authentication with registered email address and password.
More information can be found by appending --help to command.
```
james@lizard:~> kubectl get nodes
NAME                          STATUS   ROLES    AGE   VERSION
ip-10-250-0-53.ec2.internal   Ready    <none>   47m   v1.21.10
```

Get nodes information with different format output, e.g., yaml format.
```
james@lizard:~> kubectl get nodes -o yaml
```


Get detailed information about a node by running `kubectl describe node <node-name>` or `kubectl get node <node-name>.`.
```
james@lizard:~> kubectl get nodes ip-10-250-0-53.ec2.internal
NAME                          STATUS   ROLES    AGE   VERSION
ip-10-250-0-53.ec2.internal   Ready    <none>   53m   v1.21.10

james@lizard:~> kubectl get nodes ip-10-250-0-53.ec2.internal -o wide
NAME                          STATUS   ROLES    AGE   VERSION    INTERNAL-IP   EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION                CONTAINER-RUNTIME
ip-10-250-0-53.ec2.internal   Ready    <none>   56m   v1.21.10   10.250.0.53   <none>        Garden Linux 576.8   5.10.109-garden-cloud-amd64   docker://20.10.11+dfsg1

james@lizard:~> kubectl get nodes ip-10-250-0-53.ec2.internal -o yaml
james@lizard:~> kubectl get nodes ip-10-250-0-53.ec2.internal -o json

james@lizard:~> kubectl describe nodes ip-10-250-0-53.ec2.internal
```

Get namespaces information by running `kubectl get namespaces`.
```
james@lizard:~> kubectl get namespaces
NAME               STATUS   AGE
compass-system     Active   58m
default            Active   62m
istio-system       Active   55m
kube-node-lease    Active   62m
kube-public        Active   62m
kube-system        Active   62m
kyma-integration   Active   52m
kyma-system        Active   55m

```

Get running pods under specific namespace by running `kubectl get pods -n <namespace>`.
```
james@lizard:~> kubectl get pods
james@lizard:~> kubectl get pods -n kube-system
```


### Check the proxy

We can use `kubectl proxy` command to open a tunnel to the API server and make it available locally - usually on localhost:8001 / 127.0.0.1:8001. 
When I want to explore the API, this is an easy way to gain access.

Run the command `kubectl proxy &` and open `http://localhost:8001/api/v1` in browser.
Just opening `http://localhost:8001` will return an error because we are only allowed to access certain parts of the API. Hence the API path is important

```
james@lizard:~> kubectl proxy &
[1] 102358
james@lizard:~> Starting to serve on 127.0.0.1:8001
```

Example, get available API groups and so on via below link:
```
http://127.0.0.1:8001/
http://127.0.0.1:8001/api/v1
http://127.0.0.1:8001/api/v1/namespaces
http://127.0.0.1:8001/api/v1/namespaces/default
http://127.0.0.1:8001/api/v1/namespaces/sock-shop/pods
```


### Check api-versions & api-resources

Get an overview of existing APIs by running `kubectl api-versions` and `kubectl api-resources`.

```
james@lizard:~> kubectl api-resources -o wide
james@lizard:~> kubectl api-versions
```

Namespace is a cluster, which includes services. Service may be on a node, may be not. 














```
Step 5: talk to kubernetes like an application
If you access kubernetes as an application rather than an administrator, you cannot use the convenient syntax of kubectl. 
Instead you have to send HTTP requests to the cluster. 
Though there are client libraries available, in the end everything boils down to an HTTP request. 
In this step of the exercise, you will send an HTTP request directly to the cluster asking for the available nodes. 
Instead of kubectl you can use the program curl.

To figure out, how kubectl converts your query into HTTP requests, run the command from step 1 again and add a -v=9 flag to it. 
This increases the verbosity of kubectl drastically, showing you all the information you need. 
Go through the command's output and find the correct curl request.

Before you continue, make sure kubectl proxy is running and serving on localhost:8001. 
Now modify the request to be send via the proxy. 
Since the proxy has already taken care of authentication, you can omit the bearer token in your request.

Hint: if the output is not as readable as you expect it, consider changing the accepted return format to application/yaml.



Step 6 (optional) - learn some tricks
There is a forum-like page hosted by K8s with lots of information around kubectl and how to use it best. 
If you are curious, take a look at https://discuss.kubernetes.io/t/kubectl-tips-and-tricks/.


Further information & references
	• Manage multiple clusters and multiple config files: https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/
	• kubectl command documentation: https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands
	• a small gist with bash function to manage multiple config files https://github.wdf.sap.corp/gist/D051945/3f3daf9f71f7e012c1e25a48c1c6e8da
	• shell autocompletion (should work for the VM already): https://kubernetes.io/docs/tasks/tools/install-kubectl/#enabling-shell-autocompletion
	• kubectl cheat sheet:(https://kubernetes.io/docs/reference/kubectl/cheatsheet/
jsonpath in kubectl: https://kubernetes.io/docs/reference/kubectl/jsonpath/
```

## Work on pod


```
Exercise 2 - create your first pod

In this exercise you will be dealing with Pods.
Now that you know, how kubectl works and what the smallest entity on kubernetes looks like, it is time to create your own pod.


Step 0: prepare a yaml file
In kubernetes all resources have a well-described schema that is documented in the API definition. 
For example, the Pod resource is defined by kind: Pod and contains a PodSpec, which has a Container, which has an Image, which specifies the docker image to use, when running the pod.

In this step you are going to describe a pod in a yaml file (pod.yaml). Take the skeleton listed below and insert the field/values mentioned below at the right place.
    kind: Pod
    name: nginx-liveness-pod (metadata)
    image: nginx:mainline

Either check the official API reference of the pod resource for help or use kubectl explain pod to get a command-line based description of the resource. 
By appending .<field> to the resource type, the explain command will provide more details on the specified field (example: kubectl explain pod.spec).
apiVersion: v1
metadata:
spec:
  containers:
  - name: nginx
    ports:
    - containerPort: 80
      name: http-port
    livenessProbe:
      httpGet:
        path: /
        port: http-port
      initialDelaySeconds: 3
      periodSeconds: 30


Step 1: create the pod
Now tell the cluster that you would like it to schedule the pod for you. Send the file "pod.yaml" to the API server for further processing. 
You can try this directly or use the --dry-run=client flag, if you are not sure yet:
	kubectl apply -f pod.yaml --dry-run=server
	kubectl apply -f pod.yaml

If it does not work as expected, check the indentation and consult the API reference linked above. 
You can also use kubectl explain pod instead. 
To get more details about fields like spec simply append the field name with a "." like this: kubectl explain pod.spec


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG config view
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: DATA+OMITTED
    server: https://api.blr04.k8s-train.shoot.canary.k8s-hana.ondemand.com
  name: k8s-training
contexts:
- context:
    cluster: k8s-training
    namespace: part-0013
    user: participant
  name: training
current-context: training
kind: Config
preferences: {}
users:
- name: participant
  user:
    client-certificate-data: REDACTED
    client-key-data: REDACTED


Switch to part-0013 namespace 

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG config set-context training --cluster=k8s-training --namespace=part-0013 --user=participant
Context "training" modified.

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG config use-context training
Switched to context "training".

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG config get-contexts
CURRENT   NAME       CLUSTER        AUTHINFO      NAMESPACE
*         training   k8s-training   participant   part-0013

james@lizard:~> mkdir /opt/docker-k8s-training/kubernetes/ex02/

james@lizard:~> cp /opt/docker-k8s-training/kubernetes/demo/02a_simple_pod.yaml /opt/docker-k8s-training/kubernetes/ex02/

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG create -n part-0013 -f /opt/docker-k8s-training/kubernetes/ex02/02a_simple_pod.yaml
pod/my-first-pod created



Step 2: verify that the pod is running
Use kubectl with the get verb, to check, if your pod has been scheduled. It should be up and running after a few seconds. Check the cheat-sheet for help. 
Experiment with -o=yaml to modify the output. Compare the result with your local pod.yaml file. Can you spot the odd/differences?

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get pods
NAME           READY   STATUS    RESTARTS   AGE
my-first-pod   1/1     Running   0          20s


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get pods my-first-pod -owide
NAME           READY   STATUS    RESTARTS   AGE   IP             NODE                                                  NOMINATED NODE   READINESS GATES
my-first-pod   1/1     Running   0          58s   100.96.3.214   shoot--k8s-train--blr04-worker-gflpa-z1-7544c-cwm54   <none>           <none>





Step 3: get the logs
Use kubectl with the logs command and get the logs of your pod. Check the cheat-sheet for help. You should see the liveness probe requests coming in.

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG logs my-first-pod
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
2022/02/02 23:15:50 [notice] 1#1: using the "epoll" event method
2022/02/02 23:15:50 [notice] 1#1: nginx/1.21.5
2022/02/02 23:15:50 [notice] 1#1: built by gcc 10.2.1 20210110 (Debian 10.2.1-6)
2022/02/02 23:15:50 [notice] 1#1: OS: Linux 5.10.0-9-cloud-amd64
2022/02/02 23:15:50 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576
2022/02/02 23:15:50 [notice] 1#1: start worker processes
2022/02/02 23:15:50 [notice] 1#1: start worker process 32
2022/02/02 23:15:50 [notice] 1#1: start worker process 33
2022/02/02 23:15:50 [notice] 1#1: start worker process 34
2022/02/02 23:15:50 [notice] 1#1: start worker process 35



Step 4: exec into your pod
In case logs or describe or any other of the output generating commands don't help you to get to the root cause of an issue, you may want to take a look yourself. 
The exec command helps you in this situation. Adapt and run the following command, to open a shell session into the container running as part of the pod:
	kubectl exec -it <my-pod> -- bash


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG exec -it my-first-pod -- bash
.  ..  bin  boot  dev  docker-entrypoint.d  docker-entrypoint.sh  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
root@my-first-pod:/# exit


Step 4.1: labels your pods

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get pods
NAME           READY   STATUS    RESTARTS   AGE
my-first-pod   1/1     Running   0          5m25s

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get pods --show-labels
NAME           READY   STATUS    RESTARTS   AGE    LABELS
my-first-pod   1/1     Running   0          6m1s   <none>

Add two lables

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG label pod my-first-pod nginx=mainline
pod/my-first-pod labeled
james@lizard:~> kubectl --kubeconfig=$KUBECONFIG label pod my-first-pod env=training
pod/my-first-pod labeled
james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get pods --show-labels
NAME           READY   STATUS    RESTARTS   AGE     LABELS
my-first-pod   1/1     Running   0          6m47s   env=training,nginx=mainline

Search pods by labels

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get pods -l env=training
NAME           READY   STATUS    RESTARTS   AGE
my-first-pod   1/1     Running   0          7m30s
james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get pods -l env=class
No resources found in part-0013 namespace.

Remove a label

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG label pods my-first-pod env-
pod/my-first-pod unlabeled
james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get pods --show-labels
NAME           READY   STATUS    RESTARTS   AGE     LABELS
my-first-pod   1/1     Running   0          8m36s   nginx=mainline


We can do the same for nodes

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get nodes --show-labels
james@lizard:~> kubectl --kubeconfig=$KUBECONFIG label nodes shoot--k8s-train--blr04-worker-gflpa-z1-7544c-6jqvk env=training


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG describe pods my-first-pod
Name:         my-first-pod
Namespace:    part-0013
Priority:     0
Node:         shoot--k8s-train--blr04-worker-gflpa-z1-7544c-cwm54/10.250.0.5
Start Time:   Thu, 03 Feb 2022 07:15:49 +0800
Labels:       nginx=mainline
Annotations:  cni.projectcalico.org/podIP: 100.96.3.214/32
              cni.projectcalico.org/podIPs: 100.96.3.214/32
              kubernetes.io/limit-ranger: LimitRanger plugin set: cpu, memory request for container nginx; cpu, memory limit for container nginx
              kubernetes.io/psp: gardener.privileged
Status:       Running
IP:           100.96.3.214
IPs:
  IP:  100.96.3.214
Containers:
  nginx:
    Container ID:   containerd://50ea8046ff01d7a347b333a4403513279349f13b3bebf7d45ce1497584a61c90
    Image:          nginx:mainline
    Image ID:       docker.io/library/nginx@sha256:0d17b565c37bcbd895e9d92315a05c1c3c9a29f762b011a10c54a66cd53c9b31
    Port:           80/TCP
    Host Port:      0/TCP
    State:          Running
      Started:      Thu, 03 Feb 2022 07:15:50 +0800
    Ready:          True
    Restart Count:  0
    Limits:
      cpu:     500m
      memory:  300Mi
    Requests:
      cpu:     100m
      memory:  100Mi
    Environment:
      KUBERNETES_SERVICE_HOST:  api.blr04.k8s-train.internal.canary.k8s.ondemand.com
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-wmpgw (ro)
Conditions:
  Type              Status
  Initialized       True
  Ready             True
  ContainersReady   True
  PodScheduled      True
Volumes:
  kube-api-access-wmpgw:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
QoS Class:                   Burstable
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  14m   default-scheduler  Successfully assigned part-0013/my-first-pod to shoot--k8s-train--blr04-worker-gflpa-z1-7544c-cwm54
  Normal  Pulled     14m   kubelet            Container image "nginx:mainline" already present on machine
  Normal  Created    14m   kubelet            Created container nginx
  Normal  Started    14m   kubelet            Started container nginx




Step 5: clean up
It's time to clean up - go and delete the pod you created. But before open a second shell and run watch kubectl get pods. 
Now you can remove the pod from the cluster by running a delete command. Check the cheat-sheet for help. Which phases of the pod do you observe in your second shell?

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG delete pod my-first-pod
pod "my-first-pod" deleted



Step 7: Create two containers under one node  FAILED

james@lizard:~> cat /opt/docker-k8s-training/kubernetes/ex02/02a_simple_pod_new.yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-first-pod-nginx
spec:
  containers:
  - name: nginx1
    image: nginx:mainline
    ports:
    - containerPort: 80
  - name: nginx2
    image: nginx:latest
    ports:
    - containerPort: 80


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG apply -f /opt/docker-k8s-training/kubernetes/ex02/02a_simple_pod_new.yaml
pod/my-first-pod-nginx created

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get pods my-first-pod-nginx -owide
NAME                 READY   STATUS   RESTARTS      AGE   IP            NODE                                                  NOMINATED NODE   READINESS GATES
my-first-pod-nginx   1/2     Error    1 (10s ago)   14s   100.96.1.16   shoot--k8s-train--blr04-worker-gflpa-z1-7544c-mdc6n   <none>           <none>

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get pods
NAME                 READY   STATUS   RESTARTS      AGE
my-first-pod-nginx   1/2     Error    2 (21s ago)   28s


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG describe pod my-first-pod-nginx
Name:         my-first-pod-nginx
Namespace:    part-0013
Priority:     0
Node:         shoot--k8s-train--blr04-worker-gflpa-z1-7544c-mdc6n/10.250.0.7
Start Time:   Thu, 27 Jan 2022 00:47:45 +0800
Labels:       <none>
Annotations:  cni.projectcalico.org/podIP: 100.96.1.17/32
              cni.projectcalico.org/podIPs: 100.96.1.17/32
              kubernetes.io/limit-ranger:
                LimitRanger plugin set: cpu, memory request for container nginx1; cpu, memory limit for container nginx1; cpu, memory request for containe...
              kubernetes.io/psp: gardener.privileged
Status:       Running
IP:           100.96.1.17
IPs:
  IP:  100.96.1.17
Containers:
  nginx1:
    Container ID:   containerd://95f965d9b711ba7e30e721d27833982ee5ca221eb2896eecf283638573e5acb2
    Image:          nginx:mainline
    Image ID:       docker.io/library/nginx@sha256:0d17b565c37bcbd895e9d92315a05c1c3c9a29f762b011a10c54a66cd53c9b31
    Port:           80/TCP
    Host Port:      0/TCP
    State:          Running
      Started:      Thu, 27 Jan 2022 00:47:45 +0800
    Ready:          True
    Restart Count:  0
    Limits:
      cpu:     500m
      memory:  300Mi
    Requests:
      cpu:     100m
      memory:  100Mi
    Environment:
      KUBERNETES_SERVICE_HOST:  api.blr04.k8s-train.internal.canary.k8s.ondemand.com
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-vs7vx (ro)
  nginx2:
    Container ID:   containerd://26c00f54da91852c9b49acd081082319e8b849f446dd0274dc7209276d7f0a47
    Image:          nginx:latest
    Image ID:       docker.io/library/nginx@sha256:20d5b519920fbc0009e2560418b291c69b69155a524db88525368bce6b712465
    Port:           80/TCP
    Host Port:      0/TCP
    State:          Terminated
      Reason:       Error
      Exit Code:    1
      Started:      Thu, 27 Jan 2022 00:48:16 +0800
      Finished:     Thu, 27 Jan 2022 00:48:18 +0800
    Last State:     Terminated
      Reason:       Error
      Exit Code:    1
      Started:      Thu, 27 Jan 2022 00:47:57 +0800
      Finished:     Thu, 27 Jan 2022 00:48:00 +0800
    Ready:          False
    Restart Count:  2
    Limits:
      cpu:     500m
      memory:  300Mi
    Requests:
      cpu:     100m
      memory:  100Mi
    Environment:
      KUBERNETES_SERVICE_HOST:  api.blr04.k8s-train.internal.canary.k8s.ondemand.com
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-vs7vx (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             False 
  ContainersReady   False 
  PodScheduled      True 
Volumes:
  kube-api-access-vs7vx:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
QoS Class:                   Burstable
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type     Reason     Age                From               Message
  ----     ------     ----               ----               -------
  Normal   Scheduled  45s                default-scheduler  Successfully assigned part-0013/my-first-pod-nginx to shoot--k8s-train--blr04-worker-gflpa-z1-7544c-mdc6n
  Normal   Pulled     45s                kubelet            Container image "nginx:mainline" already present on machine
  Normal   Created    45s                kubelet            Created container nginx1
  Normal   Started    45s                kubelet            Started container nginx1
  Normal   Pulled     39s                kubelet            Successfully pulled image "nginx:latest" in 6.161631881s
  Normal   Pulled     33s                kubelet            Successfully pulled image "nginx:latest" in 834.678548ms
  Normal   Pulling    15s (x3 over 45s)  kubelet            Pulling image "nginx:latest"
  Normal   Created    14s (x3 over 37s)  kubelet            Created container nginx2
  Normal   Started    14s (x3 over 37s)  kubelet            Started container nginx2
  Normal   Pulled     14s                kubelet            Successfully pulled image "nginx:latest" in 837.911122ms
  Warning  BackOff    11s (x2 over 30s)  kubelet            Back-off restarting failed container





Troubleshooting
The structure of a pod can be found in the API documentation. 
Go to API reference and choose "Workload Resources". Within this section of the docs select the "Pod".
Alternatively use kubectl explain pod. 
To get detailed information about a field within the pod use its "path" like this: kubectl explain pod.spec.containers.


Further information & references
	• Pod basics https://kubernetes.io/docs/concepts/workloads/pods/pod/
	• Lifecycle & phases https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/



Kubernetes pod design pattern 
https://www.cnblogs.com/zhenyuyaodidiao/p/6514907.html

```
## Deployment

```
Exercise 3: Deployment

In this exercise, you will be dealing with Pods, Labels & Selectors and Deployments.

With the deletion of the pod all information associated with it have been removed as well. 
Though an unplanned, forcefully deletion is an unlikely scenario, it illustrates the lack of resilience of the pod construct quite well.

To overcome this shortage Kubernetes offers a hierarchical constructed api. 
The pod, which encapsulated the container, is now wrapped in a more complex construct that takes care of the desired state - the deployment. 
In this case "desired state" means that a specified quorum of running instances is fulfilled.


Step 0: deployments - the easy way
Run the following command and check what happens: 
	kubectl create deployment nginx --image=nginx:1.21 
It should create a new resource of type deployment named "nginx". 
Use kubectl get deployment nginx -o yaml and kubectl describe deployment nginx to get more detailed information on the deployment you just created. 
Based on those information, determine the labels and selectors used by your deployment.

Can you figure out the name of the pod belonging to your deployment by using the label information? 
Hint: use the -l switch in combination with kubectl get pods


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG create deployment nginx --image=nginx:1.21
deployment.apps/nginx created

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get pods --show-labels
NAME                     READY   STATUS    RESTARTS   AGE   LABELS
my-first-pod             1/1     Running   0          10m   nginx=mainline
nginx-5c95dfd78d-rjlcl   1/1     Running   0          19s   app=nginx,pod-template-hash=5c95dfd78d

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get deployment nginx --show-labels
NAME    READY   UP-TO-DATE   AVAILABLE   AGE   LABELS
nginx   1/1     1            1           19m   app=nginx

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get deployment nginx -o yaml

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG describe deployment nginx
Name:                   nginx
Namespace:              part-0013
CreationTimestamp:      Thu, 03 Feb 2022 07:26:04 +0800
Labels:                 app=nginx
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=nginx
Replicas:               1 desired | 1 updated | 1 total | 1 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=nginx
  Containers:
   nginx:
    Image:        nginx:1.21
    Port:         <none>
    Host Port:    <none>
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  <none>
NewReplicaSet:   nginx-5c95dfd78d (1/1 replicas created)
Events:
  Type    Reason             Age    From                   Message
  ----    ------             ----   ----                   -------
  Normal  ScalingReplicaSet  3m10s  deployment-controller  Scaled up replica set nginx-5c95dfd78d to 1




Step 1: scaling

Congratulations, you created your first deployment of a webserver. Now it's time to scale: 
kubectl scale deployment nginx --replicas=3 
Check the number of pods and the status of your deployment. Also don't miss the labels being attached to the pods. 
Run kubectl get pods -l app=nginx to filter for the pods belonging to your deployment.

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG scale deployment nginx --replicas=3 
deployment.apps/nginx scaled

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get pods -l app=nginx
NAME                     READY   STATUS    RESTARTS   AGE
nginx-5c95dfd78d-7rjf7   1/1     Running   0          20s
nginx-5c95dfd78d-rjlcl   1/1     Running   0          20m
nginx-5c95dfd78d-whjj4   1/1     Running   0          20s




Step 2: delete a pod
In this step you will test the resilience of your deployment. 
To be able to monitor the events open a second shell and run the following command: 
watch kubectl get pods 

Now delete a pod from your deployment and observe, how the deployment's desired state (replicas=3) is kept. 
kubectl delete pod <pod-name>

james@lizard:~> watch kubectl --kubeconfig=$KUBECONFIG get pods
Every 2.0s: kubectl --kubeconfig=/home/james/.kube/config-training get pods                     lizard: Thu Feb  3 07:47:54 2022

NAME                     READY   STATUS    RESTARTS   AGE
my-first-pod             1/1     Running   0          32m
nginx-5c95dfd78d-7rjf7   1/1     Running   0          81s
nginx-5c95dfd78d-rjlcl   1/1     Running   0          21m
nginx-5c95dfd78d-whjj4   1/1     Running   0          81s


Delete one deployment and a replacement will be created automtically

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG delete pods nginx-5c95dfd78d-7rjf7
pod "nginx-5c95dfd78d-7rjf7" deleted


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get pods
NAME                     READY   STATUS    RESTARTS   AGE
my-first-pod             1/1     Running   0          34m
nginx-5c95dfd78d-rjlcl   1/1     Running   0          24m
nginx-5c95dfd78d-whjj4   1/1     Running   0          3m33s
nginx-5c95dfd78d-x9nf7   1/1     Running   0          43s






Step 3: rolling update
Basically you could also achieve all the previous steps with a so called ReplicaSet. And in fact, you did. A deployment itself does not manage the number of replicas. 
It just creates a ReplicaSet and tells it, how many replicas it should have. 
Checkout the ReplicaSet created by your deployment: kubectl get replicaset, try also -o yaml to see its full configuration.

But a deployment can do more than managing replicasets in order to scale. It also allows you to perform a rolling update. 
Run watch kubectl rollout status deployment/nginx to monitor the process of updating. 

Now trigger the update with the following command:
kubectl set image deployment/nginx nginx=nginx:mainline --record
Note that the --record option "logs" the kubectl command and stores it in the deployment's annotations. 
When checking the rollout history later, the command will be shown as change cause.

Once finished, check the deployment, pods and ReplicaSets available in your namespace. 
By now there should be two ReplicaSets - one scaled to 0 and one scaled to 3 (or whatever number of replicas you had before the update).

This way you would be able to roll back in case of an issue during update or with the new version. 
Check kubectl rollout history deployment/nginx for the existing versions of your deployment. 
By specifying --revision=1 you will be able to get detailed on revision number one.


james@lizard:~> watch kubectl --kubeconfig=$KUBECONFIG rollout status deployment/nginx
Every 2.0s: kubectl --kubeconfig=/home/james/.kube/config-training rollout status deployment/nginx                           lizard: Thu Feb  3 07:52:33 2022

deployment "nginx" successfully rolled out


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG set image deployment/nginx nginx=nginx:mainline --record
Flag --record has been deprecated, --record will be removed in the future
deployment.apps/nginx image updated


Nginx based on image nginx:1.21 was created in step 0, Nginx based on image nginx:mainline was create in step above.

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get replicaset -owide
NAME               DESIRED   CURRENT   READY   AGE   CONTAINERS   IMAGES           SELECTOR
nginx-5c95dfd78d   0         0         0       27m   nginx        nginx:1.21       app=nginx,pod-template-hash=5c95dfd78d
nginx-d64cb58b5    3         3         3       28s   nginx        nginx:mainline   app=nginx,pod-template-hash=d64cb58b5

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get pods -owide
NAME                    READY   STATUS    RESTARTS   AGE     IP             NODE                                                  NOMINATED NODE   READINESS GATES
my-first-pod            1/1     Running   0          43m     100.96.3.214   shoot--k8s-train--blr04-worker-gflpa-z1-7544c-cwm54   <none>           <none>
nginx-d64cb58b5-jt7bf   1/1     Running   0          5m47s   100.96.0.243   shoot--k8s-train--blr04-worker-gflpa-z1-7544c-lckrb   <none>           <none>
nginx-d64cb58b5-mdgr9   1/1     Running   0          5m48s   100.96.1.198   shoot--k8s-train--blr04-worker-gflpa-z1-7544c-mdc6n   <none>           <none>
nginx-d64cb58b5-rwkxf   1/1     Running   0          5m45s   100.96.3.216   shoot--k8s-train--blr04-worker-gflpa-z1-7544c-cwm54   <none>           <none>

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG rollout history deployment/nginx
deployment.apps/nginx
REVISION  CHANGE-CAUSE
1         <none>
2         kubectl set image deployment/nginx nginx=nginx:mainline --kubeconfig=/home/james/.kube/config-training --record=true

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG rollout history deployment/nginx --revision=2
deployment.apps/nginx with revision #2
Pod Template:
  Labels:       app=nginx
        pod-template-hash=d64cb58b5
  Annotations:  kubernetes.io/change-cause:
          kubectl set image deployment/nginx nginx=nginx:mainline --kubeconfig=/home/james/.kube/config-training --record=true
  Containers:
   nginx:
    Image:      nginx:mainline
    Port:       <none>
    Host Port:  <none>
    Environment:        <none>
    Mounts:     <none>
  Volumes:      <none>




Step 4: update & rollback
Now that already you know the rollout status/history commands, let's take a look at undo.

Similar to the previous step, initiate another update while monitoring the rollout status (kubectl rollout status deployment/nginx) in parallel. 
However this time set the image version to an not existing tag. It could be a typo like mianlin or something completely different.

When listing the pods you should get one pod with an ImagePullBackOff error and the rollout should be stuck with the update of 1 new replica.

Why is the responsible controller not attempting to patch all the other replicas in parallel? 
The deployment specifies a maxUnavailable parameter as part of its update strategy (kubectl explain deployment.spec.strategy.rollingUpdate). 
It defaults to 25%, which means in our case, that with 3 replicas no more than one pod at a time is allowed to be unavailable.

Since the attempt to patch the deployment to a new image obviously failed, you have to undo action:
kubectl rollout undo deployment nginx
Check the rollout status again to make sure, your image is nginx:mainline and all pods are up and running.


james@lizard:~> watch kubectl --kubeconfig=$KUBECONFIG rollout status deployment/nginx

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG set image deployment/nginx nginx=nginx:001 --record   <--changed
Flag --record has been deprecated, --record will be removed in the future
deployment.apps/nginx image updated


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get replicaset -owide
NAME               DESIRED   CURRENT   READY   AGE     CONTAINERS   IMAGES           SELECTOR
nginx-5c95dfd78d   0         0         0       37m     nginx        nginx:1.21       app=nginx,pod-template-hash=5c95dfd78d
nginx-678b495695   1         1         0       2m24s   nginx        nginx:001        app=nginx,pod-template-hash=678b495695
nginx-d64cb58b5    3         3         3       10m     nginx        nginx:mainline   app=nginx,pod-template-hash=d64cb58b5

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get pods -owide  <--with 3 replicas no more than one pod at a time is allowed to be unavailable.
NAME                     READY   STATUS             RESTARTS   AGE     IP             NODE                                                  NOMINATED NODE   READINESS GATES
my-first-pod             1/1     Running            0          49m     100.96.3.214   shoot--k8s-train--blr04-worker-gflpa-z1-7544c-cwm54   <none>           <none>
nginx-678b495695-dhc2v   0/1     ImagePullBackOff   0          3m53s   100.96.2.189   shoot--k8s-train--blr04-worker-gflpa-z1-7544c-6jqvk   <none>           <none>
nginx-d64cb58b5-jt7bf    1/1     Running            0          11m     100.96.0.243   shoot--k8s-train--blr04-worker-gflpa-z1-7544c-lckrb   <none>           <none>
nginx-d64cb58b5-mdgr9    1/1     Running            0          11m     100.96.1.198   shoot--k8s-train--blr04-worker-gflpa-z1-7544c-mdc6n   <none>           <none>
nginx-d64cb58b5-rwkxf    1/1     Running            0          11m     100.96.3.216   shoot--k8s-train--blr04-worker-gflpa-z1-7544c-cwm54   <none>           <none>

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG rollout history deployment/nginx
deployment.apps/nginx
REVISION  CHANGE-CAUSE
1         <none>
2         kubectl set image deployment/nginx nginx=nginx:mainline --kubeconfig=/home/james/.kube/config-training --record=true
3         kubectl set image deployment/nginx nginx=nginx:001 --kubeconfig=/home/james/.kube/config-training --record=true

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG rollout history deployment/nginx --revision=3
deployment.apps/nginx with revision #3
Pod Template:
  Labels:       app=nginx
        pod-template-hash=678b495695
  Annotations:  kubernetes.io/change-cause: kubectl set image deployment/nginx nginx=nginx:001 --kubeconfig=/home/james/.kube/config-training --record=true
  Containers:
   nginx:
    Image:      nginx:001
    Port:       <none>
    Host Port:  <none>
    Environment:        <none>
    Mounts:     <none>
  Volumes:      <none>


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG explain deployment.spec.strategy.rollingUpdate
KIND:     Deployment
VERSION:  apps/v1

RESOURCE: rollingUpdate <Object>

DESCRIPTION:
     Rolling update config params. Present only if DeploymentStrategyType =
     RollingUpdate.

     Spec to control the desired behavior of rolling update.

FIELDS:
   maxSurge     <string>
     The maximum number of pods that can be scheduled above the desired number
     of pods. Value can be an absolute number (ex: 5) or a percentage of desired
     pods (ex: 10%). This can not be 0 if MaxUnavailable is 0. Absolute number
     is calculated from percentage by rounding up. Defaults to 25%. Example:
     when this is set to 30%, the new ReplicaSet can be scaled up immediately
     when the rolling update starts, such that the total number of old and new
     pods do not exceed 130% of desired pods. Once old pods have been killed,
     new ReplicaSet can be scaled up further, ensuring that total number of pods
     running at any time during the update is at most 130% of desired pods.

   maxUnavailable       <string>
     The maximum number of pods that can be unavailable during the update. Value
     can be an absolute number (ex: 5) or a percentage of desired pods (ex:
     10%). Absolute number is calculated from percentage by rounding down. This
     can not be 0 if MaxSurge is 0. Defaults to 25%. Example: when this is set
     to 30%, the old ReplicaSet can be scaled down to 70% of desired pods
     immediately when the rolling update starts. Once new pods are ready, old
     ReplicaSet can be scaled down further, followed by scaling up the new
     ReplicaSet, ensuring that the total number of pods available at all times
     during the update is at least 70% of desired pods.



james@lizard:~> kubectl --kubeconfig=$KUBECONFIG rollout undo deployment nginx
deployment.apps/nginx rolled back


Rolled back from revision 3 to revision 2, that is, promote revision 2 to revision 4 as the latest available revision. There is no revision 2 after that.

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG rollout history deployment/nginx
deployment.apps/nginx
REVISION  CHANGE-CAUSE
1         <none>
3         kubectl set image deployment/nginx nginx=nginx:001 --kubeconfig=/home/james/.kube/config-training --record=true
4         kubectl set image deployment/nginx nginx=nginx:mainline --kubeconfig=/home/james/.kube/config-training --record=true



Step 5: from file
Of course it is possible to create deployments from a yaml file. The following step gives an example, how it could look like.

Firstly, delete the deployment you just created: kubectl delete deployment nginx

Secondly, try to write your own yaml file for a new deployment that creates 3 replicas of an nginx image, with version tag latest.

Below is a skeleton of a deployment, however it is still missing some essential fields. Use kubectl explain deployment or check the api reference for details.
    kind: Deployment
    containers (check the pod spec from exercise 2 or the deployment created with run)
    values for matchLabels

apiVersion: apps/v1
metadata:
  name: nginx-deployment
  labels:
    tier: application
spec:
  replicas: 3
  selector:
    matchLabels:
  template:
    metadata:
      labels:
        run: nginx
    spec:


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get deployment
NAME    READY   UP-TO-DATE   AVAILABLE   AGE
nginx   3/3     3            3           43m

After deletion of deployment, all replica, pods of nginx were deleted as well.

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG delete deployment nginx
deployment.apps "nginx" deleted

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get deployment
No resources found in part-0013 namespace.

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get pods -owide
NAME           READY   STATUS    RESTARTS   AGE   IP             NODE                                                  NOMINATED NODE   READINESS GATES
my-first-pod   1/1     Running   0          54m   100.96.3.214   shoot--k8s-train--blr04-worker-gflpa-z1-7544c-cwm54   <none>           <none>

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get replicaset -owide
No resources found in part-0013 namespace.

james@lizard:~> cd /opt/docker-k8s-training/kubernetes/demo/
james@lizard:/opt/docker-k8s-training/kubernetes/demo> cp 03_deployment.yaml ../ex03/

james@lizard:~> vi /opt/docker-k8s-training/kubernetes/ex03/03_deployment.yaml

james@lizard:~> cat /opt/docker-k8s-training/kubernetes/ex03/03_deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    tier: application
spec:
  replicas: 3
  selector:
    matchLabels:
      run: nginx
  template:
    metadata:
      labels:
        run: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:mainline
        ports:
        - containerPort: 80




Step 6: deploy(ment)!
Now create the deployment again. Remember that you can always use the --dry-run flag to test. 
Use the yaml file you just wrote instead of the create generator.
kubectl apply -f <your-file>.yaml

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG apply -f /opt/docker-k8s-training/kubernetes/ex03/03_deployment.yaml
deployment.apps/nginx-deployment created

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get deployment
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment   3/3     3            3           10s

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get pods -owide
NAME                                READY   STATUS    RESTARTS   AGE   IP             NODE                                                  NOMINATED NODE   READINESS GATES
my-first-pod                        1/1     Running   0          70m   100.96.3.214   shoot--k8s-train--blr04-worker-gflpa-z1-7544c-cwm54   <none>           <none>
nginx-deployment-69745449db-776f5   1/1     Running   0          10m   100.96.2.190   shoot--k8s-train--blr04-worker-gflpa-z1-7544c-6jqvk   <none>           <none>
nginx-deployment-69745449db-7fqnx   1/1     Running   0          10m   100.96.0.244   shoot--k8s-train--blr04-worker-gflpa-z1-7544c-lckrb   <none>           <none>
nginx-deployment-69745449db-hznjk   1/1     Running   0          10m   100.96.1.199   shoot--k8s-train--blr04-worker-gflpa-z1-7544c-mdc6n   <none>           <none>

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get replicaset -owide
NAME                          DESIRED   CURRENT   READY   AGE   CONTAINERS   IMAGES           SELECTOR
nginx-deployment-69745449db   3         3         3       19m   nginx        nginx:mainline   pod-template-hash=69745449db,run=nginx

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG rollout history deployment/nginx-deployment
deployment.apps/nginx-deployment
REVISION  CHANGE-CAUSE
1         <none>




Step 7: kubectl diff
Congratulations - you have described a more complex resource in yaml format and deployed it to the cluster! 
But the above step had a bug and instead of mainline images with the latest tag are used. 
To switch to mainline you could use the edit mechanism again. 
However this will only affect the live version, not the file on disk. 
Instead of implementing the same change twice, let's use a more efficient way:
	• edit the local yaml file and change the image's tag to mainline
	• run kubectl diff -f <your-file>.yaml to make sure only, the image has been changed. diff compares the live version with the given file. It allows you to evaluate the result before acctually making the change.
	• update the live version with kubectl apply --record -f <your-file>.yaml

Finally, do not delete the latest version of your deployment. It will be used throughout the following exercises.

Change the yaml file like below.

james@lizard:~> cat /opt/docker-k8s-training/kubernetes/ex03/03_deployment_new.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment  <--keep same deployment
  labels:
    tier: application
spec:
  replicas: 3
  selector:
    matchLabels:
      run: nginx
  template:
    metadata:
      labels:
        run: nginx
    spec:
      containers:
      - name: nginx-new
        image: nginx:mainline
        ports:
        - containerPort: 80


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG diff -f /opt/docker-k8s-training/kubernetes/ex03/03_deployment_new.yaml
           f:spec:
             f:containers:
-              k:{"name":"nginx"}:
+              k:{"name":"nginx-new"}:

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG apply --record -f /opt/docker-k8s-training/kubernetes/ex03/03_deployment_new.yaml
Flag --record has been deprecated, --record will be removed in the future
deployment.apps/nginx-deployment configured


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG rollout history deployment/nginx-deployment
deployment.apps/nginx-deployment
REVISION  CHANGE-CAUSE
1         <none>
2         kubectl apply --kubeconfig=/home/james/.kube/config-training --record=true --filename=/opt/docker-k8s-training/kubernetes/ex03/03_deployment_new.yaml







Troubleshooting
In case of issues with the labels, make sure that the deployment.spec.selector.matchLabels query matches the labels specified within the deployment.spec.template.metadata.labels.

The structure of a deployment can be found in the API documentation. 
Go to API reference and choose "Workload Resources". Within the API docs select the "Deployment".

Alternatively use kubectl explain deployment. 
To get detailed information about a field within the pod use its "path" like this: kubectl explain deployment.spec.replicas.






Further information & references
	• Deployments in K8s concepts documentation https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
	• doing it the old way - replication controller https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller/
	• labels in K8s https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/


```
## Expose application


```
Exercise 4: Expose your application

In this exercise, you will be dealing with Pods, Deployments, Labels & Selectors, Services and Service Types.

Now that the application is running and resilient to failure of a single pod, it is time to make it available to other users inside and outside of the cluster.

Note: This exercise builds upon the previous exercise. If you did not manage to finish the previous exercise successfully, you can use the YAML file 03_deployment.yaml in the solutions folder to create a deployment. Please use the file only if you did not manage to complete the previous exercise.


Step 0: prerequisites
Once again make sure, everything is up and running. Use kubectl and check your deployment and the respective pods.

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get deployment --show-labels
NAME               READY   UP-TO-DATE   AVAILABLE   AGE   LABELS
nginx-deployment   3/3     3            3           37m   tier=application

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get pods --show-labels
NAME                                READY   STATUS    RESTARTS   AGE    LABELS
my-first-pod                        1/1     Running   0          97m    nginx=mainline
nginx-deployment-585797d45f-4k6wf   1/1     Running   0          8m3s   pod-template-hash=585797d45f,run=nginx
nginx-deployment-585797d45f-hbprl   1/1     Running   0          8m5s   pod-template-hash=585797d45f,run=nginx
nginx-deployment-585797d45f-xnl6p   1/1     Running   0          8m4s   pod-template-hash=585797d45f,run=nginx

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get replicaset --show-labels
NAME                          DESIRED   CURRENT   READY   AGE     LABELS
nginx-deployment-585797d45f   3         3         3       8m27s   pod-template-hash=585797d45f,run=nginx
nginx-deployment-69745449db   0         0         0       37m     pod-template-hash=69745449db,run=nginx






Step 1: create a service
Kubernetes provides a convenient way to expose applications. 
Simply run kubectl expose deployment <deployment-name> --type=LoadBalancer --port=80 --target-port=80. 
With --type=LoadBalancer you request our training infrastructure (GCP) to provision a public IP address. 
It will also automatically assign a cluster-IP and a NodePort in the current setup of the cluster. 

To create a service that gets only a cluster-IP, and does cluster interal load balancing but can only be called within the cluster from other pods 
but not via a public IP from the outside, use --type=ClusterIP or leave it away since it is the default.


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG expose deployment nginx-deployment --type=LoadBalancer --port=80 --target-port=80
service/nginx-deployment exposed




Step 2: connect to your service
Checkout the newly created service object in your namespace. Try to get detailed information with get -o=yaml or describe. 
Note down the different ports exposed and try to access the application via the external IP.

The service created below is available via  http://104.199.34.76:80



james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get services -n part-0013
NAME               TYPE           CLUSTER-IP     EXTERNAL-IP     PORT(S)        AGE
nginx-deployment   LoadBalancer   100.66.211.2   104.199.34.76   80:30732/TCP   2m1s

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get services -n part-0013 -o=yaml
apiVersion: v1
items:
- apiVersion: v1
  kind: Service
  metadata:
    creationTimestamp: "2022-02-03T00:56:13Z"
    finalizers:
    - service.kubernetes.io/load-balancer-cleanup
    labels:
      tier: application
    name: nginx-deployment
    namespace: part-0013
    resourceVersion: "7197114"
    uid: 5cfd8794-72a9-4d6d-b972-2f11e3f3c128
  spec:
    allocateLoadBalancerNodePorts: true
    clusterIP: 100.66.211.2
    clusterIPs:
    - 100.66.211.2
    externalTrafficPolicy: Cluster
    internalTrafficPolicy: Cluster
    ipFamilies:
    - IPv4
    ipFamilyPolicy: SingleStack
    ports:
    - nodePort: 30732
      port: 80
      protocol: TCP
      targetPort: 80
    selector:
      run: nginx
    sessionAffinity: None
    type: LoadBalancer
  status:
    loadBalancer: {}
kind: List
metadata:
  resourceVersion: ""
  selfLink: ""


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG delete services nginx-deployment
service "nginx-deployment" deleted



Step 3: create a service from a yaml file.
Before going on, delete the service you created with the expose command. Now write your own yaml to define the service. 
Check, that the label selector matches the labels of your deployment/pods and (re-)create the service (kubectl create -f <your-file>.yaml).

Important: don't delete this service, you will need it during the following exercises.

The service created below is available via http://34.78.249.22:80


james@lizard:~> mkdir /opt/docker-k8s-training/kubernetes/ex04/
james@lizard:~> cp /opt/docker-k8s-training/kubernetes/demo/04_service.yaml /opt/docker-k8s-training/kubernetes/ex04/

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG create -f /opt/docker-k8s-training/kubernetes/ex04/04_service.yaml
service/nginx-service created


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get services -n part-0013 -o=wide
NAME               TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)        AGE   SELECTOR
nginx-deployment   LoadBalancer   100.66.211.2     104.199.34.76   80:30732/TCP   28m   run=nginx
nginx-service      LoadBalancer   100.69.230.189   34.78.249.22    80:31045/TCP   45s   run=nginx


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get services -n part-0013 -o=yaml
apiVersion: v1
items:
- apiVersion: v1
  kind: Service
  metadata:
    creationTimestamp: "2022-02-03T00:56:13Z"
    finalizers:
    - service.kubernetes.io/load-balancer-cleanup
    labels:
      tier: application
    name: nginx-deployment
    namespace: part-0013
    resourceVersion: "7197398"
    uid: 5cfd8794-72a9-4d6d-b972-2f11e3f3c128
  spec:
    allocateLoadBalancerNodePorts: true
    clusterIP: 100.66.211.2
    clusterIPs:
    - 100.66.211.2
    externalTrafficPolicy: Cluster
    internalTrafficPolicy: Cluster
    ipFamilies:
    - IPv4
    ipFamilyPolicy: SingleStack
    ports:
    - nodePort: 30732
      port: 80
      protocol: TCP
      targetPort: 80
    selector:
      run: nginx
    sessionAffinity: None
    type: LoadBalancer
  status:
    loadBalancer:
      ingress:
      - ip: 104.199.34.76
- apiVersion: v1
  kind: Service
  metadata:
    creationTimestamp: "2022-02-03T01:23:56Z"
    finalizers:
    - service.kubernetes.io/load-balancer-cleanup
    labels:
      tier: networking
    name: nginx-service
    namespace: part-0013
    resourceVersion: "7207658"
    uid: 7eab2760-cd89-48ee-9813-b404fd50b3b0
  spec:
    allocateLoadBalancerNodePorts: true
    clusterIP: 100.69.230.189
    clusterIPs:
    - 100.69.230.189
    externalTrafficPolicy: Cluster
    internalTrafficPolicy: Cluster
    ipFamilies:
    - IPv4
    ipFamilyPolicy: SingleStack
    ports:
    - nodePort: 31045
      port: 80
      protocol: TCP
      targetPort: 80
    selector:
      run: nginx
    sessionAffinity: None
    type: LoadBalancer
  status:
    loadBalancer:
      ingress:
      - ip: 34.78.249.22
kind: List
metadata:
  resourceVersion: ""
  selfLink: ""







Step 4: optional/advanced - learn how to label
In this last step you will expose another pod through a service. 
Simply create the pod from the 2nd exercise again and try to expose it as LoadBalancer with kubectl expose pod ....

You will probably get an error message concerning missing labels. 
Solve this by adding a custom label to your pod and try again to expose it.

Once you are able to access the nginx via the LoadBalancer, take a look at the pod and the service. 
Determine the label as well as the corresponding selectors. 
Now remove the label from the pod. Please note, the trailing "-" is acutally required: kubectl label pod <your-pod> <your-label-key>- and try again to access the nginx via the LoadBalancer. 
Most likely this won't work anymore.

Finally, clean up and remove the pod as well as the service you created in step 4.


Copy file 02a_simple_pod.yaml from ex02 folder to ex04, and modify it like below

james@lizard:~> cat /opt/docker-k8s-training/kubernetes/ex04/02a_simple_pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-first-pod-nginx
spec:
  containers:
  - name: nginx
    image: nginx:mainline
    ports:
    - containerPort: 80


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG create -n part-0013 -f /opt/docker-k8s-training/kubernetes/ex04/02a_simple_pod.yaml
pod/my-first-pod-nginx created

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get pods --show-labels
NAME                                READY   STATUS    RESTARTS   AGE    LABELS
my-first-pod                        1/1     Running   0          134m   nginx=mainline
my-first-pod-nginx                  1/1     Running   0          12s    <none>
nginx-deployment-585797d45f-4k6wf   1/1     Running   0          45m    pod-template-hash=585797d45f,run=nginx
nginx-deployment-585797d45f-hbprl   1/1     Running   0          45m    pod-template-hash=585797d45f,run=nginx
nginx-deployment-585797d45f-xnl6p   1/1     Running   0          45m    pod-template-hash=585797d45f,run=nginx

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG expose pod my-first-pod-nginx --type=LoadBalancer --port=80 --target-port=80
error: couldn't retrieve selectors via --selector flag or introspection: the pod has no labels and cannot be exposed

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG label pod my-first-pod-nginx nginx=mainline
james@lizard:~> kubectl --kubeconfig=$KUBECONFIG label pod my-first-pod-nginx type=LoadBalancer
james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get pod --show-labels
NAME                                READY   STATUS    RESTARTS   AGE     LABELS
my-first-pod                        1/1     Running   0          136m    nginx=mainline
my-first-pod-nginx                  1/1     Running   0          2m30s   nginx=mainline,type=LoadBalancer
nginx-deployment-585797d45f-4k6wf   1/1     Running   0          47m     pod-template-hash=585797d45f,run=nginx
nginx-deployment-585797d45f-hbprl   1/1     Running   0          47m     pod-template-hash=585797d45f,run=nginx
nginx-deployment-585797d45f-xnl6p   1/1     Running   0          47m     pod-template-hash=585797d45f,run=nginx

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG expose pod my-first-pod-nginx --type=LoadBalancer --port=80 --target-port=80
james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get services -n part-0013 -o=wide
NAME                 TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)        AGE   SELECTOR
my-first-pod-nginx   LoadBalancer   100.67.15.30     34.140.75.240   80:30465/TCP   82s   nginx=mainline,type=LoadBalancer
nginx-deployment     LoadBalancer   100.66.211.2     104.199.34.76   80:30732/TCP   39m   run=nginx
nginx-service        LoadBalancer   100.69.230.189   34.78.249.22    80:31045/TCP   11m   run=nginx


http://34.140.75.240:80
http://104.199.34.76:80
http://34.78.249.22:80



Troubleshooting
In case your service is not routing traffic properly, run kubectl describe service <service-name> and check, if the list of Endpoints contains at least 1 IP address. 
The number of addresses should match the replica count of the deployment it is supposed to route traffic to.

Check the correctness of the label - selector combination by running the query manually. 
Firstly, get the selector from the service by running kubectl get service <service-name> -o yaml. 
Use the <key>: <value> pairs stored in service.spec.selector to get all pods with the corresponding label set: kubectl get pods -l <key>=<value>. 
These pods are what the service is selecting / looking for. Quite often the selector used within service matches the selector specified within the deployment.

Finally, there might be some caching on various levels of the used infrastructure. 
To break caching on corporate proxy level, request a dedicated resource like the index page: http:<LoadBalancer IP>/index.html.

The structure of a service can be found in the API documentation. 
Go to API reference and choose "Service Resources". Within the API docs select the "Service".

Alternatively use kubectl explain service. 
To get detailed information about a field within the service use its "path" like this: kubectl explain deployment.spec.ports.








Further information & references
services in K8s  https://kubernetes.io/docs/concepts/services-networking/service/
connecting a front end to a backend  https://kubernetes.io/docs/tasks/access-application-cluster/connecting-frontend-backend/
cluster internal DNS https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/

```
## Persistence

```
Exercise 5: Persistence
In this exercise, you will be dealing with Pods, Deployments, Services, Labels & Selectors, Persistent Volumes, Persistent Volume Claims and Storage Classes.

After you exposed your webserver to the network in the previous exercise, we will now add some custom content to it which resides on persistent storage outside of pods and containers.

Note: This exercise loosely builds upon the previous exercise. 
If you did not manage to finish the previous exercise successfully, you can use the YAML file 04_service.yaml in the solutions folder to create a service. 
Please use this file only if you did not manage to complete the previous exercise.


Step 0: Prepare and check your environment
Firstly, remove the deployment you created in the earlier exercise. Check the cheat sheet for the respective command.
Next, take a look around: kubectl get persistentvolume and kubectl get persistentvolumeclaims. 
Are there already resources present in the cluster? 
Inspect the resources you found and try to figure out how they are related (hint - look for status: bound).

By the way, you don't have to type persistentvolume all the time. 
You can abbreviate it with pv and similarly use pvc for the claim resource.


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get persistentvolume -n part-0013
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                    STORAGECLASS   REASON   AGE
pv--00d66ade-4cf3-42a9-b202-1e5bbc5dc52f   1Gi        RWO            Delete           Bound    part-0010/www-web-0      default                 6d15h
… …

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get persistentvolumeclaims
No resources found in part-0013 namespace.





Step 1: Create a PersistentVolume and a corresponding claim
Instead of creating a PersistentVolume (PV) first and then bind it to a PersistentVolumeClaim (PVC), you will directly request storage via a PVC using the default storage class. 
This is not only convenient, but also helps to avoid confusion. PVC are bound to a namespace, PV resource are not. 
When there is a fitting PV, it can be bound to any PVC in any namespace. So there is some conflict potential, if your colleagues always claim your PV's :) 
The concept of the storage classes overcomes this problem. 
The tooling masked by the storage class auto-provisions PV's of a defined volume type for each requested PVC.

Use the resource stored in the repository or copy the snippet from below to your VM:
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: nginx-pvc
spec:
  storageClassName: default
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi

Create the resource: kubectl create -f pvc.yaml and verify that your respective claim has been created.

Given the policy of the storage class, a PV might not be provisioned immediately and the PVC is "stuck" in status Pending. 
This is perfectly fine, but take a closer look with kubectl describe pvc <pvc-name>.


james@lizard:~> mkdir /opt/docker-k8s-training/kubernetes/ex05/
james@lizard:~> cp /opt/docker-k8s-training/kubernetes/demo/05*.yaml /opt/docker-k8s-training/kubernetes/ex05/

james@lizard:~> l /opt/docker-k8s-training/kubernetes/ex05/
-rw-r--r-- 1 james wheel  608 Feb  3 09:43 05_deployment_with_pvc.yaml
-rw-r--r-- 1 james wheel  341 Feb  3 09:43 05_pod_with_pvc.yaml
-rw-r--r-- 1 james wheel  186 Feb  3 09:43 05_pvc.yaml

james@lizard:~> cat /opt/docker-k8s-training/kubernetes/ex05/05_pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: nginx-pvc
spec:
  storageClassName: default
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG create -f /opt/docker-k8s-training/kubernetes/ex05/05_pvc.yaml
persistentvolumeclaim/nginx-pvc created

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get persistentvolumeclaim
NAME        STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
nginx-pvc   Pending                                      default        6m39s

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG describe pvc nginx-pvc
Name:          nginx-pvc
Namespace:     part-0013
StorageClass:  default
Status:        Pending
Volume:
Labels:        <none>
Annotations:   <none>
Finalizers:    [kubernetes.io/pvc-protection]
Capacity:
Access Modes:
VolumeMode:    Filesystem
Used By:       <none>
Events:
  Type    Reason                Age                     From                         Message
  ----    ------                ----                    ----                         -------
  Normal  WaitForFirstConsumer  3m13s (x26 over 9m19s)  persistentvolume-controller  waiting for first consumer to be created before binding




Step 2: Attach the PVC to a pod
Expand the deployment used in the previous exercise and make use of the PVC as a volume. 
Fill in the volumeMounts section to get access to your PVC within the actual container. 
The snippet below is not complete, so fill in the ??? with the corresponding values.
spec:
  volumes:
  - name: content-storage
    persistentVolumeClaim:
      claimName: ???
  containers:
  - name: nginx
    image: nginx:mainline
    ports:
    - containerPort: 80
    volumeMounts:
    - mountPath: "/usr/share/nginx/html"
      name: ???

Important: The PVC's access mode is ReadWriteOnce. Hence, reduce the number of replicas in your deployment to 1.

Once you re-created the deployment, make sure to check that the pod is status Running before you continue. 
You can also have a look at the PVC again. It should be backed by PV by now.

Modify file 05_pod_with_pvc.yaml like below

james@lizard:~> cat /opt/docker-k8s-training/kubernetes/ex05/05_pod_with_pvc.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-storage-pod
spec:
  volumes:
    - name: content-storage
      persistentVolumeClaim:
       claimName: nginx-pvc
  containers:
  - name: nginx
    image: nginx:mainline
    ports:
    - containerPort: 80
    volumeMounts:
    - mountPath: "/usr/share/nginx/html"
      name: content-storage


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG create -f /opt/docker-k8s-training/kubernetes/ex05/05_pod_with_pvc.yaml
pod/nginx-storage-pod created

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get pods
NAME                                READY   STATUS    RESTARTS   AGE
my-first-pod                        1/1     Running   0          171m
my-first-pod-nginx                  1/1     Running   0          36m
nginx-deployment-585797d45f-4k6wf   1/1     Running   0          82m
nginx-deployment-585797d45f-hbprl   1/1     Running   0          82m
nginx-deployment-585797d45f-xnl6p   1/1     Running   0          82m
nginx-storage-pod                   1/1     Running   0          32s


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get persistentvolumeclaim
NAME        STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
nginx-pvc   Bound    pv--08c23a7c-0c3a-4675-bdde-a762c9813e7a   1Gi        RWO            default        19m

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG describe pvc nginx-pvc
Name:          nginx-pvc
Namespace:     part-0013
StorageClass:  default
Status:        Bound
Volume:        pv--08c23a7c-0c3a-4675-bdde-a762c9813e7a
Labels:        <none>
Annotations:   pv.kubernetes.io/bind-completed: yes
               pv.kubernetes.io/bound-by-controller: yes
               volume.beta.kubernetes.io/storage-provisioner: pd.csi.storage.gke.io
               volume.kubernetes.io/selected-node: shoot--k8s-train--blr04-worker-gflpa-z1-7544c-lckrb
Finalizers:    [kubernetes.io/pvc-protection]
Capacity:      1Gi
Access Modes:  RWO
VolumeMode:    Filesystem
Used By:       nginx-storage-pod
Events:
  Type    Reason                 Age                 From                                                                                               Message
  ----    ------                 ----                ----                                                                                               -------
  Normal  WaitForFirstConsumer   59m (x62 over 74m)  persistentvolume-controller                                                                        waiting for first consumer to be created before binding
  Normal  Provisioning           56m                 pd.csi.storage.gke.io_csi-driver-controller-5c69cd58d8-zlcmj_05fdb1b3-e60e-4dff-a416-72717f0dd526  External provisioner is provisioning volume for claim "part-0013/nginx-pvc"
  Normal  ProvisioningSucceeded  56m                 pd.csi.storage.gke.io_csi-driver-controller-5c69cd58d8-zlcmj_05fdb1b3-e60e-4dff-a416-72717f0dd526  Successfully provisioned volume pv--08c23a7c-0c3a-4675-bdde-a762c9813e7a


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get persistentvolume | grep part-0013
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                       STORAGECLASS   REASON   AGE
pv--08c23a7c-0c3a-4675-bdde-a762c9813e7a   1Gi        RWO            Delete           Bound    part-0013/nginx-pvc         default                 9m41s






Step 3: create custom content
If you would try to access the nginx running in your pod, you would probably get an error message 403 Forbidden. 
This is expected since you are hiding the original index.html with a bind-mount. So let's move on and create some content on the volume we have available.

Locate the nginx pod and open a shell session into it: kubectl exec -it <pod-name> -- bash 
Navigate to the directory mentioned in the volumeMounts section and create a custom index.html. 
You can re-use the code you used in the docker exercises the other day. 
Once you are done, disconnect from the pod and close the shell session.
__Hint__
With the index page in place, try to access the webserver via the service you created in the previous exercise. It should bring up the new page now.



james@lizard:~> kubectl --kubeconfig=$KUBECONFIG exec -it nginx-storage-pod bash
kubectl exec [POD] [COMMAND] is DEPRECATED and will be removed in a future version. Use kubectl exec [POD] -- [COMMAND] instead.
root@nginx-storage-pod:/# cd /usr/share/nginx/html
root@nginx-storage-pod:/usr/share/nginx/html# echo "Welcome to k8s training" > index.html
root@nginx-storage-pod:/usr/share/nginx/html# ls
index.html  lost+found
root@nginx-storage-pod:/usr/share/nginx/html# exit






Step 4: Scaling does not work, does it?
In the previous step, the deployment was deliberately created with only one replica since the access mode "ReadWriteOnce" does not allow multiple consumers. 
In this section we will take a closer look at the implications of the access mode.

Firstly, try to bring up more pods by increasing the deployment's replica count to 5. 
Use kubectl get pods -o wide to monitor on which nodes pods are scheduled and on which node copies acutally transition to status "Running".

Is there a node, where multiple pods successully started?

If a pod stays in status Pending or ContainerCreating you could use kubectl describe pod <pod-name> to check the events logged for this pod. 
They give a first idea, of what is acutally happening (or not working).

If you compare the age of the pods, you will like find that only on the node, where the very first pod runs other pods managed to start up. 
Essentially, this is because the access mode limits only the number of nodes, you could mount a volume to. 
Within the context of a node, multiple bind-mounts are very well possible. Hence be careful with scaling operations and the use of storage.

Finally, scale the deployment back to a replica count of 1.

Important: do not delete the deployment,service or PVC





Create new file 05_pvc_new.yaml like below

james@lizard:~> cat /opt/docker-k8s-training/kubernetes/ex05/05_pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: nginx-pvc-new
spec:
  storageClassName: default
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG create -f /opt/docker-k8s-training/kubernetes/ex05/05_pvc_new.yaml
persistentvolumeclaim/nginx-pvc-new created

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get persistentvolumeclaim
NAME            STATUS    VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
nginx-pvc       Bound     pv--08c23a7c-0c3a-4675-bdde-a762c9813e7a   1Gi        RWO            default        82m
nginx-pvc-new   Pending                                                                        default        21s


Modify file 05_deployment_with_pvc.yaml like below


james@lizard:~> cat /opt/docker-k8s-training/kubernetes/ex05/05_deployment_with_pvc.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment-pvc
  labels:
    tier: application
spec:
  replicas: 1
  selector:
    matchLabels:
      run: nginx
  template:
    metadata:
      labels:
        run: nginx
    spec:
      volumes:
      - name: content-storage
        persistentVolumeClaim:
          claimName: nginx-pvc-new
#          readOnly: true
      containers:
      - name: nginx
        image: nginx:mainline
        ports:
        - containerPort: 80
        volumeMounts:
        - mountPath: "/usr/share/nginx/html"
          name: content-storage
#          readOnly: true


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG create -f /opt/docker-k8s-training/kubernetes/ex05/05_deployment_with_pvc.yaml
deployment.apps/nginx-deployment-pvc created


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get pods
NAME                                   READY   STATUS    RESTARTS   AGE
my-first-pod                           1/1     Running   0          3h57m
my-first-pod-nginx                     1/1     Running   0          103m
nginx-deployment-585797d45f-4k6wf      1/1     Running   0          148m
nginx-deployment-585797d45f-hbprl      1/1     Running   0          148m
nginx-deployment-585797d45f-xnl6p      1/1     Running   0          148m
nginx-deployment-pvc-9458c5564-x5k4w   1/1     Running   0          57s
nginx-storage-pod                      1/1     Running   0          11m


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG describe pod nginx-deployment-pvc-9458c5564-x5k4w
Name:         nginx-deployment-pvc-9458c5564-x5k4w
Namespace:    part-0013
Priority:     0
Node:         shoot--k8s-train--blr04-worker-gflpa-z1-7544c-6jqvk/10.250.0.4
Start Time:   Thu, 03 Feb 2022 11:12:38 +0800
Labels:       pod-template-hash=9458c5564
              run=nginx
Annotations:  cni.projectcalico.org/podIP: 100.96.2.192/32
              cni.projectcalico.org/podIPs: 100.96.2.192/32
              kubernetes.io/limit-ranger: LimitRanger plugin set: cpu, memory request for container nginx; cpu, memory limit for container nginx
              kubernetes.io/psp: gardener.privileged
Status:       Running
IP:           100.96.2.192
IPs:
  IP:           100.96.2.192
Controlled By:  ReplicaSet/nginx-deployment-pvc-9458c5564
Containers:
  nginx:
    Container ID:   containerd://ed3ddc732980976a26024bceeb65d85eea44e507b83d07345985f8bfefef1932
    Image:          nginx:mainline
    Image ID:       docker.io/library/nginx@sha256:0d17b565c37bcbd895e9d92315a05c1c3c9a29f762b011a10c54a66cd53c9b31
    Port:           80/TCP
    Host Port:      0/TCP
    State:          Running
      Started:      Thu, 03 Feb 2022 11:12:59 +0800
    Ready:          True
    Restart Count:  0
    Limits:
      cpu:     500m
      memory:  300Mi
    Requests:
      cpu:     100m
      memory:  100Mi
    Environment:
      KUBERNETES_SERVICE_HOST:  api.blr04.k8s-train.internal.canary.k8s.ondemand.com
    Mounts:
      /usr/share/nginx/html from content-storage (rw)
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-zg96c (ro)
Conditions:
  Type              Status
  Initialized       True
  Ready             True
  ContainersReady   True
  PodScheduled      True
Volumes:
  content-storage:
    Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
    ClaimName:  nginx-pvc-new
    ReadOnly:   false
  kube-api-access-zg96c:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
QoS Class:                   Burstable
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type    Reason                  Age   From                     Message
  ----    ------                  ----  ----                     -------
  Normal  Scheduled               59s   default-scheduler        Successfully assigned part-0013/nginx-deployment-pvc-9458c5564-x5k4w to shoot--k8s-train--blr04-worker-gflpa-z1-7544c-6jqvk
  Normal  SuccessfulAttachVolume  46s   attachdetach-controller  AttachVolume.Attach succeeded for volume "pv--b20ba5c7-c6a4-4704-8c45-a2ccaa9e96b9"
  Normal  Pulled                  39s   kubelet                  Container image "nginx:mainline" already present on machine
  Normal  Created                 39s   kubelet                  Created container nginx
  Normal  Started                 39s   kubelet                  Started container nginx





james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get persistentvolumeclaim
NAME            STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
nginx-pvc       Bound    pv--08c23a7c-0c3a-4675-bdde-a762c9813e7a   1Gi        RWO            default        86m
nginx-pvc-new   Bound    pv--b20ba5c7-c6a4-4704-8c45-a2ccaa9e96b9   1Gi        RWO            default        4m52s

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG describe pvc nginx-pvc
Name:          nginx-pvc
Namespace:     part-0013
StorageClass:  default
Status:        Bound
Volume:        pv--08c23a7c-0c3a-4675-bdde-a762c9813e7a
Labels:        <none>
Annotations:   pv.kubernetes.io/bind-completed: yes
               pv.kubernetes.io/bound-by-controller: yes
               volume.beta.kubernetes.io/storage-provisioner: pd.csi.storage.gke.io
               volume.kubernetes.io/selected-node: shoot--k8s-train--blr04-worker-gflpa-z1-7544c-lckrb
Finalizers:    [kubernetes.io/pvc-protection]
Capacity:      1Gi
Access Modes:  RWO
VolumeMode:    Filesystem
Used By:       nginx-storage-pod
Events:        <none>



james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get persistentvolume | grep part-0013
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                      STORAGECLASS   REASON   AGE
pv--08c23a7c-0c3a-4675-bdde-a762c9813e7a   1Gi        RWO            Delete           Bound    part-0013/nginx-pvc        default                 69m
pv--b20ba5c7-c6a4-4704-8c45-a2ccaa9e96b9   1Gi        RWO            Delete           Bound    part-0013/nginx-pvc-new    default                 3m52s







Troubleshooting
In case the pods of the deployment stay in status Pending or ContainerCreation for quite some time, check the events of one of the pods by running kubectl describe pod <pod-name>.
How to check if a disk is mounted!

You can try to see if the storage device is unmounted by:
	• Use kubectl get pvc <pcv-name> to get the name of the bounded persistent volume.
	• Use kubectl get pv <pv-name> -o json | jq ".spec.gcePersistentDisk" to get the name of the physical disk used by the persistent volume.
	• Use kubectl get nodes -o yaml | grep <physical-disk-name> to see if the physical disk is still conected to a node? If it is you get 3 lines per connected node.

Service Problems

In case your service is not routing traffic properly, run kubectl describe service <service-name> and check, if the list of Endpoints contains at least 1 IP address. The number of addresses should match the replica count of the deployment it is supposed to route traffic to.
Caching issues

Finally, there might be some caching on various levels of the used infrastructure. 
To break caching on corporate proxy level and display the custom page, append a URL parameter with a random number (like 15): http:<LoadBalancer IP>/?random=15.






Further information & references
	• descripton of the volumes API  https://kubernetes.io/docs/concepts/storage/volumes/
	• how to use PV & PVC  https://kubernetes.io/docs/concepts/storage/persistent-volumes/
	• storage classes  https://kubernetes.io/docs/concepts/storage/storage-classes/
	• volume snapshots  https://kubernetes.io/docs/concepts/storage/volume-snapshots/

```
## ConfigMaps and Secrets

```
Exercise 6 - ConfigMaps and Secrets

In this exercise, you will be dealing with Pods, Deployments, Services, Labels & Selectors, Persistent Volume Claims, Config Maps and Secrets.

ConfigMaps and secrets bridge the gap between the requirements to build generic images but run them with a specific configuration in an secured environment. 
In this exercise you will move credentials and configuration into the Kubernetes cluster and make them available to your pods.

Note: This exercise builds upon the previous exercises. If you did not manage to finish the previous exercises successfully, you can use the script prereq-exercise-06.sh in the solutions folder to create the prerequisites (run it with bash, not sh). 
Please use this script only if you did not manage to complete the previous exercises.

Step 0: clean up
Before you start with this exercise, remove the deployment(s) and service(s) from the previous exercises. 
However do NOT delete the persistentVolumeClaim! We will use it in this exercise as well. 
Check the cheat sheet for respective delete commands.


james@lizard:~> mkdir /opt/docker-k8s-training/kubernetes/ex06
james@lizard:~> cp /opt/docker-k8s-training/kubernetes/demo/07* /opt/docker-k8s-training/kubernetes/ex06/
james@lizard:~> cp /opt/docker-k8s-training/kubernetes/demo/04_service.yaml /opt/docker-k8s-training/kubernetes/ex06/
james@lizard:~> cp /opt/docker-k8s-training/kubernetes/solutions/06_default.conf /opt/docker-k8s-training/kubernetes/ex06/
james@lizard:~> cp /opt/docker-k8s-training/kubernetes/solutions/06_deployment_https.yaml /opt/docker-k8s-training/kubernetes/ex06/

james@lizard:~> l /opt/docker-k8s-training/kubernetes/ex06/
-rw-r--r-- 1 james wheel  622 Feb  3 13:13 06_default.conf
-rw-r--r-- 1 james wheel 1646 Feb  3 13:31 06_deployment_https.yaml
-rw-r--r-- 1 james wheel  189 Feb  3 11:24 06_pvc.yaml
-rw-r--r-- 1 james wheel  105 Feb  3 13:16 07a_configMap.yaml
-rw-r--r-- 1 james wheel  482 Feb  3 13:16 07b_pod_with_configmap.yaml
-rw-r--r-- 1 james wheel  444 Feb  3 13:16 07c_demo_secret.yaml
-rw-r--r-- 1 james wheel 1281 Feb  3 13:16 07d_demo_pod_with_secret.yaml




Create new file 06_pvc_new.yaml like below

james@lizard:~> cat /opt/docker-k8s-training/kubernetes/ex06/06_pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: nginx-pvc-07
spec:
  storageClassName: default
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG create -f /opt/docker-k8s-training/kubernetes/ex06/06_pvc.yaml
persistentvolumeclaim/nginx-pvc-07 created

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get persistentvolumeclaim
NAME            STATUS    VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
nginx-pvc       Bound     pv--08c23a7c-0c3a-4675-bdde-a762c9813e7a   1Gi        RWO            default        3h2m
nginx-pvc-07    Pending                                                                        default        84m
nginx-pvc-new   Bound     pv--b20ba5c7-c6a4-4704-8c45-a2ccaa9e96b9   1Gi        RWO            default        100m



Step 1: Create a certificate
In the first exercises you ran a webserver with plain HTTP. Now you are going to rebuild this setup and add HTTPS to your nginx.

Start by creating a new certificate:
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /tmp/nginx.key -out /tmp/nginx.crt -subj "/CN=nginxsvc/O=nginxsvc"

james@lizard:~> openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout $HOME/nginx.key -out $HOME/nginx.crt -subj "/CN=nginxsvc/O=nginxsvc"
Generating a RSA private key
................................................................+++++
..............+++++
writing new private key to '/home/james/nginx.key'
-----






Step 2: Store the certificate in Kubernetes
In order to use the certificate with our nginx, you need to add it to kubernetes and store it in a secret resource of type tls in your namespace. 
Note that Kubernetes changes the names of the files to a standardized string. For example, nginx.crt should become tls.crt.
kubectl create secret tls nginx-sec --cert=/tmp/nginx.crt --key=/tmp/nginx.key

Check, if the secret is present by running kubectl get secret nginx-sec.

Run kubectl describe secret nginx-sec to get more detailed information. The result should look like this:
Name:         nginx-sec
...

Type:  kubernetes.io/tls

Data
====
tls.crt:  1143 bytes
tls.key:  1708 bytes

Important: remember the file names in the data section of the output. They are relevant for the next step.


james@lizard:~> kubectl create secret tls nginx-sec --cert=$HOME/nginx.crt --key=$HOME/nginx.key
secret/nginx-sec created

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG describe secret nginx-sec
Name:         nginx-sec
Namespace:    part-0013
Labels:       <none>
Annotations:  <none>

Type:  kubernetes.io/tls

Data
====
tls.crt:  1164 bytes
tls.key:  1704 bytes


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get secret nginx-sec
NAME        TYPE                DATA   AGE
nginx-sec   kubernetes.io/tls   2      98s










Step 3: Create a nginx configuration
Once the certificate secret is prepared, create a configuration and store it to kubernetes as well. 
It will enable nginx to serve HTTPS traffic on port 443 using a certificate located at /etc/nginx/ssl/.

Download from gitHub or create a file default.conf with the following content. In any case, ensure the file's name is default.conf.
server {
        listen 80 default_server;
        listen [::]:80 default_server ipv6only=on;

        listen 443 ssl;

        root /usr/share/nginx/html;
        index index.html;

        server_name localhost;
        ssl_certificate /etc/nginx/ssl/tls.crt;
        ssl_certificate_key /etc/nginx/ssl/tls.key;

        location / {
                try_files $uri $uri/ =404;
        }

        location /healthz {
          access_log off;
          return 200 'OK';
        }

        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   /usr/share/nginx/html;
        }

}

Make sure, the values for ssl_certificate and ssl_certificate_key match the names of the files within the secret. 
In this example output the files are named tls.crt and tls.key in the secret as well as the configuration. 
The location in the filesystem will be set via the volumeMount, when you create your deployment. 
Also note, that there is a location explicitly defined for a healthcheck. If called, /healthz will return a status code 200 to satisfy a liveness probe.



james@lizard:~> cat /opt/docker-k8s-training/kubernetes/ex06/06_default.conf
server {
        listen 80 default_server;
        listen [::]:80 default_server ipv6only=on;

        listen 443 ssl;

        root /usr/share/nginx/html;
        index index.html;

        server_name localhost;
        ssl_certificate /etc/nginx/ssl/tls.crt;
        ssl_certificate_key /etc/nginx/ssl/tls.key;

        location / {
                try_files $uri $uri/ =404;
        }

        location /healthz {
          access_log off;
          return 200 'OK';
        }

        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   /usr/share/nginx/html/;
        }

}






Step 4: Upload the configuration to kubernetes
Run kubectl create configmap nginxconf --from-file=<path/to/your/>default.conf to create a configMap resource with the corresponding content from default.conf.

Verify the configmap exists with kubectl get configmap.


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG create configmap nginxconf-0013 --from-file=/opt/docker-k8s-training/kubernetes/ex06/06_default.conf
configmap/nginxconf-0013 created

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get configmap
NAME                 DATA   AGE
istio-ca-root-cert   1      6d19h
kube-root-ca.crt     1      12d
nginxconf-0013       1      19s






Step 5: Combine everything into a deployment
Now it is time to combine the persistentVolumeClaim, secret and configMap in a new deployment. 
As a result nginx should display the custom index.html page, serve HTTP traffic on port 80 and HTTPS on port 443. 
In order for new the setup to work, use app: nginx-https as label/selector for the "secured" nginx.

Complete the snippet below by inserting the missing parts (look for ??? blocks):
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-https-deployment
  labels:
    tier: application
spec:
  replicas: 3
  selector:
    matchLabels:
      ???: ???
  template:
    metadata:
      labels:
        app: nginx-https
    spec:
      volumes:
      - name: content-storage
        persistentVolumeClaim:
          claimName: nginx-pvc
          readOnly: true
      - name: tls-secret
        secret:
          secretName: nginx-sec
      - name: nginxconf
        configMap:
          name: nginxconf
      containers:
      - name: nginx
        image: nginx:mainline
        ports:
        - containerPort: 80
          name: http
        - containerPort: 443
          name: https
        livenessProbe:
          httpGet:
            path: ???
            port: http
          initialDelaySeconds: 3
          periodSeconds: 5
        volumeMounts:
        - mountPath: "/usr/share/nginx/html"
          name: content-storage
          readOnly: true
        - mountPath: /etc/nginx/ssl
          name: ???
          readOnly: true
        - mountPath: /etc/nginx/conf.d
          name: ???

Verify that the newly created pods use the pvc, configMap and secret by running kubectl describe pod <pod-name>.




james@lizard:~> cat /opt/docker-k8s-training/kubernetes/ex06/06_deployment_https.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-https-deployment
  labels:
    tier: application
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx-https
  template:
    metadata:
      labels:
        app: nginx-https
    spec:
       # list of volumes that can be mounted by containers belonging to the pod
      volumes:
        # make the persistentVolumeClaim with the index.html page available
      - name: content-storage
        persistentVolumeClaim:
          claimName: nginx-pvc-07
          readOnly: true
        # make the secret with the TLS certificates available
      - name: tls-secret
        secret:
          secretName: nginx-sec
        # make the configMap with the server configuration available
      - name: nginxconf
        configMap:
          name: nginxconf-0013
      containers:
      - name: nginx
        image: nginx:mainline-alpine
        ports:
        - containerPort: 80
          name: http
        - containerPort: 443
          name: https
        livenessProbe:
          httpGet:
            # point the livenessProbe to the URI specified in the server configuration (configMap)
            path: /healthz
            # reference the port by its name
            port: http
          initialDelaySeconds: 3
          periodSeconds: 5
        # define how/where to container can acces the available volumes
        volumeMounts:
        - mountPath: "/usr/share/nginx/html"
          name: content-storage
          readOnly: true
        - mountPath: /etc/nginx/ssl
          name: tls-secret
          readOnly: true
        - mountPath: /etc/nginx/conf.d
          name: nginxconf



james@lizard:~> kubectl --kubeconfig=$KUBECONFIG create -f /opt/docker-k8s-training/kubernetes/ex06/06_deployment_https.yaml
deployment.apps/nginx-https-deployment created

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get deployment
NAME                     READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment         3/3     3            3           6h20m
nginx-deployment-pvc     1/1     1            1           3h23m
nginx-https-deployment   1/1     1            1           36s


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get pods
NAME                                      READY   STATUS    RESTARTS   AGE
my-first-pod                              1/1     Running   0          7h20m
my-first-pod-nginx                        1/1     Running   0          5h5m
nginx-deployment-585797d45f-4k6wf         1/1     Running   0          5h51m
nginx-deployment-585797d45f-hbprl         1/1     Running   0          5h51m
nginx-deployment-585797d45f-xnl6p         1/1     Running   0          5h51m
nginx-deployment-pvc-9458c5564-x5k4w      1/1     Running   0          3h23m
nginx-https-deployment-5f665f49fb-sqcvc   1/1     Running   0          21s
nginx-storage-pod                         1/1     Running   0          3h34m


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG describe pods nginx-https-deployment-5f665f49fb-sqcvc
Name:         nginx-https-deployment-5f665f49fb-sqcvc
Namespace:    part-0013
Priority:     0
Node:         shoot--k8s-train--blr04-worker-gflpa-z1-7544c-cwm54/10.250.0.5
Start Time:   Thu, 03 Feb 2022 14:35:43 +0800
Labels:       app=nginx-https
              pod-template-hash=5f665f49fb
Annotations:  cni.projectcalico.org/podIP: 100.96.3.220/32
              cni.projectcalico.org/podIPs: 100.96.3.220/32
              kubernetes.io/limit-ranger: LimitRanger plugin set: cpu, memory request for container nginx; cpu, memory limit for container nginx
              kubernetes.io/psp: gardener.privileged
Status:       Running
IP:           100.96.3.220
IPs:
  IP:           100.96.3.220
Controlled By:  ReplicaSet/nginx-https-deployment-5f665f49fb
Containers:
  nginx:
    Container ID:   containerd://e3b2188a32c8e513cdec607a74c2d6b83093b6c2a4a417638c8aa95e9b3362b3
    Image:          nginx:mainline-alpine
    Image ID:       docker.io/library/nginx@sha256:da9c94bec1da829ebd52431a84502ec471c8e548ffb2cedbf36260fd9bd1d4d3
    Ports:          80/TCP, 443/TCP
    Host Ports:     0/TCP, 0/TCP
    State:          Running
      Started:      Thu, 03 Feb 2022 14:36:02 +0800
    Ready:          True
    Restart Count:  0
    Limits:
      cpu:     500m
      memory:  300Mi
    Requests:
      cpu:     100m
      memory:  100Mi
    Liveness:  http-get http://:http/healthz delay=3s timeout=1s period=5s #success=1 #failure=3
    Environment:
      KUBERNETES_SERVICE_HOST:  api.blr04.k8s-train.internal.canary.k8s.ondemand.com
    Mounts:
      /etc/nginx/conf.d from nginxconf (rw)
      /etc/nginx/ssl from tls-secret (ro)
      /usr/share/nginx/html from content-storage (ro)
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-ll4l9 (ro)
Conditions:
  Type              Status
  Initialized       True
  Ready             True
  ContainersReady   True
  PodScheduled      True
Volumes:
  content-storage:
    Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
    ClaimName:  nginx-pvc-07
    ReadOnly:   true
  tls-secret:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  nginx-sec
    Optional:    false
  nginxconf:
    Type:      ConfigMap (a volume populated by a ConfigMap)
    Name:      nginxconf-0013
    Optional:  false
  kube-api-access-ll4l9:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
QoS Class:                   Burstable
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type    Reason                  Age   From                     Message
  ----    ------                  ----  ----                     -------
  Normal  Scheduled               108s  default-scheduler        Successfully assigned part-0013/nginx-https-deployment-5f665f49fb-sqcvc to shoot--k8s-train--blr04-worker-gflpa-z1-7544c-cwm54
  Normal  SuccessfulAttachVolume  95s   attachdetach-controller  AttachVolume.Attach succeeded for volume "pv--9ad170fb-0da4-4df3-812d-b3469715bcda"
  Normal  Pulling                 90s   kubelet                  Pulling image "nginx:mainline-alpine"
  Normal  Pulled                  89s   kubelet                  Successfully pulled image "nginx:mainline-alpine" in 829.910127ms
  Normal  Created                 89s   kubelet                  Created container nginx
  Normal  Started                 89s   kubelet                  Started container nginx




james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get deployment --show-labels
NAME                     READY   UP-TO-DATE   AVAILABLE   AGE     LABELS
nginx-deployment         3/3     3            3           6h28m   tier=application
nginx-deployment-pvc     1/1     1            1           3h31m   tier=application
nginx-https-deployment   1/1     1            1           8m27s   tier=application


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get pods --show-labels
NAME                                      READY   STATUS    RESTARTS   AGE     LABELS
my-first-pod                              1/1     Running   0          7h28m   nginx=mainline
my-first-pod-nginx                        1/1     Running   0          5h14m   nginx=mainline,type=LoadBalancer
nginx-deployment-585797d45f-4k6wf         1/1     Running   0          5h59m   pod-template-hash=585797d45f,run=nginx
nginx-deployment-585797d45f-hbprl         1/1     Running   0          5h59m   pod-template-hash=585797d45f,run=nginx
nginx-deployment-585797d45f-xnl6p         1/1     Running   0          5h59m   pod-template-hash=585797d45f,run=nginx
nginx-deployment-pvc-9458c5564-x5k4w      1/1     Running   0          3h31m   pod-template-hash=9458c5564,run=nginx
nginx-https-deployment-5f665f49fb-sqcvc   1/1     Running   0          8m47s   app=nginx-https,pod-template-hash=5f665f49fb
nginx-storage-pod                         1/1     Running   0          3h42m   <none>










Step 6: create a service
Finally, you have to create a new service to expose your https-deployment.

Derive the ports you have to expose and extend the service.yaml from the previous exercise. 
Make sure, that the labels used in the deployment and the selector specified by the service match.

Once the service has an external IP try to call it with an HTTPS prefix.       --with error 403 Forbidden,???
Check the certificate it returns - it should match the subject and organization specified in step 1. 
Since we signed the certificate ourself, your Browser will complain about the certificate (depending on your browser) and you have to accept the risk browsing the url.

Important: do not delete this setup with deployment, PVC, configMap, secret and service.



Delete one expose service because current 3 services exposed and exceed the server quota.
Error from server (Forbidden): services "nginx-https-deployment" is forbidden: exceeded quota: training-quota, requested: services.loadbalancers=1, used: services.loadbalancers=3, limited: services.loadbalancers=3

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get services -n part-0013
NAME                 TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)        AGE
my-first-pod-nginx   LoadBalancer   100.67.15.30     34.140.75.240   80:30465/TCP   5h10m
nginx-deployment     LoadBalancer   100.66.211.2     104.199.34.76   80:30732/TCP   5h49m
nginx-service        LoadBalancer   100.69.230.189   34.78.249.22    80:31045/TCP   5h21m

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG delete services my-first-pod-nginx -n part-0013
service "my-first-pod-nginx" deleted


Modify file 04_service.yaml like below. App name in selector will be used to map the pod nginx-https-deployment-5f665f49fb-sqcvc.

james@lizard:~> cat /opt/docker-k8s-training/kubernetes/ex06/04_service.yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-https-service
spec:
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
    name: http
  - port: 443
    protocol: TCP
    targetPort: 443
    name: https
  selector:
    app: nginx-https
  type: LoadBalancer



james@lizard:~> kubectl --kubeconfig=$KUBECONFIG create -f /opt/docker-k8s-training/kubernetes/ex06/04_service.yaml
service/nginx-https-service created

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get services -n part-0013
NAME                  TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)                      AGE
nginx-deployment      LoadBalancer   100.66.211.2     104.199.34.76   80:30732/TCP                 6h26m
nginx-https-service   LoadBalancer   100.64.238.60    34.140.75.240   80:32388/TCP,443:31228/TCP   66s
nginx-service         LoadBalancer   100.69.230.189   34.78.249.22    80:31045/TCP                 5h58m











Troubleshooting
The deployment has grown throughout this exercise. There should be 3 volumes specified as part of deployment.spec.template.spec.volumes (a pvc, configMap & secret). 
Each item of the volumes list defines a (local/pod-internal) name and references the actual K8s object. 
Also these 3 volumes should be used and mounted to a specific location within the container (defined in deployment.spec.template.spec.containers.volumeMount). 
The local/pod-internal name is used for the name field.

When creating the service double check the used selector. It should match the labels given to any pod created by the new deployment. 
The value can be found at deployment.spec.template.metadata.labels. 
In case your service is not routing traffic properly, run kubectl describe service <service-name> and check, if the list of Endpoints contains at least 1 IP address. 
The number of addresses should match the replica count of the deployment it is supposed to route traffic to.

Also check, if the IP addresses point to the pods created during this exercise. 
In case of doubt check the correctness of the label - selector combination by running the query manually. 
Firstly, get the selector from the service by running kubectl get service <service-name> -o yaml. 
Use the <key>: <value> pairs stored in service.spec.selector to get all pods with the corresponding label set: kubectl get pods -l <key>=<value>. 
These pods are what the service is selecting / looking for. 
Quite often the selector used within service matches the selector specified within the deployment.

Finally, there might be some caching on various levels of the used infrastructure. 
To break caching on corporate proxy level and display the custom page, request index.html directly: http:<LoadBalancer IP>/index.html.




Further information & references
secrets in k8s https://kubernetes.io/docs/concepts/configuration/secret/
options to use a configMap https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/


```
## Ingress

```
Exercise 7 - Ingress

In this exercise, you will be dealing with Pods, Deployments, Services, Labels & Selectors, Init Containers and Ingresses.

Ingress resources allow us to expose services through a URL. 
In addition, it is possible to configure an Ingress so that traffic can be directed to different services, depending on the URL that is used for a request. 
In this exercise, you will set up a simple Ingress resource.

In addition to all that, you will use Init-Containers to initialize your nginx deployment and load the application's content.

Note: This exercise builds upon the previous exercises. 
If you did not manage to finish the previous exercises successfully, you can use the script prereq-exercise-07.sh in the solutions folder to create the prerequisites. 
Please use this script only if you did not manage to complete the previous exercises.



Step 0 - obtain necessary detail information
Since the ingress controller is specific to the cluster, you need some information to construct a valid URL processable by the controller.

Here is a command to find out your cluster's and project's names:
echo "Clustername: $(kubectl config view -o json | jq  ".clusters[0].cluster.server" | cut -d. -f2)"; echo "Projectname: $(kubectl config view -o json | jq  ".clusters[0].cluster.server" | cut -d. -f3)"

If there are any issues, check with your trainer.


james@lizard:~> echo "Clustername: $(kubectl config view -o json | jq  ".clusters[0].cluster.server" | cut -d. -f2)"; echo "Projectname: $(kubectl config view -o json | jq  ".clusters[0].cluster.server" | cut -d. -f3)"
Clustername: blr04
Projectname: k8s-train


james@lizard:~> cp /opt/docker-k8s-training/kubernetes/solutions/07_ingress.yaml /opt/docker-k8s-training/kubernetes/ex07/

james@lizard:~> l /opt/docker-k8s-training/kubernetes/ex07/
-rw-r--r-- 1 james wheel 2734 Feb  3 16:04 07_ingress.yaml










Step 1 - init: prepare pods and services
For this exercise you can either re-use already existing deployments, pods and services or create them from scratch. 
Please continue to use an nginx webserver as backend application. 
For the sake of resource consumption, please use replica: 1 for new resources.

When you create a new deployment, remember that you can generate a skeleton by right-clicking the VM desktop -> context menu "new documents" -> deployment. 
You could also try to add an init container. The init container should write a string like the hostname or "hello world" to and index.html on an emptyDir volume. 
Use this volume in the nginx container as well to get a customized index.html page.

The snippets below might give an idea, how to create a cache volume and pass an appropriate command to a busybox running as init container.

volumes:
- name: index-html
  emptyDir: {}

command:
- /bin/sh
- -c
- echo HelloWorld! > /work-dir/index.html

More details about init containers can be found here and here.

Step 2 - write a simple ingress and deploy it
To expose your application via an ingress, you need to construct a valid URL. 
Within the Gardener environment you have to use the following schema: <your-custom-endpoint>.ingress.<GARDENER-CLUSTER-NAME>.<GARDENER-PROJECT-NAME>.shoot.canary.k8s-hana.ondemand.com

For <your-custom-endpoint> it is recommended to use your generated participant ID. 
You are going to expose the URL to public internet and most likely you don't want to publish information like your d/i -user there. 
Also insert the cluster and project names you obtained from your trainer accordingly.

Check the help section to get more information.

Write the ingress yaml file and reference to your service. 
Use the following skeleton and check the kubernetes API reference for details and further info.

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: <ingress resource name>
# annotations are optional at this stage! 
  annotations:
    <annotations-key>: <annotations-value>
  labels:
    <label-key>: <label-value>
spec:
  rules:
  - host: <host string>
    http:
      paths:
      - path: <URI relative to the host>
        pathType: Prefix
        backend:
          service: 
            name: <string>
            port:
              number : <int>

Finally, deploy your ingress and test the URL.


Delete some services to release more for new deployment.

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get service -n part-0013
NAME                  TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)                      AGE
nginx-deployment      LoadBalancer   100.66.211.2     104.199.34.76   80:30732/TCP                 7h15m
nginx-https-service   LoadBalancer   100.64.238.60    34.140.75.240   80:32388/TCP,443:31228/TCP   49m
nginx-service         LoadBalancer   100.69.230.189   34.78.249.22    80:31045/TCP                 6h47m

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG delete service nginx-deployment -n part-0013
service "nginx-deployment" deleted


james@lizard:~> cat /opt/docker-k8s-training/kubernetes/ex07/07_ingress.yaml
#########################################################
## adapt the cluster and project name before deploying ##
#########################################################
#
# specify a deployment first - this will be the backend all traffic is routed to.
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: simple-nginx
  labels:
    tier: application
spec:
  replicas: 1
  selector:
    matchLabels:
      app: simple-nginx
  template:
    metadata:
      labels:
        app: simple-nginx
    spec:
      volumes:
      - name: index-html
        emptyDir: {}
      initContainers:
      - name: setup
        image: alpine:latest
        command:
        - /bin/sh
        - -c
        - echo This is a simple nginx! > /work-dir/index.html
        volumeMounts:
        - name: index-html
          mountPath: "/work-dir"
      containers:
      - name: nginx
        image: nginx:mainline
        ports:
        - containerPort: 80
        volumeMounts:
        - name: index-html
          mountPath: /usr/share/nginx/html
---
# next, a service is required to handle traffic to the pods created by the deployment
apiVersion: v1
kind: Service
metadata:
  name: simple-nginx-service
  labels:
    tier: networking
spec:
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
  selector:
    app: simple-nginx
  type: ClusterIP
---
# finally, define the ingress
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: simple-nginx-ingress
  # annotations are part of the metadata object
  # usually annotations are used to sent information to a controller
  # here we instruct the ingress-controller to set the connect-timeout to 61s and rewrite the target to '/' for this specific host/URL
  annotations:
    nginx.ingress.kubernetes.io/proxy-connect-timeout: "61"
    nginx.ingress.kubernetes.io/rewrite-target: /$1
# define the routing rules for the ingress in its 'spec'
spec:
  rules:
    # an ingress can have one to many hosts. A host is fully qualified URL
    # TODO: replace in ingress host URL the <participantId>, <cluster-name> and <project-name> parameters of the training cluster
    # e.g. '0007-simple-nginx.ingress.wdfcw48.k8s-train.shoot.canary.k8s-hana.ondemand.com'
  - host: 0013-simple-nginx.ingress.blr04.k8s-train.shoot.canary.k8s-hana.ondemand.com
    http:
      paths:
      # the ingress controller routes traffic to a service backend based on a <host>/<path> combination
      # in this case traffic coming in to <host>/my-app will be routed to the service 'simple-nginx-service'
      - path: /my-app(.*)
        pathType: Prefix
        backend:
          service:
            name: simple-nginx-service
            port:
              number: 80




james@lizard:~> kubectl --kubeconfig=$KUBECONFIG create -f /opt/docker-k8s-training/kubernetes/ex07/07_ingress.yaml
deployment.apps/simple-nginx created
service/simple-nginx-service created
ingress.networking.k8s.io/simple-nginx-ingress created

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get deployment
NAME                     READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment         3/3     3            3           8h
nginx-deployment-pvc     1/1     1            1           5h6m
nginx-https-deployment   1/1     1            1           102m
simple-nginx             1/1     1            1           56s

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get service
NAME                   TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)                      AGE
nginx-https-service    LoadBalancer   100.64.238.60    34.140.75.240   80:32388/TCP,443:31228/TCP   57m
nginx-service          LoadBalancer   100.69.230.189   34.78.249.22    80:31045/TCP                 6h55m
simple-nginx-service   ClusterIP      100.71.24.235    <none>          80/TCP                       66s

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get ingress
NAME                   CLASS    HOSTS                                                                          ADDRESS         PORTS   AGE
simple-nginx-ingress   <none>   0013-simple-nginx.ingress.blr04.k8s-train.shoot.canary.k8s-hana.ondemand.com   35.205.76.251   80      92s

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get replicasets
NAME                                DESIRED   CURRENT   READY   AGE
nginx-deployment-585797d45f         3         3         3       7h34m
nginx-deployment-69745449db         0         0         0       8h
nginx-deployment-pvc-9458c5564      1         1         1       5h7m
nginx-https-deployment-5f665f49fb   1         1         1       103m
simple-nginx-544dd54c77             1         1         1       109s

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get pods
NAME                                      READY   STATUS    RESTARTS   AGE
my-first-pod                              1/1     Running   0          9h
my-first-pod-nginx                        1/1     Running   0          6h50m
nginx-deployment-585797d45f-4k6wf         1/1     Running   0          7h35m
nginx-deployment-585797d45f-hbprl         1/1     Running   0          7h35m
nginx-deployment-585797d45f-xnl6p         1/1     Running   0          7h35m
nginx-deployment-pvc-9458c5564-x5k4w      1/1     Running   0          5h8m
nginx-https-deployment-5f665f49fb-sqcvc   1/1     Running   0          104m
nginx-storage-pod                         1/1     Running   0          5h18m
simple-nginx-544dd54c77-cggm4             1/1     Running   0          2m56s



http://0013-simple-nginx.ingress.blr04.k8s-train.shoot.canary.k8s-hana.ondemand.com/
https://0013-simple-nginx.ingress.blr04.k8s-train.shoot.canary.k8s-hana.ondemand.com/




Step 3 - annotate!
Besides the labels, K8s uses also a concept called "annotations". 
Annotations are part of the metadata section and can be written directly to the yaml file as well as added via kubectl annotate .... Similar to the labels, annotations are also key-value pairs. 
Most commonly annotations are used to store additional information, describe a resource more detailed or tweak it's behavior.

In our case, the used ingress controller knows several annotations and reacts to them in a predefined way. 
The known annotations and their effect are described here.

So let's assume, you want to change the timeout behavior of the nginx exposed via the ingress. 
Check the list of annotations for the proxy-connect-timeout and apply a suitable configuration to your ingress. 
Of course don't forget to test the URL.



optional step 4 - rewrite target
Now that you know how an annotation works and how it affects your ingress, lets move on the fanout scenario. 
Assume you want your ingress to serve something different at its root level / and you want to move your application to /my-app. 
Your URL would look like this <your-custom-endpoint>.ingress.<GARDENER-CLUSTER-NAME>.<GARDENER-PROJECT-NAME>.shoot.canary.k8s-hana.ondemand.com/my-app.

In a first step, you need to add path: /my-app(.*) to your backend configuration within the ingress. 
Take a look at the fanout demo, if you need inspiration. Once you applied your the change, go to your URL and test the different paths. 
But don't be surprised, if you don't see the expected pages.

The ingress is forwarding traffic to /my-app also to /my-app at the backend. 
So unless you configured your nginx pods to serve at /my-app there is no valid endpoint available. 
You can solve the issue by rewriting the target to /$1 of the backend pods. 
Check the rewrite-target annotation for details and apply it accordingly. 
The documentation features an example as well.


















Troubleshooting
In addition to the checking of service <> deployment connection via labels and selectors, there is another entity which holds relevant information - the actual ingress router running in kube-system namespace.

Get the full name of the addons-nginx-ingress-controller pod running in kube-system and check the last 50 log entries for occurrences of your ingress name or host name and related errors. Increase the number (--tail=100), when your resource is not part of the output:
	• kubectl -n kube-system get pods
	• kubectl -n kube-system logs --tail=50 addons-nginx-ingress-controller-<some ID>






Further information & references
	• annotations https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/
	• init containers https://kubernetes.io/docs/concepts/workloads/pods/init-containers/
	• debugging of init containers https://kubernetes.io/docs/tasks/debug-application-cluster/debug-init-containers/
	• ingress https://kubernetes.io/docs/concepts/services-networking/ingress/
	• list of ingress controllers https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/
	• nginx ingress controller https://www.nginx.com/products/nginx/kubernetes-ingress-controller


```
## StatefulSet

```
Exercise 8: StatefulSet
In this exercise, you will be dealing with Pods, Persistent Volumes, Persistent Volume Claims, Headless Services and Stateful Sets.
In this exercise you will deploy a nginx webserver as a StatefulSet and scale it.
Note: This exercise does not build on any of the previous exercises.


Step 0: Create a headless service
Firstly, you need to create a so called "headless" service. These services are of type: ClusterIP and explicitly specify their clusterIP with None. 
Try to create such a service and think of a suitable name as well as selector for labels. 
Either re-use an existing service yaml file or start a new one from scratch. Make sure, you refer to a named port.

And don't forget to deploy the service to the cluster ;)

Step 1: Build a StatefulSet
Now that you have the service, you meet the prerequisite to create a StatefulSet.

Next, describe your desired state in a yaml file. Use the snippets below to create a valid yaml file for a StatefulSet resource. 
Also fill in the blanks (marked with ???) with values. 
Note that during the run of the initContainer the current host name will be written into the index.html file every time the pod is started.

If you are looking for more info, check the official api reference for StatefulSets.

apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web

volumeClaimTemplates:
- metadata:
    name: ???
  spec:
    accessModes: [ "ReadWriteOnce" ]
    resources:
      requests:
        storage: 1Gi

spec:
  replicas: 2

spec:
  initContainers:
  - name: setup
    image: alpine:3.8
    command:
    - /bin/sh
    - -c
    - echo $(hostname) >> /work-dir/index.html
    volumeMounts:
    - name: ???
      mountPath: /work-dir
  containers:
  - name: nginx
    image: nginx:mainline
    ports:
    - containerPort: 80
      name: ???
    volumeMounts:
    - name: ???
      mountPath: /usr/share/nginx/html

serviceName: "???"
selector:
  matchLabels:
    ???: ???

template:
  metadata:
    labels:
      ???: ???



james@lizard:~> cat /opt/docker-k8s-training/kubernetes/ex08/08_statefulset_with_svc.yaml
# declaration of a headless service
apiVersion: v1
kind: Service
metadata:
  name: stateful-nginx
  labels:
    app: stateful-nginx
spec:
  ports:
  - port: 80
    name: web
  # by assigning the value 'None' to 'clusterIP' the service becomes "headless".
  # a headless service has no separate cluster internal IP.
  clusterIP: None
  selector:
    app: stateful-nginx
# with '---' two different resources can be separated even though they reside in the same file
---
# declaration of a statefulset (sts)
# deployments belong to api group 'apps' in version 'v1'
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  # link the statefulset to its headless service
  serviceName: "stateful-nginx"
  replicas: 2
  selector:
    matchLabels:
      app: stateful-nginx
  # the following section describes the pods that will be created.
  template:
    metadata:
      labels:
        app: stateful-nginx
    spec:
      # initContainers is a list similar to 'containers'.
      # all containers defined here, will be executed prior to the regular container(s)
      # initContainers have access to volumes defined for the pod
      initContainers:
      - name: setup
        image: alpine:latest
        command:
        - /bin/sh
        - -c
        - echo $(hostname) >> /work-dir/index.html
        volumeMounts:
        - name: www
          mountPath: /work-dir
      containers:
      - name: nginx
        image: nginx:mainline
        ports:
        - containerPort: 80
          name: web
        volumeMounts:
        - name: www
          mountPath: /usr/share/nginx/html
  # statefulsets allow to specify required storage as a template
  # a new PVC is created for each replica of the statefulset
  # hence each replica has access to a dedicated & individual storage
  volumeClaimTemplates:
  - metadata:
      name: www
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 1Gi



james@lizard:~> kubectl --kubeconfig=$KUBECONFIG create -f /opt/docker-k8s-training/kubernetes/ex08/08_statefulset_with_svc.yaml
service/stateful-nginx created
statefulset.apps/web created






Step 2: Ordered creation
Before you create the StatefulSet, open a 2nd terminal and start to watch the pods in your namespace: watch kubectl get pods

Now post your yaml file to the API server and monitor the upcoming new pods. 
You should observe the ordered creation of pods (by their ordinal index). 
Note that the pod name does not have any randomly generated string (as with deployments), but consists of the statefulset's name + the index.

Additionally you should find new PVC resources in your namespace.

Quickly spin up a temporary pod and directly connect to it: kubectl run dns-test -i --tty --restart=Never --rm --image=alpine:3.12 -- ash

Within pod's shell context, run nslookup [pod-name].[service-name] to check, if your individual pods are accessible via the service.

Also download the index.html page of each instance using wget -q -O - [pod-name].[service-name]. You should get the corresponding host name that was written by the initContainer.


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get persistentvolumeclaim
NAME            STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
nginx-pvc       Bound    pv--08c23a7c-0c3a-4675-bdde-a762c9813e7a   1Gi        RWO            default        6h57m
nginx-pvc-07    Bound    pv--9ad170fb-0da4-4df3-812d-b3469715bcda   1Gi        RWO            default        5h18m
nginx-pvc-new   Bound    pv--b20ba5c7-c6a4-4704-8c45-a2ccaa9e96b9   1Gi        RWO            default        5h35m
www-web-0       Bound    pv--6c1880c4-169b-486b-b952-8869770082ec   1Gi        RWO            default        4m43s
www-web-1       Bound    pv--efe1f0ed-b212-4335-b40d-791d54d5b943   1Gi        RWO            default        4m15s


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get persistentvolume | grep 0013
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                     STORAGECLASS   REASON   AGE
pv--08c23a7c-0c3a-4675-bdde-a762c9813e7a   1Gi        RWO            Delete           Bound    part-0013/nginx-pvc       default                 6h36m
pv--6c1880c4-169b-486b-b952-8869770082ec   1Gi        RWO            Delete           Bound    part-0013/www-web-0       default                 2m30s
pv--9ad170fb-0da4-4df3-812d-b3469715bcda   1Gi        RWO            Delete           Bound    part-0013/nginx-pvc-07    default                 173m
pv--b20ba5c7-c6a4-4704-8c45-a2ccaa9e96b9   1Gi        RWO            Delete           Bound    part-0013/nginx-pvc-new   default                 5h30m
pv--efe1f0ed-b212-4335-b40d-791d54d5b943   1Gi        RWO            Delete           Bound    part-0013/www-web-1       default                 2m3s

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get pods
NAME                                      READY   STATUS    RESTARTS   AGE
my-first-pod                              1/1     Running   0          9h
my-first-pod-nginx                        1/1     Running   0          7h15m
nginx-deployment-585797d45f-4k6wf         1/1     Running   0          8h
nginx-deployment-585797d45f-hbprl         1/1     Running   0          8h
nginx-deployment-585797d45f-xnl6p         1/1     Running   0          8h
nginx-deployment-pvc-9458c5564-x5k4w      1/1     Running   0          5h33m
nginx-https-deployment-5f665f49fb-sqcvc   1/1     Running   0          130m
nginx-storage-pod                         1/1     Running   0          5h44m
simple-nginx-544dd54c77-cggm4             1/1     Running   0          28m
web-0                                     1/1     Running   0          5m30s
web-1                                     1/1     Running   0          5m2s


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get deployment
NAME                     READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment         3/3     3            3           8h
nginx-deployment-pvc     1/1     1            1           5h33m
nginx-https-deployment   1/1     1            1           130m
simple-nginx             1/1     1            1           28m


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get services
NAME                   TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)                      AGE
nginx-https-service    LoadBalancer   100.64.238.60    34.140.75.240   80:32388/TCP,443:31228/TCP   84m
nginx-service          LoadBalancer   100.69.230.189   34.78.249.22    80:31045/TCP                 7h22m
simple-nginx-service   ClusterIP      100.71.24.235    <none>          80/TCP                       28m
stateful-nginx         ClusterIP      None             <none>          80/TCP                       5m49s

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get statefulsets -o wide
NAME   READY   AGE   CONTAINERS   IMAGES
web    2/2     10m   nginx        nginx:mainline




james@lizard:~> kubectl --kubeconfig=$KUBECONFIG run dns-test -i --tty --restart=Never --rm --image=alpine:3.12 -- ash
If you don't see a command prompt, try pressing enter.
/ # nslookup web-0.stateful-nginx
Server:         100.64.0.10
Address:        100.64.0.10:53

** server can't find web-0.stateful-nginx: NXDOMAIN

** server can't find web-0.stateful-nginx: NXDOMAIN

/ # wget web-0.stateful-nginx
Connecting to web-0.stateful-nginx (100.96.1.205:80)
saving to 'index.html'
index.html           100% |**********************************************************************************************|     6  0:00:00 ETA
'index.html' saved
/ # cat index.html
web-0
/ # exit
pod "dns-test" deleted





Step 3: Stable hostnames

StatefulSets guarantee stable/reliable names. Since the pod name is also the hostname, it won't change over time - even when the pod gets killed and re-created.

Delete the pods of your StatefulSet while watching the pods in you namespace. Observe, how the pods will be re-created with the exact same names.

Again, spin up a temporary deployment of a busybox and directly connect to it. 
If you re-run nslookup, notice the IP addresses probably have changed. 
Since the initContainer wrote the "new" hostname to the index.html page, download it with wget and check for the expected content.



james@lizard:~> kubectl --kubeconfig=$KUBECONFIG run dns-test -i --tty --restart=Never --rm --image=busybox
If you don't see a command prompt, try pressing enter.
/ # nslookup web-0.stateful-nginx
Server:         100.64.0.10
Address:        100.64.0.10:53

** server can't find web-0.stateful-nginx: NXDOMAIN

*** Can't find web-0.stateful-nginx: No answer

/ # wget web-0.stateful-nginx
Connecting to web-0.stateful-nginx (100.96.1.205:80)
saving to 'index.html'
index.html           100% |**********************************************************************************************|     6  0:00:00 ETA
'index.html' saved
/ # cat index.html
web-0
/ # exit


Delete one pod and the same will be created automatically per replicaset.

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG delete pods web-0
pod "web-0" deleted

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get pods
NAME                                      READY   STATUS    RESTARTS   AGE
dns-test                                  1/1     Running   0          3m21s
my-first-pod                              1/1     Running   0          10h
my-first-pod-nginx                        1/1     Running   0          7h51m
nginx-deployment-585797d45f-4k6wf         1/1     Running   0          8h
nginx-deployment-585797d45f-hbprl         1/1     Running   0          8h
nginx-deployment-585797d45f-xnl6p         1/1     Running   0          8h
nginx-deployment-pvc-9458c5564-x5k4w      1/1     Running   0          6h9m
nginx-https-deployment-5f665f49fb-sqcvc   1/1     Running   0          166m
nginx-storage-pod                         1/1     Running   0          6h19m
simple-nginx-544dd54c77-cggm4             1/1     Running   0          64m
web-0                                     1/1     Running   0          7s
web-1                                     1/1     Running   0          40m


Rerun it again.  Two web-0 now.

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG run dns-test -i --tty --restart=Never --rm --image=busybox
If you don't see a command prompt, try pressing enter.
/ # nslookup web-0.stateful-nginx
Server:         100.64.0.10
Address:        100.64.0.10:53

** server can't find web-0.stateful-nginx: NXDOMAIN

*** Can't find web-0.stateful-nginx: No answer

/ # wget web-0.stateful-nginx
Connecting to web-0.stateful-nginx (100.96.1.205:80)
saving to 'index.html'
index.html           100% |**********************************************************************************************|     6  0:00:00 ETA
'index.html' saved
/ # cat index.html
web-0
web-0
/ # exit


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get pods --watch
NAME                                      READY   STATUS    RESTARTS   AGE
my-first-pod                              1/1     Running   0          10h
my-first-pod-nginx                        1/1     Running   0          8h
nginx-deployment-585797d45f-4k6wf         1/1     Running   0          8h
nginx-deployment-585797d45f-hbprl         1/1     Running   0          8h
nginx-deployment-585797d45f-xnl6p         1/1     Running   0          8h
nginx-deployment-pvc-9458c5564-x5k4w      1/1     Running   0          6h17m
nginx-https-deployment-5f665f49fb-sqcvc   1/1     Running   0          174m
nginx-storage-pod                         1/1     Running   0          6h28m
simple-nginx-544dd54c77-cggm4             1/1     Running   0          72m
web-0                                     1/1     Running   0          8m36s
web-1                                     1/1     Running   0          49m
web-2                                     1/1     Running   0          3m12s
web-3                                     1/1     Running   0          2m44s
web-4                                     1/1     Running   0          2m17s

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get pods
NAME                                      READY   STATUS    RESTARTS   AGE
my-first-pod                              1/1     Running   0          10h
my-first-pod-nginx                        1/1     Running   0          8h
nginx-deployment-585797d45f-4k6wf         1/1     Running   0          8h
nginx-deployment-585797d45f-hbprl         1/1     Running   0          8h
nginx-deployment-585797d45f-xnl6p         1/1     Running   0          8h
nginx-deployment-pvc-9458c5564-x5k4w      1/1     Running   0          6h18m
nginx-https-deployment-5f665f49fb-sqcvc   1/1     Running   0          175m
nginx-storage-pod                         1/1     Running   0          6h28m
simple-nginx-544dd54c77-cggm4             1/1     Running   0          73m
web-0                                     1/1     Running   0          9m7s
web-1                                     1/1     Running   0          49m
web-2                                     1/1     Running   0          3m43s
web-3                                     1/1     Running   0          3m15s
web-4                                     1/1     Running   0          2m48s


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get svc
NAME                   TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)                      AGE
nginx-https-service    LoadBalancer   100.64.238.60    34.140.75.240   80:32388/TCP,443:31228/TCP   130m
nginx-service          LoadBalancer   100.69.230.189   34.78.249.22    80:31045/TCP                 8h
simple-nginx-service   ClusterIP      100.71.24.235    <none>          80/TCP                       74m
stateful-nginx         ClusterIP      None             <none>          80/TCP                       51m


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG describe svc stateful-nginx
Name:              stateful-nginx
Namespace:         part-0013
Labels:            app=stateful-nginx
Annotations:       <none>
Selector:          app=stateful-nginx
Type:              ClusterIP
IP Family Policy:  SingleStack
IP Families:       IPv4
IP:                None
IPs:               None
Port:              web  80/TCP
TargetPort:        80/TCP
Endpoints:         100.96.1.209:80,100.96.1.211:80,100.96.2.193:80 + 2 more...
Session Affinity:  None
Events:            <none>











Step 4 (optional): rolling update with canary
Statefulsets support advanced mechanisms to update to a new version (i.e. of the used container image). 
For this exercise, you will add an update strategy to your StatefulSet and perform an update with one pod serving as canary before moving all of your replicas to the new version.

Firstly increase the number of replicas to 3. Then continue by patching your Statefulset. 
The partition parameter controls the replicas that are patched based on an "equals or greater" evaluation of the ordinal index of the replica. 
If you have 3 replicas [0,1,2], a partition parameter with value "2" will limit the effect of an update to replica #2 only.

kubectl patch statefulset web -p '{"spec":{"updateStrategy":{"type":"RollingUpdate","rollingUpdate":{"partition":2}}}}'

Examine the result (get -o yaml) or continue with the next step. Start a watch for the pods in you namespace. 
Then again, use the json path with the patch command to change the image version in your podSpec template:

kubectl patch statefulset web --type='json' -p='[{"op": "replace", "path": "/spec/template/spec/containers/0/image", "value":"nginx:1.13.12"}]'

Observe, how the pod web-2 will be terminated and re-created. Check the image version of the updated pod:

kubectl get po web-2 --template '{{range $i, $c := .spec.containers}}{{$c.image}}{{end}}'

Once you tested the canary and want to move all replicas to the new version, move "partition" to "0".



james@lizard:~> kubectl patch statefulset web -p '{"spec":{"updateStrategy":{"type":"RollingUpdate","rollingUpdate":{"partition":2}}}}'
statefulset.apps/web patched

james@lizard:~> kubectl patch statefulset web --type='json' -p='[{"op": "replace", "path": "/spec/template/spec/containers/0/image", "value":"nginx:1.13.12"}]'
statefulset.apps/web patched

james@lizard:~> kubectl get po web-2 --template '{{range $i, $c := .spec.containers}}{{$c.image}}{{end}}'






















Troubleshooting

In this exercise all the network traffic happens cluster internally. That's also why you have to create a helper pod and connect to it. Only then you have access to the cluster network and can contact cluster DNS to resolve names.

Note that the service needs to be of type: ClusterIP AND has to specify the field clusterIP: None. Anything else than ClusterIP is not valid or allowed in this specific combination. To expose pods of a StatefulSet create a regular service with an actual cluster IP.

To be able to use the headless service in combination with the pod names for DNS, the service has to be specified as part of the statefulset resource: kubectl explain statefulset.spec.serviceName


Further information & references
	• statefulset documentation https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/
	• cassandara deployed as a statefulset https://kubernetes.io/docs/tutorials/stateful-application/cassandra/
	• init containers https://kubernetes.io/docs/concepts/workloads/pods/init-containers/
	• debugging of init containers https://kubernetes.io/docs/tasks/debug-application-cluster/debug-init-containers/

```
## Network Policy

```
Exercise 9 - Network Policy

In this exercise, you will be dealing with Pods, Deployments, Labels & Selectors, Services and Network Policies.

Network policies in your namespace help you restrict access to your nginx deployment. 
From within any pod that is not labeled correctly you will not be able to access your nginx instances.

Note: This exercise loosely builds on the previous exercises as you will need a deployment and a service. 
In case you do not have a deployment with a service ready because you did not manage to finish exercise 5, use the script prereq-exercise-06.sh in the solutions folder. 
Please use this script only if you do not have a working deployment that has been exposed through a service.


Step 0: verify the setup
Before you deploy a network policy, check the connection from a random pod to the nginx pods via the service.

Start an alpine image and connect to it. Try to re-use the storage-pod.yaml from exercise 05 but without the volumes and mounts. 
Use the exec command to open a shell session into it. 
Alternatively spin up a a temporary deployment with kubectl run tester -i --tty --restart=Never --rm --image=alpine:3.12 -- ash.

Do you remember, that your service name is also a valid DNS name? 
Instead of using an IP address to connect to your service, you can use its actual name (like nginx-https).

Run wget --timeout=1 -q -O - <your-service-name> from within the pod to send an HTTP request to the nginx service.

If everything works fine, the result should look like this (maybe with a different service name):
# wget --timeout=1 -q -O - nginx-https
Connecting to nginx (10.7.249.39:80)

It proves the network connection to the pods masked by the service is working properly.


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get service
NAME                   TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)                      AGE
nginx-https-service    LoadBalancer   100.64.238.60    34.140.75.240   80:32388/TCP,443:31228/TCP   23h
nginx-service          LoadBalancer   100.69.230.189   34.78.249.22    80:31045/TCP                 29h
simple-nginx-service   ClusterIP      100.71.24.235    <none>          80/TCP                       23h
stateful-nginx         ClusterIP      None             <none>          80/TCP                       22h

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG run tester -i --tty --restart=Never --rm --image=alpine:3.12 -- ash
If you don't see a command prompt, try pressing enter.
/ # wget --timeout=1 -q -O - simple-nginx-service
This is a simple nginx!
/ #






Step 1: create a network policy
To restrict the access, you are going to create a NetworkPolicy resource.

The network policy features two selector sections:
	• networkpolicy.spec.podSelector.matchLabels determines the target pods -> traffic to all matching pods will be filtered (allow or drop)
	• networkpolicy.spec.ingress.from lists the sources, from which traffic is accepted. There are different ways to identify trusted sources
		○ by podSelector.matchLabels - to filter for labels of pods in the same namespace
		○ by namespaceSelector.matchLabels- to filter for traffic from a specific namespace (can be combined with podSelector)
		○ by ipBlock.cidr - an IP address range defined as trustworthy

Use the snippet below and fill in the correct values for the matchLabels selector.

Hint: you can take a look at the nginx service with -o yaml to get correct labels.
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: access-nginx
spec:
  podSelector:
    matchLabels:
      ???: ???
  ingress:
  - from:
    - podSelector:
        matchLabels:
          access: "true"
# allow access originating from SAP networks
    - ipBlock:
        # Germany WDF
        cidr: 155.56.0.0/16
    - ipBlock:
        # Germany WDF
        cidr: 193.16.224.0/24
    - ipBlock:
        # Ireland
        cidr: 84.203.229.48/29
    - ipBlock:
        # Palo Alto
        cidr: 169.145.89.192/26
    - ipBlock:
        # Montreal
        cidr: 68.67.33.0/25
    - ipBlock:
        # Montreal
        cidr: 208.49.239.224/28

If you're location is not on the list, check with your trainer to get the address blocks. 
You can also check the network information portal and search for your location.

If you are unsure about the labels, run the queries you are about to implement manually - e.g. kubectl get pods -l <my-ke>=<my-value>. 
This way you can check, if the results match your intention.

Create the resource as usual with kubectl apply -f <your file>.yaml and check its presence with kubectl get networkpolicy.



james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get networkpolicy
No resources found in part-0013 namespace

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG create -f /opt/docker-k8s-training/kubernetes/ex09/09_network_policy_ingress.yaml
networkpolicy.networking.k8s.io/access-nginx created

james@lizard:~> kubectl --kubeconfig=$KUBECONFIG get networkpolicy
NAME           POD-SELECTOR   AGE
access-nginx   run=nginx      4s



Step 2: Trying to connect, please wait ...

Again, connect to the busybox pod you used in step 0 or spin up a new one. Run the same wget command and check the output.

As the network policy is in place now, it should report a timeout: wget: download timed out


james@lizard:~> kubectl --kubeconfig=$KUBECONFIG run tester -i --tty --restart=Never --rm --image=alpine:3.12 -- ash
If you don't see a command prompt, try pressing enter.
/ # wget --timeout=1 -q -O - simple-nginx-service
This is a simple nginx!
/ #










Step 3: Regain access

To regain access you need to add the corresponding label to the pod from which you want to access the nginx service. The label has to match the spec.ingress.from.podSelector.matchLabels key-value pair specified in the network policy.

Use kubectl label ... or add a -l <key>=<value> to the run command. Then connect again to the pod and run wget. It should give you the same result as in step 0.


Troubleshooting

If you're having trouble regaining or limiting access, check the label selectors in use. A network policy often uses the same selectors as the service to identify, the target pods to which traffic management should apply.

When it comes to networkpolicy.spec.ingress.from, note that it is explicit whitelisting of trusted sources. So if your traffic originates from a different source (like a different external IP address), it will be dropped. Make sure that your temporary helper pod has the labels which are specified in networkpolicy.spec.ingress.from.podSelector.matchLabels.


Further information & references

    network policy basics  https://kubernetes.io/docs/concepts/services-networking/network-policies/
    example / tutorial on network policies  https://kubernetes.io/docs/tasks/administer-cluster/declare-network-policy/

```
## Helming

```
Exercise 10: Happy Helming

In this exercise, you will be dealing with Helm.

Helm is a tool to manage complex deployments of multiple components belonging to the same application stack. In this exercise, you will install the helm client locally. Once this is working you will deploy your first chart into your namespace. For further information, visit the official docs pages (https://docs.helm.sh/)

Note: This exercise does not build on any of the previous exercises.



Step 0: get the helm tool

Download and unpack the helm client:

curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash

Check, if everything worked well. The 1st command should return the location of the helm binary. The 2nd command should return the version of the client.

which helm
helm version

Step 1: no need to initialize helm (anymore)

The helm client uses the information stored in .kube/config to talk to the kubernetes cluster. This includes the user, its credentials but also the target namespace. Restrictions such as RBAC or pod security policies, which apply to your user, also apply to everything you try to install using helm.

And that's it - helm is ready to use!

Compared to the previous v2 setup procedure, this is a significant improvement. The server-side component tiller has been removed completely.



Step 2: looking for charts?

Helm organizes applications in so called charts, which contain parameters you can set during installation. By default, helm (v3) is not configured to search any remote repository for charts. So as a first step, add the stable repository, which hosts charts maintained on github.com.

helm repo add stable https://charts.helm.sh/stable

helm repo list

Check out the available charts and search for the chaoskube:

helm search repo chaoskube

Found it? Check the github page for a detailed description of the chart.

Of course, there are other ways to find charts. You can go to charts org on github and take a look into the stable, test or incubator repositories. This is also where you find the yaml / template files of charts.

Note: The charts repo is officially deprecated. The helm organization recently created Artifact Hub. It is a very convenient way to search for a chart and lets you access multiple / different repositories at once (like stable or incubator). However, not all charts from the former stable repo have been migrated (e.g. chaoskube is not yet availalbe).



Step 3: install a chart

Run the following command to install the chaoskube chart. It installs everything that is associated with the chart into your namespace. Note the --set flags, which specify parameters of the chart.

helm install <any-name> stable/chaoskube --set namespaces=<your-namespace> --set rbac.serviceAccountName=chaoskube --debug

The parameter namespaces defines in which namespaces the chaoskube will delete pods. rbac.serviceAccountName specifies which serviceAccount the scheduled chaoskube pod will use. Here we give it the chaoskube account, which has been created as part of the cluster setup already. This is mainly because chaoskube wants to query pods across all namespaces - which requires a ClusterRoleBinding to the ClusterRole training:cluster-view. As participants are not allowed to modify resources on cluster level, it is part of the setup to prepare for this exercise. If you want to know more defails, take a look at the kubecfggen script.

To learn more about the configuration options the chaoskube chart provides, check again the github page mentioned above.



Step 4: inspect your chaoskube

Next, check your installation by running helm list. It returns all installed releases including your chaoskube. You can reference it by its name. Get more information by running helm status <your-releases-name>

Also check the pods running inside your kubernetes namespace. Don't forget to look into the logs of the chaoskube to see what would have happened with the dry-run flag set. kubectl logs -f pod/<your chaoskube-pod-name>



Step 5: clean up

Clean up by deleting the chaoskube release: helm delete <your-releases-name>

Now run helm list again to verify there are no leftovers.

```
## Bulletinboard

```
Exercises
01 Exercise: "Build and Push the Docker Images"

    Build and push the docker images for bulletinboard-ads and bulletinboard-reviews.
    Create an ImagePullSecret for the training-registry.

02 Exercise: "Setup Bulletinboard-Ads Database"

    Database will run as a Statefulset secured with a password: Create a Secret for the password.
    Create a Statefulset for the Ads DB together with a headless Service.

03 Exercise: "Setup Bulletinboard-Ads Application"

    Create required Configmap
    Create Deployment for Ads App, using the Configmap and the Secret of the DB.
    Publish Ads App via Service and Ingress

04 Exercise: "Using Helm-chart to setup Bulletinboard-Reviews

    Deploy Bulletinboard-Reviews via existing Helm chart

05 Exercise: "Networkpolicies & TLS for Bulletinboard-Ads"

    Increase security and establish a Network policy for
        Bulletinboard-Ads Database
        Bulletinboard-Ads App
    Enable HTTPS connection by adding TLS certificates to Ingress

Troubleshooting section

Since we are using the master branch, there is a slight chance that a new commit has broken the basic functionality. In case you run into any issues you can use a commit, which is tested, to build the docker images from:
Bulletinboard-Ads

git checkout ac5ddd541d6d7d8aa0ac645ab8e865e1eb483453

Bulletinboard-Reviews

git checkout 561848ef786cfe6ebad3dcb0144b040fe7239cb2

```













