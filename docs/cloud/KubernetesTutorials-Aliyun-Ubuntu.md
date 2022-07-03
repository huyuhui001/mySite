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

Set `kubectl` [auto-completion](https://github.com/scop/bash-completion) following the [guideline](https://kubernetes.io/docs/tasks/tools/included/optional-kubectl-configs-bash-linux/).
```
# apt install -y bash-completion
# source /usr/share/bash-completion/bash_completion
# source <(kubectl completion bash)
# echo "source <(kubectl completion bash)" >> ~/.bashrc
```

If we set an alias for kubectl, we can extend shell completion to work with that alias:
```
echo 'alias k=kubectl' >>~/.bashrc
echo 'complete -o default -F __start_kubectl k' >>~/.bashrc
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

With `kubeadm init` to initiate cluster, we need understand below three options about network.

* `--pod-network-cidr`: 
    * Specify range of IP addresses for the pod network. If set, the control plane will automatically allocate CIDRs for every node.
    * Be noted that `10.244.0.0/16` is default range of flannel. If it's changed here, please do change the same when deploy `Flannel`.
* `--apiserver-bind-port`: 
    * Port for the API Server to bind to. (default 6443)
* `--service-cidr`: 
    * Use alternative range of IP address for service VIPs. (default "10.96.0.0/12")

Note: 

* service VIPs (a.k.a. Cluster IP), specified by option `--service-cidr`.
* podCIDR (a.k.a. endpoint IP)，specified by option `--pod-network-cidr`.

There are 4 distinct networking problems to address:

* Highly-coupled container-to-container communications: this is solved by Pods (podCIDR) and localhost communications.
* Pod-to-Pod communications: 
    * a.k.a. container-to-container. 
    * Example with Flannel, the flow is: Pod --> veth pair --> cni0 --> flannel.1 --> host eth0 --> host eth0 --> flannel.1 --> cni0 --> veth pair --> Pod.
* Pod-to-Service communications:
    * Flow: Pod --> Kernel --> Servive iptables --> service --> Pod iptables --> Pod
* External-to-Service communications: 
    * LoadBalancer: SLB --> NodePort --> Service --> Pod

`kube-proxy` is responsible for iptables, not traffic. 







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


### Demo: Static Pod

Create yaml file in directory `/etc/kubernetes/manifests/`.
`kubectl` will automatically check yaml file in `/etc/kubernetes/manifests/` and create the static pod once it's detected.
```
root@cka001:~# kubectl run nginx --image=nginx:mainline --dry-run=client -n jh-namespace -oyaml > /etc/kubernetes/manifests/my-nginx.yaml

root@cka001:~# kubectl get pod
NAME           READY   STATUS    RESTARTS   AGE
nginx-cka001   1/1     Running   0          6s
```

Delete the yaml file `/etc/kubernetes/manifests/my-nginx.yaml`, the static pod will be deleted automatically.
```
root@cka001:~# rm /etc/kubernetes/manifests/my-nginx.yaml 
```




### Demo: Init containers

This example defines a simple Pod that has two init containers in `02-init-pod.yaml`. 
The first waits for myservice, and the second waits for mydb. 
Once both init containers complete, the Pod runs the app container from its spec section.
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

Create the Pod `myapp-pod`.
```
kubectl apply -f 02-init-pod.yaml
```

Check Pod status.
```
# kubectl get pod myapp-pod
NAME        READY   STATUS     RESTARTS   AGE
myapp-pod   0/1     Init:0/2   0          12m
```

Inspect Pods.
```
kubectl logs myapp-pod -c init-myservice # Inspect the first init container
kubectl logs myapp-pod -c init-mydb      # Inspect the second init container
```

At this point, those init containers will be waiting to discover Services named mydb and myservice.

Here's a configuration `04-myservice.yaml` we can use to make those Services appear :
```
---
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
```

To create the `mydb` and `myservice` services:
```
kubectl apply -f 04-myservice.yaml
```

We'll now see that those init containers complete, and that the myapp-pod Pod moves into the Running state:
```
root@cka001:~# kubectl get -f 04-myservice.yaml
NAME        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
myservice   ClusterIP   10.103.101.99   <none>        80/TCP    40s
mydb        ClusterIP   10.96.79.220    <none>        80/TCP    40s

root@cka001:~# kubectl get pod myapp-pod
NAME        READY   STATUS    RESTARTS   AGE
myapp-pod   1/1     Running   0          13m
```


### Demo Mutil-Container Pod

Create the sampel yaml file `multi-pod.yaml`.
```
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
```

Create the pod.
```
root@cka001:~# kubectl apply -f multi-pod.yaml

root@cka001:~# kubectl get pod multi-container-pod
NAME                  READY   STATUS    RESTARTS   AGE
multi-container-pod   2/2     Running   0          81s
```

Get details of the pod we created via command `kubectl describe pod multi-container-pod` and we can see below events.
```
Events:
  Type    Reason     Age    From               Message
  ----    ------     ----   ----               -------
  Normal  Scheduled  3m14s  default-scheduler  Successfully assigned jh-namespace/multi-container-pod to cka003
  Normal  Pulling    3m14s  kubelet            Pulling image "nginx"
  Normal  Pulled     3m12s  kubelet            Successfully pulled image "nginx" in 2.02130736s
  Normal  Created    3m11s  kubelet            Created container container-1-nginx
  Normal  Started    3m11s  kubelet            Started container container-1-nginx
  Normal  Pulling    3m11s  kubelet            Pulling image "alpine"
  Normal  Pulled     3m3s   kubelet            Successfully pulled image "alpine" in 8.317148653s
  Normal  Created    3m3s   kubelet            Created container container-2-alpine
  Normal  Started    3m3s   kubelet            Started container container-2-alpine
```

For multi-container pod, container name is needed if we want to get log of pod via command `kubectl logs <pod_name> <container_name>`.
```
root@cka001:~# kubectl logs multi-container-pod
error: a container name must be specified for pod multi-container-pod, choose one of: [container-1-nginx container-2-alpine]

root@cka001:~# kubectl logs multi-container-pod container-1-nginx
......
::1 - - [02/Jul/2022:01:12:29 +0000] "GET / HTTP/1.1" 200 615 "-" "Wget" "-"
```

Same if we need specify container name to login into the pod via command `kubectl exec -it <pod_name> -c <container_name> -- <commands>`.
```
root@cka001:~# kubectl exec -it multi-container-pod -c container-1-nginx -- /bin/bash
root@multi-container-pod:/# ls
bin  boot  dev  docker-entrypoint.d  docker-entrypoint.sh  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
```








### Demo: Usage of kubectl

#### Grant Authorization to ServiceAccount
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

root@cka001:~# kubectl get role -n jh-namespace
No resources found in jh-namespace namespace.

root@cka001:~# kubectl get rolebinding -n jh-namespace
No resources found in jh-namespace namespace.
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

Get pod resources in namespace `jh-namespace` via API server with JSON layout.
```
curl $APISERVER/api/v1/namespaces/jh-namespace/pods --header "Authorization: Bearer $TOKEN" --insecure
```

We will receive below error message. The serviceaccount `default` does not have authorization to access pod.
```
"message": "pods is forbidden: User \"system:serviceaccount:jh-namespace:default\" cannot list resource \"pods\" in API group \"\" in the namespace \"jh-namespace\"",
```

Let's create a rolebinding `rolebinding-admin` to bind cluster role `admin` to service account `default` in namespapce `jh-namespace`.
Hence service account `default` is granted adminstrator authorization in namespace `jh-namespace`.
```
# Usage:
kubectl create rolebinding <rule> --clusterrole=<clusterrule> --serviceaccount=<namespace>:<name> --namespace=<namespace>

# Crate rolebinding:
kubectl create rolebinding rolebinding-admin --clusterrole=admin --serviceaccount=jh-namespace:default --namespace=jh-namespace
```

Result looks like below.
```
root@cka001:~# kubectl get rolebinding -n jh-namespace
NAME                ROLE                AGE
rolebinding-admin   ClusterRole/admin   39s
```

Try again, get pod resources in namespace `jh-namespace` via API server with JSON layout.
```
curl $APISERVER/api/v1/namespaces/jh-namespace/pods --header "Authorization: Bearer $TOKEN" --insecure
```


#### Label Node

Get current label of nodes.
```
root@cka001:~# kubectl get node --show-labels
NAME     STATUS   ROLES                  AGE   VERSION   LABELS
cka001   Ready    control-plane,master   4d    v1.23.8   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=cka001,kubernetes.io/os=linux,node-role.kubernetes.io/control-plane=,node-role.kubernetes.io/master=,node.kubernetes.io/exclude-from-external-load-balancers=
cka002   Ready    <none>                 4d    v1.23.8   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=cka002,kubernetes.io/os=linux
cka003   Ready    <none>                 4d    v1.23.8   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=cka003,kubernetes.io/os=linux
```

Label a node `cka003`.
```
root@cka001:~# kubectl label node cka003 node=demonode
```


#### Deployment

Create a deployment `myapp`. `--port=8080` means the port that this container exposes.
```
kubectl create deployment myapp --image=docker.io/jocatalin/kubernetes-bootcamp:v1 --replicas=1 --port=8080
```
Get the status of the deployment.
```
root@cka001:~# kubectl get deployment -o wide
NAME    READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS            IMAGES                                       SELECTOR
myapp   0/1     1            0           19s   kubernetes-bootcamp   docker.io/jocatalin/kubernetes-bootcamp:v1   app=myapp
```

Get the details of deployment.
```
root@cka001:~# kubectl describe deployment myapp
```

Get the status of the Pod.
```
root@cka001:~# kubectl get pod -o wide
NAME                    READY   STATUS    RESTARTS   AGE     IP            NODE     NOMINATED NODE   READINESS GATES
myapp-b5d775f5d-6jtgs   1/1     Running   0          2m36s   10.244.2.12   cka003   <none>           <none>
```

Get the details of the Pod.
```
root@cka001:~# kubectl describe pod myapp-b5d775f5d-6jtgs
```


#### Namespace

Get current available namespaces.
```
root@cka001:~# kubectl get namespace
NAME              STATUS   AGE
default           Active   4d1h
jh-namespace      Active   2d19h
kube-node-lease   Active   4d1h
kube-public       Active   4d1h
kube-system       Active   4d1h
```

Get Pod under a specific namespace.
```
root@cka001:~# kubectl get pod -n kube-system
NAME                             READY   STATUS    RESTARTS   AGE
coredns-6d8c4cb4d-9khd8          1/1     Running   0          4d1h
coredns-6d8c4cb4d-qcp2l          1/1     Running   0          4d1h
etcd-cka001                      1/1     Running   0          4d1h
kube-apiserver-cka001            1/1     Running   0          4d1h
kube-controller-manager-cka001   1/1     Running   0          4d1h
kube-flannel-ds-hfvf7            1/1     Running   0          4d
kube-flannel-ds-m5mdl            1/1     Running   0          4d
kube-flannel-ds-rf54c            1/1     Running   0          4d
kube-proxy-bj75j                 1/1     Running   0          4d
kube-proxy-gxjj4                 1/1     Running   0          4d
kube-proxy-v7rsr                 1/1     Running   0          4d1h
kube-scheduler-cka001            1/1     Running   0          4d1h
```

Get Pods in all namespaces.
```
root@cka001:~# kubectl get pod --all-namespaces
root@cka001:~# kubectl get pod -A
```



#### Expose Service

Get current running Pod we created just now.
```
root@cka001:~# kubectl get deployment myapp -o wide
NAME    READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS            IMAGES                                       SELECTOR
myapp   1/1     1            1           44m   kubernetes-bootcamp   docker.io/jocatalin/kubernetes-bootcamp:v1   app=myapp

root@cka001:~# kubectl get pod -o wide
NAME                    READY   STATUS    RESTARTS   AGE   IP            NODE     NOMINATED NODE   READINESS GATES
myapp-b5d775f5d-6jtgs   1/1     Running   0          25m   10.244.2.12   cka003   <none>           <none>
```

Send http request to the Pod.
```
root@cka001:~# curl 10.244.2.12:8080
Hello Kubernetes bootcamp! | Running on: myapp-b5d775f5d-6jtgs | v=1
```

To make pod be accessed outside, we need expose port `8080` to a node port. A related service will be created. 
```
root@cka001:~# kubectl expose deployment myapp --type=NodePort --port=8080
service/myapp exposed
```

Get details of service `myapp`.
```
root@cka001:~# kubectl get svc myapp -o wide
NAME    TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE     SELECTOR
myapp   NodePort   10.108.93.159   <none>        8080:30520/TCP   5h14m   app=myapp

root@cka001:~# kubectl get svc myapp -o yaml
root@cka001:~# kubectl describe svc myapp
```

Get details of related endpoint `myapp`.
```
root@cka001:~# kubectl get endpoints myapp -o wide
NAME    ENDPOINTS          AGE
myapp   10.244.2.12:8080   5h21m

root@cka001:~# kubectl describe ep myapp
Name:         myapp
Namespace:    jh-namespace
Labels:       app=myapp
Annotations:  endpoints.kubernetes.io/last-change-trigger-time: 2022-06-29T08:03:17Z
Subsets:
  Addresses:          10.244.2.12
  NotReadyAddresses:  <none>
  Ports:
    Name     Port  Protocol
    ----     ----  --------
    <unset>  8080  TCP

Events:  <none>
```

Get details of Pod of `myapp`.
```
root@cka001:~# kubectl get pod -owide
NAME                    READY   STATUS    RESTARTS   AGE   IP            NODE     NOMINATED NODE   READINESS GATES
myapp-b5d775f5d-6jtgs   1/1     Running   0          70m   10.244.2.12   cka003   <none>           <none>

root@cka001:~# kubectl get node -o wide
NAME     STATUS   ROLES                  AGE    VERSION   INTERNAL-IP     EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION      CONTAINER-RUNTIME
cka001   Ready    control-plane,master   4d2h   v1.23.8   172.16.18.161   <none>        Ubuntu 20.04.4 LTS   5.4.0-113-generic   containerd://1.5.9
cka002   Ready    <none>                 4d1h   v1.23.8   172.16.18.160   <none>        Ubuntu 20.04.4 LTS   5.4.0-113-generic   containerd://1.5.9
cka003   Ready    <none>                 4d1h   v1.23.8   172.16.18.159   <none>        Ubuntu 20.04.4 LTS   5.4.0-113-generic   containerd://1.5.9
```

Send http request to the service and node sucessfully. Pod port `8080` is mapped to node port `30520`.
```
root@cka001:~# curl http://10.108.93.159:8080
Hello Kubernetes bootcamp! | Running on: myapp-b5d775f5d-6jtgs | v=1

root@cka001:~# curl http://172.16.18.159:30520
Hello Kubernetes bootcamp! | Running on: myapp-b5d775f5d-6jtgs | v=1
```


#### Scalling

Deployment `myapp` is now having 1 replica.
```
root@cka001:~# kubectl get deployment myapp -o wide
NAME    READY   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS            IMAGES                                       SELECTOR
myapp   1/1     1            1           6h12m   kubernetes-bootcamp   docker.io/jocatalin/kubernetes-bootcamp:v1   app=myapp
```

Scale to 2 replicas.
```
root@cka001:~# kubectl scale deployment myapp --replicas=2
deployment.apps/myapp scaled

root@cka001:~# kubectl get deployment myapp -o wide
NAME    READY   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS            IMAGES                                       SELECTOR
myapp   2/2     2            2           6h14m   kubernetes-bootcamp   docker.io/jocatalin/kubernetes-bootcamp:v1   app=myapp
```

Scale to 1 replicas. We can see interim phase that one Pos is been terminating.
```
root@cka001:~# kubectl get deployment myapp -o wide
NAME    READY   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS            IMAGES                                       SELECTOR
myapp   1/1     1            1           6h17m   kubernetes-bootcamp   docker.io/jocatalin/kubernetes-bootcamp:v1   app=myapp

root@cka001:~# kubectl get pod
NAME                    READY   STATUS        RESTARTS   AGE
myapp-b5d775f5d-6jtgs   1/1     Running       0          6h17m
myapp-b5d775f5d-mpshb   1/1     Terminating   0          3m28s
```



#### Rolling


Get current deployment image version.
```
root@cka001:~# kubectl get deployment -o wide
NAME    READY   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS            IMAGES                                       SELECTOR
myapp   1/1     1            1           6h21m   kubernetes-bootcamp   docker.io/jocatalin/kubernetes-bootcamp:v1   app=myapp
```

Update image to new versions.
```
kubectl set image deployment/myapp kubernetes-bootcamp=docker.io/jocatalin/kubernetes-bootcamp:v2 --record
kubectl set image deployment/myapp kubernetes-bootcamp=docker.io/jocatalin/kubernetes-bootcamp:v3 --record
kubectl set image deployment/myapp kubernetes-bootcamp=docker.io/jocatalin/kubernetes-bootcamp:v4 --record
kubectl set image deployment/myapp kubernetes-bootcamp=docker.io/jocatalin/kubernetes-bootcamp:v5 --record
```

We can observe that Pod's IP is changed to new one, and running on another node.
New Pod is in `ImagePullBackOff` status due to network issue to access `docker.io/jocatalin/kubernetes-bootcamp`.

```
root@cka001:~# kubectl get pod -o wide
NAME                     READY   STATUS             RESTARTS   AGE     IP            NODE     NOMINATED NODE   READINESS GATES
myapp-75ccb85dd6-hzc82   0/1     ImagePullBackOff   0          2m15s   10.244.1.13   cka002   <none>           <none>
myapp-b5d775f5d-6jtgs    1/1     Running            0          6h24m   10.244.2.12   cka003   <none>           <none>
```

Let's verify if the service is still available after rolling update. Send http request to the node sucessfully.
```
root@cka001:~# curl http://172.16.18.160:30520
Hello Kubernetes bootcamp! | Running on: myapp-b5d775f5d-6jtgs | v=1
```

Get rolling update history.
```
root@cka001:~# kubectl rollout history deployment/myapp
deployment.apps/myapp 
REVISION  CHANGE-CAUSE
1         <none>
2         kubectl set image deployment/myapp kubernetes-bootcamp=docker.io/jocatalin/kubernetes-bootcamp:v2 --record=true
3         kubectl set image deployment/myapp kubernetes-bootcamp=docker.io/jocatalin/kubernetes-bootcamp:v3 --record=true
4         kubectl set image deployment/myapp kubernetes-bootcamp=docker.io/jocatalin/kubernetes-bootcamp:v4 --record=true
5         kubectl set image deployment/myapp kubernetes-bootcamp=docker.io/jocatalin/kubernetes-bootcamp:v5 --record=true
```

Reverse to revision 3. Copied revision `3` to `6` as current revision.

```
root@cka001:~# kubectl rollout undo deployment/myapp --to-revision=3
deployment.apps/myapp rolled back

root@cka001:~# kubectl rollout history deployment/myapp
deployment.apps/myapp 
REVISION  CHANGE-CAUSE
1         <none>
2         kubectl set image deployment/myapp kubernetes-bootcamp=docker.io/jocatalin/kubernetes-bootcamp:v2 --record=true
4         kubectl set image deployment/myapp kubernetes-bootcamp=docker.io/jocatalin/kubernetes-bootcamp:v4 --record=true
5         kubectl set image deployment/myapp kubernetes-bootcamp=docker.io/jocatalin/kubernetes-bootcamp:v5 --record=true
6         kubectl set image deployment/myapp kubernetes-bootcamp=docker.io/jocatalin/kubernetes-bootcamp:v3 --record=true
```


#### Event

Get detail event info of related Pod.
```
root@cka001:~# kubectl describe pod myapp-78bdb65cd8-bnjbj
```

Result looks like below.
```
Events:
  Type     Reason     Age                 From               Message
  ----     ------     ----                ----               -------
  Normal   Scheduled  15m                 default-scheduler  Successfully assigned jh-namespace/myapp-78bdb65cd8-bnjbj to cka002
  Normal   Pulling    14m (x4 over 15m)   kubelet            Pulling image "docker.io/jocatalin/kubernetes-bootcamp:v3"
  Warning  Failed     14m (x4 over 15m)   kubelet            Failed to pull image "docker.io/jocatalin/kubernetes-bootcamp:v3": rpc error: code = NotFound desc = failed to pull and unpack image "docker.io/jocatalin/kubernetes-bootcamp:v3": failed to resolve reference "docker.io/jocatalin/kubernetes-bootcamp:v3": docker.io/jocatalin/kubernetes-bootcamp:v3: not found
  Warning  Failed     14m (x4 over 15m)   kubelet            Error: ErrImagePull
  Warning  Failed     14m (x6 over 15m)   kubelet            Error: ImagePullBackOff
  Normal   BackOff    44s (x65 over 15m)  kubelet            Back-off pulling image "docker.io/jocatalin/kubernetes-bootcamp:v3"
```

Get detail event info of entire cluster.
```
root@cka001:~# kubectl get event
```


#### Logging

Get log info of Pod.
```
kubectl logs -f <pod_name>
kubectl logs -f <pod_name> -c <container_name> 
```
```
root@cka001:~# kubectl logs -f myapp-78bdb65cd8-bnjbj
Error from server (BadRequest): container "kubernetes-bootcamp" in pod "myapp-78bdb65cd8-bnjbj" is waiting to start: trying and failing to pull image
```

Get log info of K8s components. 
```
root@cka001:~# kubectl logs kube-apiserver-cka001 -n kube-system
root@cka001:~# kubectl logs kube-controller-manager-cka001 -n kube-system
root@cka001:~# kubectl logs kube-scheduler-cka001 -n kube-system
root@cka001:~# kubectl logs etcd-cka001 -n kube-system
root@cka001:~# systemctl status kubelet
root@cka001:~# journalctl -fu kubelet
root@cka001:~# kubectl logs kube-proxy-bj75j -n kube-system
```



### Demo: Workload Resources

#### Deployment

Create deployment via command `kubectl create`.
```
root@cka001:~# kubectl create deployment deploy-http-app1 --image=nginx:1.19
```

Create deployment via yaml file and apply it.
```
root@cka001:~# cat > deploy-http-app2.yaml <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deploy-http-app2
  labels:
    app: deploy-http-app2
spec:
  selector:
    matchLabels:
      app: deploy-http-app2
  replicas: 1
  template:
    metadata:
      labels:
        app: deploy-http-app2
    spec:
      containers:
      - name: nginx
        image: nginx:1.19
EOF


root@cka001:~# kubectl apply -f deploy-http-app2.yaml
```

Get Deployment Pod created just now.

```
root@cka001:~# kubectl get pod
NAME                                READY   STATUS    RESTARTS   AGE
deploy-http-app1-7cbc9b645d-zztg9   1/1     Running   0          116s
deploy-http-app2-5f5f7765c9-7hcmt   1/1     Running   0          46s
```

Use below commands to check details of deployment pod we creatd just now.
```
# kubectl describe deployment
# kubectl get deployment -oyaml
# kubectl describe pod
# kubectl get pod -oyaml
```




#### StatefulSet

Create StatefulSet with yaml file and apply it.
```
root@cka001:~# cat > stateufulset-web.yaml <<EOF
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

root@cka001:~# kubectl apply -f stateufulset-web.yaml
```

Get details of StatefulSet Pod created just now.
```
root@cka001:~# kubectl get pod | grep web
NAME                                READY   STATUS    RESTARTS   AGE
web-0                               1/1     Running   0          2m1s
web-1                               1/1     Running   0          117s

root@cka001:~# kubectl get sts -o wide
NAME   READY   AGE   CONTAINERS   IMAGES
web    2/2     88s   nginx        nginx
```

Use command `kubectl edit sts web` to update an existing StatefulSet.
ONLY these fields can be updated: `replicas`、`image`、`rolling updates`、`labels`、`resource request/limit` and `annotations`.

Note: 
Copy of StatefulSet Pod will not be created automatically in other node when it's dead in current node.  


#### DaemonSet

Create DaemonSet with yaml file and apply it.
```
root@cka001:~# cat > daemonset-busybox.yaml <<EOF
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


root@cka001:~# kubectl apply -f daemonset-busybox.yaml
```

Get status of DaemonSet Pod. Note, it's deployed on each node.
```
root@cka001:~# kubectl get daemonset
NAME                DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
daemonset-busybox   3         3         3       3            3           <none>          5m33s

root@cka001:~# kubectl get pod -o wide | grep daemonset-busybox
NAME                                READY   STATUS    RESTARTS   AGE   IP            NODE     NOMINATED NODE   READINESS GATES
daemonset-busybox-kb2kp             1/1     Running   0          75s   10.244.0.6    cka001   <none>           <none>
daemonset-busybox-lnspq             1/1     Running   0          75s   10.244.2.16   cka003   <none>           <none>
daemonset-busybox-r6sc7             1/1     Running   0          75s   10.244.1.17   cka002   <none>           <none>
```







#### Job

Create Job with yaml file and apply it.
```
root@cka001:~# cat > job-pi.yaml <<EOF
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

root@cka001:~# kubectl apply -f job-pi.yaml
```

Get details of Job.
```
root@cka001:~# kubectl get jobs
```

Get details of Job Pod. The status `Completed` means the job was done successfully.
```
root@cka001:~# kubectl get pod pi-s28pr
```

Get log info of the Job Pod.
```
root@cka001:~# kubectl logs pi-s28pr
3.141592653589793..............
```



#### Cronjob

Create Cronjob with yaml file and apply it.
```
root@cka001:~# cat > cronjob-hello.yaml <<EOF
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


root@cka001:~# kubectl apply -f cronjob-hello.yaml
```

Get detail of Cronjob
```
root@cka001:~# kubectl get cronjobs
```

Monitor Jobs. Every 1 minute a new job will be created. 

```
root@cka001:~# kubectl get jobs -w
```




## Label and Annotation




### Demo: Label and Annotation

#### Label

Set Label `disktype=ssd` for node `cka003`.
```
root@cka001:~# kubectl label node cka002 disktype=ssd
```

Get Label info
```
root@cka001:~# kubectl get node --show-labels
root@cka001:~# kubectl describe node cka003
root@cka001:~# kubectl get node cka003 -oyaml
```

Overwrite Label with `disktype=hdd` for node `cka003`.
```
root@cka001:~# kubectl label node cka003 disktype=hdd --overwrite
```

Remove Label for node `cka003`
```
root@cka001:~# kubectl label node cka003 disktype-
```



#### Annotation

Create Nginx deployment
```
root@cka001:~# kubectl create deploy nginx --image=nginx:mainline
```

Get Annotation info.
```
root@cka001:~# kubectl describe deployment/nginx

Labels:                 app=nginx
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=nginx
```

Add new Annotation.
```
root@cka001:~# kubectl annotate deployment nginx owner=jh

Annotations:            deployment.kubernetes.io/revision: 1
                        owner: jh
Selector:               app=nginx
```

Update/Overwrite Annotation.
```
root@cka001:~# kubectl annotate deployment/nginx owner=qwer --overwrite

Annotations:            deployment.kubernetes.io/revision: 1
                        owner: qwer
Selector:               app=nginx
```

Remove Annotation

```
root@cka001:~# kubectl annotate deployment/nginx owner-

Labels:                 app=nginx
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=nginx
```



## Health Check

### Status of Pod and Container

Create a yaml file `multi-pods.yaml`. 
```
root@cka001:~# cat > multi-pods.yaml  <<EOF
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

Apply the yaml file to create a Pod `multi-pods` with two containers `nginx` and `busybox`. 
```
root@cka001:~# kubectl apply -f multi-pods.yaml
```

Minotor the status with option `--watch`. The status of Pod was changed from `ContainerCreating` to `NotReady` to `CrashLoopBackOff`.
```
root@cka001:~# kubectl get pod multi-pods --watch
NAME         READY   STATUS              RESTARTS   AGE
multi-pods   0/2     ContainerCreating   0          49s
multi-pods   1/2     NotReady            1          99s
multi-pods   1/2     CrashLoopBackOff    2          110s
```

Get details of the Pod `multi-pods`, focus on Container's state under segment `Containers` and Conditions of Pod under segment `Conditions`.
```
root@cka001:~# kubectl describe pod multi-pods
......
Containers:
  nginx:
    ......
    State:          Running
      Started:      Sun, 03 Jul 2022 12:52:42 +0800
    Ready:          True
    Restart Count:  0
    ......
  busybox:
    ......
    State:          Terminated
      Reason:       Completed
      Exit Code:    0
      Started:      Sun, 03 Jul 2022 12:58:43 +0800
      Finished:     Sun, 03 Jul 2022 12:58:43 +0800
    Ready:          False
    Restart Count:  6
    ......
Conditions:
  Type              Status
  Initialized       True     # Set to True when initCounter completed successfully.
  Ready             False    # Set to True when ContainersReady is True.
  ContainersReady   False    # Set to True when all containers are ready.
  PodScheduled      True     # Set to True when Pos schedule completed successfully.
...... 
```





### LivenessProbe

Create a yaml file `liveness.yaml` with `livenessProbe` setting and apply it.
```
root@cka001:~# cat > liveness.yaml <<EOF
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
    - touch /tmp/healthy; sleep 30; rm -rf /tmp/healthy; sleep 30
    livenessProbe:
      exec:
        command:
        - cat
        - /tmp/healthy
      initialDelaySeconds: 5
      periodSeconds: 5
EOF

root@cka001:~# kubectl apply -f liveness.yaml
```

Let's see what happened in the Pod `liveness-exec`.

* Create a folder `/tmp/healthy`.
* Execute the the command `cat /tmp/healthy` and return successful code.
* After 30 seconds, execute command `rm -rf /tmp/healthy` to delete the folder. The probe `livenessProbe` detects the failure and return error message.
* After 30 seconds, pull the image again and the folder is created again `touch /tmp/healthy`.

Once failure detected, image will be pulled again and the folder `/tmp/healthy` is in place again.

Execute the command `kubectl describe pod liveness-exec` every 30 seconds to check the messge changes. 



### ReadinessProbe

Create a yaml file `readiness.yaml` with `readinessProbe` setting and apply it.
```
root@cka001:~# cat > readiness.yaml <<EOF
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
      - touch /tmp/healthy; sleep 5;rm -rf /tmp/healthy; sleep 30
      readinessProbe:
        exec:
          command:
          - cat
          - /tmp/healthy
        initialDelaySeconds: 10
        periodSeconds: 5
EOF

root@cka001:~# kubectl apply -f readiness.yaml
```

The ready status of the Pod is 0/1, that is, the Pod is not up successfully.
```
root@cka001:~# kubectl get pod readiness --watch
NAME        READY   STATUS    RESTARTS   AGE
readiness   0/1     Running   0          15s
```

Execute command `kubectl describe pod readiness` to check status of Pod. We will see failure message `Readiness probe failed`.



### 实际意义

基于 Nginx 的 Deployment + Service 的健康检查实践，创建对应 YAML 并应用

```shell
cat > nginx-healthcheck.yaml <<EOF
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

kubectl apply -f nginx-healthcheck.yaml
```

查看 nginx-healthcheck Pod

```shell
kubectl get pod -owide
```

输出

```shell
NAME                                 READY   STATUS             RESTARTS   AGE     IP            NODE    NOMINATED NODE   READINES
nginx-healthcheck-5bfd86bd46-cvw8r   1/1     Running            0          2m15s   10.244.0.72   cka001   <none>           <none>
nginx-healthcheck-5bfd86bd46-cw8bz   1/1     Running            0          7m45s   10.244.0.71   cka002   <none>           <none>
```

通过 curl 访问 Pod IP，修改为自己实际的 Pod IP

```shell
curl 10.244.0.72
curl 10.244.0.71
```

正常输出 Nginx 的 index.html 页面

```html
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
```

查看 Service 的详情

```shell
kubectl describe svc nginx-healthcheck
```

关注 Endpoints 字段

```SHELL
Name:                     nginx-healthcheck
Namespace:                default
Labels:                   <none>
Annotations:              <none>
Selector:                 name=nginx-healthcheck
Type:                     NodePort
IP Families:              <none>
IP:                       10.107.42.168
IPs:                      10.107.42.168
Port:                     <unset>  80/TCP
TargetPort:               80/TCP
NodePort:                 <unset>  30388/TCP
Endpoints:                10.244.0.71:80,10.244.0.72:80
Session Affinity:         None
External Traffic Policy:  Cluster
Events:                   <none>
```

也可以通过 endpoints 对象查看

```
kubectl get endpoints nginx-healthcheck
```

输出

```
NAME                ENDPOINTS                       AGE
nginx-healthcheck   10.244.0.71:80,10.244.0.72:80   10m
```

此时 两个 nginx-healthcheck Pod 都正常提供服务。

删除其中一个 nginx-healthcheck Pod 的 index.html 文件，模拟应用异常 readinessProbe 就绪探针检查失败的场景

exec 进入 nginx-healthcheck Pod 的容器里面，删除 index.html 文件，nginx-healthcheck-5bfd86bd46-cvw8r 需要修改为实际的 Pod Name

```shell
kubectl exec -it nginx-healthcheck-5bfd86bd46-cvw8r -- bash
cd /usr/share/nginx/html/
rm -rf index.html
exit
```

重新查看这个 Pod 的详情，Pod Name 替换为自己实际的 Pod

```shell
kubectl describe pod nginx-healthcheck-5bfd86bd46-cvw8r
```

出现 Readiness probe failed 的异常事件

```shell
Events:
  Type     Reason     Age               From               Message
  ----     ------     ----              ----               -------
  Normal   Scheduled  10m               default-scheduler  Successfully assigned default/nginx-healthcheck-5bfd86bd46-cvw8r to cka01
  Normal   Pulled     10m               kubelet            Container image "nginx:latest" already present on machine
  Normal   Created    10m               kubelet            Created container nginx-healthcheck
  Normal   Started    10m               kubelet            Started container nginx-healthcheck
  Warning  Unhealthy  0s (x3 over 10s)  kubelet            Readiness probe failed: HTTP probe failed with statuscode: 403
root@cka01:~# kubectl describe pod nginx-healthcheck-5bfd86bd46-cvw8r
```

通过 curl 访问 Pod IP，修改为自己实际的 Pod IP

```shell
curl 10.244.0.72
```

输出 403 错误

```html
<html>
<head><title>403 Forbidden</title></head>
<body>
<center><h1>403 Forbidden</h1></center>
<hr><center>nginx/1.19.10</center>
</body>
</html>
```

查看 Service 的详情

```shell
kubectl describe svc nginx-healthcheck
```

关注 Endpoints 字段，只剩下一个 nginx-healthcheck Pod 的 endpoint

```SHELL
Name:                     nginx-healthcheck
Namespace:                default
Labels:                   <none>
Annotations:              <none>
Selector:                 name=nginx-healthcheck
Type:                     NodePort
IP Families:              <none>
IP:                       10.107.42.168
IPs:                      10.107.42.168
Port:                     <unset>  80/TCP
TargetPort:               80/TCP
NodePort:                 <unset>  30388/TCP
Endpoints:                10.244.0.71:80
Session Affinity:         None
External Traffic Policy:  Cluster
Events:                   <none>
```

也可以通过 endpoints 对象查看，同样只剩下一个 nginx-healthcheck Pod 的 endpoint

```shell
kubectl get endpoints nginx-healthcheck
```

输出

```shell
NAME                ENDPOINTS        AGE
nginx-healthcheck   10.244.0.71:80   20m
```

此时只有一个 nginx-healthcheck Pod 正常提供服务，另外一个 Pod 由于就绪健康检查不通过，被移出了 endpoints 列表。

恢复 index.html 文件模拟应用故障恢复，记得替换 nginx-healthcheck-5bfd86bd46-cvw8r 为实际 Pod Name

```shell
kubectl exec -it nginx-healthcheck-5bfd86bd46-cvw8r -- bash
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

检查，记得将示例 Pod Name 替换为自己实际的 Pod

```shell
kubectl describe pod nginx-healthcheck-5bfd86bd46-cvw8r

kubectl describe svc nginx-healthcheck

kubectl get endpoints nginx-healthcheck
```


## Namespace

查看 Namespace
```shell
kubectl get namespace
```

查看 Namespace 的 Label

```shell
kubectl get ns --show-labels
```

创建 Namespace

```shell
kubectl create namespace cka
```

给 Namespace 打 Label

```shell
kubectl label ns cka cka=true
```

在 cka Namespace 下创建 Nginx Deployment

```shell
kubectl create deploy nginx --image=nginx --namespace cka
```

查看 cka Namespace 下的 Deployment 和 Pod

```shell
kubectl get deploy,pod -n cka
```

删除 Namespace（思考一下，删除之后，Namespace 下的资源对象会如何？）

```shell
kubectl delete ns cka
```





## HPA


- HPA 需要依赖 Metrics Server 组件，先安装 Metrics Server

下载 Metrics Server YAML 文件

```shell
wget https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

替换 YAML 文件中的 gcr 镜像

```
sed -i 's/k8s\.gcr\.io\/metrics-server\/metrics-server\:v0\.6\.1/registry\.aliyuncs\.com\/google_containers\/metrics-server\:v0\.6\.1/g' components.yaml
```

修改 metrics-server 的启动参数，增加 `--kubelet-insecure-tls` 参数禁用证书验证

```shell
vim components.yaml
```

```
    spec:
      containers:
      - args:
        - --cert-dir=/tmp
        - --secure-port=4443
        - --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
        - --kubelet-use-node-status-port
        - --metric-resolution=15s
        - --kubelet-insecure-tls
```

![image-20220702020852780](https://typora-picgo-1304429945.cos.ap-guangzhou.myqcloud.com/image-20220702020852780.png)

```shell
kubectl apply -f components.yaml
```

确认 metrics-server 服务运行正常

```shell
kubectl get pod -n kube-system |grep metrics-server
```

验证 metrics-server 功能正常，`kubectl top node` 阔以查看到节点的 CPU、内存使用情况

```shell
kubectl top node
```

```shell
NAME     CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
cka001   127m         6%     921Mi           24%
cka002   68m          3%     352Mi           9%
cka003   44m          2%     366Mi           9%
```

---



### 部署待压测应用 podinfo

创建 YAML 并应用
```shell
cat > podinfo.yaml << EOF
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

kubectl apply -f podinfo.yaml
```

---



### 配置 HPA

创建 HPA YAML 并应用，触发器阀值为 CPU 的平均使用率超过 50% 时触发弹性伸缩，保证最少有 2 个 Replicas，最多 10 个 Replicas。 
```SHELL
cat > hpa.yaml <<EOF
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

kubectl apply -f hpa.yaml
```

查看
```shell
kubectl get hpa
NAME    REFERENCE            TARGETS    MINPODS   MAXPODS   REPLICAS   AGE
nginx   Deployment/podinfo   100%/50%   2         10        2          47s
```

---



### 压测

使用 ab 进行压力测试，模拟 1000 个并发量

#### 安装 ab

```shell
apt install apache2-utils -y
```

ab 命令最基本的参数是 `-n` 和 `-c`：
```bash
-n 执行的请求数量
-c 并发请求个数

其它参数：
-t 测试所进行的最大秒数
-p 包含了需要 POST 的数据的文件
-T POST 数据所使用的 Content-type 头信息
-k 启用 HTTP KeepAlive 功能，即在一个 HTTP 会话中执行多个请求，默认时，不启用 KeepAlive 功能
```

命令示例：
```shell
ab -n 1000 -c 100 http://www.baidu.com/
```

#### 并发压测

```
ab -c 1000 -t 60 http://127.0.0.1:31198/
```

可以看见随着 CPU 压力的增加，Deployment 已经自动 scale 了
```shell
kubectl get hpa -w
NAME    REFERENCE            TARGETS    MINPODS   MAXPODS   REPLICAS   AGE
nginx   Deployment/podinfo   940%/50%   2         10        8          13m
```
需要注意的是，scale up 是一个阶段性的过程，并不是一次性就直接 scale 到 max 了，而是一个阶段性的过程，扩容算法就是上文介绍的内容。隔段时间没操作压力下来后，会自动 scale down 缩减 Pod。

持续观察一段时间（5~10分钟），由于并发压测的结束，CPU 使用率下降，开始逐渐自动 scale down 收缩 Pod

```shell
kubectl get hpa -w
```


