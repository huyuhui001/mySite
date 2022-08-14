# Multiple Nodes Installation

## Local VM setting

VMWare Setting.

* VMnet1: host-only, subnet: 192.168.150.0/24
* VMnet8: NAT, subnet: 11.0.1.0/24

Create guest machine with VMWare Player.

* 4 GB RAM
* 1 CPUs with 2 Cores
* Ubuntu Server 22.04
* NAT

!!! info
    Kubernetes running on Containerd.


## Ubuntu Post Installation

!!! info
    Log onto each VM with the account created during Ubuntu installation, and perform below tasks on every VM. 


Create user `vagrant` on all guests.
```console
sudo adduser vagrant
sudo usermod -aG adm,sudo,syslog,cdrom,dip,plugdev,lxd vagrant
sudo passwd vagrant
```

Set password for `root` on all guests.
```console
sudo passwd root
```

Enable root ssh logon.
```console
sudo vi /etc/ssh/sshd_config
```

Update parameter `PermitRootLogin` from `prohibit-password` to `yes`.
```
PermitRootLogin yes
#PermitRootLogin prohibit-password
```

Restart the sshd service.
```console
sudo systemctl restart sshd
```

Change host name, e.g., `ubu1`.
```console
sudo hostnamectl set-hostname ubu1
sudo hostnamectl set-hostname ubu1 --pretty
```

Verify if the hostname is set to expected name, e.g., `ubu1`.
```console
cat /etc/machine-info
```

Verify if the hostname is set to expected name, e.g., `ubu1`.
```console
cat /etc/hostname
```

Verify if the hostname of `127.0.1.1` is set to expected name, e.g., `ubu1`. And add all nodes into the file `/etc/hosts`.
```console
sudo vi /etc/hosts
```
Related setting looks like below.
```
127.0.1.1 ubu1
11.0.1.129 ubu1
11.0.1.130 ubu2
11.0.1.131 ubu3
11.0.1.132 ubu4
```

Create file `/etc/netplan/00-installer-config.yaml`.
```console
sudo vi /etc/netplan/00-installer-config.yaml
```

Update it with information below to set VM with fixed IP with actual IP address, e.g, `11.0.1.129`.
```
network:
  ethernets:
    ens33:
      dhcp4: false
      addresses:
      - 11.0.1.129/24
      nameservers:
        addresses:
        - 11.0.1.2
      routes:
      - to: default
        via: 11.0.1.2
  version: 2
```

Effect above change.
```console
sudo netplan apply
```

!!! Attention
    The current ssh connection will be broken due to network setting change.


Disable swap and firewall on all nodes.
```console
sudo swapoff -a
sudo ufw disable
sudo ufw status verbose
```
And comment the last line of swap setting in file `/etc/fstab`. Need *reboot* guest here.
```console
sudo vi /etc/fstab
```
Result likes below.
```
/dev/disk/by-uuid/df370d2a-83e5-4895-8c7f-633f2545e3fe / ext4 defaults 0 1
# /swap.img     none    swap    sw      0       0
```

Setup timezone on all nodes
```console
sudo ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

sudo cp /etc/profile /etc/profile.bak
echo 'LANG="en_US.UTF-8"' | sudo tee -a /etc/profile

source /etc/profile
```

Something like this after execute command `ll /etc/localtime`
```
lrwxrwxrwx 1 root root 33 Jul 15 22:00 /etc/localtime -> /usr/share/zoneinfo/Asia/Shanghai
```

Kernel setting.
```
cat <<EOF | sudo tee /etc/modules-load.d/containerd.conf
overlay
br_netfilter
EOF
```

Effect changes above.
```
sudo modprobe overlay
sudo modprobe br_netfilter
```

Network setting.
```
cat <<EOF | sudo tee /etc/sysctl.d/99-kubernetes-cri.conf
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF
```

Effect changes above.
```
sudo sysctl --system
```

!!! Attention
    Reboot the VM.
    All tasks below will use account `vagrant`.



## Install Containerd

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

  
## Install nerdctl

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



## Install Kubernetes

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




## Setup Master Node

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


## Install Flannel

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

## Setup Work Nodes

Command usage:
```
kubeadm join <your master node eth0 ip>:6443 --token <token generated by kubeadm init> --discovery-token-ca-cert-hash <hash key generated by kubeadm init>
```
Use `kubeadm token` to generate the join token and hash value.
```
kubeadm token create --print-join-command
```


## Check Cluster Status
```
kubectl cluster-info
kubectl get nodes -owide
kubectl get pod -A
```


## Reset cluster

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



## Install Helm

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


