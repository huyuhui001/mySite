# Kubernetes Installation

## Single Node Installation

VMWare Setting.

* VMnet1: host-only, subnet: 192.168.150.0/24
* VMnet8: NAT, subnet: 11.0.1.0/24

Create guest machine with VMWare Player.

* 4 GB RAM
* 2 CPUs with 2 Cores
* Ubuntu Server 22.04
* NAT

Kubernetes running on Docker.


### Ubuntu Post Installation

Create user `vagrant`.
```
sudo adduser vagrant
sudo usermod -aG adm,sudo,syslog,cdrom,dip,plugdev,lxd vagrant
sudo passwd vagrant
```

Set password for `root`.
```
sudo passwd root
```

Update guest's hostname. Here it's `ubusvr`.
```
sudo hostnamectl set-hostname ubusvr
sudo hostnamectl set-hostname ubusvr --pretty
```
Verify if the hostname is set to `ubusvr`.
```
cat /etc/machine-info
```
Verify if the hostname is set to `ubusvr`.
```
cat /etc/hostname
```
Verify if the hostname of `127.0.1.1` is set to `ubusvr`. 
```
cat /etc/hosts
```
```
127.0.0.1 localhost
127.0.1.1 ubusrv

# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```

Set guest with fix ip, e.g, `11.0.1.136`.
```
sudo vi 00-installer-config.yaml
```
```
network:
  ethernets:
    ens33:
      dhcp4: false
      addresses:
      - 11.0.1.136/24
      nameservers:
        addresses:
        - 11.0.1.2
      routes:
      - to: default
        via: 11.0.1.2
  version: 2
```
```
sudo netplan apply
```

Disable swap
```
sudo swapoff -a
sudo ufw disable
sudo ufw status verbose
```
And comment the last line of swap setting in file `/etc/fstab`. Need reboot guest here.
```
/dev/disk/by-uuid/df370d2a-83e5-4895-8c7f-633f2545e3fe / ext4 defaults 0 1
# /swap.img     none    swap    sw      0       0
```

Setup timezone
```
sudo ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
sudo echo 'LANG="en_US.UTF-8"' >> /etc/profile
source /etc/profile
```
Something like this after execute command `ll /etc/localtime`
```
lrwxrwxrwx 1 root root 33 Jul 15 22:00 /etc/localtime -> /usr/share/zoneinfo/Asia/Shanghai
```


Kernel setting

```
cat <<EOF | sudo tee /etc/modules-load.d/containerd.conf
overlay
br_netfilter
EOF
```
```
sudo modprobe overlay
sudo modprobe br_netfilter
```
```
cat <<EOF | sudo tee /etc/sysctl.d/99-kubernetes-cri.conf
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF
```
```
sudo sysctl --system
```



### Install Docker

[Reference](https://docs.docker.com/engine/install/ubuntu/) 

```
sudo apt-get install \
ca-certificates \
curl \
gnupg \
lsb-release
```
```
sudo mkdir -p /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
```
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```
```
sudo systemctl status docker.service

sudo systemctl status containerd.service
```
```
sudo groupadd docker
sudo usermod -aG docker $USER
```

Setup Containerd
```
containerd config default | sudo tee /etc/containerd/config.toml
sudo vi /etc/containerd/config.toml
```
```
sudo systemctl restart containerd
sudo systemctl status containerd
```


### Install Kubernetes

Install kubeadm
```
sudo apt-get update && sudo apt-get install -y apt-transport-https ca-certificates curl
```

```
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg

echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
```
```
sudo apt-get update
sudo apt-get install ebtables
sudo apt-get install libxtables12
sudo apt-get upgrade iptables
```
```
apt policy kubeadm
```
```
sudo apt-get -y install kubelet=1.23.8-00 kubeadm=1.23.8-00 kubectl=1.23.8-00 --allow-downgrades
```


Setup Master Node
```
sudo kubeadm config print init-defaults
```
Dry run
```
sudo kubeadm init --dry-run --pod-network-cidr=10.244.0.0/16 --image-repository=registry.aliyuncs.com/google_containers --kubernetes-version=v1.23.8
```
Run
```
sudo kubeadm init --pod-network-cidr=10.244.0.0/16 --image-repository=registry.aliyuncs.com/google_containers --kubernetes-version=v1.23.8
```
```
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```


Install Flannel. If NetworkPolicy is the case, then install Calico. Refer to the "Install Calico or Flannel" of below section "Installation on Aliyun Ubuntu".
```
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```


Setup on Worker Node

Command usage:
```
kubeadm join <your master node eth0 ip>:6443 --token <token generated by kubeadm init> --discovery-token-ca-cert-hash <hash key generated by kubeadm init>
```
```
kubeadm join 11.0.1.136:6443 --token 6zqh1u.8b4afzc2ov4e7iuj \
  --discovery-token-ca-cert-hash sha256:815fdb9dd9e3ae0af07ffaf6c216964388098b150ef01ee3ae900c261a429d24
```


Setup bash auto completion on all nodes
```
sudo apt install -y bash-completion
source /usr/share/bash-completion/bash_completion
source <(kubectl completion bash)
echo "source <(kubectl completion bash)" >> ~/.bashrc
```

Create alias
```
echo 'alias k=kubectl' >>~/.bashrc
echo 'complete -o default -F __start_kubectl k' >>~/.bashrc
```

Check Cluster Status
```
kubectl cluster-info
kubectl get nodes -owide
kubectl get pod -A
```

### Reset cluster

CAUTION: below steps will destroy current cluster. 

Delete all nodes in the cluster.
```
kubeadm reset
```

Clean up rule of `iptables`.
```
iptables -F && iptables -t nat -F && iptables -t mangle -F && iptables -X
```

Clean up rule of `IPVS` if using `IPVS`.
```
ipvsadm --clear
```


### Install Helm

Helm Client Installation: 
```
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
```
```
chmod 700 get_helm.sh
```
```
./get_helm.sh
```
Output:
```
Downloading https://get.helm.sh/helm-v3.9.0-linux-amd64.tar.gz
Verifying checksum... Done.
Preparing to install helm into /usr/local/bin
helm installed into /usr/local/bin/helm
```





## Multiple Nodes Installation

VMWare Setting.

* VMnet1: host-only, subnet: 192.168.150.0/24
* VMnet8: NAT, subnet: 11.0.1.0/24

Create guest machine with VMWare Player.

* 4 GB RAM
* 2 CPUs with 2 Cores
* Ubuntu Server 22.04
* NAT


Kubernetes running on Containerd.


### Ubuntu Post Installation

Create user `james` on all guests.
```
sudo adduser james
sudo usermod -aG adm,sudo,syslog,cdrom,dip,plugdev,lxd james
sudo passwd james
```

Set password for `root` on all guests.
```
sudo passwd root
```

Update all guests' hostname, `ubu01`,`ubu02`,`ubu03`,`ubu04`. 
```
sudo hostnamectl set-hostname ubu01
sudo hostnamectl set-hostname ubu01 --pretty
```
Verify if the hostname is set to expected name, e.g., `ubu01`.
```
cat /etc/machine-info
```
Verify if the hostname is set to expected name, e.g., `ubu01`.
```
cat /etc/hostname
```
Verify if the hostname of `127.0.1.1` is set to expected name, e.g., `ubu01`. And add all nodes  into the file `/etc/hosts`.
```
cat /etc/hosts
```
```
127.0.0.1 localhost
127.0.1.1 ubu01

11.0.1.131 ubu01
11.0.1.132 ubu02
11.0.1.133 ubu03
11.0.1.134 ubu04

# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```

Set all guests with fixed IP, e.g, `11.0.1.131`.
```
sudo vi 00-installer-config.yaml
```
```
network:
  ethernets:
    ens33:
      dhcp4: false
      addresses:
      - 11.0.1.131/24
      nameservers:
        addresses:
        - 11.0.1.2
      routes:
      - to: default
        via: 11.0.1.2
  version: 2
```
```
sudo netplan apply
```

Disable swap and firewall on all nodes.
```
sudo swapoff -a
sudo ufw disable
sudo ufw status verbose
```
And comment the last line of swap setting in file `/etc/fstab`. Need *reboot* guest here.
```
/dev/disk/by-uuid/df370d2a-83e5-4895-8c7f-633f2545e3fe / ext4 defaults 0 1
# /swap.img     none    swap    sw      0       0
```

Setup timezone on all nodes
```
sudo ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
sudo echo 'LANG="en_US.UTF-8"' >> /etc/profile
source /etc/profile
```
Something like this after execute command `ll /etc/localtime`
```
lrwxrwxrwx 1 root root 33 Jul 15 22:00 /etc/localtime -> /usr/share/zoneinfo/Asia/Shanghai
```


Kernel setting on all nodes.
```
cat <<EOF | sudo tee /etc/modules-load.d/containerd.conf
overlay
br_netfilter
EOF
```
```
sudo modprobe overlay
sudo modprobe br_netfilter
```
```
cat <<EOF | sudo tee /etc/sysctl.d/99-kubernetes-cri.conf
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF
```
```
sudo sysctl --system
```



### Install Containerd

Install Containerd sevice on all nodes.

Backup source file.
```
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
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

Install nerdctl sevice on all nodes.

The goal of [`nerdctl`](https://github.com/containerd/nerdctl) is to facilitate experimenting the cutting-edge features of containerd that are not present in Docker.

```
wget https://github.com/containerd/nerdctl/releases/download/v0.21.0/nerdctl-0.21.0-linux-amd64.tar.gz

tar -zxvf nerdctl-0.21.0-linux-amd64.tar.gz

cp nerdctl /usr/bin/
```

Verify nerdctl.
```
# nerdctl --help
```

To list local Kubernetes containers.
```
# nerdctl -n k8s.io ps
```



### Install Kubernetes

Install Kubernetes on all nodes.

Install dependencied packages.
```
sudo apt-get update && sudo apt-get install -y apt-transport-https ca-certificates curl
```

Install gpg certificate.
```
# For Ubuntu 20.04 release
curl https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg | apt-key add -

# For Ubuntu 22.04 release
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg
```
Add Kubernetes repo. 
```
# For Ubuntu 20.04 release
cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main
EOF

# For Ubuntu 22.04 release
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
```

Update and install dependencied packages.
```
sudo apt-get update
sudo apt-get install ebtables
sudo apt-get install libxtables12
sudo apt-get upgrade iptables
```

Check available versions of kubeadm.
```
apt policy kubeadm
```

Install `1.23.8-00` version.
```
sudo apt-get -y install kubelet=1.23.8-00 kubeadm=1.23.8-00 kubectl=1.23.8-00 --allow-downgrades
```

Set `kubectl` [auto-completion](https://github.com/scop/bash-completion) following the [guideline](https://kubernetes.io/docs/tasks/tools/included/optional-kubectl-configs-bash-linux/).
```
sudo apt install -y bash-completion
source /usr/share/bash-completion/bash_completion
source <(kubectl completion bash)
echo "source <(kubectl completion bash)" >> ~/.bashrc
```

If we set an alias for kubectl, we can extend shell completion to work with that alias:
```
echo 'alias k=kubectl' >>~/.bashrc
echo 'complete -o default -F __start_kubectl k' >>~/.bashrc
```




### Setup Master Node

Check kubeadm default parameters for initialization.
```
sudo kubeadm config print init-defaults
```

Dry run
```
sudo kubeadm init --dry-run --pod-network-cidr=10.244.0.0/16 --image-repository=registry.aliyuncs.com/google_containers --kubernetes-version=v1.23.8
```

Initialize master node. Save the output, which will be used later on work nodes.
```
sudo kubeadm init --pod-network-cidr=10.244.0.0/16 --image-repository=registry.aliyuncs.com/google_containers --kubernetes-version=v1.23.8
```

Set `kubeconfig` file for current user.
```
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```


### Install Flannel

If NetworkPolicy is the case, then install Calico. Refer to the "Install Calico or Flannel" of below section "Installation on Aliyun Ubuntu".

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
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```
Output:
```
Warning: policy/v1beta1 PodSecurityPolicy is deprecated in v1.21+, unavailable in v1.25+
podsecuritypolicy.policy/psp.flannel.unprivileged created
clusterrole.rbac.authorization.k8s.io/flannel created
clusterrolebinding.rbac.authorization.k8s.io/flannel created
serviceaccount/flannel created
configmap/kube-flannel-cfg created
daemonset.apps/kube-flannel-ds created
```

### Setup Work Nodes

Command usage:
```
kubeadm join <your master node eth0 ip>:6443 --token <token generated by kubeadm init> --discovery-token-ca-cert-hash <hash key generated by kubeadm init>
```
Use `kubeadm token` to generate the join token and hash value.
```
kubeadm token create --print-join-command
```


### Check Cluster Status
```
kubectl cluster-info
kubectl get nodes -owide
kubectl get pod -A
```


### Reset cluster

CAUTION: below steps will destroy current cluster. 

Delete all nodes in the cluster.
```
kubeadm reset
```

Clean up rule of `iptables`.
```
iptables -F && iptables -t nat -F && iptables -t mangle -F && iptables -X
```

Clean up rule of `IPVS` if using `IPVS`.
```
ipvsadm --clear
```



### Install Helm

Helm is the Kubernetes package manager. It doesn't come with Kubernetes. 

Three concepts of helm:

* A *Chart* is a Helm package. 
    * It contains all of the resource definitions necessary to run an application, tool, or service inside of a Kubernetes cluster. 
    * Think of it like the Kubernetes equivalent of a Homebrew formula, an Apt dpkg, or a Yum RPM file.
* A *Repository* is the place where charts can be collected and shared. 
    * It's like Perl's CPAN archive or the Fedora Package Database, but for Kubernetes packages.
* A *Release* is an instance of a chart running in a Kubernetes cluster. 
    * One chart can often be installed many times into the same cluster. And each time it is installed, a new release is created. 
    * Consider a MySQL chart. If you want two databases running in your cluster, you can install that chart twice. Each one will have its own release, which will in turn have its own release name.


Reference:

* [installation guide](https://helm.sh/docs/intro/install/)
* [binary release](https://github.com/helm/helm/releases)
* [source code](https://github.com/helm/helm).


Helm Client Installation: 
```
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
```
```
chmod 700 get_helm.sh
```
```
./get_helm.sh
```
Output:
```
Downloading https://get.helm.sh/helm-v3.9.1-linux-amd64.tar.gz
Verifying checksum... Done.
Preparing to install helm into /usr/local/bin
helm installed into /usr/local/bin/helm
```

Note:
[`helm init`](https://helm.sh/docs/helm/helm_init/) does not exist in Helm 3, following the removal of Tiller. You no longer need to install Tiller in your cluster in order to use Helm.

`helm search` can be used to search two different types of source:

* `helm search hub` searches the [Artifact Hub](https://artifacthub.io/), which lists helm charts from dozens of different repositories.
* `helm search repo` searches the repositories that you have added to your local helm client (with helm repo add). This search is done over local data, and no public network connection is needed.










## Installation on Aliyun openSUSE

Before, Kubic from openSUSE is focusing on kubeadm as open source project. CaaSP is comercial product for Kubenetes, compared with Kubic. 

After SUSE aand Rancher mergered, their fucus on Kubernetes turn to [K3s](https://rancher.com/docs/k3s/latest/en/)/[RKE](https://rancher.com/docs/rke/latest/en/)/[RKE2](https://docs.rke2.io/) and [MicroOS](https://lists.opensuse.org/archives/list/kubic@lists.opensuse.org/thread/23ODJTP4PLGC3HWFQNA2MD4ETFSNW4KV/), not Kubic nor CaaSP. 

Hence, for learning purpose, it's recommended to use K3s, for comercial perspective, may consider RKE or RKE2. 

Below demo only shows deployment of native Kubernetes on openSUSE 15sp3, which may just a refernce with native deployment on Ubuntu or RedHat. 


### Preparation

Register Aliyun account via [Alibaba Cloud home console](https://home.console.aliyun.com/home/dashboard/ProductAndService).

Request three Elastic Computer Service(ECS) instances with below sizing:

* System: 2vCPU+4GiB
* OS: openSUSE 15sp3 x86_64
* Instance Type: ecs.sn1.medium 
* Instance Name: leap1, leap2, leap3
* Network: both public IPs and private IPs
* Maximum Bandwidth: 100Mbps (Peak Value)
* Cloud disk: 40GiB
* Billing Method: Preemptible instance (spot price)

Generate SSH key pairs with name `cka-key-pair` in local directory `/opt`.

Change access control to `400` per security required by command `sudo chmod 400 cka-key-pair.pem`.

Access remote cka servers via command `ssh -i cka-key-pair.pem root@<your public ip address>`


### Initialize VMs


#### Configure /etc/hosts file
Add private IPs in the `/etc/hosts` file in all VMs.

#### Disable firewall

SUSE introduces firewalld as the new default software firewall, replacing SuSEfirewall2. SuSEfirewall2 has not been removed and is still part of the main repository, though not installed by default. 

Firewalld and SuSEfirewall2 packages was not installed during initialization.


### Turn off swap

Turn off swap by command `swapoff -a` in all VMs.

### Set timezone and locale

Set timezone and local for all VMs. For ECS with SLES 15sp3 version created by Aliyun, this step is not needed.
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

Load `overlay` and `br_netfilter` modules. Check the active module loaded list. The removed module is not on the module loaded list.
```
# lsmod | grep overlay
# lsmod | grep br_netfilter

# sudo modprobe overlay
# sudo modprobe br_netfilter
```

Set `net/bridge/bridge-nf-call-iptables=1` to ensure simple configurations (like Docker with a bridge) work correctly with the iptables proxy. [Why `net/bridge/bridge-nf-call-iptables=1` need to be enable by Kubernetes](https://cloud.tencent.com/developer/article/1828060).

IP forwarding is also known as routing. When it comes to Linux, it may also be called Kernel IP forwarding because it uses the kernel variable `net.ipv4.ip_forward` to enable or disable the IP forwarding feature. The default preset value is `ip_forward=0`. Hence, the Linux IP forwarding feature is disabled by default.
```
# cat <<EOF >> /etc/sysctl.conf
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
net.ipv4.conf.all.forwarding        = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF
```

The `sysctl` command reads the information from the `/proc/sys` directory. `/proc/sys` is a virtual directory that contains file objects that can be used to view and set the current kernel parameters.

By commadn `sysctl -w net.ipv4.ip_forward=1`, the change takes effect immediately, but it is not persistent. After a system reboot, the default value is loaded. Write the settings to `/etc/sysctl.conf` is to set a parameter permanently, you’ll need to  or another configuration file in the /etc/sysctl.d directory:
```
# sudo sysctl --system
```


### Install Containerd

Install docker in all VMs.
```
# zypper install docker
```

Start Containerd service
```
# systemctl enable containerd.service 
# systemctl start containerd.service 
# systemctl status containerd.service 
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

Install conntrackd, which is required by kubelet.
```
# sudo zypper in conntrack-tools
```

Add repository for installing Kubernetes packages.
```
# cat <<EOF > /etc/zypp/repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
enabled=1
autorefresh=1
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/
type=rpm-md
gpgcheck=1
repo_gpgcheck=1
pkg_gpgcheck=1
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
exclude=kubelet kubeadm kubectl
EOF
```

Refresh the repo
```
# sudo zypper ref kubernetes
```

List curren tavailable packages in repo Kubernetes.
```
# sudo zypper packages --repo kubernetes
```

Install `1.23.8-00` version of kubeadm and will upgrade to `1.24.2` later. Ignoring conntrack breakout, just pick.
```
# sudo zypper in kubelet=1.23.8-00 kubeadm=1.23.8-00 kubectl=1.23.8-00
```

Enable kubelet service on boot:
```
# sudo systemctl enable kubelet
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
# sudo zypper in bash-completion
# source /usr/share/bash-completion/bash_completion
# source <(kubectl completion bash)
# echo "source <(kubectl completion bash)" >> ~/.bashrc
```


### Setup Work Nodes

Perform on all VMs playing work nodes.
```
# kubeadm join <your master node ip>:6443 --token <token generated by kubeadm init> --discovery-token-ca-cert-hash <hash key generated by kubeadm init>
```


Verify status on master node.
```
root@cka001:~# kubectl get node
NAME    STATUS   ROLES                  AGE     VERSION
leap1   Ready    control-plane,master   16m     v1.23.8
leap2   Ready    <none>                 9m39s   v1.23.8
leap3   Ready    <none>                 9m51s   v1.23.8
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


Two references I used.

* [How to install kubernetes in Suse Linux enterprize server 15 virtual machines](https://stackoverflow.com/questions/62795930/how-to-install-kubernetes-in-suse-linux-enterprize-server-15-virtual-machines)
* [How to Install Kubernetes Cluster in openSUSE Leap 15.1](https://nugi.abdiansyah.com/how-to-kubernetes-in-opensuse-leap-15-1-hardest-way/)






## Installation on Aliyun Ubuntu

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


Open a local terminal, log onto remote ECS `cka001` using the key pair (e.g., `aliyun-root`) from Aliyun cloud.
```
ssh -i aliyun-root root@cka001
```

Create a common user (e.g., `james`), and set primary group as `sudo` and other group as `root`.
```
adduser james
usermod -g sudo james
usermod -a -G root james
```

Back to the local terminal, generate key for common user `james` by below command.
```
# Windows
ssh-keygen.exe

# Linux
ssh-keygen
```

Two files will be created, e.g., `aliyun-james` and `aliyun-james.pub`

Upload the public key `aliyun-james.pub` to remote `cka001` using `sftp` command.
```
sftp -i aliyun-root root@cka001
put aliyun-james.pub
```

Log onto remote ECS `cka001` using `root` account again. 
Move the key `aliyun-james.pub` to `/home/james/.ssh/`. 
Rename file `aliyun-james.pub` to `authorized_keys`.
Change ower of file `authorized_keys` to `james`.
Change default group of file `authorized_keys` to `sudo`.
```
mkdir /home/james/.ssh/
mv aliyun-james.pub /home/james/.ssh/authorized_keys
chown james.sudo /home/james/.ssh/authorized_keys
chmod 600 /home/james/.ssh/authorized_keys
```

Check file `/etc/ssh/sshd_config`, make sure password authentication is disabled `PasswordAuthentication no`
```
cat /etc/ssh/sshd_config
```

Back to the local terminal, use `james` to log onto remote `cka001`.
```
ssh -i aliyun-james james@cka001
```

Upload the public key `aliyun-james.pub` to remote `cka002` and `cka003` using `sftp` command and do the same set up on `cka002` and `cka003` in order to enable user `james` to log onto `cka002` and `cka003`.

Till now, user `james` can log onto `cka001`, `cka002` and `cka003` using key `aliyun-james`. 

All demo below will be done by user `james`.




### Initialize VMs


#### Configure /etc/hosts file
Add private IPs in the `/etc/hosts` file in all VMs.
```
vi /etc/hosts
```

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

Turn off swap in all VMs.
```
sudo swapoff -a
```

### Set timezone and locale

Set timezone and local for all VMs. This step was already done during Aliyun ECS installation.
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
lrwxrwxrwx 1 root root 33 Jul  5 14:51 /etc/localtime -> /usr/share/zoneinfo/Asia/Shanghai
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
sudo vi /etc/containerd/config.toml
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
sudo cp nerdctl /usr/bin/
sudo cp containerd-rootless* /usr/bin/
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

Install gpg certificate. 
```
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg
```

Add Kubernetes repo. Just choose one of below command and execute.
```
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://mirrors.aliyun.com/kubernetes/apt/ \
  kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
```

Update and install dependencied packages.
```
sudo apt-get update
sudo apt-get install ebtables
sudo apt-get install libxtables12
sudo apt-get upgrade iptables
```

Check available versions of kubeadm.
```
apt policy kubeadm
```

Install `1.24.0-00` version of kubeadm and will upgrade to `1.24.2` later.
```
sudo apt-get -y install kubelet=1.24.0-00 kubeadm=1.24.0-00 kubectl=1.24.0-00 --allow-downgrades
```


### Setup Master Node

### kubeadm init

Set up Control Plane on VM playing master node.

Check kubeadm default parameters for initialization.
```
kubeadm config print init-defaults
```
Reuslt:
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
  criSocket: unix:///var/run/containerd/containerd.sock
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
kubernetesVersion: 1.24.0
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
sudo kubeadm init \
  --dry-run \
  --pod-network-cidr=10.244.0.0/16 \
  --service-cidr 11.244.0.0/16 \
  --image-repository=registry.aliyuncs.com/google_containers \
  --kubernetes-version=v1.24.0

sudo kubeadm init \
  --pod-network-cidr=10.244.0.0/16 \
  --service-cidr 11.244.0.0/16 \
  --image-repository=registry.aliyuncs.com/google_containers \
  --kubernetes-version=v1.24.0
```


### kubeconfig file

Set `kubeconfig` file for current user (here it's `james`).
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
kubectl config get-contexts
```
Result
```
CURRENT   NAME                          CLUSTER      AUTHINFO           NAMESPACE
*         kubernetes-admin@kubernetes   kubernetes   kubernetes-admin   
```



### Setup Work Nodes

Perform on all VMs playing work nodes.
```
# kubeadm join <your master node eth0 ip>:6443 --token <token generated by kubeadm init> --discovery-token-ca-cert-hash <hash key generated by kubeadm init>
```

Use `kubeadm token` to generate the join token and hash value. 
```
kubeadm token create --print-join-command
```

Execute the command generated above on each node that we want to join the cluster as Worker node.


Verify status on master node. All nodes' status is `NotReady`. Leave it at the moment and continue to install network plugin.
```
kubectl get node -o wide
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
Result
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
Result
```
calico-kube-controllers-555bc4b957-l8bn2   0/1     Pending    0          28s
calico-node-255pc                          0/1     Init:1/3   0          29s
calico-node-7tmnb                          0/1     Init:1/3   0          29s
calico-node-w8nvl                          0/1     Init:1/3   0          29s
```

Verify network status.
```
sudo nerdctl network ls
```
Result
```
NETWORK ID    NAME               FILE
              k8s-pod-network    /etc/cni/net.d/10-calico.conflist
0             bridge             /etc/cni/net.d/nerdctl-bridge.conflist
              host               
              none 
```



### Check Cluster Status

Perform `kubectl cluster-info` command on master node we will get below information.

* Kubernetes control plane is running at `https://<mster node ip>:6443`
* CoreDNS is running at `https://<mster node ip>:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy`

```
kubectl cluster-info
```

Get nodes status.
```
kubectl get nodes -owide
```

All nodes are up with normal status.

* OS Image: Ubuntu 20.04.4 LTS
* Kernel Version: 5.4.0-122-generic
* Container Runtime: containerd://1.5.9

```
NAME     STATUS   ROLES           AGE     VERSION
cka001   Ready    control-plane   13m     v1.24.0
cka002   Ready    <none>          8m35s   v1.24.0
cka003   Ready    <none>          8m26s   v1.24.0
```

Get pods status
```
kubectl get pod -A
```
Result:
```
NAMESPACE     NAME                                       READY   STATUS    RESTARTS   AGE
kube-system   calico-kube-controllers-555bc4b957-l8bn2   1/1     Running   0          7m18s
kube-system   calico-node-255pc                          1/1     Running   0          7m19s
kube-system   calico-node-7tmnb                          1/1     Running   0          7m19s
kube-system   calico-node-w8nvl                          1/1     Running   0          7m19s
kube-system   coredns-74586cf9b6-4jwmk                   1/1     Running   0          15m
kube-system   coredns-74586cf9b6-c5mll                   1/1     Running   0          15m
kube-system   etcd-cka001                                1/1     Running   0          15m
kube-system   kube-apiserver-cka001                      1/1     Running   0          15m
kube-system   kube-controller-manager-cka001             1/1     Running   0          15m
kube-system   kube-proxy-dmj2t                           1/1     Running   0          15m
kube-system   kube-proxy-n77zw                           1/1     Running   0          11m
kube-system   kube-proxy-qs6rf                           1/1     Running   0          11m
kube-system   kube-scheduler-cka001                      1/1     Running   0          15m
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

Check if the kubeconfig file is update to udpate and exists in right place.

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






### Post Installation

#### Bash Autocomplete

On each node.

Set `kubectl` [auto-completion](https://github.com/scop/bash-completion) following the [guideline](https://kubernetes.io/docs/tasks/tools/included/optional-kubectl-configs-bash-linux/).
```
apt install -y bash-completion
source /usr/share/bash-completion/bash_completion
source <(kubectl completion bash)
echo "source <(kubectl completion bash)" >> ~/.bashrc
```

#### Alias

If we set an alias for kubectl, we can extend shell completion to work with that alias:
```
echo 'alias k=kubectl' >>~/.bashrc
echo 'complete -o default -F __start_kubectl k' >>~/.bashrc
```

#### Update Default Context

Get current context.
```
kubectl config get-contexts 
```

In below result, we know:

* Contenxt name is `kubernetes-admin@kubernetes`.
* Cluster name is `kubernetes`.
* User is `kubernetes-admin`.
* No namespace explicitly defined.

```
CURRENT   NAME                          CLUSTER      AUTHINFO           NAMESPACE
*         kubernetes-admin@kubernetes   kubernetes   kubernetes-admin 
```

To set a context with new update, e.g, update default namespace, etc.. 
```
# Usage:
kubectl config set-context <context name> --cluster=<cluster name> --namespace=<namespace name> --user=<user name> 

# Set default namespace
kubectl config set-context kubernetes-admin@kubernetes --cluster=kubernetes --namespace=default --user=kubernetes-admin
```

To switch to a new context.
```
kubectl config use-context <context name>
```
```
kubectl config use-context kubernetes-admin@kubernetes
```

Reference of [kubectl](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/) and [commandline](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands). 













