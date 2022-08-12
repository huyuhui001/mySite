# Single Node Installation

## Local VM setting

VMWare Setting.

* VMnet1: host-only, subnet: 192.168.150.0/24
* VMnet8: NAT, subnet: 11.0.1.0/24

Create guest machine with VMWare Player.

* 4 GB RAM
* 2 CPUs with 2 Cores
* Ubuntu Server 22.04
* NAT

Kubernetes running on Docker.


## Ubuntu Post Installation

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



## Install Docker

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


## Install Kubernetes

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
