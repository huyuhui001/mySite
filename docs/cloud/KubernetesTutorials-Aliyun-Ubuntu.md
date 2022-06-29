# Kubernetes Tutourials: Ubuntu@Aliyun

## Deployment

### Preparation

Register Aliyun account via [Alibaba Cloud home console](https://home.console.aliyun.com/home/dashboard/ProductAndService).

Request three Elastic Computer Service(ECS) instances with below sizing:

* System: 2vCPU+4GiB
* OS: Ubuntu  20.04 x86_64
* Instance Type: ecs.sn1.medium 
* Instance Name: cka001, cka002, cka003
* Network: both public IPs and private IPs
* Maximum Bandwidth: 100Mbps (Peak Value)
* Cloud disk: 40GiB
* Billing Method: Preemptible instance (spot price)

Generate SSH key pairs with name `cka-key-pair` in local directcory `/opt`.

Change access control to `400` per security required by command `sudo chmod 400 cka-key-pair.pem`.
cka003
Access remote cka servers via command `ssh -i cka-key-pair.pem root@<your public ip address>`


### Initialize VMs


#### Configure /etc/hosts file
Add private IPs in the `/etc/hosts` file in all VMs.

#### Disable firewall

Disable firewall by command `ufw disable` in all VMs.

### Turn off swap

Turn off swap by command `swapoff -a` in all VMs.

### Set timezone and locale

Set timezone and local for all VMs. For ECS with Ubuntu 20.04 version created by Aliyun, this step is not needed.
```
# ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
# sudo echo 'LANG="en_US.UTF-8"' >> /etc/profile
# source /etc/profile
```
Something like this:
```
root@cka001:~# ll /etc/localtime
lrwxrwxrwx 1 root root 33 May 24 18:14 /etc/localtime -> /usr/share/zoneinfo/Asia/Shanghai
```

### Kernel setting

Perform below kernel setting in all VMs.

Create file `/etc/modules-load.d/containerd.conf` to set up containerd configure file.
It's to load two modules `overlay` and `br_netfilter`.

Service `containerd` depends on `overlay` filesystem. Sometimes referred to as union-filesystems. An [overlay-filesystem](https://developer.aliyun.com/article/660712) tries to present a filesystem which is the result over overlaying one filesystem on top of the other. 

The `br_netfilter` module is required to enable transparent masquerading and to facilitate Virtual Extensible LAN (VxLAN) traffic for communication between Kubernetes pods across the cluster. 
```
# cat <<EOF | sudo tee /etc/modules-load.d/containerd.conf
overlay
br_netfilter
EOF
```

Load `overlay` and `br_netfilter` modules.
```
# sudo modprobe overlay
# sudo modprobe br_netfilter
```

Create file `99-kubernetes-cri.conf` to set up configure file for Kubernetes CRI.

Set `net/bridge/bridge-nf-call-iptables=1` to ensure simple configurations (like Docker with a bridge) work correctly with the iptables proxy. [Why `net/bridge/bridge-nf-call-iptables=1` need to be enable by Kubernetes](https://cloud.tencent.com/developer/article/1828060).

IP forwarding is also known as routing. When it comes to Linux, it may also be called Kernel IP forwarding because it uses the kernel variable `net.ipv4.ip_forward` to enable or disable the IP forwarding feature. The default preset value is `ip_forward=0`. Hence, the Linux IP forwarding feature is disabled by default.
```
# cat <<EOF | sudo tee /etc/sysctl.d/99-kubernetes-cri.conf
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF
```

The `sysctl` command reads the information from the `/proc/sys` directory. `/proc/sys` is a virtual directory that contains file objects that can be used to view and set the current kernel parameters.

By commadn `sysctl -w net.ipv4.ip_forward=1`, the change takes effect immediately, but it is not persistent. After a system reboot, the default value is loaded. Write the settings to `/etc/sysctl.conf` is to set a parameter permanently, you’ll need to  or another configuration file in the /etc/sysctl.d directory:
```
sudo sysctl --system
```


### Install Containerd

Install Containerd sevice fro all VMs.

Backup source file.
```
# sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
```

Add proper repo sources. For ECS with Ubuntu 20.04 version created by Aliyun, this step is not needed.
```
cat > /etc/apt/sources.list << EOF
deb http://mirrors.cloud.aliyuncs.com/ubuntu/ focal main restricted
deb-src http://mirrors.cloud.aliyuncs.com/ubuntu/ focal main restricted
deb http://mirrors.cloud.aliyuncs.com/ubuntu/ focal-updates main restricted
deb-src http://mirrors.cloud.aliyuncs.com/ubuntu/ focal-updates main restricted
deb http://mirrors.cloud.aliyuncs.com/ubuntu/ focal universe
deb-src http://mirrors.cloud.aliyuncs.com/ubuntu/ focal universe
deb http://mirrors.cloud.aliyuncs.com/ubuntu/ focal-updates universe
deb-src http://mirrors.cloud.aliyuncs.com/ubuntu/ focal-updates universe
deb http://mirrors.cloud.aliyuncs.com/ubuntu/ focal multiverse
deb-src http://mirrors.cloud.aliyuncs.com/ubuntu/ focal multiverse
deb http://mirrors.cloud.aliyuncs.com/ubuntu/ focal-updates multiverse
deb-src http://mirrors.cloud.aliyuncs.com/ubuntu/ focal-updates multiverse
deb http://mirrors.cloud.aliyuncs.com/ubuntu/ focal-backports main restricted universe multiverse
deb-src http://mirrors.cloud.aliyuncs.com/ubuntu/ focal-backports main restricted universe multivers
deb http://mirrors.cloud.aliyuncs.com/ubuntu focal-security main restricted
deb-src http://mirrors.cloud.aliyuncs.com/ubuntu focal-security main restricted
deb http://mirrors.cloud.aliyuncs.com/ubuntu focal-security universe
deb-src http://mirrors.cloud.aliyuncs.com/ubuntu focal-security universe
# deb http://mirrors.cloud.aliyuncs.com/ubuntu focal-security multiverse
# deb-src http://mirrors.cloud.aliyuncs.com/ubuntu focal-security multiverse
EOF
```

Install Containered.
```
# sudo apt-get update && sudo apt-get install -y containerd
```

Configure Containerd. Modify file `/etc/containerd/config.toml`.
```
# sudo mkdir -p /etc/containerd
# containerd config default | sudo tee /etc/containerd/config.toml
# vi /etc/containerd/config.toml
```

Update `sandbox_image` with new value `"registry.aliyuncs.com/google_containers/pause:3.6"`.
Update `SystemdCgroup ` with new value `true`.
```
[plugins]
  [plugins."io.containerd.gc.v1.scheduler"]

  [plugins."io.containerd.grpc.v1.cri"]
    sandbox_image = "registry.aliyuncs.com/google_containers/pause:3.6"
    
    [plugins."io.containerd.grpc.v1.cri".cni]
    [plugins."io.containerd.grpc.v1.cri".containerd]
      [plugins."io.containerd.grpc.v1.cri".containerd.default_runtime]
        [plugins."io.containerd.grpc.v1.cri".containerd.default_runtime.options]
      [plugins."io.containerd.grpc.v1.cri".containerd.runtimes]
        [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]

          [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
            SystemdCgroup = true
```

Restart Containerd service.
```
# sudo systemctl restart containerd
# sudo systemctl status containerd
```

  
### Install nerdctl

Install nerdctl sevice fro all VMs.

The goal of [`nerdctl`](https://github.com/containerd/nerdctl) is to facilitate experimenting the cutting-edge features of containerd that are not present in Docker.

```
# wget https://github.com/containerd/nerdctl/releases/download/v0.21.0/nerdctl-0.21.0-linux-amd64.tar.gz
# tar -zxvf nerdctl-0.21.0-linux-amd64.tar.gz
# cp nerdctl /usr/bin/
```

Verify nerdctl.
```
# nerdctl --help
```

To list local Kubernetes containers.
```
# nerdctl -n k8s.io ps
```


### Install kubeadm

Update `apt-transport-https`,  `ca-certificates`, and `curl`.
```
# apt-get update && sudo apt-get install -y apt-transport-https ca-certificates curl
```

Install gpg certificate.
```
# curl https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg | apt-key add -
```

Add Kubernetes repo.
```
# cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main
EOF
```

Update  and install dependencied packages.
```
# apt-get update
# apt-get install ebtables
# apt-get install libxtables12=1.8.4-3ubuntu2
# apt-get upgrade iptables
```

Check available versions of kubeadm.
```
# apt policy kubeadm
```

Install `1.23.8-00` version of kubeadm and will upgrade to `1.24.2` later.
```
# sudo apt-get -y install kubelet=1.23.8-00 kubeadm=1.23.8-00 kubectl=1.23.8-00 --allow-downgrades
```


### Setup Master Node

Set up Control Plane on VM playing master node.

Check kubeadm default parameters for initialization.
```
# kubeadm config print init-defaults
```

Dry rune and run. Save the output, which will be used later on work nodes.
Be noted that `10.244.0.0/16` is default range of flannel. If it's changed here, please do change the same when deploy flannel. 
```
# kubeadm init --dry-run --pod-network-cidr=10.244.0.0/16 --image-repository=registry.aliyuncs.com/google_containers --kubernetes-version=v1.23.8

# kubeadm init --pod-network-cidr=10.244.0.0/16 --image-repository=registry.aliyuncs.com/google_containers --kubernetes-version=v1.23.8

```

Set `kubeconfig` file for current user (here it's `root`).
```
# mkdir -p $HOME/.kube
# sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
# sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

Set `kubectl` auto-completion.
```
# apt install -y bash-completion
# source /usr/share/bash-completion/bash_completion
# source <(kubectl completion bash)
# echo "source <(kubectl completion bash)" >> ~/.bashrc
```




### Setup Work Nodes

Perform on all VMs playing work nodes.
```
# kubeadm join <your master node eth0 ip>:6443 --token <token generated by kubeadm init> --discovery-token-ca-cert-hash <hash key generated by kubeadm init>
```


Verify status on master node.
```
root@cka001:~# kubectl get node
NAME     STATUS   ROLES                  AGE     VERSION
cka001   Ready    control-plane,master   24m     v1.23.8
cka002   Ready    <none>                 9m39s   v1.23.8
cka003   Ready    <none>                 9m27s   v1.23.8
```

### Install Flannel

[Flannel](https://github.com/flannel-io/flannel) is a simple and easy way to configure a layer 3 network fabric designed for Kubernetes.

Deploy Flannel on master node.
In the kube-flannel.yml we can get the default network setting of Flannel, which is same with `--pod-network-cidr=10.244.0.0/16` we defined before when we initiated `kubeadm`.
```
  net-conf.json: |
    {
      "Network": "10.244.0.0/16",
      "Backend": {
        "Type": "vxlan"
      }
    }
```
```
root@cka001:~# kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
Warning: policy/v1beta1 PodSecurityPolicy is deprecated in v1.21+, unavailable in v1.25+
podsecuritypolicy.policy/psp.flannel.unprivileged created
clusterrole.rbac.authorization.k8s.io/flannel created
clusterrolebinding.rbac.authorization.k8s.io/flannel created
serviceaccount/flannel created
configmap/kube-flannel-cfg created
daemonset.apps/kube-flannel-ds created
```


### Check Cluster Status

Perform `kubectl cluster-info` command on master node we will get below information.

* Kubernetes control plane is running at https://<mster node ip>:6443
* CoreDNS is running at https://<mster node ip>:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

```
# kubectl cluster-info
# kubectl get nodes -owide
# kubectl get pod -A
```


### Reset cluster

CAUTION: below steps will destroy current cluster. 

Delete all nodes in the cluster.
```
# kubeadm reset
```

Clean up rule of `iptables`.
```
# iptables -F && iptables -t nat -F && iptables -t mangle -F && iptables -X
```

Clean up rule of `IPVS` if using `IPVS`.
```
# ipvsadm --clear
```


## Snapshot of deployment

Till now, the initial deployment is completed sucessfully.

### Container Layer
We are using Containerd service to manage our images and containers via command `nerdctl`.

Get current namespaces.
```
root@cka001:~# nerdctl namespace ls
NAME      CONTAINERS    IMAGES    VOLUMES    LABELS
k8s.io    18            27        0  
```

Get containers under the namespace `k8s.io` by command `nerdctl -n k8s.io ps`.
```
root@cka001:~# nerdctl -n k8s.io container ls
CONTAINER ID    IMAGE                                                                      COMMAND                   CREATED         STATUS    PORTS    NAMES
1eb9a51e0406    registry.aliyuncs.com/google_containers/kube-apiserver:v1.23.8             "kube-apiserver --ad…"    28 hours ago    Up                 k8s://kube-system/kube-apiserver-cka001/kube-apiserver                      
1ebee10176c4    registry.aliyuncs.com/google_containers/kube-proxy:v1.23.8                 "/usr/local/bin/kube…"    28 hours ago    Up                 k8s://kube-system/kube-proxy-v7rsr/kube-proxy                               
2c5e1d183fc7    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  28 hours ago    Up                 k8s://kube-system/kube-apiserver-cka001                                     
2dd9743cecad    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  27 hours ago    Up                 k8s://kube-system/kube-flannel-ds-rf54c                                     
39306eef76cd    docker.io/rancher/mirrored-flannelcni-flannel:v0.18.1                      "/opt/bin/flanneld -…"    27 hours ago    Up                 k8s://kube-system/kube-flannel-ds-rf54c/kube-flannel                        
3ca6fdda63a5    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  28 hours ago    Up                 k8s://kube-system/kube-scheduler-cka001                                     
49e07d9b2b98    registry.aliyuncs.com/google_containers/coredns:v1.8.6                     "/coredns -conf /etc…"    27 hours ago    Up                 k8s://kube-system/coredns-6d8c4cb4d-9khd8/coredns                           
555a3bf58832    registry.aliyuncs.com/google_containers/kube-scheduler:v1.23.8             "kube-scheduler --au…"    28 hours ago    Up                 k8s://kube-system/kube-scheduler-cka001/kube-scheduler                      
5812c42bf572    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  28 hours ago    Up                 k8s://kube-system/etcd-cka001                                               
8619e3c979a3    registry.aliyuncs.com/google_containers/coredns:v1.8.6                     "/coredns -conf /etc…"    27 hours ago    Up                 k8s://kube-system/coredns-6d8c4cb4d-qcp2l/coredns                           
a9459900f462    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  27 hours ago    Up                 k8s://kube-system/coredns-6d8c4cb4d-9khd8                                   
bb2b4624bfd5    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  27 hours ago    Up                 k8s://kube-system/coredns-6d8c4cb4d-qcp2l                                   
c9462709baff    registry.aliyuncs.com/google_containers/kube-controller-manager:v1.23.8    "kube-controller-man…"    28 hours ago    Up                 k8s://kube-system/kube-controller-manager-cka001/kube-controller-manager    
e68c3fbc90f9    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  28 hours ago    Up                 k8s://kube-system/kube-proxy-v7rsr                                          
eae550221813    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  28 hours ago    Up                 k8s://kube-system/kube-controller-manager-cka001                            
ff6626664c43    registry.aliyuncs.com/google_containers/etcd:3.5.1-0                       "etcd --advertise-cl…"    28 hours ago    Up                 k8s://kube-system/etcd-cka001/etcd     
```

Some management and commands options of `nertctl`.
```
root@cka001:~# nertctl --help
root@cka001:~# nerdctl image ls -a
root@cka001:~# nerdctl volume ls
root@cka001:~# nerdctl stats
```

Get below network list with command `nerdctl network ls` in Containerd layer.
```
root@cka001:~# nerdctl network ls
NETWORK ID    NAME      FILE
              cbr0      /etc/cni/net.d/10-flannel.conflist
0             bridge    /etc/cni/net.d/nerdctl-bridge.conflist
              host      
              none  
```

Get network interface in host `cka001` with command `ip addr list`.
```
lo               : inet 127.0.0.1/8 qlen 1000
eth0             : inet 172.16.18.161/24 brd 172.16.18.255 qlen 1000
flannel.1        : inet 10.244.0.0/32
cni0             : inet 10.244.0.1/24 brd 10.244.0.255 qlen 1000
vethb0a35696@if3 : noqueue master cni0
veth72791f64@if3 : noqueue master cni0
```


### Kubernetes Layer

Kubernetes is beyond container layer above. 

In Kubernetes layer, we have three nodes, `cka001`, `cka002`, and `cka003`.
```
root@cka001:~# kubectl get node
NAME     STATUS   ROLES                  AGE   VERSION
cka001   Ready    control-plane,master   27h   v1.23.8
cka002   Ready    <none>                 27h   v1.23.8
cka003   Ready    <none>                 27h   v1.23.8
```

We have four initial namespaces across three nodes.
```
root@cka001:~# kubectl get namespace -A
NAME              STATUS   AGE
default           Active   27h
kube-node-lease   Active   27h
kube-public       Active   27h
kube-system       Active   27h
```

We have some initial pods. 
```
root@cka001:~# kubectl get pod -A -o wide
NAMESPACE     NAME                             READY   STATUS    RESTARTS   AGE   IP              NODE     NOMINATED NODE   READINESS GATES
kube-system   coredns-6d8c4cb4d-9khd8          1/1     Running   0          27h   <cni0 IP>       cka001   <none>           <none>
kube-system   coredns-6d8c4cb4d-qcp2l          1/1     Running   0          27h   <cni0 IP>       cka001   <none>           <none>
kube-system   etcd-cka001                      1/1     Running   0          27h   <eth0 IP>       cka001   <none>           <none>
kube-system   kube-apiserver-cka001            1/1     Running   0          27h   <eth0 IP>       cka001   <none>           <none>
kube-system   kube-controller-manager-cka001   1/1     Running   0          27h   <eth0 IP>       cka001   <none>           <none>
kube-system   kube-flannel-ds-hfvf7            1/1     Running   0          27h   <eth0 IP>       cka003   <none>           <none>
kube-system   kube-flannel-ds-m5mdl            1/1     Running   0          27h   <eth0 IP>       cka002   <none>           <none>
kube-system   kube-flannel-ds-rf54c            1/1     Running   0          27h   <eth0 IP>       cka001   <none>           <none>
kube-system   kube-proxy-bj75j                 1/1     Running   0          27h   <eth0 IP>       cka002   <none>           <none>
kube-system   kube-proxy-gxjj4                 1/1     Running   0          27h   <eth0 IP>       cka003   <none>           <none>
kube-system   kube-proxy-v7rsr                 1/1     Running   0          27h   <eth0 IP>       cka001   <none>           <none>
kube-system   kube-scheduler-cka001            1/1     Running   0          27h   <eth0 IP>       cka001   <none>           <none>
```

Summary below shows the relationship between containers and pods. 
Good references about container pause: [article](https://zhuanlan.zhihu.com/p/464712164) and [artical](https://cloud.tencent.com/developer/article/1583919).

* Master node:
    * CoreDNS: 2 pods, 2 containers of each pod
        * From image `coredns:v1.8.6`:
            * k8s://kube-system/coredns-6d8c4cb4d-9khd8/coredns
            * k8s://kube-system/coredns-6d8c4cb4d-qcp2l/coredns
        * By image `pause:3.6`
            * k8s://kube-system/coredns-6d8c4cb4d-9khd8
            * k8s://kube-system/coredns-6d8c4cb4d-qcp2l
    * etcd: 1 pod, 2 containers
        * By image `etcd:3.5.1-0`
            * k8s://kube-system/etcd-cka001/etcd
        * By image `pause:3.6`
            * k8s://kube-system/etcd-cka001
    * apiserver: 1 pod, 2 containers
        * By image `kube-apiserver:v1.23.8`
            * k8s://kube-system/kube-apiserver-cka001/kube-apiserver
        * By image `pause:3.6`
            * k8s://kube-system/kube-apiserver-cka001
    * controller-manager: 1 pod, 2 containers
        * By image `kube-controller-manager:v1.23.8`
            * k8s://kube-system/kube-controller-manager-cka001/kube-controller-manager
        * By image `pause:3.6`
            * k8s://kube-system/kube-controller-manager-cka001
    * scheduler: 1 pod, 2 containers
        * By image `kube-scheduler:v1.23.8`
            * k8s://kube-system/kube-scheduler-cka001/kube-scheduler
        * By image `pause:3.6`
            * k8s://kube-system/kube-scheduler-cka001
* All nodes:
    * Flannel DS: 1 pod of each, 2 containers of each pod
        * By image `mirrored-flannelcni-flannel:v0.18.1`
            * k8s://kube-system/kube-flannel-ds-rf54c/kube-flannel
        * By image `pause:3.6`
            * k8s://kube-system/kube-flannel-ds-rf54c
    * Proxy: 1 pod of each, 2 containers of each pod
        * By image `kube-proxy:v1.23.8`
            * k8s://kube-system/kube-proxy-v7rsr/kube-proxy
        * By image `pause:3.6`
            * k8s://kube-system/kube-proxy-v7rsr


Let's check current configuration context of Kubernetes we just initialized. 

* Contenxt name is `kubernetes-admin@kubernetes`.
* Cluster name is `kubernetes`.
* User is `kubernetes-admin`.
* No namespace explicitly defined.

```
root@cka001:~# kubectl config get-contexts
CURRENT   NAME                          CLUSTER      AUTHINFO           NAMESPACE
*         kubernetes-admin@kubernetes   kubernetes   kubernetes-admin 
```

Create a new namespace `jh-namespace`.
```
root@cka001:~# kubectl create namespace jh-namespace
```

Update current context `kubernetes-admin@kubernetes` with new namespace `jh-namespace` as default namespace. 
```
root@cka001:~# kubectl config set-context kubernetes-admin@kubernetes --cluster=kubernetes --namespace=jh-namespace --user=kubernetes-admin 
```

Now default namespace is shown in current configuration context. 
```
root@cka001:~# kubectl config get-contexts
CURRENT   NAME                          CLUSTER      AUTHINFO           NAMESPACE
*         kubernetes-admin@kubernetes   kubernetes   kubernetes-admin   jh-namespace
```

Let's execute command `kubectl apply -f 02-sample-pod.yaml` to create a pod `my-first-pod` on namespace `jh-namespace` with below content of file `02-sample-pod.yaml`.
```
apiVersion: v1
kind: Pod
metadata:
  name: my-first-pod
spec:
  containers:
  - name: nginx
    image: nginx:mainline
    ports:
    - containerPort: 80
```

By command `kubectl get pod -o wide` we get the pod status.

The pod's ip is allocated by `cni0`. Node is assigned by `Scheduler`. 

We can also find related containers of pod `my-first-pod` via command `nerdctl -n k8s.io container ls` on `cka003`.

```
root@cka001:~# kubectl get pod -o wide
NAME           READY   STATUS    RESTARTS   AGE   IP           NODE     NOMINATED NODE   READINESS GATES
my-first-pod   1/1     Running   0          19s   10.244.2.2   cka003   <none>           <none>
```


### Case Study

Scenario: stop kubelet service on worker node `cka003`.

Question:

* What's the status of each node?
* What's containers changed via command `nerdctl`?
* What's pods status via command `kubectl get pod -owide -A`? 

Demo:

Execute command `systemctl stop kubelet.service` on `cka003`.

Execute command `kubectl get node` on either `cka001` or `cka003`, the status of `cka003` is `NotReady`.

Execute command `nerdctl -n k8s.io container ls` on `cka003` and we can observe all containers are still up and running, including the pod `my-first-pod`.

Execute command `systemctl start kubelet.service` on `cka003`.

Conclusion:

* The node status is changed to `NotReady` from `Ready`.
* For those DaemonSet pods, like `flannel`、`kube-proxy`, are exclusively running on each node. They won't be terminated after `kubelet` is down.
* The status of pod `my-first-pod` keeps showing `Terminating` on each node because status can not be synced to other nodes via `apiserver` from `cka003` because `kubelet` is down.
* The status of pod is marked by `controller` and recycled by `kubelet`.
* When we start kubelet service on `cka003`, the pod `my-first-pod` will be termiated completely on `cka003`.

In addition, let's create a deployment with 3 replicas. Two are running on `cka003` and one is running on `cka002`.
```
root@cka001:~# kubectl get pod -o wide -w
NAME                               READY   STATUS    RESTARTS   AGE    IP           NODE     NOMINATED NODE   READINESS GATES
nginx-deployment-9d745469b-2xdk4   1/1     Running   0          2m8s   10.244.2.3   cka003   <none>           <none>
nginx-deployment-9d745469b-4gvmr   1/1     Running   0          2m8s   10.244.2.4   cka003   <none>           <none>
nginx-deployment-9d745469b-5j927   1/1     Running   0          2m8s   10.244.1.3   cka002   <none>           <none>
```
After we stop kubelet service on `cka003`, the two running on `cka003` are terminated and another two are created and running on `cka002` automatically. 






## kubectl

Three approach to operate Kubernetes cluster:

* via [API](https://kubernetes.io/docs/reference/kubernetes-api/)
* via kubectl
* via Dashboard


Example with `kubectl`:

With Kubernetes 1.23 and lower version, when we create a new namespace, Kubernetes will automatically create a ServiceAccount `default` and a token `default-token-xxxxx`.

We can say that the ServiceAccount `default` is an account under the namespace.

Here is an example of new namespace `jh-namespace` I created.

* ServiceAcccount: `default`
* Token: `default-token-8vrsc`
```
root@cka001:~# kubectl get sa -n jh-namespace
NAME      SECRETS   AGE
default   1         26h

root@cka001:~# kubectl get secrets -n jh-namespace
NAME                  TYPE                                  DATA   AGE
default-token-8vrsc   kubernetes.io/service-account-token   3      26h
```

There is a cluster rule `admin`, and no related rolebinding.
```
root@cka001:~# kubectl get clusterrole admin -n jh-namespace
NAME    CREATED AT
admin   2022-06-25T06:24:44Z

root@cka001:~# kubectl get role admin -n jh-namespace
Error from server (NotFound): roles.rbac.authorization.k8s.io "admin" not found

root@cka001:~# kubectl get role -n jh-namespace
No resources found in jh-namespace namespace.

root@cka001:~# kubectl get rolebinding -n jh-namespace
No resources found in jh-namespace namespace.
```

Let's create a rolebinding `rolebinding-admin` to bind cluster role `admin` to service account `default` in namespapce `jh-namespace`.
Hence service account `default` is granted adminstrator authorization in namespace `jh-namespace`.
```
kubectl create rolebinding <rule> --clusterrole=<clusterrule> --serviceaccount=<namespace>:<name> --namespace=<namespace>
```
```
root@cka001:~# kubectl create rolebinding rolebinding-admin --clusterrole=admin --serviceaccount=jh-namespace:default --namespace=jh-namespace
rolebinding.rbac.authorization.k8s.io/rolebinding-admin created

root@cka001:~# kubectl get rolebinding -n jh-namespace
NAME                ROLE                AGE
rolebinding-admin   ClusterRole/admin   39s
```

Get token of the service account `default`.
```
root@cka001:~# TOKEN=$(kubectl describe secret $(kubectl get secrets | grep default | cut -f1 -d ' ') | grep -E '^token' | cut -f2 -d':' | tr -d ' ')
root@cka001:~# echo $TOKEN
```

Get API Service address.
```
root@cka001:~# APISERVER=$(kubectl config view | grep https | cut -f 2- -d ":" | tr -d " ")
root@cka001:~# echo $APISERVER
```

Get pod resources in namespace `jh-namespace` via API server with JSON layout.
```
root@cka001:~# curl $APISERVER/api/v1/namespaces/jh-namespace/pods --header "Authorization: Bearer $TOKEN" --insecure
```

We can also access the link `$APISERVER/api/v1/namespaces/jh-namespace/pods` in browser for details.






### Config File

Kubernetes provides a command line tool `kubectl` for communicating with a Kubernetes cluster's control plane, using the Kubernetes API.

kubectl controls the Kubernetes *cluster manager*.

For configuration, kubectl looks for a file named config in the `$HOME/.kube` directory, which is a copy of file `/etc/kubernetes/admin.conf` generated by `kubeadm init`. 

We can specify other kubeconfig files by setting the `KUBECONFIG` environment variable or by setting the `--kubeconfig flag`.  If the `KUBECONFIG` environment variable doesn't exist, kubectl uses the default kubeconfig file, `$HOME/.kube/config`.

A *context* element in a kubeconfig file is used to group access parameters under a convenient name. Each context has three parameters: cluster, namespace, and user. By default, the kubectl command-line tool uses parameters from the current context to communicate with the cluster.

A sample of `.kube/config`.
```
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: <certificate string>
    server: https://<eth0 ip>:6443
  name: <cluster name>
contexts:
- context:
    cluster: <cluster name>
    namespace: <namespace name>
    user: <user name>
  name: <context user>@<context name>
current-context: <context name>
kind: Config
preferences: {}
users:
- name: <user name>
  user:
    client-certificate-data: <certificate string>
    client-key-data: <certificate string>
```

To get the current context:
```
root@cka001:~# kubectl config get-contexts
CURRENT   NAME                          CLUSTER      AUTHINFO           NAMESPACE
*         kubernetes-admin@kubernetes   kubernetes   kubernetes-admin   jh-namespace
```

To set a context with new update, e.g, update default namespace, etc..
```
kubectl config set-context <context name> --cluster=<cluster name> --namespace=<namespace name> --user=<user name> 
```

To use a new context.
```
kubectl config use-contexts <context name>
```


Reference of [kubectl](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/) and [commandline](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands). 



### Bash Autocomplete

Use TAB for bash auto-completion.

Ubuntu：
```
apt install -y bash-completion
source /usr/share/bash-completion/bash_completion
echo "source <(kubectl completion bash)" >> ~/.bashrc
source <(kubectl completion bash)
```




### Common Usage


Get cluster status.
```
# kubectl cluster-info
# kubectl cluster-info dump
```

Get health status of control plane.
```
# kubectl get componentstatuses
# kubectl get cs
```

Get node status.
```
kubectl get nodes
kubectl get nodes -o wide
```

Update or get node lable.
```
# Update node label
kubectl label node cka002 node=demonode

# Get node info with label info
kubectl get nodes –show-labels

# Search node by label
kubectl get node -l node=demonode
```

Create a deployment, option `--image` specifies a image，option `--port` specifies port for external access. A pod is also created when deployment is created.
```
kubectl create deployment myapp --image=nginx --replicas=1 --port=80
kubectl get deployment myapp -o wide
```

Get detail information of pod.
```
kubectl describe pod <pod name>
```

Get detail information of deployment.
```
kubectl describe deployment <deployment>
```

Get resources under a namespace or all namespace.
```
kubectl get namespace
kubectl get pod -n <namespace name>
kubectl get pod --all-namespaces
kubectl get pod -A

kubectl get deployment -n <namespace name>
kubectl get deployment --all-namespaces
kubectl get deployment -A
```

By default, pod can only be internally accessed within cluster. 
We can map pod port to node port for external access by exposing a pod, e.g., browser `http://<node_ip>:<port_number>`.
```
# Expose myapp as service to node port 80.
kubectl expose deployment myapp --type=NodePort --port=80

# Get service
kubectl get service
kubectl get svc -o wide
```

Scale out by replicaset. We set three replicasets to scale out deployment `myapp`. The number of deployment `myapp` is now three.
```
# Scale out deployment
kubectl scale deployment myapp --replicas=3

# Get status of deployment
kubectl get deployment myapp

# Get status of replicaset
kubectl get replicaset
```


Rolling update.

Command usage: `kubectl set image (-f FILENAME | TYPE NAME) CONTAINER_NAME_1=CONTAINER_IMAGE_1 ... CONTAINER_NAME_N=CONTAINER_IMAGE_N`.

With the command `kubectl get deployment`, we will get deployment name `myapp` and related container name `nginx`.
```
kubectl get deployment myapp -o wide
```

With the command `kubectl set image` to update image nginx from `nginx` to `nginx:1.19` and log the change under deployment's annotations with option `--record`.
```
kubectl set image deployment myapp nginx=nginx:1.19 --record
```
By the command `kubectl set image`, all pods are running under new replicaset `myapp-b997fb85f` with new image version `nginx:1.19`.
```
root@cka001:~# kubectl get replicaset -o wide -l app=myapp
NAME              DESIRED   CURRENT   READY   AGE     CONTAINERS   IMAGES       SELECTOR
myapp-948688ff6   0         0         0       80m     nginx        nginx        app=myapp,pod-template-hash=948688ff6
myapp-b997fb85f   3         3         3       6m29s   nginx        nginx:1.19   app=myapp,pod-template-hash=b997fb85f
```

We can get the change history under `metadata.annotations` by command `kubectl get deployment -o yaml`.
```
root@cka001:~# kubectl get deployment myapp -o yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    deployment.kubernetes.io/revision: "2"
    kubernetes.io/change-cause: kubectl set image deployment myapp nginx=nginx:1.19
      --record=true
  creationTimestamp: "2022-06-28T06:33:14Z"
```

We can also get the change history by command `kubectl rollout history`, and show details with specific revision `--revision=<revision_number>`.
```
root@cka001:~# kubectl rollout history deployment/myapp
deployment.apps/myapp 
REVISION  CHANGE-CAUSE
1         kubectl set image deployment/myapp myapp=nginx:1.19 --record=true
2         kubectl set image deployment myapp nginx=nginx:1.19 --record=true

root@cka001:~# kubectl rollout history deployment/myapp --revision=1
deployment.apps/myapp with revision #1
Pod Template:
  Labels:       app=myapp
        pod-template-hash=948688ff6
  Annotations:  kubernetes.io/change-cause: kubectl set image deployment/myapp myapp=nginx:1.19 --record=true
  Containers:
   nginx:
    Image:      nginx
    Port:       80/TCP
    Host Port:  0/TCP
    Environment:        <none>
    Mounts:     <none>
  Volumes:      <none>


root@cka001:~# kubectl rollout history deployment/myapp --revision=2
deployment.apps/myapp with revision #2
Pod Template:
  Labels:       app=myapp
        pod-template-hash=b997fb85f
  Annotations:  kubernetes.io/change-cause: kubectl set image deployment myapp nginx=nginx:1.19 --record=true
  Containers:
   nginx:
    Image:      nginx:1.19
    Port:       80/TCP
    Host Port:  0/TCP
    Environment:        <none>
    Mounts:     <none>
  Volumes:      <none>
```

Roll back to previous revision with command `kubectl rollout undo `, or roll back to specific revision with option `--to-revision=<revision_number>`.
```
# kubectl rollout undo deployment/myapp --to-revision=1
```

Get system event information.
```
kubectl describe pod <pod_name> -n <namespace_name>
```

Get the logs for a container in a pod or specified resource. If the pod has only one container, the container name is optional.








## Kubernetes API and Resource

The REST API is the fundamental fabric of Kubernetes. 
All operations and communications between components, and external user commands are REST API calls that the API Server handles. 
Consequently, everything in the Kubernetes platform is treated as an *API object* and has a corresponding entry in the API.


### API Version

The API versioning and software versioning are indirectly related. 
The API and release versioning proposal describes the relationship between API versioning and software versioning.
Different API versions indicate different levels of stability and support. 

Here's a summary of each level:

* Alpha:
    * The version names contain alpha (for example, v1alpha1).
    * The software may contain bugs. Enabling a feature may expose bugs. A feature may be disabled by default.
    * The support for a feature may be dropped at any time without notice.
    * The API may change in incompatible ways in a later software release without notice.
    * The software is recommended for use only in short-lived testing clusters, due to increased risk of bugs and lack of long-term support.
* Beta:
    * The version names contain beta (for example, v2beta3).
    * The software is well tested. Enabling a feature is considered safe. Features are enabled by default.
    * The support for a feature will not be dropped, though the details may change.
    * The schema and/or semantics of objects may change in incompatible ways in a subsequent beta or stable release. When this happens, migration instructions are provided. Schema changes may require deleting, editing, and re-creating API objects. The editing process may not be straightforward. The migration may require downtime for applications that rely on the feature.
    * The software is not recommended for production uses. Subsequent releases may introduce incompatible changes. If you have multiple clusters which can be upgraded independently, you may be able to relax this restriction.
      Note: Please try beta features and provide feedback. After the features exit beta, it may not be practical to make more changes.
* Stable:
    * The version name is vX where X is an integer.
    * The stable versions of features appear in released software for many subsequent versions.


Command to get current API
```
kubectl api-resources
```

### API Group

[API groups](https://git.k8s.io/design-proposals-archive/api-machinery/api-group.md) make it easier to extend the Kubernetes API. 
The API group is specified in a REST path and in the apiVersion field of a serialized object.

There are several API groups in Kubernetes:

* The core (also called legacy) group is found at REST path `/api/v1`. 
    * The core group is not specified as part of the apiVersion field, for example, apiVersion: v1.
* The named groups are at REST path `/apis/$GROUP_NAME/$VERSION` and use apiVersion: `$GROUP_NAME/$VERSION` (for example, apiVersion: batch/v1). 





### Resource

Kubernetes resources and "records of intent" are all stored as API objects, and modified via RESTful calls to the API. 
The API allows configuration to be managed in a declarative way. 
Users can interact with the Kubernetes API directly, or via tools like kubectl. 
The core Kubernetes API is flexible and can also be extended to support custom resources.

* Workload Resources
    * *Pod*. Pod is a collection of containers that can run on a host.
    * *PodTemplate*. PodTemplate describes a template for creating copies of a predefined pod.
    * *ReplicationController*. ReplicationController represents the configuration of a replication controller.
    * *ReplicaSet*. ReplicaSet ensures that a specified number of pod replicas are running at any given time.
    * *Deployment*. Deployment enables declarative updates for Pods and ReplicaSets.
    * *StatefulSet*. StatefulSet represents a set of pods with consistent identities.
    * *ControllerRevision*. ControllerRevision implements an immutable snapshot of state data.
    * *DaemonSet*. DaemonSet represents the configuration of a daemon set.
    * *Job*. Job represents the configuration of a single job.
    * *CronJob*. CronJob represents the configuration of a single cron job.
    * *HorizontalPodAutoscaler*. configuration of a horizontal pod autoscaler.
    * *HorizontalPodAutoscaler*. HorizontalPodAutoscaler is the configuration for a horizontal pod autoscaler, which automatically manages the replica count of any resource implementing the scale subresource based on the metrics specified.
    * *HorizontalPodAutoscaler v2beta2*. HorizontalPodAutoscaler is the configuration for a horizontal pod autoscaler, which automatically manages the replica count of any resource implementing the scale subresource based on the metrics specified.
    * *PriorityClass*. PriorityClass defines mapping from a priority class name to the priority integer value.
* Service Resources
    * *Service*. Service is a named abstraction of software service (for example, mysql) consisting of local port (for example 3306) that the proxy listens on, and the selector that determines which pods will answer requests sent through the proxy.
    * *Endpoints*. Endpoints is a collection of endpoints that implement the actual service.
    * *EndpointSlice*. EndpointSlice represents a subset of the endpoints that implement a service.
    * *Ingress*. Ingress is a collection of rules that allow inbound connections to reach the endpoints defined by a backend.
    * *IngressClass*. IngressClass represents the class of the Ingress, referenced by the Ingress Spec.
* Config and Storage Resources
    * *ConfigMap*. ConfigMap holds configuration data for pods to consume.
    * *Secret*. Secret holds secret data of a certain type.
    * *Volume*. Volume represents a named volume in a pod that may be accessed by any container in the pod.
    * *PersistentVolumeClaim*. PersistentVolumeClaim is a user's request for and claim to a persistent volume.
    * *PersistentVolume*. PersistentVolume (PV) is a storage resource provisioned by an administrator.
    * *StorageClass*. StorageClass describes the parameters for a class of storage for which PersistentVolumes can be dynamically provisioned.
    * *VolumeAttachment*. VolumeAttachment captures the intent to attach or detach the specified volume to/from the specified node.
    * *CSIDriver*. CSIDriver captures information about a Container Storage Interface (CSI) volume driver deployed on the cluster.
    * *CSINode*. CSINode holds information about all CSI drivers installed on a node.
    * *CSIStorageCapacity*. CSIStorageCapacity stores the result of one CSI GetCapacity call.
* Authentication Resources
    * *ServiceAccount*. ServiceAccount binds together: 
        * a name, understood by users, and perhaps by peripheral systems, for an identity 
        * a principal that can be authenticated and authorized 
        * a set of secrets.
    * *TokenRequest*. TokenRequest requests a token for a given service account.
    * *TokenReview*. TokenReview attempts to authenticate a token to a known user.
    * *CertificateSigningRequest*. CertificateSigningRequest objects provide a mechanism to obtain x509 certificates by submitting a certificate signing request, and having it asynchronously approved and issued.
* Authorization Resources
    * *LocalSubjectAccessReview*. LocalSubjectAccessReview checks whether or not a user or group can perform an action in a given namespace.
    * *SelfSubjectAccessReview*. SelfSubjectAccessReview checks whether or the current user can perform an action.
    * *SelfSubjectRulesReview*. SelfSubjectRulesReview enumerates the set of actions the current user can perform within a namespace.
    * *SubjectAccessReview*. SubjectAccessReview checks whether or not a user or group can perform an action.
    * *ClusterRole*. ClusterRole is a cluster level, logical grouping of PolicyRules that can be referenced as a unit by a RoleBinding or ClusterRoleBinding.
    * *ClusterRoleBinding*. ClusterRoleBinding references a ClusterRole, but not contain it.
    * *Role*. Role is a namespaced, logical grouping of PolicyRules that can be referenced as a unit by a RoleBinding.
    * *RoleBinding*. RoleBinding references a role, but does not contain it.
* Policy Resources
    * *LimitRange*. LimitRange sets resource usage limits for each kind of resource in a Namespace.
    * *ResourceQuota*. ResourceQuota sets aggregate quota restrictions enforced per namespace.
    * *NetworkPolicy*. NetworkPolicy describes what network traffic is allowed for a set of Pods.
    * *PodDisruptionBudget*. PodDisruptionBudget is an object to define the max disruption that can be caused to a collection of pods.
    * *PodSecurityPolicy v1beta1*. PodSecurityPolicy governs the ability to make requests that affect the Security Context that will be applied to a pod and container.
* Extend Resources
    * *CustomResourceDefinition*. CustomResourceDefinition represents a resource that should be exposed on the API server.
    * *MutatingWebhookConfiguration*. MutatingWebhookConfiguration describes the configuration of and admission webhook that accept or reject and may change the object.
    * *ValidatingWebhookConfiguration(). ValidatingWebhookConfiguration describes the configuration of and admission webhook that accept or reject and object without changing it.
* Cluster Resources
    * *Node*. Node is a worker node in Kubernetes.
    * *Namespace*. Namespace provides a scope for Names.
    * *Event*. Event is a report of an event somewhere in the cluster.
    * *APIService*. APIService represents a server for a particular GroupVersion.
    * *Lease*. Lease defines a lease concept.
    * *RuntimeClass*. RuntimeClass defines a class of container runtime supported in the cluster.
    * *FlowSchema v1beta2*. FlowSchema defines the schema of a group of flows.
    * *PriorityLevelConfiguration v1beta2*. PriorityLevelConfiguration represents the configuration of a priority level.
    * *Binding*. Binding ties one object to another; for example, a pod is bound to a node by a scheduler.
    * *ComponentStatus*. ComponentStatus (and ComponentStatusList) holds the cluster validation info.


Command `kubectl explain RESOURCE [options]` describes the fields associated with each supported API resource. 
Fields are identified via a simple JSONPath identifier:











## Pods

### Basic

### InitContainer

### Static Pod












