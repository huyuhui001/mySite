# Kubernetes Tutourials: Ubuntu@Aliyun

## 1.Installation

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

Disable swap on Ubuntu.
```
sudo ufw disable
```

Check status of swap on Ubuntu.
```
sudo ufw status verbose
```


### Turn off swap

Turn off swap by command `swapoff -a` in all VMs.


### Set timezone and locale

Set timezone and local for all VMs. For ECS with Ubuntu 20.04 version created by Aliyun, this step is not needed.
```
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
sudo echo 'LANG="en_US.UTF-8"' >> /etc/profile
source /etc/profile
```
Something like this:
```
ll /etc/localtime
```
```
lrwxrwxrwx 1 root root 33 May 24 18:14 /etc/localtime -> /usr/share/zoneinfo/Asia/Shanghai
```


### Kernel setting

Perform below kernel setting in all VMs.

Create file `/etc/modules-load.d/containerd.conf` to set up containerd configure file.
It's to load two modules `overlay` and `br_netfilter`.

Service `containerd` depends on `overlay` filesystem. Sometimes referred to as union-filesystems. An [overlay-filesystem](https://developer.aliyun.com/article/660712) tries to present a filesystem which is the result over overlaying one filesystem on top of the other. 

The `br_netfilter` module is required to enable transparent masquerading and to facilitate Virtual Extensible LAN (VxLAN) traffic for communication between Kubernetes pods across the cluster. 
```
cat <<EOF | sudo tee /etc/modules-load.d/containerd.conf
overlay
br_netfilter
EOF
```

Load `overlay` and `br_netfilter` modules.
```
sudo modprobe overlay
sudo modprobe br_netfilter
```

Verify
```
lsmod | grep br_netfilter
```




Create file `99-kubernetes-cri.conf` to set up configure file for Kubernetes CRI.

Set `net/bridge/bridge-nf-call-iptables=1` to ensure simple configurations (like Docker with a bridge) work correctly with the iptables proxy. [Why `net/bridge/bridge-nf-call-iptables=1` need to be enable by Kubernetes](https://cloud.tencent.com/developer/article/1828060).

IP forwarding is also known as routing. When it comes to Linux, it may also be called Kernel IP forwarding because it uses the kernel variable `net.ipv4.ip_forward` to enable or disable the IP forwarding feature. The default preset value is `ip_forward=0`. Hence, the Linux IP forwarding feature is disabled by default.
```
cat <<EOF | sudo tee /etc/sysctl.d/99-kubernetes-cri.conf
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF
```

The `sysctl` command reads the information from the `/proc/sys` directory. `/proc/sys` is a virtual directory that contains file objects that can be used to view and set the current kernel parameters.

By commadn `sysctl -w net.ipv4.ip_forward=1`, the change takes effect immediately, but it is not persistent. After a system reboot, the default value is loaded. 
Write the settings to `/etc/sysctl.conf` is to set a parameter permanently, you’ll need to  or another configuration file in the `/etc/sysctl.d` directory:
```
sudo sysctl --system
```

Verify.
```
sysctl net.ipv4.ip_forward
```





### Install Containerd

Install Containerd sevice for all VMs.

Backup source file.
```
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
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
sudo apt-get update && sudo apt-get install -y containerd
```

Configure Containerd. Modify file `/etc/containerd/config.toml`.
```
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml
vi /etc/containerd/config.toml
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
sudo systemctl restart containerd
sudo systemctl status containerd
```

  
### Install nerdctl

Install nerdctl sevice fro all VMs.

The goal of [`nerdctl`](https://github.com/containerd/nerdctl) is to facilitate experimenting the cutting-edge features of containerd that are not present in Docker.

Get the release from the link https://github.com/containerd/nerdctl/releases.

```
wget https://github.com/containerd/nerdctl/releases/download/v0.22.0/nerdctl-0.22.0-linux-amd64.tar.gz
tar -zxvf nerdctl-0.22.0-linux-amd64.tar.gz
cp nerdctl /usr/bin/
```

Verify nerdctl.
```
nerdctl --help
```

To list local Kubernetes containers.
```
nerdctl -n k8s.io ps
```




### Install kubeadm

Update `apt-transport-https`,  `ca-certificates`, and `curl`.
```
apt-get update && sudo apt-get install -y apt-transport-https ca-certificates curl
```

Install gpg certificate. Just choose one of below command and execute.
```
# For Ubuntu 20.04 release.
curl https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg | apt-key add -

# For Ubuntu 22.04 release
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg
```

Add Kubernetes repo. Just choose one of below command and execute.
```
# For Ubuntu20.04 release
cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main
EOF

# For Ubuntu 22.04 release
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://mirrors.aliyun.com/kubernetes/apt/ \
  kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
```

Update and install dependencied packages.
```
apt-get update
apt-get install ebtables
apt-get install libxtables12
apt-get upgrade iptables
```

Check available versions of kubeadm.
```
apt policy kubeadm
```

Install `1.23.8-00` version of kubeadm and will upgrade to `1.24.2` later.
```
sudo apt-get -y install kubelet=1.23.8-00 kubeadm=1.23.8-00 kubectl=1.23.8-00 --allow-downgrades
```


### Setup Master Node

#### kubeadm init

Set up Control Plane on VM playing master node.

Check kubeadm default parameters for initialization.
```
kubeadm config print init-defaults
```
```
apiVersion: kubeadm.k8s.io/v1beta3
bootstrapTokens:
- groups:
  - system:bootstrappers:kubeadm:default-node-token
  token: abcdef.0123456789abcdef
  ttl: 24h0m0s
  usages:
  - signing
  - authentication
kind: InitConfiguration
localAPIEndpoint:
  advertiseAddress: 1.2.3.4
  bindPort: 6443
nodeRegistration:
  criSocket: /var/run/dockershim.sock
  imagePullPolicy: IfNotPresent
  name: node
  taints: null
---
apiServer:
  timeoutForControlPlane: 4m0s
apiVersion: kubeadm.k8s.io/v1beta3
certificatesDir: /etc/kubernetes/pki
clusterName: kubernetes
controllerManager: {}
dns: {}
etcd:
  local:
    dataDir: /var/lib/etcd
imageRepository: k8s.gcr.io
kind: ClusterConfiguration
kubernetesVersion: 1.23.0
networking:
  dnsDomain: cluster.local
  serviceSubnet: 10.96.0.0/12
scheduler: {}
```

Dry rune and run. Save the output, which will be used later on work nodes.

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

```
kubeadm init \
  --dry-run \
  --pod-network-cidr=10.244.0.0/16 \
  --service-cidr 11.244.0.0/16 \
  --image-repository=registry.aliyuncs.com/google_containers \
  --kubernetes-version=v1.23.8

kubeadm init \
  --pod-network-cidr=10.244.0.0/16 \
  --service-cidr 11.244.0.0/16 \
  --image-repository=registry.aliyuncs.com/google_containers \
  --kubernetes-version=v1.23.8
```


#### kubeconfig file

Set `kubeconfig` file for current user (here it's `root`).
```
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

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
*         kubernetes-admin@kubernetes   kubernetes   kubernetes-admin   dev
```

To set a context with new update, e.g, update default namespace, etc..
```
kubectl config set-context <context name> --cluster=<cluster name> --namespace=<namespace name> --user=<user name> 
```

To switch to a new context.
```
kubectl config use-contexts <context name>
```

Reference of [kubectl](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/) and [commandline](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands). 





### Setup Work Nodes

Perform on all VMs playing work nodes.
```
# kubeadm join <your master node eth0 ip>:6443 --token <token generated by kubeadm init> --discovery-token-ca-cert-hash <hash key generated by kubeadm init>
```
Use `kubeadm token` to generate the join token and hash value.
```
kubeadm token create --print-join-command
```

Verify status on master node.
```
root@cka001:~# kubectl get node
NAME     STATUS   ROLES                  AGE     VERSION
cka001   Ready    control-plane,master   24m     v1.23.8
cka002   Ready    <none>                 9m39s   v1.23.8
cka003   Ready    <none>                 9m27s   v1.23.8
```








### Install Calico or Flannel

Choose Calico or Flannel. 

For NetworkPolicy purpose, choose Calico.


#### Install Flannel

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


#### Install Calico

Here is guidance of [End-to-end Calico installation](https://projectcalico.docs.tigera.io/getting-started/kubernetes/hardway/).
Detail practice demo, can be found in section "Install Calico" of "A1.Discussion" below. 

Install Calico
```
curl https://docs.projectcalico.org/manifests/calico.yaml -O
kubectl apply -f calico.yaml
```
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


Install `calicoctl`.

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
NAME     ASN       IPV4               IPV6   
cka001   (64512)   10.4.0.1/24               
cka002   (64512)   172.16.18.160/24          
cka003   (64512)   172.16.18.159/24 
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


Verify status of Calico.
```
kubectl get pod -n kube-system | grep calico
```

Verify network status.
```
nerdctl network ls
```
```
NETWORK ID    NAME               FILE
              k8s-pod-network    /etc/cni/net.d/10-calico.conflist
0             bridge             /etc/cni/net.d/nerdctl-bridge.conflist
              host               
              none
```




### Check Cluster Status

Perform `kubectl cluster-info` command on master node we will get below information.

* Kubernetes control plane is running at https://<mster node ip>:6443
* CoreDNS is running at https://<mster node ip>:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

```
kubectl cluster-info
```

```
kubectl get nodes -owide
```
```
NAME     STATUS   ROLES                  AGE   VERSION   INTERNAL-IP     EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION      CONTAINER-RUNTIME
cka001   Ready    control-plane,master   29m   v1.23.8   172.16.18.161   <none>        Ubuntu 20.04.4 LTS   5.4.0-113-generic   containerd://1.5.9
cka002   Ready    <none>                 27m   v1.23.8   172.16.18.160   <none>        Ubuntu 20.04.4 LTS   5.4.0-113-generic   containerd://1.5.9
cka003   Ready    <none>                 27m   v1.23.8   172.16.18.159   <none>        Ubuntu 20.04.4 LTS   5.4.0-113-generic   containerd://1.5.9
```

```
kubectl get pod -A
```
```
NAMESPACE     NAME                                       READY   STATUS    RESTARTS   AGE
kube-system   calico-kube-controllers-5c64b68895-fqqsd   1/1     Running   0          19m
kube-system   calico-node-2pc7d                          1/1     Running   0          19m
kube-system   calico-node-nr8pd                          0/1     Running   0          19m
kube-system   calico-node-ssxn7                          1/1     Running   0          19m
kube-system   coredns-6d8c4cb4d-v7pvc                    1/1     Running   0          28m
kube-system   coredns-6d8c4cb4d-vlwnh                    1/1     Running   0          28m
kube-system   etcd-cka001                                1/1     Running   2          28m
kube-system   kube-apiserver-cka001                      1/1     Running   2          28m
kube-system   kube-controller-manager-cka001             1/1     Running   2          28m
kube-system   kube-proxy-55qkw                           1/1     Running   0          26m
kube-system   kube-proxy-5qllr                           1/1     Running   0          28m
kube-system   kube-proxy-qkvxh                           1/1     Running   0          27m
kube-system   kube-scheduler-cka001                      1/1     Running   2          28m
```


### Reset cluster

CAUTION: below steps will destroy current cluster. 

Delete all nodes in the cluster.
```
kubeadm reset
```
Output:
```
[reset] Reading configuration from the cluster...
[reset] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -o yaml'
W0717 08:15:17.411992 3913615 preflight.go:55] [reset] WARNING: Changes made to this host by 'kubeadm init' or 'kubeadm join' will be reverted.
[reset] Are you sure you want to proceed? [y/N]: y
[preflight] Running pre-flight checks
[reset] Stopping the kubelet service
[reset] Unmounting mounted directories in "/var/lib/kubelet"
[reset] Deleting contents of directories: [/etc/kubernetes/manifests /etc/kubernetes/pki]
[reset] Deleting files: [/etc/kubernetes/admin.conf /etc/kubernetes/kubelet.conf /etc/kubernetes/bootstrap-kubelet.conf /etc/kubernetes/controller-manager.conf /etc/kubernetes/scheduler.conf]
[reset] Deleting contents of stateful directories: [/var/lib/etcd /var/lib/kubelet /var/lib/dockershim /var/run/kubernetes /var/lib/cni]

The reset process does not clean CNI configuration. To do so, you must remove /etc/cni/net.d

The reset process does not reset or clean up iptables rules or IPVS tables.
If you wish to reset iptables, you must do so manually by using the "iptables" command.

If your cluster was setup to utilize IPVS, run ipvsadm --clear (or similar)
to reset your system's IPVS tables.

The reset process does not clean your kubeconfig files and you must remove them manually.
Please, check the contents of the $HOME/.kube/config file.
```


Clean up network setting
```
rm -rf /var/run/flannel /opt/cni /etc/cni /var/lib/cni
```

Clean up rule of `iptables`.
```
iptables -F && iptables -t nat -F && iptables -t mangle -F && iptables -X
```

Clean up rule of `IPVS` if using `IPVS`.
```
ipvsadm --clear
```



### Troubleshooting

#### Issue 1 
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



#### Issue 2 

"Container runtime network not ready" networkReady="NetworkReady=false reason:NetworkPluginNotReady message:Network plugin returns error: cni plugin not initialized"

**Try**:

Restart Containerd service.
```
sudo systemctl restart containerd
sudo systemctl status containerd
```

Till now, the initial deployment is completed sucessfully.



## 2.Post Installation

### Bash Autocomplete

Set `kubectl` [auto-completion](https://github.com/scop/bash-completion) following the [guideline](https://kubernetes.io/docs/tasks/tools/included/optional-kubectl-configs-bash-linux/).
```
apt install -y bash-completion
source /usr/share/bash-completion/bash_completion
source <(kubectl completion bash)
echo "source <(kubectl completion bash)" >> ~/.bashrc
```

### Alias

If we set an alias for kubectl, we can extend shell completion to work with that alias:
```
echo 'alias k=kubectl' >>~/.bashrc
echo 'complete -o default -F __start_kubectl k' >>~/.bashrc
```






## 3.Cluster Overview

### Container Layer

We are using Containerd service to manage our images and containers via command `nerdctl`, which is same concept with Docker.

Tasks:

* Get namespace.
* Get containers.
* Get images.
* Get volumes.
* Get overall status.
* Get network status.



Get namespaces.
```
nerdctl namespace ls
```
Result
```
NAME       CONTAINERS    IMAGES    VOLUMES    LABELS
default    1             1         0              
k8s.io     20            60        0      
```

Get containers under specific namespace with `-n` option.
```
nerdctl -n k8s.io ps
```
Result
```
CONTAINER ID    IMAGE                                                                      COMMAND                   CREATED           STATUS    PORTS    NAMES
027b1167f7d0    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  7 hours ago       Up                 k8s://kube-system/etcd-cka001
2e6e2571bb4e    registry.aliyuncs.com/google_containers/kube-apiserver:v1.23.8             "kube-apiserver --ad…"    7 hours ago       Up                 k8s://kube-system/kube-apiserver-cka001/kube-apiserver
381ee220fd2f    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  7 hours ago       Up                 k8s://kube-system/kube-scheduler-cka001
596917cbbb26    registry.aliyuncs.com/google_containers/kube-controller-manager:v1.23.8    "kube-controller-man…"    7 hours ago       Up                 k8s://kube-system/kube-controller-manager-cka001/kube-controller-manager
5fecb056a080    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  7 hours ago       Up                 k8s://kube-system/kube-controller-manager-cka001
7d94a2daaa50    registry.aliyuncs.com/google_containers/kube-proxy:v1.23.8                 "/usr/local/bin/kube…"    7 hours ago       Up                 k8s://kube-system/kube-proxy-kwhwj/kube-proxy
90ff5ef27b9d    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  7 hours ago       Up                 k8s://kube-system/kube-apiserver-cka001
9a0a6f6b0aed    docker.io/calico/node:v3.23.3                                              "start_runit"             44 seconds ago    Up                 k8s://kube-system/calico-node-94fqj/calico-node
bfbd0ba3c8e1    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  44 seconds ago    Up                 k8s://kube-system/calico-node-94fqj
ca75c9280dfd    registry.aliyuncs.com/google_containers/kube-scheduler:v1.23.8             "kube-scheduler --au…"    7 hours ago       Up                 k8s://kube-system/kube-scheduler-cka001/kube-scheduler
dc177e25c7de    registry.aliyuncs.com/google_containers/etcd:3.5.1-0                       "etcd --advertise-cl…"    7 hours ago       Up                 k8s://kube-system/etcd-cka001/etcd
e79a3f675a6e    registry.aliyuncs.com/google_containers/pause:3.6                          "/pause"                  7 hours ago       Up                 k8s://kube-system/kube-proxy-kwhwj
```

```
nerdctl -n default ps
```
Result
```
CONTAINER ID    IMAGE                             COMMAND                   CREATED        STATUS    PORTS                 NAMES
96e5f2ac531a    docker.io/library/nginx:alpine    "/docker-entrypoint.…"    2 weeks ago    Up        0.0.0.0:80->80/tcp    nginx
```

Get images.
```
nerdctl image ls -a
nerdctl -n k8s.io image ls -a
```

Get volumes
```
nerdctl -n default volume ls
nerdctl -n k8s.io volume ls
```

Get overall status
```
nerdctl stats
```
Result
```
CONTAINER ID   NAME      CPU %     MEM USAGE / LIMIT   MEM %     NET I/O           BLOCK I/O     PIDS
96e5f2ac531a   nginx     0.00%     4.684MiB / 8EiB     0.00%     30.3kB / 36.5kB   6.21MB / 0B   3
```

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
eth0                 : inet 172.16.18.161/24 brd 172.16.18.255 qlen 1000
tunl0@NONE           : inet 10.244.228.192/32 scope global tunl0
caliba807c85a4d@if4  :
caliddefc8c6f4a@if4  :
nerdctl0             : inet 10.4.0.1/24 brd 10.4.0.255 scope global nerdctl0
vethf06612f5@if3     :
```





### Kubernetes Layer

Kubernetes is beyond container layer. 

Summary: 

* Nodes
* Namespaces
* System Pods
* Contexts

#### Node

In Kubernetes layer, we have three nodes here, `cka001`, `cka002`, and `cka003`.

Get nodes status.
```
kubectl get node
```
Result
```
NAME     STATUS   ROLES                  AGE     VERSION   INTERNAL-IP     EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION      CONTAINER-RUNTIME
cka001   Ready    control-plane,master   6h59m   v1.23.8   172.16.18.161   <none>        Ubuntu 20.04.4 LTS   5.4.0-113-generic   containerd://1.5.9
cka002   Ready    <none>                 6h57m   v1.23.8   172.16.18.160   <none>        Ubuntu 20.04.4 LTS   5.4.0-113-generic   containerd://1.5.9
cka003   Ready    <none>                 6h57m   v1.23.8   172.16.18.159   <none>        Ubuntu 20.04.4 LTS   5.4.0-113-generic   containerd://1.5.9
```

#### Namespaces

We have four initial namespaces across three nodes.
```
kubectl get namespace -A
```
Result
```
NAME              STATUS   AGE
default           Active   27h
kube-node-lease   Active   27h
kube-public       Active   27h
kube-system       Active   27h
```

#### System Pods

We have some initial pods. 
```
kubectl get pod -A -o wide
```
Result
```
NAMESPACE     NAME                                       READY   STATUS    RESTARTS   AGE     IP               NODE     NOMINATED NODE   READINESS GATES
kube-system   calico-kube-controllers-5c64b68895-fqqsd   1/1     Running   0          4h40m   10.244.228.194   cka001   <none>           <none>
kube-system   calico-node-2pc7d                          1/1     Running   0          4h40m   172.16.18.159    cka003   <none>           <none>
kube-system   calico-node-nr8pd                          0/1     Running   0          4h40m   172.16.18.161    cka001   <none>           <none>
kube-system   calico-node-ssxn7                          1/1     Running   0          4h40m   172.16.18.160    cka002   <none>           <none>
kube-system   coredns-6d8c4cb4d-v7pvc                    1/1     Running   0          4h48m   10.244.228.193   cka001   <none>           <none>
kube-system   coredns-6d8c4cb4d-vlwnh                    1/1     Running   0          4h48m   10.244.102.1     cka003   <none>           <none>
kube-system   etcd-cka001                                1/1     Running   2          4h48m   172.16.18.161    cka001   <none>           <none>
kube-system   kube-apiserver-cka001                      1/1     Running   2          4h48m   172.16.18.161    cka001   <none>           <none>
kube-system   kube-controller-manager-cka001             1/1     Running   2          4h48m   172.16.18.161    cka001   <none>           <none>
kube-system   kube-proxy-55qkw                           1/1     Running   0          4h47m   172.16.18.159    cka003   <none>           <none>
kube-system   kube-proxy-5qllr                           1/1     Running   0          4h48m   172.16.18.161    cka001   <none>           <none>
kube-system   kube-proxy-qkvxh                           1/1     Running   0          4h47m   172.16.18.160    cka002   <none>           <none>
kube-system   kube-scheduler-cka001                      1/1     Running   2          4h48m   172.16.18.161    cka001   <none>           <none>
```

Summary below shows the relationship between containers and pods. 

Good references about container pause: [article](https://zhuanlan.zhihu.com/p/464712164) and [artical](https://cloud.tencent.com/developer/article/1583919).

* Master node:
    * CoreDNS: 1 Pod
    * etcd: 1 Pod
    * apiserver: 1 Pod
    * controller-manager: 1 Pod
    * scheduler: 1 Pod
* All nodes:
    * Calico: 
        * Controller: 1 Pod
        * Node: 1 Pod
    * Proxy: 1 Pod



#### Contexts

Let's check current configuration context of Kubernetes we just initialized. 

```
kubectl config get-contexts
```

* Contenxt name is `kubernetes-admin@kubernetes`.
* Cluster name is `kubernetes`.
* User is `kubernetes-admin`.
* No namespace explicitly defined.

```
CURRENT   NAME                          CLUSTER      AUTHINFO           NAMESPACE
*         kubernetes-admin@kubernetes   kubernetes   kubernetes-admin 
```

Create a new namespace `dev`.
```
kubectl create namespace dev
```

Update current context `kubernetes-admin@kubernetes` with new namespace `dev` as default namespace. 
```
kubectl config set-context kubernetes-admin@kubernetes --cluster=kubernetes --namespace=dev --user=kubernetes-admin 
```

Now default namespace is shown in current configuration context. 
```
kubectl config get-contexts
```
Result
```
CURRENT   NAME                          CLUSTER      AUTHINFO           NAMESPACE
*         kubernetes-admin@kubernetes   kubernetes   kubernetes-admin   dev
```

With below command we create a pod `my-first-pod` on namespace `dev`.
```
kubectl apply -f - << EOF
apiVersion: v1
kind: Pod
metadata:
  namespace: dev
  name: my-first-pod
spec:
  containers:
  - name: nginx
    image: nginx:mainline
    ports:
    - containerPort: 80
EOF
```

By command `kubectl get pod -o wide` we get the pod status. The Pod is running on node `cka002`. The pod's ip is allocated by `tunl0`. Node is assigned by `Scheduler`. 
```
NAME           READY   STATUS    RESTARTS   AGE   IP             NODE     NOMINATED NODE   READINESS GATES
my-first-pod   1/1     Running   0          52s   10.244.112.1   cka002   <none>           <none>
```

Log onto node `cka002`, we can find the containers of Pod `my-first-pod` via command `nerdctl -n k8s.io container ls | grep my-first-pod`.
```
CONTAINER ID    IMAGE                                                         COMMAND                   CREATED           STATUS    PORTS    NAMES
3f9bdafde24f    docker.io/library/nginx:mainline                              "/docker-entrypoint.…"    11 minutes ago    Up                 k8s://dev/my-first-pod/nginx
dab890f44541    registry.aliyuncs.com/google_containers/pause:3.6             "/pause"                  11 minutes ago    Up                 k8s://dev/my-first-pod
```







## 4.Kubernetes API and Resource

### kubectl

Three approach to operate Kubernetes cluster:

* via [API](https://kubernetes.io/docs/reference/kubernetes-api/)
* via kubectl
* via Dashboard


Get cluster status.
```
kubectl cluster-info
kubectl cluster-info dump
```

Get health status of control plane.
```
kubectl get componentstatuses
kubectl get cs
```

Get node status.
```
kubectl get nodes
kubectl get nodes -o wide
```


### Static Pod

`kubectl` will automatically check yaml file in `/etc/kubernetes/manifests/` and create the static pod once it's detected.

Some system static Pods are already in place.
```
ll /etc/kubernetes/manifests/
```
Result
```
-rw------- 1 root root 2292 Jul 21 09:04 etcd.yaml
-rw------- 1 root root 3889 Jul 21 09:04 kube-apiserver.yaml
-rw------- 1 root root 3395 Jul 21 09:04 kube-controller-manager.yaml
-rw------- 1 root root 1464 Jul 21 09:04 kube-scheduler.yaml
```

Create yaml file in directory `/etc/kubernetes/manifests/`.
```
kubectl run my-nginx --image=nginx:mainline --dry-run=client -n dev -oyaml > /etc/kubernetes/manifests/my-nginx.yaml
```
Check status of the Pod `my-nginx`.
```
kubectl get pod
```
The node name `cka001` is part of the Pod name, which means the Pod is running on node `cka001`.
```
NAME              READY   STATUS    RESTARTS   AGE
my-nginx-cka001   1/1     Running   0          106s
```

Delete the yaml file `/etc/kubernetes/manifests/my-nginx.yaml`, the static pod will be deleted automatically.
```
rm /etc/kubernetes/manifests/my-nginx.yaml 
```


### Mutil-Container Pod

Summary:



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

Get details of the pod we created via command `kubectl describe pod multi-container-pod` and we can see below events.
```
.......
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  47s   default-scheduler  Successfully assigned dev/multi-container-pod to cka002
  Normal  Pulling    46s   kubelet            Pulling image "nginx"
  Normal  Pulled     44s   kubelet            Successfully pulled image "nginx" in 2.110312099s
  Normal  Created    44s   kubelet            Created container container-1-nginx
  Normal  Started    44s   kubelet            Started container container-1-nginx
  Normal  Pulling    44s   kubelet            Pulling image "alpine"
  Normal  Pulled     35s   kubelet            Successfully pulled image "alpine" in 8.754753417s
  Normal  Created    35s   kubelet            Created container container-2-alpine
  Normal  Started    35s   kubelet            Started container container-2-alpine
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
::1 - - [02/Jul/2022:01:12:29 +0000] "GET / HTTP/1.1" 200 615 "-" "Wget" "-"
```

Same if we need specify container name to login into the pod via command `kubectl exec -it <pod_name> -c <container_name> -- <commands>`.
```
kubectl exec -it multi-container-pod -c container-1-nginx -- /bin/bash
root@multi-container-pod:/# ls
bin  boot  dev  docker-entrypoint.d  docker-entrypoint.sh  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
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
NAME        READY   STATUS     RESTARTS   AGE
myapp-pod   0/1     Init:0/2   0          12m
```

Inspect Pods.
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
mydb        ClusterIP   11.244.233.190   <none>        80/TCP    11m
myservice   ClusterIP   11.244.189.202   <none>        80/TCP    11m
```
Get current Pod status.
```
kubectl get pod myapp-pod -o wide
```
The Pod is up.
```
NAME        READY   STATUS    RESTARTS   AGE   IP              NODE     NOMINATED NODE   READINESS GATES
myapp-pod   1/1     Running   0          13m   10.244.112.14   cka002   <none>           <none>
```

We now see that those init containers complete, and that the myapp-pod Pod moves into the Running state.



Clean up.
```
kubectl delete service mydb myservice 
kubectl delete pod myapp-pod 
```





### StatefulSet

Summary: 

* Create Headless Service and StatefulSet
* Scale out StatefulSet


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
NAME     READY   STATUS    RESTARTS   AGE
web-0    1/1     Running   0          28s
web-1    1/1     Running   0          24s
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
kubectl get pod -o wide | grep daemonset-busybox
```
```
NAME                      READY   STATUS    RESTARTS   AGE    IP               NODE     NOMINATED NODE   READINESS GATES
daemonset-busybox-cs95s   1/1     Running   0          102s   10.244.228.196   cka001   <none>           <none>
daemonset-busybox-twhhl   1/1     Running   0          102s   10.244.112.26    cka002   <none>           <none>
daemonset-busybox-vkp9c   1/1     Running   0          102s   10.244.102.18    cka003   <none>           <none>
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
kubectl get pod pi-572n5
```

Get log info of the Job Pod.
```
kubectl logs pi-572n5
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
kubectl get cronjobs
```

Monitor Jobs. Every 1 minute a new job will be created. 
```
kubectl get jobs -w
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
default           Active   34h
dev               Active   27h
kube-node-lease   Active   34h
kube-public       Active   34h
kube-system       Active   34h
```

Get Pod under a specific namespace.
```
kubectl get pod -n kube-system
```
Result
```
NAME                                       READY   STATUS    RESTARTS   AGE
calico-kube-controllers-5c64b68895-fqqsd   1/1     Running   0          34h
calico-node-2pc7d                          1/1     Running   0          34h
calico-node-nr8pd                          0/1     Running   0          34h
calico-node-ssxn7                          1/1     Running   0          34h
coredns-6d8c4cb4d-v7pvc                    1/1     Running   0          34h
coredns-6d8c4cb4d-vlwnh                    1/1     Running   0          34h
etcd-cka001                                1/1     Running   2          34h
kube-apiserver-cka001                      1/1     Running   2          34h
kube-controller-manager-cka001             1/1     Running   2          34h
kube-proxy-55qkw                           1/1     Running   0          34h
kube-proxy-5qllr                           1/1     Running   0          34h
kube-proxy-qkvxh                           1/1     Running   0          34h
kube-scheduler-cka001                      1/1     Running   2          34h
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
default   1         26h
```

Get current Token for ServiceAccount `default` on Namespace `dev`.
```
kubectl get secrets -n dev
```
```
NAME                  TYPE                                  DATA   AGE
default-token-jgfcn   kubernetes.io/service-account-token   3      22h
```

There is a default cluster role `admin`.
```
kubectl get clusterrole admin
```
Result
```
NAME    CREATED AT
admin   2022-07-21T01:04:59Z
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

We will receive below error message. The ServiceAccount `default` does not have authorization to access pod.
```
"message": "pods is forbidden: User \"system:serviceaccount:dev:default\" cannot list resource \"pods\" in API group \"\" in the namespace \"dev\"",
```

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
rolebinding-admin   ClusterRole/admin   39s
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
kubectl attach ubuntu -c ubuntu -i -t
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
myapp   1/1     1            1           5s    kubernetes-bootcamp   docker.io/jocatalin/kubernetes-bootcamp:v1   app=myapp
```

Get detail information of deployment.
```
kubectl describe deployment myapp
```
Result
```
Name:                   myapp
Namespace:              dev
CreationTimestamp:      Fri, 22 Jul 2022 20:28:46 +0800
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
  Type    Reason             Age    From                   Message
  ----    ------             ----   ----                   -------
  Normal  ScalingReplicaSet  2m15s  deployment-controller  Scaled up replica set myapp-b5d775f5d to 1
```



#### Expose Service

Get the Pod and Deployment we created just now.
```
kubectl get deployment myapp -o wide
kubectl get pod -o wide
```
Result
```
NAME                    READY   STATUS    RESTARTS      AGE     IP              NODE     NOMINATED NODE   READINESS GATES
myapp-b5d775f5d-kss4t   1/1     Running   0             5m33s   10.244.102.10   cka003   <none>           <none>
```

Send http request to the Pod `curl 10.244.102.10:8080` with below result.
```
Hello Kubernetes bootcamp! | Running on: myapp-b5d775f5d-6jtgs | v=1
```

To make pod be accessed outside, we need expose port `8080` to a node port. A related service will be created. 
```
kubectl expose deployment myapp --type=NodePort --port=8080
```

Get details of service `myapp` by executing `kubectl get svc myapp -o wide`.
```
NAME    TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE   SELECTOR
myapp   NodePort   11.244.141.12   <none>        8080:32566/TCP   15s   app=myapp
```

Get more details of the service.
```
kubectl get svc myapp -o yaml
kubectl describe svc myapp
```

Get details of related endpoint `myapp` by executing `kubectl get endpoints myapp -o wide`.
```
NAME    ENDPOINTS            AGE
myapp   10.244.102.10:8080   70s
```

Send http request to the service and node sucessfully. Pod port `8080` is mapped to node port `32566`.

Send http request to node port on `cka003`.
```
curl 172.16.18.159:32566
Hello Kubernetes bootcamp! | Running on: myapp-b5d775f5d-6jtgs | v=1
```

Attach to Ubuntu Pod we created and send http request to the Service and Pod of `myapp`.
```
kubectl attach ubuntu -c ubuntu -i -t
curl 10.244.102.10:8080
curl 11.244.141.12:8080
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
kubectl set image deployment/myapp kubernetes-bootcamp=docker.io/jocatalin/kubernetes-bootcamp:v3 --record
kubectl set image deployment/myapp kubernetes-bootcamp=docker.io/jocatalin/kubernetes-bootcamp:v4 --record
kubectl set image deployment/myapp kubernetes-bootcamp=docker.io/jocatalin/kubernetes-bootcamp:v5 --record
```

Current replicas status
```
kubectl get replicaset -o wide -l app=myapp
```
Result
```
NAME               DESIRED   CURRENT   READY   AGE     CONTAINERS            IMAGES                                       SELECTOR
myapp-5dbd68cc99   0         0         0       6m40s   kubernetes-bootcamp   docker.io/jocatalin/kubernetes-bootcamp:v2   app=myapp,pod-template-hash=5dbd68cc99
myapp-699dc8ccb9   0         0         0       6m40s   kubernetes-bootcamp   docker.io/jocatalin/kubernetes-bootcamp:v4   app=myapp,pod-template-hash=699dc8ccb9
myapp-75ccb85dd6   1         1         0       6m38s   kubernetes-bootcamp   docker.io/jocatalin/kubernetes-bootcamp:v5   app=myapp,pod-template-hash=75ccb85dd6
myapp-78bdb65cd8   0         0         0       6m40s   kubernetes-bootcamp   docker.io/jocatalin/kubernetes-bootcamp:v3   app=myapp,pod-template-hash=78bdb65cd8
myapp-b5d775f5d    3         3         3       38m     kubernetes-bootcamp   docker.io/jocatalin/kubernetes-bootcamp:v1   app=myapp,pod-template-hash=b5d775f5d
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
    deployment.kubernetes.io/revision: "5"
    kubernetes.io/change-cause: kubectl set image deployment/myapp kubernetes-bootcamp=docker.io/jocatalin/kubernetes-bootcamp:v5
      --record=true
  creationTimestamp: "2022-07-22T12:28:46Z"
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
3         kubectl set image deployment/myapp kubernetes-bootcamp=docker.io/jocatalin/kubernetes-bootcamp:v3 --record=true
4         kubectl set image deployment/myapp kubernetes-bootcamp=docker.io/jocatalin/kubernetes-bootcamp:v4 --record=true
5         kubectl set image deployment/myapp kubernetes-bootcamp=docker.io/jocatalin/kubernetes-bootcamp:v5 --record=true
```

Get rollout history with specific revision.
```
kubectl rollout history deployment/myapp --revision=2
```

Roll back to previous revision with command `kubectl rollout undo `, or roll back to specific revision with option `--to-revision=<revision_number>`.
```
kubectl rollout undo deployment/myapp --to-revision=3
```

Revision 3 was replaced by new revision 6 now.
```
kubectl rollout history deployment/myapp
```
Result
```
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
kubectl describe pod myapp-b5d775f5d-smcfv
```

Result looks like below.
```
......
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  13m   default-scheduler  Successfully assigned dev/myapp-b5d775f5d-smcfv to cka002
  Normal  Pulled     13m   kubelet            Container image "docker.io/jocatalin/kubernetes-bootcamp:v1" already present on machine
  Normal  Created    13m   kubelet            Created container kubernetes-bootcamp
  Normal  Started    13m   kubelet            Started container kubernetes-bootcamp
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
kubectl logs -f myapp-b5d775f5d-smcfv
```
```
Kubernetes Bootcamp App Started At: 2022-07-22T12:57:52.828Z | Running On:  myapp-b5d775f5d-smcfv
```

Get log info of K8s components. 
```
kubectl logs kube-apiserver-cka001 -n kube-system
kubectl logs kube-controller-manager-cka001 -n kube-system
kubectl logs kube-scheduler-cka001 -n kube-system
kubectl logs etcd-cka001 -n kube-system
systemctl status kubelet
journalctl -fu kubelet
kubectl logs kube-proxy-qkvxh -n kube-system
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
Name:                   nginx
Namespace:              dev
CreationTimestamp:      Fri, 22 Jul 2022 22:53:44 +0800
Labels:                 app=nginx
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=nginx
Replicas:               1 desired | 1 updated | 1 total | 1 available | 0 unavailable
StrategyType:           RollingUpdate
......
```

Add new Annotation.
```
kubectl annotate deployment nginx owner=James.H
```

Now annotation looks like below.
```
Labels:                 app=nginx
Annotations:            deployment.kubernetes.io/revision: 1
                        owner: James.H
Selector:               app=nginx
```

Update/Overwrite Annotation.
```
kubectl annotate deployment/nginx owner=K8s --overwrite
```
Now annotation looks like below.
```
Annotations:            deployment.kubernetes.io/revision: 1
                        owner: K8s
Selector:               app=nginx
```

Remove Annotation
```
kubectl annotate deployment/nginx owner-
```
```
Labels:                 app=nginx
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=nginx
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
      Started:      Fri, 22 Jul 2022 22:59:57 +0800
    Ready:          True
    Restart Count:  0
    ......
  busybox:
    ......
    State:          Waiting
      Reason:       CrashLoopBackOff
    Last State:     Terminated
      Reason:       Completed
      Exit Code:    0
      Started:      Fri, 22 Jul 2022 23:01:37 +0800
      Finished:     Fri, 22 Jul 2022 23:01:37 +0800
    Ready:          False
    Restart Count:  4
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
Events:
  Type     Reason     Age                   From               Message
  ----     ------     ----                  ----               -------
  Normal   Scheduled  4m21s                 default-scheduler  Successfully assigned dev/liveness-exec to cka002
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
Events:
  Type     Reason     Age               From               Message
  ----     ------     ----              ----               -------
  Normal   Scheduled  35s               default-scheduler  Successfully assigned dev/readiness to cka003
  Normal   Pulling    35s               kubelet            Pulling image "busybox"
  Normal   Pulled     32s               kubelet            Successfully pulled image "busybox" in 2.420171698s
  Normal   Created    32s               kubelet            Created container readiness
  Normal   Started    32s               kubelet            Started container readiness
  Warning  Unhealthy  5s (x4 over 20s)  kubelet            Readiness probe failed: cat: can't open '/tmp/healthy': No such file or directory
```


Liveness probes do not wait for readiness probes to succeed. 
If we want to wait before executing a liveness probe you should use initialDelaySeconds or a startupProbe.



### Demo: Health Check

Summary:

* Create Deployment and Service


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
nginx-healthcheck-79fc55d944-6xv98   0/1     Running   0          6s    10.244.112.35   cka002   <none>           <none>
nginx-healthcheck-79fc55d944-xqpsp   0/1     Running   0          6s    10.244.102.42   cka003   <none>           <none>
```

Access Pod IP via `curl` command, e.g., above example.
```
curl 10.244.112.35
curl 10.244.102.42
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
IP:                       11.244.236.198
IPs:                      11.244.236.198
Port:                     <unset>  80/TCP
TargetPort:               80/TCP
NodePort:                 <unset>  32159/TCP
Endpoints:                10.244.102.42:80,10.244.112.35:80
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
nginx-healthcheck   10.244.102.42:80,10.244.112.35:80   33m
```

Till now, two `nginx-healthcheck` Pods are working and providing service as expected. 


#### Simulate Error

Let's simulate an error by deleting and `index.html` file in on of `nginx-healthcheck` Pod and see what's readinessProbe will do.

First, execute `kubectl exec -it <your_pod_name> -- bash` to log into `nginx-healthcheck` Pod, and delete the `index.html` file.
```
kubectl exec -it nginx-healthcheck-79fc55d944-6xv98 -- bash
cd /usr/share/nginx/html/
rm -rf index.html
exit
```

After that, let's check the status of above Pod that `index.html` file was deleted.
```
kubectl describe pod nginx-healthcheck-79fc55d944-6xv98
```

We can now see `Readiness probe failed` error event message.
```
Events:
  Type     Reason     Age               From               Message
  ----     ------     ----              ----               -------
  Normal   Scheduled  35m               default-scheduler  Successfully assigned dev/nginx-healthcheck-79fc55d944-6xv98 to cka002
  Normal   Pulled     35m               kubelet            Container image "nginx:latest" already present on machine
  Normal   Created    35m               kubelet            Created container nginx-healthcheck
  Normal   Started    35m               kubelet            Started container nginx-healthcheck
  Warning  Unhealthy  4s (x5 over 19s)  kubelet            Readiness probe failed: HTTP probe failed with statuscode: 403
```

Let's check another Pod. 
```
kubectl describe pod nginx-healthcheck-79fc55d944-xqpsp
```
There is no error info.
```
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  37m   default-scheduler  Successfully assigned dev/nginx-healthcheck-79fc55d944-xqpsp to cka003
  Normal  Pulled     37m   kubelet            Container image "nginx:latest" already present on machine
  Normal  Created    37m   kubelet            Created container nginx-healthcheck
  Normal  Started    37m   kubelet            Started container nginx-healthcheck
```

Now, access Pod IP via `curl` command and see what the result of each Pod.
```
curl 10.244.102.42:80
curl 10.244.112.35:80
```

`curl 10.244.102.42:80` works well.
`curl 10.244.112.35:80` failed with `forbideen` error below. 
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
Namespace:                dev
Labels:                   <none>
Annotations:              <none>
Selector:                 name=nginx-healthcheck
Type:                     NodePort
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       11.244.236.198
IPs:                      11.244.236.198
Port:                     <unset>  80/TCP
TargetPort:               80/TCP
NodePort:                 <unset>  32159/TCP
Endpoints:                10.244.102.42:80
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
nginx-healthcheck   10.244.102.42:80   41m
```


#### Fix Error & Verify

Let's re-create the `index.html` file again in the Pod. 
```
kubectl exec -it nginx-healthcheck-79fc55d944-6xv98 -- bash

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
curl 10.244.102.42:80
curl 10.244.112.35:80
```

Verify the Pod status again. 
```
kubectl describe pod nginx-healthcheck-79fc55d944-6xv98
```

#### Conclusion

By delete the `index.html` file, the Pod is in unhealth status and is removed from endpoint list. 
One one health Pod can provide normal service.







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





## 9.Horizontal Pod Autoscaling (HPA)


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



## 10.Service

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
Address 1: 10.100.67.181 httpd-app.dev.svc.cluster.local
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
Address 1: 10.244.2.99 web-0.web.dev.svc.cluster.local
Address 2: 10.244.1.20 web-1.web.dev.svc.cluster.local
```

We can also use `nslookup` for `web-0.web` and `web-0.web`. Every Pod of Headless Service has own Service Name for DNS lookup.
```
/ # nslookup web-0.web
Server:    10.96.0.10
Address 1: 10.96.0.10 kube-dns.kube-system.svc.cluster.local

Name:      web-0.web
Address 1: 10.244.2.99 web-0.web.dev.svc.cluster.local
```

Clean up all resources created before.






## 11.Ingress

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


## 12.Storage

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
* namespace: `dev`

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
drwxrwxrwx  6 systemd-coredump root 4096 Jul 10 23:08 dev/
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
├── dev
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
  namespace: dev
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






## 13.Scheduling

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



## 14.ResourceQuota

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




## 15.LimitRange

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


## 16.Troubleshooting

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



## 17.RBAC

Role-based access control (RBAC) is a method of regulating access to computer or network resources based on the roles of individual users within the organization.


When using client certificate authentication, we can generate certificates manually through `easyrsa`, `openssl` or `cfssl`.

Tasks in this section:

1. Create differnet profiles for one cluster.
2. Use `cfssl` generate certificates for each profile.
3. Create new kubeconfig file with all profiles and associated users.
4. Merge old and new kubeconfig files into new kubeconfig file. We can switch different context for further demo.

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
*         kubernetes-admin@kubernetes   kubernetes   kubernetes-admin 
```


#### Create CA Config File


Get overview of directory `/etc/kubernetes/pki`.
```
tree /etc/kubernetes/pki
```
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
-rw-r--r-- 1 root root  222 Jul 18 20:36 cka-dev-csr.json
-rw-r--r-- 1 root root 1281 Jul 18 20:49 cka-dev.pem
-rw------- 1 root root 1679 Jul 18 20:49 cka-dev-key.pem
-rw-r--r-- 1 root root 1001 Jul 18 20:49 cka-dev.csr
```







#### Create file kubeconfig

Get the IP of Control Plane (e.g., `172.16.18.161` here) to composite evn variable `KUBE_APISERVER` (`https://<control_plane_ip>:<port>`).
```
kubectl get node -owide
```
```
NAME     STATUS   ROLES                  AGE   VERSION   INTERNAL-IP     EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION      CONTAINER-RUNTIME
cka001   Ready    control-plane,master   18d   v1.23.8   172.16.18.161   <none>        Ubuntu 20.04.4 LTS   5.4.0-113-generic   containerd://1.5.9
cka002   Ready    <none>                 18d   v1.23.8   172.16.18.160   <none>        Ubuntu 20.04.4 LTS   5.4.0-113-generic   containerd://1.5.9
cka003   Ready    <none>                 18d   v1.23.8   172.16.18.159   <none>        Ubuntu 20.04.4 LTS   5.4.0-113-generic   containerd://1.5.9
```

Export env `KUBE_APISERVER`.
```
echo "export KUBE_APISERVER=\"https://172.16.18.161:6443\"" >> ~/.bashrc
source ~/.bashrc
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
kubectl config set-cluster kubernetes \
  --certificate-authority=/etc/kubernetes/pki/ca.crt \
  --embed-certs=true \
  --server=${KUBE_APISERVER} \
  --kubeconfig=cka-dev.kubeconfig
```

Now we get the new config file `cka-dev.kubeconfig`
```
ll -tr | grep cka-dev
```
Output:
```
-rw-r--r-- 1 root root  222 Jul 18 20:36 cka-dev-csr.json
-rw-r--r-- 1 root root 1281 Jul 18 20:49 cka-dev.pem
-rw------- 1 root root 1679 Jul 18 20:49 cka-dev-key.pem
-rw-r--r-- 1 root root 1001 Jul 18 20:49 cka-dev.csr
-rw------- 1 root root 1671 Jul 18 20:50 cka-dev.kubeconfig
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
    server: https://172.16.18.161:6443
  name: kubernetes
contexts: null
current-context: ""
kind: Config
preferences: {}
users: null
```




##### Set up user

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
    server: https://172.16.18.161:6443
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



##### Set up Context

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


##### Verify

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
    server: https://172.16.18.161:6443
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    user: cka-dev
  name: cka-dev@kubernetes
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
          cka-dev@kubernetes            kubernetes   cka-dev            
*         kubernetes-admin@kubernetes   kubernetes   kubernetes-admin   
```



### Namespaces & Contexts

Get list of Namespace with Label information.
```
kubectl get ns --show-labels
```

Create Namespace `dev`.
```
kubectl create namespace dev
```

Use below command to set a context with new update, e.g, update default namespace, etc..
```
kubectl config set-context <context name> --cluster=<cluster name> --namespace=<namespace name> --user=<user name> 
```

Let's set default namespace to each context.
```
kubectl config set-context kubernetes-admin@kubernetes --cluster=kubernetes --namespace=default --user=kubernetes-admin
kubectl config set-context dev@kubernetes --cluster=kubernetes --namespace=dev --user=cka-dev
```

Let's check current context information.
```
kubectl config get-contexts
```
Output:
```
CURRENT   NAME                          CLUSTER      AUTHINFO           NAMESPACE
          cka-dev@kubernetes            kubernetes   cka-dev            dev
*         kubernetes-admin@kubernetes   kubernetes   kubernetes-admin   default
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
*         cka-dev@kubernetes            kubernetes   cka-dev            dev
          kubernetes-admin@kubernetes   kubernetes   kubernetes-admin   default
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

Create role with yaml file.
```
cat > role-cka-dev.yaml << EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: dev
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

kubectl apply -f role-cka-dev.yaml
```

Use `kubectl create rolebinding` command  with option `--dry-run=client` and `-o yaml` to generate yaml template for customizing.
```
kubectl create rolebinding admin --role=admin-dev --user=cka-dev --dry-run=client -o yaml
```

Create rolebinding with yaml file.
```
cat > role-binding-cka-dev.yaml << EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: admin
  namespace: dev
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: admin-dev
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: User
  name: cka-dev
EOF

kubectl apply -f role-binding-cka-dev.yaml
```

Verify authorzation of user `cka-dev` on Namespace `dev`.

Switch to context `cka-dev@kubernetes`.
```
kubectl config use-context cka-dev@kubernetes
```



Get Pods status in Namespace `dev`. Success!
```
kubectl get pod -n dev
```

Get Pods status in Namespace `kube-system`. Failed, because the authorzation is only for Namespace `dev`.
```
kubectl get pod -n kube-system
```

Get Nodes status. Failed, because the role we defined is only for Pod resource.
```
kubectl get node
```

Create a Pod in Namespace `dev`. Failed because we only have `get`,`watch`,`list` for Pod, no `create` authorization.
```
kubectl run nginx --image=nginx -n dev
```





### ClusterRole & ClusterRoleBinding

Switch to context `kubernetes-admin@kubernetes`.
```
kubectl config use-context kubernetes-admin@kubernetes
```

Create a ClusterRole with authorization `get`,`watch`,`list` for `nodes` resource.
```
cat > clusterrole-cka-dev.yaml <<EOF
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


kubectl apply -f clusterrole-cka-dev.yaml
```

Bind ClusterRole `nodes-admin` to user `cka-dev`.

```
cat > clusterrolebinding-cka-dev.yaml << EOF
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


kubectl apply -f clusterrolebinding-cka-dev.yaml
```

Verify Authorization

Switch to context `cka-dev@kubernetes`.
```
kubectl config use-context cka-dev@kubernetes
```

Get node information. Success!
```
kubectl get node
```





## 18.Network Policy

### Replace Flannel by Calico

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

Try to ping pod-netpol-2 (`10.244.112.9`) in Namespace `dev`. It's unreachable. 
```
ping 10.244.112.9
3 packets transmitted, 0 packets received, 100% packet loss
```



#### Create Allow Ingress

Create NetworkPolicy to allow access to pod-netpol-2 in namespace `dev` from all Pods in namespace `pod-netpol`.
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

Try to ping pod-netpol-2 (`10.244.112.9`) in Namespace `dev`. It's still unreachable. 
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

Try to ping pod-netpol-2 (`10.244.112.9`) in Namespace `dev`. It's now reachable. 
```
ping 10.244.112.9
3 packets transmitted, 3 packets received, 0% packet loss
```

Be noted that we can use namespace default label as well.








## 19.Cluster Management

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
evicting pod dev/mysql-nodeselector-6b7d9c875d-m862d
evicting pod quota-object-example/ns-quota-test-84c6c557b9-hkbcl
evicting pod ingress-nginx/ingress-nginx-controller-556fbd6d6f-h455s
evicting pod dev/app-before-backup-66dc9d5cb-6sqcp
evicting pod dev/pod-netpol-2-77478d77ff-96hgd
evicting pod dev/mysql-with-sc-pvc-7c97d875f8-xp42f
evicting pod kube-system/coredns-6d8c4cb4d-zdmm5
evicting pod kube-system/metrics-server-7fd564dc66-rjchn
evicting pod dev/nginx-app-1-695b7b647d-z8chz
pod/app-before-backup-66dc9d5cb-6sqcp evicted
pod/ns-quota-test-84c6c557b9-hkbcl evicted
I0714 17:19:55.890912  869782 request.go:601] Waited for 1.159970307s due to client-side throttling, not priority and fairness, request: GET:https://172.16.18.161:6443/api/v1/namespaces/dev/pods/nginx-app-1-695b7b647d-z8chz
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







## 20.Helm Chart

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

Install MySQL Chart on namespace `dev`：

```
helm install mysql bitnami/mysql -n dev
```
```
NAME: mysql
LAST DEPLOYED: Thu Jul 14 18:18:16 2022
NAMESPACE: dev
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: mysql
CHART VERSION: 9.2.0
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
```
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
mysql   dev    1               2022-07-14 18:18:16.252140606 +0800 CST deployed        mysql-9.2.0     8.0.29
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







## A1.Discussion

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
cka001   NotReady   control-plane,master   23m   v1.23.8   172.16.18.161   <none>        Ubuntu 20.04.4 LTS   5.4.0-113-generic   containerd://1.5.9
cka002   NotReady   <none>                 22m   v1.23.8   172.16.18.160   <none>        Ubuntu 20.04.4 LTS   5.4.0-113-generic   containerd://1.5.9
cka003   NotReady   <none>                 21m   v1.23.8   172.16.18.159   <none>        Ubuntu 20.04.4 LTS   5.4.0-113-generic   containerd://1.5.9
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
cka001   Ready    control-plane,master   4h50m   v1.23.8
cka002   Ready    <none>                 4h49m   v1.23.8
cka003   Ready    <none>                 4h49m   v1.23.8
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
10.244.31.1 via 172.16.18.253 dev eth0 src 172.16.18.161 uid 0 
    cache 

10.244.31.0 via 172.16.18.253 dev eth0 src 172.16.18.161 uid 0 
    cache 

10.244.28.64 via 172.16.18.253 dev eth0 src 172.16.18.161 uid 0 
    cache 
```

The via `172.16.18.161`(it's control-plane) in this example indicates the next-hop for this pod IP, which matches the IP address of the node the pod is scheduled on, as expected.
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








### Scenario: One Node Down

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




**6/30**

1. 创建一个具有两个容器的Pod（镜像可以随意选择）
2. DaemonSet可以设置replicas参数吗？为什么？
3. kubectl查看Pod日志时如何按关键字过滤

https://howtoforge.com/multi-container-pods-in-kubernetes/


**7/3**

1. 如何基于健康检查实操中的nginx-healthcheck模拟livenessProbe存活探针检查失败的场景？
    * 提示1：nginx-healthcheck的livenessProbe探测的是80端口的存活
    * 提示2：容器中可以执行sed
    * 提示3：nginx-healthcheck的默认配置文件位于/etc/nginx/conf.d/下
    * 提示4：Nginx的重新加载配置的命令是nginx -s reload

2. HPA计算CPU/内存扩缩容的百分比是如何计算出来的？分子和分母分别是取什么值



**7/5**

1. 通过kubectl create deploy nginx --image=nginx命令创建的Deployment，忘记加容器端口了，如何修改Deployment加上端口
2. 验证Service的internalTrafficPolicy参数



**7/7**

提示，用官网的YAML示例修改：

1. 创建一个hostPath类型的PV，目录自定义
2. 按照这个PV，创建一个PVC跟这个PV绑定
3. 创建一个Pod，挂载这个PVC，挂载目录自定义
4. 修改这个Pod，添加一个emptyDir类型的Volume挂载，挂载目录自定义


**7/10**

1. kubectl top命令查看Pod和Node的资源利用率如何按照利用率排序？



**7/12**

1. kubectl命令行方式创建ClusterRole，定义对Deployment的create权限
2. kubectl命令行方式创建一个Namespace
3. kubectl命令行方式在Namespace下创建一个ServiceAccount
4. kubectl命令行方式创建RoleBinding把上面创建的ClusterRole和ServiceAccount绑定起来











