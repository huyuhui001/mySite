# CKA自学笔记1:单节点虚拟机安装Kubernetes

## 摘要

在本地Windows环境中，通过VMWare安装Ubuntu虚拟机。在Ubuntu虚拟机中安装基于Docker的Kubernetes系统。在该虚拟机中同时配置主节点Master和工作节点Worker。

## 本地虚拟机设置

VMWare虚拟机设置。

* VMnet1: host-only模式, 网络subnet: 192.168.150.0/24
* VMnet8: NAT模式, 网络subnet: 11.0.1.0/24

通过VMWare创建客户机。

* 内存：4 GB
* CPU：2 CPUs with 2 Cores
* 操作系统：Ubuntu Server 22.04
* 网络：NAT

Kubernetes运行在Docker上。

## Ubuntu预配置

创建用户 `vagrant`。

```bash
sudo adduser vagrant
sudo usermod -aG adm,sudo,syslog,cdrom,dip,plugdev,lxd vagrant
sudo passwd vagrant
```

设置用户 `root`的密码。

```bash
sudo passwd root
```

更新客户机的主机名，这里是 `ubusvr`。

```bash
sudo hostnamectl set-hostname ubusvr
sudo hostnamectl set-hostname ubusvr --pretty
```

验证主机名是否已成功更新为 `ubusvr`。

```bash
cat /etc/machine-info
cat /etc/hostname
```

验证主机IP地址`127.0.1.1` 已经配置给当前虚拟机`ubusvr`。

```bash
cat /etc/hosts
```

```console
127.0.0.1 localhost
127.0.1.1 ubusrv

# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```

设置客户机为固定IP地址，这里是`11.0.1.136`。

```bash
sudo vi 00-installer-config.yaml
```

```yaml
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

```bash
sudo netplan apply
```

禁用交换分区swap。

```bash
sudo swapoff -a
sudo ufw disable
sudo ufw status verbose
```

注释掉文件`/etc/fstab`的最后一行，即禁用交换分区。需要重启客户机使之生效。

```console
/dev/disk/by-uuid/df370d2a-83e5-4895-8c7f-633f2545e3fe / ext4 defaults 0 1
# /swap.img     none    swap    sw      0       0
```

设置客户机时区。

```bash
sudo ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
sudo echo 'LANG="en_US.UTF-8"' >> /etc/profile
source /etc/profile
```

执行命令 `ll /etc/localtime`验证时区是否已正确设置并生效。

```console
lrwxrwxrwx 1 root root 33 Jul 15 22:00 /etc/localtime -> /usr/share/zoneinfo/Asia/Shanghai
```

客户机内核设置。

```bash
cat <<EOF | sudo tee /etc/modules-load.d/containerd.conf
overlay
br_netfilter
EOF
```

```bash
sudo modprobe overlay
sudo modprobe br_netfilter
```

```bash
cat <<EOF | sudo tee /etc/sysctl.d/99-kubernetes-cri.conf
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF
```

```bash
sudo sysctl --system
```

## 安装Docker

[参考帮助](https://docs.docker.com/engine/install/ubuntu/)

```bash
sudo apt-get install \
ca-certificates \
curl \
gnupg \
lsb-release
```

```bash
sudo mkdir -p /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

```bash
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

```bash
sudo systemctl status docker.service

sudo systemctl status containerd.service
```

```bash
sudo groupadd docker
sudo usermod -aG docker $USER
```

设置Containerd。

```bash
containerd config default | sudo tee /etc/containerd/config.toml
sudo vi /etc/containerd/config.toml
```

```bash
sudo systemctl restart containerd
sudo systemctl status containerd
```

## 安装Kubernetes

安装kubeadm

```bash
sudo apt-get update && sudo apt-get install -y apt-transport-https ca-certificates curl
```

```bash
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg

echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
```

```bash
sudo apt-get update
sudo apt-get install ebtables
sudo apt-get install libxtables12
sudo apt-get upgrade iptables
```

```bash
apt policy kubeadm
```

```bash
sudo apt-get -y install kubelet=1.23.8-00 kubeadm=1.23.8-00 kubectl=1.23.8-00 --allow-downgrades
```

配置主节点（Master）。

```bash
sudo kubeadm config print init-defaults
```

安装预演Dry run。

```bash
sudo kubeadm init --dry-run --pod-network-cidr=10.244.0.0/16 --image-repository=registry.aliyuncs.com/google_containers --kubernetes-version=v1.23.8
```

安装。

```bash
sudo kubeadm init --pod-network-cidr=10.244.0.0/16 --image-repository=registry.aliyuncs.com/google_containers --kubernetes-version=v1.23.8
```

```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

安装Flannel。如果需要考虑网络策略，则安装Calico。参照[阿里云ECS](./installation/aliyun-ubuntu.md)中Install Calico or Flannel部分。

```bash
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

配置工作节点（Worker Node）。

```bash
kubeadm join <your master node eth0 ip>:6443 --token <token generated by kubeadm init> --discovery-token-ca-cert-hash <hash key generated by kubeadm init>
```

```bash
kubeadm join 11.0.1.136:6443 --token 6zqh1u.8b4afzc2ov4e7iuj \
  --discovery-token-ca-cert-hash sha256:815fdb9dd9e3ae0af07ffaf6c216964388098b150ef01ee3ae900c261a429d24
```

在所有节点上配置bash自动补全功能。

```bash
sudo apt install -y bash-completion
source /usr/share/bash-completion/bash_completion
source <(kubectl completion bash)
echo "source <(kubectl completion bash)" >> ~/.bashrc
```

在所有节点上定义别名（alias）。

```bash
echo 'alias k=kubectl' >>~/.bashrc
echo 'complete -o default -F __start_kubectl k' >>~/.bashrc
```

查看当前集群状态。

```bash
kubectl cluster-info
kubectl get nodes -owide
kubectl get pod -A
```

## 安装Helm

安装Helm客户端。

```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
```

```bash
chmod 700 get_helm.sh
```

```bash
./get_helm.sh
```

输出结果：

```console
Downloading https://get.helm.sh/helm-v3.9.0-linux-amd64.tar.gz
Verifying checksum... Done.
Preparing to install helm into /usr/local/bin
helm installed into /usr/local/bin/helm
```

## 重置集群

注意：下面的操作会重置当前集群（删除集群）。

删除集群中所有节点。

```bash
kubeadm reset
```

清除`iptables`中已定义的规则。

```bash
iptables -F && iptables -t nat -F && iptables -t mangle -F && iptables -X
```

清除`IPVS`中定义的规则（如果使用`IPVS`）。

```bash
ipvsadm --clear
```
