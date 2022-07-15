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

Disable swap on Ubuntu.
```
sudo ufw disable
```

Check status of swap on Ubuntu.
```
sudo ufw status verbose
```




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

Install gpg certificate. Just choose one of below command and execute.
```
# Tested in 20.04 release.
# curl https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg | apt-key add -

# Tested in 22.04 release
# sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg
```

Add Kubernetes repo. Just choose one of below command and execute.
```
# Tested in 20.04 release
# cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main
EOF

# Tested in 22.04 release
# echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
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



### Troubleshooting

**Issue**: 
The connection to the server <master>:6443 was refused - did you specify the right host or port?

**Try**:

[Reference](https://discuss.kubernetes.io/t/the-connection-to-the-server-host-6443-was-refused-did-you-specify-the-right-host-or-port/552/15)

Check environment setting.
```
env | grep -i kub
```

Check container status.
```
sudo systemctl status containerd.service 
```

Check kubelet service.
```
sudo systemctl status kubelet.service 
```

Check port listening status.
```
netstat -pnlt | grep 6443
```

Check firewall status.
```
sudo systemctl status firewalld.service
```

Check log.
```
journalctl -xeu kubelet
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
cat > multi-pods.yaml  <<EOF
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
kubectl apply -f multi-pods.yaml
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

Detail description of the demo can be found on the [Kubernetes document](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/).

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
    - touch /tmp/healthy; sleep 30; rm -rf /tmp/healthy; sleep 600
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
* After `35` seconds, execute command `rm -rf /tmp/healthy` to delete the folder. The probe `livenessProbe` detects the failure and return error message.
* The kubelet kills the container and restarts it. The folder is created again `touch /tmp/healthy`.



By command `kubectl describe pod liveness-exec`, wec can see below event message. Once failure detected, image will be pulled again and the folder `/tmp/healthy` is in place again.
```
Events:
  Type     Reason     Age                   From               Message
  ----     ------     ----                  ----               -------
  Normal   Scheduled  4m21s                 default-scheduler  Successfully assigned jh-namespace/liveness-exec to cka002
  Normal   Pulled     4m19s                 kubelet            Successfully pulled image "busybox" in 1.906981795s
  Normal   Pulled     3m4s                  kubelet            Successfully pulled image "busybox" in 1.967545593s
  Normal   Created    109s (x3 over 4m19s)  kubelet            Created container liveness
  Normal   Started    109s (x3 over 4m19s)  kubelet            Started container liveness
  Normal   Pulled     109s                  kubelet            Successfully pulled image "busybox" in 2.051565102s
  Warning  Unhealthy  66s (x9 over 3m46s)   kubelet            Liveness probe failed: cat: can't open '/tmp/healthy': No such file or directory
  Normal   Killing    66s (x3 over 3m36s)   kubelet            Container liveness failed liveness probe, will be restarted
  Normal   Pulling    36s (x4 over 4m21s)   kubelet            Pulling image "busybox"
```




### ReadinessProbe

Readiness probes are configured similarly to liveness probes. The only difference is that you use the readinessProbe field instead of the livenessProbe field.

Create a yaml file `readiness.yaml` with `readinessProbe` setting and apply it.
```
cat > readiness.yaml <<EOF
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

kubectl apply -f readiness.yaml
```

The ready status of the Pod is 0/1, that is, the Pod is not up successfully.
```
root@cka001:~# kubectl get pod readiness --watch
NAME        READY   STATUS    RESTARTS   AGE
readiness   0/1     Running   0          15s
```

Execute command `kubectl describe pod readiness` to check status of Pod. We will see failure message `Readiness probe failed`.
```
Events:
  Type     Reason     Age               From               Message
  ----     ------     ----              ----               -------
  Normal   Scheduled  35s               default-scheduler  Successfully assigned jh-namespace/readiness to cka003
  Normal   Pulling    35s               kubelet            Pulling image "busybox"
  Normal   Pulled     32s               kubelet            Successfully pulled image "busybox" in 2.420171698s
  Normal   Created    32s               kubelet            Created container readiness
  Normal   Started    32s               kubelet            Started container readiness
  Warning  Unhealthy  5s (x4 over 20s)  kubelet            Readiness probe failed: cat: can't open '/tmp/healthy': No such file or directory
```


Liveness probes do not wait for readiness probes to succeed. If you want to wait before executing a liveness probe you should use initialDelaySeconds or a startupProbe.



### Demo of Health Check

Set up yaml file of health check for Nginx based Deployment + Service and apply it.

```
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

Check nginx-healthcheck Pod.
```
kubectl get pod -owide
```

Get below result.
```
NAME                                 READY   STATUS    RESTARTS   AGE   IP            NODE     NOMINATED NODE   READINESS GATES
nginx-healthcheck-79fc55d944-9jbvj   1/1     Running   0          50s   10.244.2.82   cka003   <none>           <none>
nginx-healthcheck-79fc55d944-rwx7n   1/1     Running   0          50s   10.244.1.11   cka002   <none>           <none>
```

Access Pod IP via `curl` command, e.g., above example.
```
curl 10.244.2.82
curl 10.244.1.11
```

We will see a successful `index.html` conten of Nginx below with above example.
```
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
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

Check details of Service craeted in above example.
```
kubectl describe svc nginx-healthcheck
```

We will see below output. There are two Pods information listed in `Endpoints`.
```
Name:                     nginx-healthcheck
Namespace:                jh-namespace
Labels:                   <none>
Annotations:              <none>
Selector:                 name=nginx-healthcheck
Type:                     NodePort
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       10.98.196.231
IPs:                      10.98.196.231
Port:                     <unset>  80/TCP
TargetPort:               80/TCP
NodePort:                 <unset>  31505/TCP
Endpoints:                10.244.1.11:80,10.244.2.82:80
Session Affinity:         None
External Traffic Policy:  Cluster
Events:                   <none>
```

We can also get information of Endpoints.
```
kubectl get endpoints nginx-healthcheck
```
Get below result.
```
NAME                ENDPOINTS                       AGE
nginx-healthcheck   10.244.1.11:80,10.244.2.82:80   8m35s
```

Till now, two `nginx-healthcheck` Pods are working and providing service as expected. 

Let's simulate an error by deleting and `index.html` file in on of `nginx-healthcheck` Pod and see what's readinessProbe will do.

First, execute `kubectl exec -it <your_pod_name> -- bash` to log into `nginx-healthcheck` Pod, and delete the `index.html` file.
```
kubectl exec -it nginx-healthcheck-79fc55d944-9jbvj -- bash
cd /usr/share/nginx/html/
rm -rf index.html
exit
```

After that, let's check the status of above Pod that `index.html` file was deleted.
```
kubectl describe pod nginx-healthcheck-79fc55d944-9jbvj
```

We can now see `Readiness probe failed` error event message.
```
Events:
  Type     Reason     Age                From               Message
  ----     ------     ----               ----               -------
  Normal   Scheduled  29m                default-scheduler  Successfully assigned jh-namespace/nginx-healthcheck-79fc55d944-9jbvj to cka003
  Normal   Pulled     29m                kubelet            Container image "nginx:latest" already present on machine
  Normal   Created    29m                kubelet            Created container nginx-healthcheck
  Normal   Started    29m                kubelet            Started container nginx-healthcheck
  Warning  Unhealthy  1s (x16 over 71s)  kubelet            Readiness probe failed: HTTP probe failed with statuscode: 403
```

Let's check another Pod. 
```
kubectl describe pod nginx-healthcheck-79fc55d944-rwx7n
```
There is no error info.
```
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  31m   default-scheduler  Successfully assigned jh-namespace/nginx-healthcheck-79fc55d944-rwx7n to cka002
  Normal  Pulled     31m   kubelet            Container image "nginx:latest" already present on machine
  Normal  Created    31m   kubelet            Created container nginx-healthcheck
  Normal  Started    31m   kubelet            Started container nginx-healthcheck
```

Now, access Pod IP via `curl` command and see what the result of each Pod.
```
curl 10.244.2.82
curl 10.244.1.11
```

We will receive error while access the first Pod `curl 10.244.2.82`. The second Pos works well `curl 10.244.1.11`. 
```
<html>
<head><title>403 Forbidden</title></head>
<body>
<center><h1>403 Forbidden</h1></center>
<hr><center>nginx/1.23.0</center>
</body>
</html>
```

Let's check current status of Nginx Service after one of Pods runs into failure. 
```
kubectl describe svc nginx-healthcheck
```

In below output, there is only one Pod information listed in Endpoint.
```
Name:                     nginx-healthcheck
Namespace:                jh-namespace
Labels:                   <none>
Annotations:              <none>
Selector:                 name=nginx-healthcheck
Type:                     NodePort
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       10.98.196.231
IPs:                      10.98.196.231
Port:                     <unset>  80/TCP
TargetPort:               80/TCP
NodePort:                 <unset>  31505/TCP
Endpoints:                10.244.1.11:80
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
NAME                ENDPOINTS        AGE
nginx-healthcheck   10.244.1.11:80   40m
```

Conclusion: 
By delete the index.html file, the Pod is in unhealth status and is removed from endpoint list. 
One one health Pod can provide normal service.

Let's re-create the `index.html` file again in the Pod. 
```
kubectl exec -it nginx-healthcheck-79fc55d944-9jbvj -- bash

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
curl 10.244.2.82
curl 10.244.1.11
```

Verify the Pod status again. 
```
kubectl describe pod nginx-healthcheck-79fc55d944-9jbvj
```



## Namespace

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





## Horizontal Pod Autoscaling (HPA)


- Install Metrics Server component

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

Verify if `metrics-server` Pod is running as expected.
```
kubectl get pod -n kube-system -owide | grep metrics-server
```

Get current usage of CPU, memory of each node.
```
kubectl top node
```
Result:
```
NAME     CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%   
cka001   148m         7%     1746Mi          45%
cka002   41m          2%     1326Mi          34%       
cka003   39m          1%     1383Mi          36%
```


### Deploy a Service `podinfo`

Create and apply the yaml file `podinfo.yaml` to deploy Deployment and Service `podinfo` for further stress testing.
```
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



### Config HPA
 
Create and apply yaml file `hpa.yaml` for HPA by setting CPU threshold `50%` to trigger auto-scalling with minimal `2` and maximal `10` Replicas.
```
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

Get status of HPA.
```
kubectl get hpa
```
Result:
```
NAME    REFERENCE            TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
nginx   Deployment/podinfo   10%/50%   2         10        2          26s
```




### Stress Testing

Here we will use `ab` tool to simulate 1000 concurrency.

The `ab` command is a command line load testing and benchmarking tool for web servers that allows you to simulate high traffic to a website. 

The short definition form apache.org is: The acronym `ab` stands for Apache Bench where bench is short for benchmarking.

#### Install ab

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

#### Concurrency Stres Test 

Simulate 1000 concurrency request to current node running command `ab`.
```
ab -c 1000 -t 60 http://127.0.0.1:31198/
```

By command `kubectl get hpa -w` we can see that CPU workload has been increasing.
```
NAME    REFERENCE            TARGETS    MINPODS   MAXPODS   REPLICAS   AGE
nginx   Deployment/podinfo   388%/50%   2         10        10         32m
```
And see auto-scalling automically triggered via commands `kubectl get pod` and `kubectl get deployment`.
```
NAME                                 READY   STATUS    RESTARTS   AGE
nginx-healthcheck-79fc55d944-9jbvj   1/1     Running   0          153m
nginx-healthcheck-79fc55d944-rwx7n   1/1     Running   0          153m
podinfo-668b5b9b5b-4rxwr             1/1     Running   0          51m
podinfo-668b5b9b5b-6vm5k             1/1     Running   0          6m
podinfo-668b5b9b5b-7p74p             1/1     Running   0          5m45s
podinfo-668b5b9b5b-8929m             1/1     Running   0          5m45s
podinfo-668b5b9b5b-9fr28             1/1     Running   0          51m
podinfo-668b5b9b5b-dz74z             1/1     Running   0          6m
podinfo-668b5b9b5b-fzszt             1/1     Running   0          5m30s
podinfo-668b5b9b5b-gb2qq             1/1     Running   0          5m45s
podinfo-668b5b9b5b-tbdvj             1/1     Running   0          5m30s
podinfo-668b5b9b5b-z6dlh             1/1     Running   0          5m45s
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



## Service

### ClusterIP

#### Create Service

Create a Deployment `http-app`.
Create a Service with same name and link with Development by Label Selector. 
Service type is `ClusterIP`, which is default type and accessable internally. 

Create yaml file `svc-clusterip.yaml` and apply it to create Deployment and Service `http-app`.
```
cat > svc-clusterip.yaml <<EOF
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

kubectl apply -f svc-clusterip.yaml
```

Execute command `kubectl get deployment,service,pod -o wide` to check resources we created. 
```
NAME                        READY   UP-TO-DATE   AVAILABLE   AGE    CONTAINERS   IMAGES   SELECTOR
deployment.apps/httpd-app   2/2     2            2           3m1s   httpd        httpd    app=httpd

NAME                TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE    SELECTOR
service/httpd-app   ClusterIP   10.100.67.181   <none>        80/TCP    3m1s   app=httpd

NAME                             READY   STATUS    RESTARTS   AGE    IP            NODE     NOMINATED NODE   READINESS GATES
pod/httpd-app-6496d888c9-mg2jt   1/1     Running   0          3m1s   10.244.2.97   cka003   <none>           <none>
pod/httpd-app-6496d888c9-pdgq8   1/1     Running   0          3m1s   10.244.1.19   cka002   <none>           <none>
```

Verify the access from node `cka001` to Pod IPs.
```
curl 10.244.2.97
curl 10.244.1.19
```
And receive below successful information.
```
<html><body><h1>It works!</h1></body></html>
```

Verify the access via ClusterIP with Port.
```
curl 10.100.67.181:80
```
And receive below successful information.
```
<html><body><h1>It works!</h1></body></html>
```



#### Expose Service

Create and attach to a temporary Pod `Busybox` and use `nslookup` to verify DNS resolution. The option `--rm` means delete the Pod after exit.
```
kubectl run -it nslookup --rm --image=busybox:1.28
```

After attach to the Pod, run command `nslookup httpd-app`. The IP address `10.100.67.181` of name `httpd-app` we received is the ClusterIP of Service `httpd-app`.
```
/ # nslookup httpd-app
Server:    10.96.0.10
Address 1: 10.96.0.10 kube-dns.kube-system.svc.cluster.local

Name:      httpd-app
Address 1: 10.100.67.181 httpd-app.jh-namespace.svc.cluster.local
```

We can check the IP of temporary Pod `Busybox` in a new terminal by executing command `kubectl get pod -o wide`. The Pod `Busybox` has different IP `10.244.2.98`.
```
root@cka001:~# kubectl get pod nslookup
NAME                         READY   STATUS    RESTARTS   AGE   IP            NODE     NOMINATED NODE   READINESS GATES
nslookup                     1/1     Running   0          12m   10.244.2.98   cka003   <none>           <none>
```




### NodePort

Create and apply yaml file `svc-nodeport.yaml` to create a Service `httpd-app`.
```
cat > svc-nodeport.yaml <<EOF
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


kubectl apply -f svc-nodeport.yaml
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
NAME        TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
httpd-app   NodePort   10.100.67.181   <none>        80:30080/TCP   78m
```

Test the connection to the Service `httpd-app` via command `curl <your_node_ip>:30080`. It's node IP, not cluster IP, nor Pod IP.
We will receive below successful information.
```
<html><body><h1>It works!</h1></body></html>
```


### Special Service

#### Headless Service

Create and apply yaml file `svc-headless.yaml` to create a `Headless Service`.
```
cat > svc-headless.yaml <<EOF
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

kubectl apply -f svc-headless.yaml
```

Check Pos by command `kubectl get pod -owide -l app=web`.
```
NAME    READY   STATUS    RESTARTS   AGE   IP            NODE     NOMINATED NODE   READINESS GATES
web-0   1/1     Running   0          85s   10.244.2.99   cka003   <none>           <none>
web-1   1/1     Running   0          82s   10.244.1.20   cka002   <none>           <none>
```

Get details of the Service by command `kubectl describe svc -l app=web`.
```
Name:              web
Namespace:         jh-namespace
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
Endpoints:         10.244.1.20:80,10.244.2.99:80
Session Affinity:  None
Events:            <none>
```

启动一个Busybox Pod，使用 nslookup 来 测试 DNS 解析

Attach to the temporary Pod `Busybox` and use `nslookup` to verify DNS resolution.
```
kubectl run -it nslookup --rm --image=busybox:1.28
```

With `nslookup` command for Headless Service `web`, we received two IP of Pods, not ClusterIP due to Headless Service. 
```
/ # nslookup web
Server:    10.96.0.10
Address 1: 10.96.0.10 kube-dns.kube-system.svc.cluster.local

Name:      web
Address 1: 10.244.2.99 web-0.web.jh-namespace.svc.cluster.local
Address 2: 10.244.1.20 web-1.web.jh-namespace.svc.cluster.local
```

We can also use `nslookup` for `web-0.web` and `web-0.web`. Every Pod of Headless Service has own Service Name for DNS lookup.
```
/ # nslookup web-0.web
Server:    10.96.0.10
Address 1: 10.96.0.10 kube-dns.kube-system.svc.cluster.local

Name:      web-0.web
Address 1: 10.244.2.99 web-0.web.jh-namespace.svc.cluster.local
```

Clean up all resources created before.






## Ingress

### Deploy Ingress Controller

Get Ingress Controller yaml file.
```
wget https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.2.1/deploy/static/provider/cloud/deploy.yaml
```

Replace grc.io to Aliyun.

* `k8s.gcr.io/ingress-nginx/kube-webhook-certgen` to `registry.aliyuncs.com/google_containers/kube-webhook-certgen`.
* `k8s.gcr.io/ingress-nginx/controller` to `registry.aliyuncs.com/google_containers/nginx-ingress-controller`.

```
sed -i 's/k8s.gcr.io\/ingress-nginx\/kube-webhook-certgen/registry.aliyuncs.com\/google\_containers\/kube-webhook-certgen/g' deploy.yaml
sed -i 's/k8s.gcr.io\/ingress-nginx\/controller/registry.aliyuncs.com\/google\_containers\/nginx-ingress-controller/g' deploy.yaml
```

Apply the yaml file `deploy.yaml` to create Ingress Nginx.
```
kubectl apply -f deploy.yaml
```

Check the status of Pod.
Please be noted that a new namespace `ingress-nginx` was created and Ingress Nginx resources are running under the new namespace.
```
kubectl get pod -n ingress-nginx
```
The result is below.
```
NAME                                        READY   STATUS      RESTARTS   AGE
ingress-nginx-admission-create-dcsww        0/1     Completed   0          3m32s
ingress-nginx-admission-patch-hslwf         0/1     Completed   0          3m32s
ingress-nginx-controller-556fbd6d6f-trl9r   1/1     Running     0          3m32s
```




### Create Deployments

Create two deployment `nginx-app-1` and `nginx-app-2`.
```
cat > nginx-app.yaml << EOF
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


kubectl apply -f nginx-app.yaml
```

Get status of Pods by executing `kubectl get pod -o wide`. Two Pods are running on node `cka003` with two different Pod IPs.
```
NAME                           READY   STATUS    RESTARTS   AGE   IP             NODE     NOMINATED NODE   READINESS GATES
nginx-app-1-695b7b647d-l76bh   1/1     Running   0          34s   10.244.2.104   cka003   <none>           <none>
nginx-app-2-7f6bf6f4d4-lvbz8   1/1     Running   0          34s   10.244.2.105   cka003   <none>           <none>
```

Access to two Pod via curl. We get `403` error.
```
curl 10.244.2.104
```

Log onto node `cka003` and create `index.html` file in path `/root/html-1/`. The directory `/root/html-1/` is already in place after `nginx-app-1` and `nginx-app-2` created.
```
echo 'This is test 1 !!' > /root/html-1/index.html
echo 'This is test 2 !!' > /root/html-2/index.html
```

Check Pods status again by executing `kubectl get pod -o wide`.
```
NAME                           READY   STATUS    RESTARTS   AGE     IP             NODE     NOMINATED NODE   READINESS GATES
nginx-app-1-695b7b647d-l76bh   1/1     Running   0          6m11s   10.244.2.104   cka003   <none>           <none>
nginx-app-2-7f6bf6f4d4-lvbz8   1/1     Running   0          6m11s   10.244.2.105   cka003   <none>           <none>
```

Access to two Pod via curl. 
```
curl 10.244.2.104
curl 10.244.2.105
```
We get correct information now.
```
This is test 1 !!
This is test 2 !!
```


### Create Service

Create Service `nginx-app-1` and `nginx-app-2` and map to related deployment `nginx-app-1` and `nginx-app-2`.
```
cat > nginx-svc.yaml << EOF
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


kubectl apply -f nginx-svc.yaml
```

Check the status by executing `kubectl get svc -o wide`.
```
NAME          TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE   SELECTOR
nginx-app-1   ClusterIP   10.111.95.99   <none>        80/TCP    22s   app=nginx-app-1
nginx-app-2   ClusterIP   10.96.15.218   <none>        80/TCP    22s   app=nginx-app-2
```

Access to two Service via curl. 
```
curl 10.111.95.99
curl 10.96.15.218
```
We get correct information.
```
This is test 1 !!
This is test 2 !!
```





### Create Ingress

Create Ingress resource via file `nginx-app-ingress.yaml`. 
Map to two Services `nginx-app-1` and `nginx-app-1` we created..
Change the namespace if needed.
```
cat > nginx-app-ingress.yaml << EOF
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: nginx-app
  namespace: jh-namespace
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


kubectl apply -f nginx-app-ingress.yaml
```

Get Ingress status by executing command `kubectl get ingress`.
```  
NAME        CLASS   HOSTS               ADDRESS   PORTS   AGE
nginx-app   nginx   app1.com,app2.com             80      64s
```



### Test Accessiblity

By executing `kubectl get pod -n ingress-nginx -o wide`, we know Ingress Controllers are running on node `cka002`.
```
NAME                                        READY   STATUS      RESTARTS   AGE   IP             NODE     NOMINATED NODE   READINESS GATES
ingress-nginx-admission-create-dcsww        0/1     Completed   0          33m   10.244.2.102   cka003   <none>           <none>
ingress-nginx-admission-patch-hslwf         0/1     Completed   0          33m   10.244.2.103   cka003   <none>           <none>
ingress-nginx-controller-556fbd6d6f-trl9r   1/1     Running     0          33m   10.244.1.22    cka002   <none>           <none>
```

By executing `kubectl get node -o wide`, we know node `cka002`'s IP is `172.16.18.159`.
```
NAME     STATUS   ROLES                  AGE   VERSION   INTERNAL-IP     EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION      CONTAINER-RUNTIME
cka001   Ready    control-plane,master   13d   v1.23.8   172.16.18.161   <none>        Ubuntu 20.04.4 LTS   5.4.0-113-generic   containerd://1.5.9
cka002   Ready    <none>                 13d   v1.23.8   172.16.18.160   <none>        Ubuntu 20.04.4 LTS   5.4.0-113-generic   containerd://1.5.9
cka003   Ready    <none>                 13d   v1.23.8   172.16.18.159   <none>        Ubuntu 20.04.4 LTS   5.4.0-113-generic   containerd://1.5.9
```

Add below into `/etc/hosts file` in one of node. Put node IP below. In above example, IP of node `cka002` is `172.16.18.160`, which is running `ingress-nginx-controller`.
```
cat >> /etc/hosts << EOF
172.16.18.160   app1.com
172.16.18.160   app2.com
EOF
```

By executing `kubectl -n ingress-nginx get svc` to get NodePort of Ingress Controller. 
```
NAME                                 TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
ingress-nginx-controller             LoadBalancer   10.110.117.253   <pending>     80:31640/TCP,443:31338/TCP   40m
ingress-nginx-controller-admission   ClusterIP      10.107.32.104    <none>        443/TCP                      40m
```

Two files `index.html` are in two Pods, the web services are exposed to outside via node IP. 
Hence we can see below result. The `ingress-nginx-controller` plays a central entry point for outside access, and provide two ports for different backend services from Pods.
```
curl app1.com:31640
This is test 1 !!
```
```
curl app2.com:31338
This is test 2 !!
```


## Storage

### emptyDir

Create a Pod with `emptyDir` type Volume.
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

Check which node the Pod `hello-producer` is running. 
```
kubectl get pod hello-producer -owide
```
The Pod is running on node `cka003`.
```
NAME             READY   STATUS    RESTARTS   AGE    IP             NODE     NOMINATED NODE   READINESS GATES
hello-producer   1/1     Running   0          106s   10.244.2.106   cka003   <none>           <none>
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
05f5e1bb6a1bb       62aedd01bd852       15 minutes ago      Running             producer            0                   995cbc23eb763       hello-producer
```
Run command `crictl inspect` to get the path of mounted `shared-volume`, which is `emptyDir`.
```
crictl inspect 05f5e1bb6a1bb | grep source | grep empty
```
The result is below.
```
"source": "/var/lib/kubelet/pods/272ba5fa-e213-4c79-ab57-d4c91f4371ba/volumes/kubernetes.io~empty-dir/shared-volume",
```
Change the path to the path of mounted `shared-volume` we get above.
```
cd /var/lib/kubelet/pods/272ba5fa-e213-4c79-ab57-d4c91f4371ba/volumes/kubernetes.io~empty-dir/shared-volume
cat hello
```
We will see the content of file `hello`. 

The path `/producer_dir` inside the Pod is mounted to the local host path. 
The file `/producer_dir/hello` we created inside the Pod is actually in the host local path.



Let's delete the container `producer`, the file `hello` is still there.
```
crictl ps
crictl stop <your_container_id>
crictl rm <your_container_id>
ls /var/lib/kubelet/pods/272ba5fa-e213-4c79-ab57-d4c91f4371ba/volumes/kubernetes.io~empty-dir/shared-volume
```


Let's delete the Pod `hello-producer`, the file `hello` was gone with error `No such file or directory`.
```
kubectl delete pod hello-producer
ls /var/lib/kubelet/pods/272ba5fa-e213-4c79-ab57-d4c91f4371ba/volumes/kubernetes.io~empty-dir/shared-volume
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


#### Verify MySQL Availability

Check status of MySQL Pod. Need document the Pod name and node it's running on.
```
kubectl get pod -l app=mysql -o wide
```

Attach into the MySQL Pod on the running node.
```
kubectl exec -it <your_pod_name> -- bash
```

Within the Pod, go to directory `/var/lib/mysql`, all files in the directory are same with all files in host directory `/tmp/mysql`.

Connect to the database in the Pod.
```
mysql -h 127.0.0.1 -uroot -ppassword
```

Operate the database.
```
mysql> show databases;
mysql> connect mysql;
mysql> show tables;
```



### PV and PVC

Here we will use NFS as backend storage to demo how to deploy PV and PVC.

#### Set up NFS Server

##### Install nfs-kernel-server

Log onto `cka002`.

Choose one Worker `cka002` to build NFS server. 
```
sudo apt-get install -y nfs-kernel-server
```

##### Configure Share Folder

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

Check whether sharefolder is configured. 
```
showmount -e
```
And see below output.
```
Export list for cka002:
/nfsdata *
```



##### Install NFS Client

Install NFS client on all nodes.
```
sudo apt-get install -y nfs-common
```



##### Verify NFS Server

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



##### Mount NFS

Execute below command to mount remote NFS folder on any other non-NFS-server node, e.g., `cka001` or `cka003`.
```
mkdir /remote-nfs-dir
mount -t nfs cka002:/nfsdata /remote-nfs-dir/
```

Use command `df -h` to verify mount point. Below is the sample output.
```
Filesystem       Size  Used Avail Use% Mounted on
cka002:/nfsdata   40G  6.8G   31G  18% /remote-nfs-dir
```

#### Create PV

Create a PV with below yaml file `mysql-pv.yaml`. Replace the NFS Server IP with actual IP that NFS server is running on.
```
cat > mysql-pv.yaml <<EOF
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
   server: 172.16.18.160
EOF

kubectl apply -f mysql-pv.yaml
```

Check the PV.
```
kubectl get pv
```
The result:
```
NAME       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM   STORAGECLASS   REASON   AGE
mysql-pv   1Gi        RWO            Retain           Available           nfs                     9s
```


#### Create PVC

Create a PVC with below yaml file `mysql-pvc.yaml`, specify storage size, access mode, and storage class. 
The PVC will be binded with PV automatically viw storage class name. 
```
cat > mysql-pvc.yaml <<EOF
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

kubectl apply -f mysql-pvc.yaml
```



#### Consume PVC

Create a Deployment to consume the PVC created.
```
cat > mysql.yaml <<EOF
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


kubectl apply -f mysql.yaml
```

Now we can see MySQL files were moved to directory `/nfsdata` on `cka002`




### StorageClass

#### Configure RBAC Authorization

RBAC authorization uses the rbac.authorization.k8s.io API group to drive authorization decisions, allowing you to dynamically configure policies through the Kubernetes API.

* ServiceAccount: `nfs-client-provisioner`
* namespace: `jh-namespace`

* ClusterRole: `nfs-client-provisioner-runner`
* ClusterRoleBinding: `run-nfs-client-provisioner`, roleRefer: above ClusterRole, link to above ServiceAccount.

* Role: `leader-locking-nfs-client-provisioner`
* RoleBinding: `leader-locking-nfs-client-provisioner`, roleRefer: above Role, link to above ServiceAccount.


Create RBAC Authorization.
```
cat > nfs-provisioner-rbac.yaml <<EOF
apiVersion: v1
kind: ServiceAccount
metadata:
  name: nfs-client-provisioner
  # replace with namespace where provisioner is deployed
  namespace: jh-namespace
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
    namespace: jh-namespace
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
  namespace: jh-namespace
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
  namespace: jh-namespace
subjects:
  - kind: ServiceAccount
    name: nfs-client-provisioner
    # replace with namespace where provisioner is deployed
    namespace: jh-namespace
roleRef:
  kind: Role
  name: leader-locking-nfs-client-provisioner
  apiGroup: rbac.authorization.k8s.io
EOF


kubectl apply -f nfs-provisioner-rbac.yaml
```


#### Install `nfs-provisioner`

Create NFS Provisioner with below yaml file. 
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
              value: 172.16.18.160
            - name: NFS_PATH
              value: /nfsdata
      volumes:
        - name: nfs-client-root
          nfs:
            server: 172.16.18.160
            path: /nfsdata
EOF

kubectl apply -f nfs-provisioner-deployment.yaml
```


#### Create NFS StorageClass


Create yaml file `nfs-storageclass.yaml`.
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



#### Verify

##### Create PVC

Create PVC 
```
cat > storageclass-pvc.yaml <<EOF
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

kubectl apply -f storageclass-pvc.yaml
```

Check the PVC status we ceated.
```
kubectl get pvc nfs-pvc-from-sc
```
```
NAME              STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
nfs-pvc-from-sc   Bound    pvc-25eaa043-911e-46c7-b17e-f65256f52725   1Gi        RWX            nfs-client     39h
```




##### Consume PVC

Create Pod to consume the PVC>
```
cat > mysql-with-sc-pvc.yaml <<EOF
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


kubectl apply -f mysql-with-sc-pvc.yaml
```


Check the Deployment status.
```
kubectl get deployment mysql-with-sc-pvc -o wide
```
```
NAME                READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES      SELECTOR
mysql-with-sc-pvc   1/1     1            1           39h   mysql        mysql:8.0   app=mysql
```

Check related Pods status. Be noted that the Pod `mysql-with-sc-pvc-7c97d875f8-dwfkc` is running on `cka003`.
```
kubectl get pod -o wide -l app=mysql
```
```
NAME                                 READY   STATUS    RESTARTS   AGE   IP             NODE     NOMINATED NODE   READINESS GATES
mysql-774db46945-sztrp               1/1     Running   0          40h   10.244.1.23    cka002   <none>           <none>
mysql-with-sc-pvc-7c97d875f8-dwfkc   1/1     Running   0          38h   10.244.2.110   cka003   <none>           <none>
```

Let's check directory `/nfsdata/` on NFS server. 
```
ll /nfsdata/
```
Two folders were created. Same content of `/remote-nfs-dir/` on other nodes.
```
drwxrwxrwx  6 systemd-coredump root 4096 Jul 10 23:08 jh-namespace/
drwxr-xr-x  6 systemd-coredump root 4096 Jul 10 21:23 mysqldata/
```

One sub-folder's name is namespace under directory `/nfsdata/` and it is mounted to Pod.
By default, namespace name will be used at mount point. 
If we want to use customized folder for that purpose, we need claim an annotation `nfs.io/storage-path`, e.g., `test-path` in below example.
```
cat > test-claim.yaml <<EOF
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

kubectl apply -f test-claim.yaml
```

In above case, the PVC was created in `kube-system` Namespace, hence we can see directory `test-path` is under directory`kube-system`. 
Overall directory structure of folder `/nfsdata/` looks like below.
```
tree /nfsdata/
```
```
/nfsdata/
├── jh-namespace
│   ├── mysql.sock -> /var/run/mysqld/mysqld.sock
│   ├── sys
│   │   └── sys_config.ibd
│   ├── undo_001
│   └── undo_002
├── kube-system
│   └── test-path
└── mysqldata
```

Please be noted that above rule is following `nfs-subdir-external-provisioner` implementation. It's may be different with other `provisioner`.

Detail about `nfs-subdir-external-provisioner` project is [here](https://github.com/kubernetes-sigs/nfs-subdir-external-provisioner)

---



### Configuration

#### ConfigMap

Create a yaml file `configmap.yaml` for ConfigMap.
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
  name: nginx
  namespace: jh-namespace
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
cat > nginx-with-cm.yaml <<EOF
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
     name: nginx
EOF

kubectl apply -f nginx-with-cm.yaml
```

Be noted:

* By default to mount ConfigMap, Kubernetes will overwrite all content of the mount point. We can use `volumeMounts.subPath` to specify that only overwrite the file `nginx.conf`.
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

Create Secret.
```
cat > secret.yaml <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
data:
  username: YWRtaW4=
  password: MTIzNDU2
EOF

kubectl apply -f secret.yaml
```

Using Volume to mount (injection) Secret to a Pod.
```
cat > busybox-with-secret.yaml <<EOF
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

kubectl apply -f busybox-with-secret.yaml
```

Let's attach to the Pod `busybox-with-secret` to verify if two data elements of `mysecret` are successfully mounted to the path `/tmp/secret` within the Pod.
```
kubectl exec -it busybox-with-secret -- sh
```
By executing below command, we can see two data elements are in the directory `/tmp/secret` as file type. 
```
/ # ls -l /tmp/secret/
lrwxrwxrwx    1 root     root            15 Jul 12 16:13 password -> ..data/password
lrwxrwxrwx    1 root     root            15 Jul 12 16:13 username -> ..data/username
```
And we can get the content of each element, which are predefined before.
```
/ # cat /tmp/secret/username
admin

/ # cat /tmp/secret/password
123456
```



#### Additional Keys

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
  namespace: jh-namespace
  resourceVersion: "2377258"
  uid: d5ab133f-5e4d-41d4-bc9e-2bbb22a872a1
```




##### Set environment variable via ConfigMap

Here we will create a Pod `pod-configmap-env` and set the environment variable `ilike` and assign value of `favorite` from ConfigMap `colors`.
```
cat > pod-configmap-env.yaml << EOF
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

kubectl apply -f pod-configmap-env.yaml
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
cat > pod-configmap-env-2.yaml << EOF
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

kubectl apply -f pod-configmap-env-2.yaml
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






## Scheduling

### nodeSelector

Let's assume the scenario below.

* We have a group of high performance servers.
* Some applications require high performance computing.
* These applicaiton need to be scheduled and running on those high performance servers.

We can leverage Kubernetes attributes node `label` and `nodeSelector` to group resources as a whole for scheduling to meet above requirement.




#### Label Node

Here I will label `cka002` with `Configuration=hight`.

```
kubectl label node cka002 configuration=hight
```

Verify. We wil see the label `configuration=hight` on `cka002`.
```
kubectl get node --show-labels
```


#### Configure nodeSelector for Pod

Create a Pod and use `nodeSelector` to schedule the Pod running on specified node.
```
cat > mysql-nodeselector.yaml <<EOF
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

kubectl apply -f mysql-nodeselector.yaml
```

Let's check with node the Pod `mysql-nodeselector` is running.
```
kubectl get pod -l app=mysql -o wide |  grep mysql-nodeselector
```

With below result, Pod `mysql-nodeselector` is running on `cka002` node.
```
NAME                                  READY   STATUS    RESTARTS   AGE     IP             NODE     NOMINATED NODE   READINESS GATES
mysql-nodeselector-6b7d9c875d-227t6   1/1     Running   0          50s     10.244.1.26    cka002   <none>           <none>
```



### nodeName

Be noted, `nodeName` has hightest priority as it's not scheduled by `Scheduler`.

Create a Pod `nginx-nodename` with `nodeName=cka003`.
```
cat > nginx-nodename.yaml <<EOF
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

kubectl apply -f nginx-nodename.yaml
```

Verify if Pod `nginx-nodename` is running on `ckc003 node.
```
kubectl get pod -owide |grep nginx-nodename
```
```
NAME                                      READY   STATUS    RESTARTS   AGE     IP             NODE     NOMINATED NODE   READINESS GATES
nginx-nodename                            1/1     Running   0          6s      10.244.2.113   cka003   <none>           <none>
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
cat > pod_nginx.yaml <<EOF
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


kubectl apply -f pod_nginx.yaml
```

Create a Pod MySql.
```
cat > pod_mysql.yaml <<EOF
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

kubectl apply -f pod_mysql.yaml
```

As we configured `podAffinity`, so Pod `mysql` will be scheduled to the same node with Pod `nginx` by Label `app:nginx`.

Via the command `kubectl get pod -o wide` we can get two Pods are running on node `cka002`.
```
NAME                                      READY   STATUS    RESTARTS   AGE     IP             NODE     NOMINATED NODE   READINESS GATES
mysql                                     1/1     Running   0          2m48s   10.244.1.28    cka002   <none>           <none>
nginx                                     1/1     Running   0          9m53s   10.244.1.27    cka002   <none>           <none>
```








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
cat > mysql-tolerations.yaml <<EOF
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

kubectl apply -f mysql-tolerations.yaml
```

The Pod of Deployment `mysql-tolerations` is scheduled and running on node `cka003` with `tolerations` setting, which is a taint node.
```
kubectl get pod -o wide | grep mysql-tolerations
```
```
NAME                                      READY   STATUS    RESTARTS   AGE     IP             NODE     NOMINATED NODE   READINESS GATES
mysql-tolerations-5c5986944b-cg9bs        1/1     Running   0          57s     10.244.2.114   cka003   <none>           <none>
```




#### Remove Taints

```
kubectl taint nodes cka003 key-
```



## ResourceQuota

### Create Namespace

Ceate a Namespace
```
kubectl create ns quota-object-example
```

### Create ResourceQuota

Create a Namespace ResourceQuota and apply to namespace `quota-object-example`.
Within the namespace, we can only create 1 PVC, 1 LoadBalancer Service, can not create NodePort Service.
```
cat > resourcequota.yaml <<EOF
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


kubectl apply -f resourcequota.yaml
```


### Verify & Test

Check Quota status
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

#### Test NodePort

Create a Deployment `ns-quota-test` on namespace `quota-object-example`.
```
kubectl create deployment ns-quota-test --image nginx --namespace=quota-object-example
```

Expose the Deployment via NodePort    
```
kubectl expose deployment ns-quota-test --port=80 --type=NodePort --namespace=quota-object-example
```
We receive below error, which is expected because we set Quota `services.nodeports: 0`.
```shell
Error from server (Forbidden): services "ns-quota-test" is forbidden: exceeded quota: object-quota-demo, requested: services.nodeports=1, used: services.nodeports=0, limited: services.nodeports=0
```
  

#### Test PVC

Create a PVC `pvc-quota-demo` on namespace `quota-object-example`.
```
cat > test-pvc-quota.yaml << EOF
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


kubectl apply -f test-pvc-quota.yaml
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




## LimitRange

A *LimitRange* provides constraints that can:

* Enforce minimum and maximum compute resources usage per Pod or Container in a namespace.
* Enforce minimum and maximum storage request per PersistentVolumeClaim in a namespace.
* Enforce a ratio between request and limit for a resource in a namespace.
* Set default request/limit for compute resources in a namespace and automatically inject them to Containers at runtime.




### Create Namespace

Create a Namespace `default-cpu-example` for demo.
```
kubectl create namespace default-cpu-example
```

### Set LimitRange

Create LimitRange by below yaml file to define range of CPU Request and CPU Limit for a Container.
After apply LimitRange resource, the CPU limitation will affect all new created Pods.
```
cat > cpu-limitrange.yaml << EOF
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


kubectl apply -f cpu-limitrange.yaml
```



### Test via Pod

#### Scenario 1: Pod without specified limits

Create a Pod without any specified limits.
```
cat > default-cpu-demo-pod.yaml << EOF
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


kubectl apply -f default-cpu-demo-pod.yaml
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
cat > default-cpu-demo-limit.yaml <<EOF
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
cat > default-cpu-demo-request.yaml <<EOF
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

kubectl apply -f default-cpu-demo-request.yaml
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


## Troubleshooting

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
  Normal  Scheduled  55s   default-scheduler  Successfully assigned jh-namespace/tomcat to cka002
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
2m16s       Normal    Scheduled        pod/tomcat                      Successfully assigned jh-namespace/tomcat to cka002
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

#### Nodes

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

Sort output by CPU or Memory using option `--sort-by`.
```
kubectl top pod --sort-by=cpu
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
cka001   Ready                      control-plane,master   18d   v1.23.8
cka002   Ready                      <none>                 18d   v1.23.8
cka003   Ready,SchedulingDisabled   <none>                 18d   v1.23.8
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
cka001   Ready    control-plane,master   18d   v1.23.8
cka002   Ready    <none>                 18d   v1.23.8
cka003   Ready    <none>                 18d   v1.23.8
```

Evict Pods on a Node.
```
kubectl drain <node_name>
kubectl drain <node_name> --ignore-daemonsets
kubectl drain <node_name> --ignore-daemonsets --delete-emptydir-data
```



## RBAC

Role-based access control (RBAC) is a method of regulating access to computer or network resources based on the roles of individual users within the organization.

### Install cfssl

Install `cfssl` tool
```
apt install golang-cfssl
```



### Create user

#### Create file `ca-config.json`

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
- Profile will be used to sign certificate.

```
cat > ca-config.json <<EOF
{
  "signing": {
    "default": {
      "expiry": "87600h"
    },
    "profiles": {
      "kubernetes": {
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



#### Create csr file for signature

Stay in the directory `/etc/kubernetes/pki`.

Create csr file.
```
cat > test-cka-csr.json <<EOF
{
  "CN": "test-cka",
  "hosts": [],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "BeiJing",
      "L": "BeiJing",
      "O": "k8s",
      "OU": "System"
    }
  ]
}
EOF
```

Generate certifcate and key.
```
cfssl gencert -ca=ca.crt -ca-key=ca.key -config=ca-config.json -profile=kubernetes test-cka-csr.json | cfssljson -bare test-cka
```

Get below files.
```
ll -tr | grep test-cka
```
```
-rw-r--r-- 1 root root  997 Jul 13 20:11 test-cka.csr
-rw-r--r-- 1 root root  221 Jul 13 20:09 test-cka-csr.json
-rw------- 1 root root 1675 Jul 13 20:11 test-cka-key.pem
-rw-r--r-- 1 root root 1281 Jul 13 20:11 test-cka.pem
```







#### Create file kubeconfig

Export env `KUBE_APISERVER`. Put master node IP `172.16.18.161` here.
```
export KUBE_APISERVER="https://172.16.18.161:6443"
```
```
NAME     STATUS   ROLES                  AGE   VERSION   INTERNAL-IP     EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION      CONTAINER-RUNTIME
cka001   Ready    control-plane,master   18d   v1.23.8   172.16.18.161   <none>        Ubuntu 20.04.4 LTS   5.4.0-113-generic   containerd://1.5.9
cka002   Ready    <none>                 18d   v1.23.8   172.16.18.160   <none>        Ubuntu 20.04.4 LTS   5.4.0-113-generic   containerd://1.5.9
cka003   Ready    <none>                 18d   v1.23.8   172.16.18.159   <none>        Ubuntu 20.04.4 LTS   5.4.0-113-generic   containerd://1.5.9
```

Verify the setting.
```
echo $KUBE_APISERVER
```
Output:
```
https://172.16.18.161:6443
```


##### Set up cluster

Stay in the directory `/etc/kubernetes/pki`.

Generate kubeconfig file.
```
kubectl config set-cluster kubernetes --certificate-authority=/etc/kubernetes/pki/ca.crt --embed-certs=true --server=${KUBE_APISERVER} --kubeconfig=test-cka.kubeconfig
```
Output:
```
Cluster "kubernetes" set.
```

Now we get the new config file `test-cka.kubeconfig`
```
ll -tr | grep test-cka
```
Output:
```
-rw-r--r-- 1 root root  221 Jul 13 20:09 test-cka-csr.json
-rw-r--r-- 1 root root 1281 Jul 13 20:11 test-cka.pem
-rw------- 1 root root 1675 Jul 13 20:11 test-cka-key.pem
-rw-r--r-- 1 root root  997 Jul 13 20:11 test-cka.csr
-rw------- 1 root root 1671 Jul 13 20:21 test-cka.kubeconfig
```

Get content of file `test-cka.kubeconfig`.
```
cat test-cka.kubeconfig
```
```
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJT......==
    server: https://172.16.18.161:6443
  name: kubernetes
contexts: null
current-context: ""
kind: Config
preferences: {}
users: null
```




##### Set up user

In file `test-cka.kubeconfig`, user info is null. 

Set up user.
```
kubectl config set-credentials test-cka --client-certificate=/etc/kubernetes/pki/test-cka.pem --client-key=/etc/kubernetes/pki/test-cka-key.pem --embed-certs=true --kubeconfig=test-cka.kubeconfig
```
Output
```
User "test-cka" set.
```

Now file `test-cka.kubeconfig` was updated and user information was added.
```
cat test-cka.kubeconfig
```
```
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0t......Cg==
    server: https://172.16.18.161:6443
  name: kubernetes
contexts: null
current-context: ""
kind: Config
preferences: {}
users:
- name: test-cka
  user:
    client-certificate-data: LS0t...S0K
    client-key-data: LS0t......Cg==
```

Now we have a complete kubeconfig file.
When we use it to get node information, receive error below because we did not set up current-context in kubeconfig file.
```
kubectl --kubeconfig test-cka.kubeconfig get nodes
```
```
The connection to the server localhost:8080 was refused - did you specify the right host or port?
```

Current contents is empty.
```
kubectl --kubeconfig test-cka.kubeconfig config get-contexts
```
```
CURRENT   NAME   CLUSTER   AUTHINFO   NAMESPACE
```



##### Set up Context

Set up context. 
```
kubectl config set-context kubernetes --cluster=kubernetes --user=test-cka  --kubeconfig=test-cka.kubeconfig
```
Output:
```
Context "kubernetes" created.
```

Now we have context now but the `CURRENT` flag is empty.
```
kubectl --kubeconfig test-cka.kubeconfig config get-contexts
```
Output:
```
CURRENT   NAME         CLUSTER      AUTHINFO   NAMESPACE
          kubernetes   kubernetes   test-cka
```

Set up default context. The context will link clusters and users for multiple clusters environment and we can switch to different cluster.
```
kubectl config use-context kubernetes --kubeconfig=test-cka.kubeconfig 
```
```
Switched to context "kubernetes".
```

##### Verify

Now `CURRENT` is marked with `*`, that is, current-context is set up.
```
kubectl --kubeconfig=/etc/kubernetes/pki/test-cka.kubeconfig config get-contexts
```
```
CURRENT   NAME         CLUSTER      AUTHINFO   NAMESPACE
*         kubernetes   kubernetes   test-cka    
```

When we get Pods infor we get error because user `test-cka` does not have authorization in the cluster.
```
kubectl --kubeconfig=test-cka.kubeconfig get pod 
```
```
Error from server (Forbidden): pods is forbidden: User "test-cka" cannot list resource "pods" in API group "" in the namespace "default"
```
```
kubectl --kubeconfig=test-cka.kubeconfig get node
```
```
Error from server (Forbidden): nodes is forbidden: User "test-cka" cannot list resource "nodes" in API group "" at the cluster scope
```



### Role & RoleBinding

Back to home directory.
```
cd ~
```

#### Create Role and RoleBinding

Create a role `pod-reader` with only `get`,`watch`,`list` authorization for Pod resource in `default` namespace.
```
cat > role.yaml <<EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""] # Empty "" means core API group
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
EOF


kubectl apply -f role.yaml
```

Bind the role `pod-reader` to user `test-cka`.
```
cat > rolebinding.yaml << EOF
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: read-pods
  namespace: default
subjects:
- kind: User
  name: test-cka
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
EOF


kubectl apply -f rolebinding.yaml
```

#### Verify Authorization

##### Check Pod Status

Get Pods status via user `test-cka`.
```
kubectl --kubeconfig /etc/kubernetes/pki/test-cka.kubeconfig get pod
```
```
No resources found in default namespace.
```


##### Check Node Status

We receive error to get node status because the role we defined is only for Pod resource.
```
kubectl --kubeconfig /etc/kubernetes/pki/test-cka.kubeconfig get node
```
```shell
Error from server (Forbidden): nodes is forbidden: User "test-cka" cannot list resource "nodes" in API group "" at the cluster scope
```



##### Delete Pod

We receive error when try to delete a Pod because we only have `get`,`watch`,`list` for Pod, no `delete` authorization.

```
kubectl --kubeconfig /etc/kubernetes/pki/test-cka.kubeconfig delete pod nslookup
```
```
Error from server (Forbidden): pods "nslookup" is forbidden: User "test-cka" cannot delete resource "pods" in API group "" in the namespace "default"
```



##### Check Pods in other Namespace

We receive error to get Pods status in other namespace because the role we defined is only for `default` namespace.
```
kubectl --kubeconfig /etc/kubernetes/pki/test-cka.kubeconfig get pod -n kube-system
```
```
Error from server (Forbidden): pods is forbidden: User "test-cka" cannot list resource "pods" in API group "" in the namespace "kube-system"
```



### ClusterRole & ClusterRoleBinding

#### Create ClusterRole and ClusterRoleBinding

Create a ClusterRole with authorization `get`,`watch`,`list` for `nodes` resource.
```
cat > clusterrole.yaml <<EOF
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: nodes-reader
rules:
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["get", "watch", "list"]
EOF


kubectl apply -f clusterrole.yaml
```

Bind ClusterRole `nodes-reader` to user `test-cka`.

```
cat > clusterrolebinding.yaml << EOF
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: read-nodes-global
subjects:
- kind: User
  name: test-cka
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: nodes-reader
  apiGroup: rbac.authorization.k8s.io
EOF


kubectl apply -f clusterrolebinding.yaml
```

#### Verify Authorization

Try to get node information, no error received.
```
kubectl --kubeconfig /etc/kubernetes/pki/test-cka.kubeconfig get node
```
```
NAME     STATUS   ROLES                  AGE   VERSION
cka001   Ready    control-plane,master   18d   v1.23.8
cka002   Ready    <none>                 18d   v1.23.8
cka003   Ready    <none>                 18d   v1.23.8
```



## Network Policy

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

Verify status of Calico. 
```
kubectl get pod -n kube-system | grep calico
```

Output. Make sure all Pods are running
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

#### Create workload for test.

Create three Deployments `pod-netpol-1`,`pod-netpol-2`,`pod-netpol-3`.

```
cat > pod-netpol.yaml << EOF
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

kubectl apply -f pod-netpol.yaml
```

Check Pods IP.
```
kubectl get pod -owide
```
Output:
```
NAME                                      READY   STATUS    RESTARTS   AGE   IP             NODE     NOMINATED NODE   READINESS GATES
pod-netpol-1-6494f6bf8b-6nwwf             1/1     Running   0          19s   10.244.102.9   cka003   <none>           <none>
pod-netpol-2-77478d77ff-96hgd             1/1     Running   0          19s   10.244.112.9   cka002   <none>           <none>
pod-netpol-3-68977dcb48-j9fkb             1/1     Running   0          19s   10.244.102.8   cka003   <none>           <none>
```

Attach to Pod `pod-netpol-1`
```
kubectl exec -it pod-netpol-1-6494f6bf8b-6nwwf -- sh
```

Execute command `ping` to check if pod-netpol-2 and pod-netpol-3 are pingable. 
```
/ # ping 10.244.112.9
3 packets transmitted, 3 packets received, 0% packet loss

/ # ping 10.244.102.8
3 packets transmitted, 3 packets received, 0% packet loss
```



#### Deny For All Ingress

Create deny policy for all ingress.
```
cat > networkpolicy-default-deny-ingress.yaml << EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
spec:
  podSelector: {}
  policyTypes:
  - Ingress
EOF


kubectl apply -f networkpolicy-default-deny-ingress.yaml
```

Attach to Pod `pod-netpol-1` again
```
kubectl exec -it pod-netpol-1-6494f6bf8b-6nwwf -- sh
```

Execute command `ping` to check if pod-netpol-2 and pod-netpol-3 are pingable. Both ping are denied as expected.
```
/ # ping 10.244.112.9
3 packets transmitted, 0 packets received, 100% packet loss

/ # ping 10.244.102.8
3 packets transmitted, 0 packets received, 100% packet loss
```



#### Allow For Specific Ingress

Create NetworkPlicy to allow ingress from pod-netpol-1 to pod-netpol-2.
```
cat > allow-pod-netpol-1-to-pod-netpol-2.yaml <<EOF
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

kubectl apply -f allow-pod-netpol-1-to-pod-netpol-2.yaml
```

#### Verify NetworkPolicy

Attach to Pod `pod-netpol-1` again.
```
kubectl exec -it pod-netpol-1-6494f6bf8b-6nwwf -- sh
```

Execute command `ping` to check if pod-netpol-2 and pod-netpol-3 are pingable. 
As expected, pod-netpol-2 is reachable and pod-netpol-3 is still unreachable. 
```
/ # ping 10.244.112.9
3 packets transmitted, 3 packets received, 0% packet loss

/ # ping 10.244.102.8
3 packets transmitted, 0 packets received, 100% packet loss
```



### Inbound Across Namespace

#### Create workload and namespace for test

Create Namespace `ns-netpol`.
Create Deployment `pod-netpol`.

```
kubectl create ns ns-netpol

cat > pod-netpol.yaml << EOF
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


kubectl apply -f pod-netpol.yaml
```

Check Pod status on new namespace.
```
kubectl get pod -n ns-netpol
```
Output:
```
NAME                          READY   STATUS    RESTARTS   AGE
pod-netpol-5b67b6b496-zxppp   1/1     Running   0          10s
```

Attach into `pod-netpol` Pod.
```
kubectl exec -it pod-netpol-5b67b6b496-zxppp -n ns-netpol -- sh
```

Try to ping pod-netpol-2 (`10.244.112.9`) in Namespace `jh-namespace`. It's unreachable. 
```
ping 10.244.112.9
3 packets transmitted, 0 packets received, 100% packet loss
```



#### Create Allow Ingress

Create NetworkPolicy to allow access to pod-netpol-2 in namespace `jh-namespace` from all Pods in namespace `pod-netpol`.
```
cat > allow-ns-netpol-to-pod-netpol-2.yaml <<EOF
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

kubectl apply -f allow-ns-netpol-to-pod-netpol-2.yaml
```



#### Verify Policy

Attach into `pod-netpol` Pod.
```
kubectl exec -it pod-netpol-5b67b6b496-zxppp -n ns-netpol -- sh
```

Try to ping pod-netpol-2 (`10.244.112.9`) in Namespace `jh-namespace`. It's still unreachable. 
```
ping 10.244.112.9
3 packets transmitted, 0 packets received, 100% packet loss
```

What we allowed ingress is from namespace with label `allow: to-pod-netpol-2`, but namespace `ns-netpol` does not have it and we need label it.
```
kubectl label ns ns-netpol allow=to-pod-netpol-2
```

Attach into `pod-netpol` Pod.
```
kubectl exec -it pod-netpol-5b67b6b496-zxppp -n ns-netpol -- sh
```

Try to ping pod-netpol-2 (`10.244.112.9`) in Namespace `jh-namespace`. It's now reachable. 
```
ping 10.244.112.9
3 packets transmitted, 3 packets received, 0% packet loss
```

Be noted that we can use namespace default label as well.








## Cluster Management

### `etcd` Backup and Restore

#### Install `etcdctl`


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

#### Create Deployment Before Backup

Create Deployment before backup.
```
kubectl create deployment app-before-backup --image=nginx
```


#### Backup `etcd`

Command usage: 

* `<CONTROL_PLANE_IP_ADDRESS>` is the actual IP address of Control Plane.
* `--endpoints`: specify where to save backup of etcd, 2379 is etcd port.
* `--cert`: sepcify etcd certificate, which was generated by `kubeadm` and saved in `/etc/kubernetes/pki/etcd/`.
* `--key`: specify etcd certificate key, which was generated by `kubeadm` and saved in `/etc/kubernetes/pki/etcd/`.
* `--cacert`: specify etcd certificate CA, which was generated by `kubeadm` and saved in `/etc/kubernetes/pki/etcd/`.

```
etcdctl --endpoints=https://<CONTROL_PLANE_IP_ADDRESS>:2379 --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key --cacert=/etc/kubernetes/pki/etcd/ca.crt snapshot save snapshot-$(date +"%Y%m%d%H%M%S").db
```

```
etcdctl --endpoints=https://172.16.18.161:2379 --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key --cacert=/etc/kubernetes/pki/etcd/ca.crt snapshot save snapshot-$(date +"%Y%m%d%H%M%S").db
```
Output:
```
{"level":"info","ts":"2022-07-14T14:37:39.232+0800","caller":"snapshot/v3_snapshot.go:65","msg":"created temporary db file","path":"snapshot-20220714143739.db.part"}
{"level":"info","ts":"2022-07-14T14:37:39.239+0800","logger":"client","caller":"v3/maintenance.go:211","msg":"opened snapshot stream; downloading"}
{"level":"info","ts":"2022-07-14T14:37:39.239+0800","caller":"snapshot/v3_snapshot.go:73","msg":"fetching snapshot","endpoint":"https://172.16.18.161:2379"}
{"level":"info","ts":"2022-07-14T14:37:39.332+0800","logger":"client","caller":"v3/maintenance.go:219","msg":"completed snapshot read; closing"}
{"level":"info","ts":"2022-07-14T14:37:39.359+0800","caller":"snapshot/v3_snapshot.go:88","msg":"fetched snapshot","endpoint":"https://172.16.18.161:2379","size":"5.6 MB","took":"now"}
{"level":"info","ts":"2022-07-14T14:37:39.359+0800","caller":"snapshot/v3_snapshot.go:97","msg":"saved","path":"snapshot-20220714143739.db"}
```

We can get the backup file in current directory with `ls -al` command.
```
-rw------- 1 root root 5632032 Jul 14 14:37 snapshot-20220714143739.db
```



#### Create Deployment After Backup

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



#### Restore `etcd`

##### Stop Services


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
1eb9a51e0406    registry.aliyuncs.com/google_containers/kube-apiserver:v1.23.8             "kube-apiserver --ad…"    2 weeks ago     Created             k8s://kube-system/kube-apiserver-cka001/kube-apiserver
2c5e1d183fc7    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  2 weeks ago     Created             k8s://kube-system/kube-apiserver-cka001
73d0fdef9c16    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  16 hours ago    Up                  k8s://kube-system/kube-apiserver-cka001
c7e67d4cf78c    registry.aliyuncs.com/google_containers/kube-apiserver:v1.23.8             "kube-apiserver --ad…"    16 hours ago    Up                  k8s://kube-system/kube-apiserver-cka001/kube-apiserver
```
Stop those `up` status containers.
```
nerdctl -n k8s.io stop <container_id>

nerdctl -n k8s.io stop 73d0fdef9c16
nerdctl -n k8s.io stop c7e67d4cf78c
```
No `up` status `kube-apiserver` now.
```
nerdctl -n k8s.io ps -a | grep apiserver
```
```
1eb9a51e0406    registry.aliyuncs.com/google_containers/kube-apiserver:v1.23.8             "kube-apiserver --ad…"    2 weeks ago     Created             k8s://kube-system/kube-apiserver-cka001/kube-apiserver
2c5e1d183fc7    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  2 weeks ago     Created             k8s://kube-system/kube-apiserver-cka001
73d0fdef9c16    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  16 hours ago    Created             k8s://kube-system/kube-apiserver-cka001
c7e67d4cf78c    registry.aliyuncs.com/google_containers/kube-apiserver:v1.23.8             "kube-apiserver --ad…"    16 hours ago    Created             k8s://kube-system/kube-apiserver-cka001/kube-apiserver
```



Stop etcd
```
nerdctl -n k8s.io ps -a | grep etcd
```
```
5812c42bf572    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  2 weeks ago     Created             k8s://kube-system/etcd-cka001
7f4da4416356    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  16 hours ago    Up                  k8s://kube-system/etcd-cka001
897a3e83a512    registry.aliyuncs.com/google_containers/etcd:3.5.1-0                       "etcd --advertise-cl…"    16 hours ago    Up                  k8s://kube-system/etcd-cka001/etcd
ff6626664c43    registry.aliyuncs.com/google_containers/etcd:3.5.1-0                       "etcd --advertise-cl…"    2 weeks ago     Created             k8s://kube-system/etcd-cka001/etcd
```
Stop those `up` status containers.
```
nerdctl -n k8s.io stop <container_id>
```
```
nerdctl -n k8s.io stop 7f4da4416356
nerdctl -n k8s.io stop 897a3e83a512
```
No `up` status `etcd` now.
```
nerdctl -n k8s.io ps -a | grep etcd
```
```
5812c42bf572    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  2 weeks ago     Created             k8s://kube-system/etcd-cka001
7f4da4416356    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  16 hours ago    Created             k8s://kube-system/etcd-cka001
897a3e83a512    registry.aliyuncs.com/google_containers/etcd:3.5.1-0                       "etcd --advertise-cl…"    16 hours ago    Created             k8s://kube-system/etcd-cka001/etcd
ff6626664c43    registry.aliyuncs.com/google_containers/etcd:3.5.1-0                       "etcd --advertise-cl…"    2 weeks ago     Created             k8s://kube-system/etcd-cka001/etcd
```






##### Restore `etcd`

Execute the restore operation on Control Plane node with actual backup file.
```
etcdctl snapshot restore snapshot-20220714143739.db \
    --endpoints=172.16.18.161:2379 \
    --cert=/etc/kubernetes/pki/etcd/server.crt \
    --key=/etc/kubernetes/pki/etcd/server.key \
    --cacert=/etc/kubernetes/pki/etcd/ca.crt\
    --data-dir=/var/lib/etcd
```
Output:
```
Deprecated: Use `etcdutl snapshot restore` instead.

2022-07-14T15:19:53+08:00       info    snapshot/v3_snapshot.go:248     restoring snapshot      {"path": "snapshot-20220714143739.db", "wal-dir": "/var/lib/etcd/member/wal", "data-dir": "/var/lib/etcd", "snap-dir": "/var/lib/etcd/member/snap", "stack": "go.etcd.io/etcd/etcdutl/v3/snapshot.(*v3Manager).Restore\n\t/go/src/go.etcd.io/etcd/release/etcd/etcdutl/snapshot/v3_snapshot.go:254\ngo.etcd.io/etcd/etcdutl/v3/etcdutl.SnapshotRestoreCommandFunc\n\t/go/src/go.etcd.io/etcd/release/etcd/etcdutl/etcdutl/snapshot_command.go:147\ngo.etcd.io/etcd/etcdctl/v3/ctlv3/command.snapshotRestoreCommandFunc\n\t/go/src/go.etcd.io/etcd/release/etcd/etcdctl/ctlv3/command/snapshot_command.go:129\ngithub.com/spf13/cobra.(*Command).execute\n\t/go/pkg/mod/github.com/spf13/cobra@v1.1.3/command.go:856\ngithub.com/spf13/cobra.(*Command).ExecuteC\n\t/go/pkg/mod/github.com/spf13/cobra@v1.1.3/command.go:960\ngithub.com/spf13/cobra.(*Command).Execute\n\t/go/pkg/mod/github.com/spf13/cobra@v1.1.3/command.go:897\ngo.etcd.io/etcd/etcdctl/v3/ctlv3.Start\n\t/go/src/go.etcd.io/etcd/release/etcd/etcdctl/ctlv3/ctl.go:107\ngo.etcd.io/etcd/etcdctl/v3/ctlv3.MustStart\n\t/go/src/go.etcd.io/etcd/release/etcd/etcdctl/ctlv3/ctl.go:111\nmain.main\n\t/go/src/go.etcd.io/etcd/release/etcd/etcdctl/main.go:59\nruntime.main\n\t/go/gos/go1.16.15/src/runtime/proc.go:225"}
2022-07-14T15:19:53+08:00       info    membership/store.go:141 Trimming membership information from the backend...
2022-07-14T15:19:53+08:00       info    membership/cluster.go:421       added member    {"cluster-id": "cdf818194e3a8c32", "local-member-id": "0", "added-peer-id": "8e9e05c52164694d", "added-peer-peer-urls": ["http://localhost:2380"]}
2022-07-14T15:19:53+08:00       info    snapshot/v3_snapshot.go:269     restored snapshot       {"path": "snapshot-20220714143739.db", "wal-dir": "/var/lib/etcd/member/wal", "data-dir": "/var/lib/etcd", "snap-dir": "/var/lib/etcd/member/snap"}
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



##### Start Services

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



#### Verify


Check cluster status, if the Pod `app-before-backup` is there.
```
kubectl get deploy
```
```
NAME                     READY   UP-TO-DATE   AVAILABLE   AGE
app-before-backup        1/1     1            1           4h39m
```




### Upgrade `kubeadm`

#### Upgrade `Control Plane`

##### Preparation

首先驱逐节点

Evict Control Plane node.
```
kubectl drain <control_plane_node_name> --ignore-daemonsets 
```
```
kubectl drain cka001 --ignore-daemonsets 
```
```
node/cka001 cordoned
WARNING: ignoring DaemonSet-managed Pods: kube-system/calico-node-v7xdm, kube-system/kube-proxy-msw2z
node/cka001 drained
```

The Control Plane node is now in `SchedulingDisabled` status.
```
NAME     STATUS                     ROLES                  AGE   VERSION
cka001   Ready,SchedulingDisabled   control-plane,master   19d   v1.23.8
cka002   Ready                      <none>                 19d   v1.23.8
cka003   Ready                      <none>                 19d   v1.23.8
```

Check current available version of `kubeadm`.
```
apt policy kubeadm
```
```
kubeadm:
  Installed: 1.23.8-00
  Candidate: 1.24.2-00
  Version table:
     1.24.2-00 500
        500 https://mirrors.aliyun.com/kubernetes/apt kubernetes-xenial/main amd64 Packages
     1.24.1-00 500
        500 https://mirrors.aliyun.com/kubernetes/apt kubernetes-xenial/main amd64 Packages
     1.24.0-00 500
        500 https://mirrors.aliyun.com/kubernetes/apt kubernetes-xenial/main amd64 Packages
 *** 1.23.8-00 500
        500 https://mirrors.aliyun.com/kubernetes/apt kubernetes-xenial/main amd64 Packages
        100 /var/lib/dpkg/status
     1.23.7-00 500
        500 https://mirrors.aliyun.com/kubernetes/apt kubernetes-xenial/main amd64 Packages
     1.23.6-00 500
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
Components that must be upgraded manually after you have upgraded the control plane with 'kubeadm upgrade apply':
COMPONENT   CURRENT       TARGET
kubelet     3 x v1.23.8   v1.23.9

Upgrade to the latest version in the v1.23 series:

COMPONENT                 CURRENT   TARGET
kube-apiserver            v1.23.8   v1.23.9
kube-controller-manager   v1.23.8   v1.23.9
kube-scheduler            v1.23.8   v1.23.9
kube-proxy                v1.23.8   v1.23.9
CoreDNS                   v1.8.6    v1.8.6
etcd                      3.5.1-0   3.5.3-0

You can now apply the upgrade by executing the following command:

        kubeadm upgrade apply v1.23.9

_____________________________________________________________________

Components that must be upgraded manually after you have upgraded the control plane with 'kubeadm upgrade apply':
COMPONENT   CURRENT       TARGET
kubelet     3 x v1.23.8   v1.24.3

Upgrade to the latest stable version:

COMPONENT                 CURRENT   TARGET
kube-apiserver            v1.23.8   v1.24.3
kube-controller-manager   v1.23.8   v1.24.3
kube-scheduler            v1.23.8   v1.24.3
kube-proxy                v1.23.8   v1.24.3
CoreDNS                   v1.8.6    v1.8.6
etcd                      3.5.1-0   3.5.3-0

You can now apply the upgrade by executing the following command:

        kubeadm upgrade apply v1.24.3

Note: Before you can perform this upgrade, you have to update kubeadm to v1.24.3.

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





##### Upgrade

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
NAME     STATUS                     ROLES           AGE   VERSION
cka001   Ready,SchedulingDisabled   control-plane   19d   v1.24.2
cka002   Ready                      <none>          19d   v1.23.8
cka003   Ready                      <none>          19d   v1.23.8
```

等待片刻，升级完成确认节点 Ready 后，取消禁止调度
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
NAME     STATUS   ROLES           AGE   VERSION
cka001   Ready    control-plane   19d   v1.24.2
cka002   Ready    <none>          19d   v1.23.8
cka003   Ready    <none>          19d   v1.23.8
```





#### Upgrade Worker

##### Preparation

Evict Worker nodes, explicitly specify to remove local storage if needed.
```
kubectl drain <worker_node_name> --ignore-daemonsets --force
kubectl drain <worker_node_name> --ignore-daemonsets --delete-emptydir-data --force
```

```
kubectl drain cka002 --ignore-daemonsets --ignore-daemonsets --delete-emptydir-data --force
```
```
node/cka002 already cordoned
WARNING: ignoring DaemonSet-managed Pods: kube-system/calico-node-4qm45, kube-system/kube-proxy-9rrpv
evicting pod jh-namespace/mysql-nodeselector-6b7d9c875d-m862d
evicting pod quota-object-example/ns-quota-test-84c6c557b9-hkbcl
evicting pod ingress-nginx/ingress-nginx-controller-556fbd6d6f-h455s
evicting pod jh-namespace/app-before-backup-66dc9d5cb-6sqcp
evicting pod jh-namespace/pod-netpol-2-77478d77ff-96hgd
evicting pod jh-namespace/mysql-with-sc-pvc-7c97d875f8-xp42f
evicting pod kube-system/coredns-6d8c4cb4d-zdmm5
evicting pod kube-system/metrics-server-7fd564dc66-rjchn
evicting pod jh-namespace/nginx-app-1-695b7b647d-z8chz
pod/app-before-backup-66dc9d5cb-6sqcp evicted
pod/ns-quota-test-84c6c557b9-hkbcl evicted
I0714 17:19:55.890912  869782 request.go:601] Waited for 1.159970307s due to client-side throttling, not priority and fairness, request: GET:https://172.16.18.161:6443/api/v1/namespaces/jh-namespace/pods/nginx-app-1-695b7b647d-z8chz
pod/nginx-app-1-695b7b647d-z8chz evicted
pod/metrics-server-7fd564dc66-rjchn evicted
pod/mysql-nodeselector-6b7d9c875d-m862d evicted
pod/mysql-with-sc-pvc-7c97d875f8-xp42f evicted
pod/coredns-6d8c4cb4d-zdmm5 evicted
pod/ingress-nginx-controller-556fbd6d6f-h455s evicted
pod/pod-netpol-2-77478d77ff-96hgd evicted
node/cka002 drained
```

Upgrade kubeadm on **Worker node**.

Log on to `cka002` and download `kubeadm` with version `v1.24.2`.
```
sudo apt-get -y install kubeadm=1.24.2-00 --allow-downgrades
```

##### Upgrade 

Perform upgrade on **Worker node**.

Log onto `cka002`.
```
sudo kubeadm upgrade node
```

Upgrade `kubelet`.
```
sudo apt-get -y install kubelet=1.24.2-00 --allow-downgrades
sudo systemctl daemon-reload
sudo systemctl restart kubelet
```

Check node status. 
```
kubectl get node
```
```
NAME     STATUS                     ROLES           AGE   VERSION
cka001   Ready                      control-plane   19d   v1.24.2
cka002   Ready,SchedulingDisabled   <none>          19d   v1.24.2
cka003   Ready                      <none>          19d   v1.23.8
```

Make sure all nodes are in Ready status, then, enable node scheduling.
```
kubectl uncordon <worker_node_name>
```
```
kubectl uncordon cka002
```



#### Verify

```
kubectl get node
```
```
NAME     STATUS   ROLES           AGE   VERSION
cka001   Ready    control-plane   19d   v1.24.2
cka002   Ready    <none>          19d   v1.24.2
cka003   Ready    <none>          19d   v1.23.8
```

Repeat the same on node `cka003`.

Log onto `cka001` to evict node `cka003`.
```
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
NAME     STATUS   ROLES           AGE   VERSION
cka001   Ready    control-plane   19d   v1.24.2
cka002   Ready    <none>          19d   v1.24.2
cka003   Ready    <none>          19d   v1.24.2
```







## Helm Chart

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
scp -i cka-key-pair.pem helm-v3.8.2-linux-amd64.tar.gz root@cka001:/root/
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



#### Install MySQL from Helm

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

Install MySQL Chart on namespace `jh-namespace`：

```
helm install mysql bitnami/mysql -n jh-namespace
```
```
NAME: mysql
LAST DEPLOYED: Thu Jul 14 18:18:16 2022
NAMESPACE: jh-namespace
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: mysql
CHART VERSION: 9.2.0
APP VERSION: 8.0.29

** Please be patient while the chart is being deployed **

Tip:

  Watch the deployment status using the command: kubectl get pods -w --namespace jh-namespace

Services:

  echo Primary: mysql.jh-namespace.svc.cluster.local:3306

Execute the following to get the administrator credentials:

  echo Username: root
  MYSQL_ROOT_PASSWORD=$(kubectl get secret --namespace jh-namespace mysql -o jsonpath="{.data.mysql-root-password}" | base64 -d)

To connect to your database:

  1. Run a pod that you can use as a client:

      kubectl run mysql-client --rm --tty -i --restart='Never' --image  docker.io/bitnami/mysql:8.0.29-debian-11-r9 --namespace jh-namespace --env MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD --command -- bash

  2. To connect to primary service (read/write):

      mysql -h mysql.jh-namespace.svc.cluster.local -uroot -p"$MYSQL_ROOT_PASSWORD"
```

Check installed release：
```
helm list
```
```
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
mysql   jh-namespace    1               2022-07-14 18:18:16.252140606 +0800 CST deployed        mysql-9.2.0     8.0.29
```

Check installed mysql release information.
```
helm status mysql
```

Check mysql Pod status.
```
kubectl get pod
```
```
NAME                                      READY   STATUS    RESTARTS   AGE
mysql-0                                   1/1     Running   0          76s
```


**思考题**

1. 查看 MySQL Pod 运行情况，目前 Pod 状态是什么？
2. 为什么当前处于 Pending 状态？
3. 如何排查？( `kubectl describe pod` )
4. 为什么无法绑定 PVC？
5. PVC的状态是什么？( `kubectl get pvc`, `kubectl describe pvc data-mysql-0` )
6. 为什么在 `11 存储`实验中部署的 StorageClass 无法满足要求？( `accessMode` )
7. 如何手动创建满足要求的 PV？









### Develop a Chart

Below is a demo on how to develop a Chart.

1. Execute `helm create` to initiate a Chart：

```
# Naming conventions of Chart: lowercase a~z and -(minus sign)
helm create cka-demo
```

A folder `cka-demo` was created. Check the folder structure.

```
cd cka-demo/
tree
```
```
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
rm -rf charts
rm -rf templates/tests 
rm -rf templates/*.yaml
echo "" > values.yaml
echo "" > templates/NOTES.txt
echo "" > templates/_helpers.tpl
```

Now new structure looks like below.
```
├── Chart.yaml
├── templates
│   ├── _helpers.tpl
│   └── NOTES.txt
└── values.yaml
```






#### NOTES.txt

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



#### Deployment Template

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





#### ConfigMap Template

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



#### _helpers.tpl

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



#### Chart.yaml

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
  - name: Yinlin.Li
```

Final `Chart.yaml` looks like below.
```
apiVersion: v2
name: cka-demo
description: A Helm chart for CKA demo.
type: application
version: 0.1.0
appVersion: "v1.24"
maintainers:
  - name: James.H
icon: file://./kubernetes-cka-color.svg
```



#### Chart Debug

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
```
NAME: cka-demo
LAST DEPLOYED: Fri Jul 15 20:54:52 2022
NAMESPACE: cka
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
Come on! you can do it next time!
```

If any error, need to unstall `cka-demo` and reinstall it.
```
helm list --all-namespace
helm uninstall cka-demo -n <your_namespace>
```



Check container log of `busybox`.
```
kubectl logs -n cka -l app=cka-demo
```
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
LAST DEPLOYED: Fri Jul 15 20:58:01 2022
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

Check container log of `busybox`.
```
kubectl logs -n cka -l app=cka-demo
```
```
Your CKA score is 100 and your CKA certificate ID number is fwauD8TJW1OzD
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








## Homework

### 6/26

1. 将cka003节点的kubelet服务关闭


2. 在节点上发生了什么，通过nerdctl查看容器发生了什么
3. 在集群层面观察对应节点处于什么状态，本来在节点上运行的Pod发生了什么（kubectl get pod -owide -A -w持续监视Pod变化）


### 6/28

1. 用alias给kubectl设置一个别名k，以后操作kubectl就可以只打k啦，比如k get node


### 6/30

1. 创建一个具有两个容器的Pod（镜像可以随意选择）
2. DaemonSet可以设置replicas参数吗？为什么？
3. kubectl查看Pod日志时如何按关键字过滤

https://howtoforge.com/multi-container-pods-in-kubernetes/


### 7/3

1. 如何基于健康检查实操中的nginx-healthcheck模拟livenessProbe存活探针检查失败的场景？
    * 提示1：nginx-healthcheck的livenessProbe探测的是80端口的存活
    * 提示2：容器中可以执行sed
    * 提示3：nginx-healthcheck的默认配置文件位于/etc/nginx/conf.d/下
    * 提示4：Nginx的重新加载配置的命令是nginx -s reload

2. HPA计算CPU/内存扩缩容的百分比是如何计算出来的？分子和分母分别是取什么值



### 7/5

1. 通过kubectl create deploy nginx --image=nginx命令创建的Deployment，忘记加容器端口了，如何修改Deployment加上端口
2. 验证Service的internalTrafficPolicy参数



### 7/7

提示，用官网的YAML示例修改：

1. 创建一个hostPath类型的PV，目录自定义
2. 按照这个PV，创建一个PVC跟这个PV绑定
3. 创建一个Pod，挂载这个PVC，挂载目录自定义
4. 修改这个Pod，添加一个emptyDir类型的Volume挂载，挂载目录自定义


### 7/10

1. kubectl top命令查看Pod和Node的资源利用率如何按照利用率排序？



### 7/12

1. kubectl命令行方式创建ClusterRole，定义对Deployment的create权限
2. kubectl命令行方式创建一个Namespace
3. kubectl命令行方式在Namespace下创建一个ServiceAccount
4. kubectl命令行方式创建RoleBinding把上面创建的ClusterRole和ServiceAccount绑定起来











