# Kubernetes Foundation

## **1.Preparation and Setup**

### System environment for the demo

Linux: openSUSE 15.3
```
james@lizard:/opt> cat /etc/os-release 
NAME="openSUSE Leap"
VERSION="15.3"
ID="opensuse-leap"
ID_LIKE="suse opensuse"
VERSION_ID="15.3"
PRETTY_NAME="openSUSE Leap 15.3"
ANSI_COLOR="0;32"
CPE_NAME="cpe:/o:opensuse:leap:15.3"
BUG_REPORT_URL="https://bugs.opensuse.org"
HOME_URL="https://www.opensuse.org/"
```



## **2. Docker Fundamentals**

### Linux Primitives used by Containers

chroot(using pivot_root)

- Changes the root directory for a process to any given directory

namespaces

- Different processes see different environments even though they are on the same host/OS
    - mnt (mount points)
    - pid (process tree)
    - net (network interfaces and connectivity)
    - ipc (interprocess communication framework)
    - uts (unix timesharing - domain name, hostname, etc.)
    - uid (user IDs and mappings)

cgroups(control groups)

- manage/limit resource allocation to individual processes
- Prioritization of processes

Apparmor and SELinux profiles
- Security profiles to govern access to resources

Kernel capabilities

- without capabilities: root can do everything, everybody else may do nothing
- 38 granular facilities to control privileges

seccomp policies

- Limitation of allowed kernel syscalls
- Unallowed syscalls lead to process termination

Netlink
- A Linux kernel interface used for inter-process communication (IPC) between both the kernel and userspace processes, and between different userspace processes. 

Netfilter

- A framework provided by the Linux kernel that allows various networking-related operations
- Packet filtering, network address translation, and port translation(iptables/nftables)
- used to direct network packages to individual containers

More inforamtion could refer to [LXC/LXD](https://linuxcontainers.org/)



### Installing Docker

Install Docker engine by referring the [guide](https://docs.docker.com/engine/), and Docker Desktop by referring the [guide](https://docs.docker.com/desktop/).

Install engine via openSUSE repository automatically.
```
james@lizard:/opt> sudo zypper in docker
```

The docker group is automatically created at package installation time. 
The user can communicate with the local Docker daemon upon its next login. 
The Docker daemon listens on a local socket which is accessible only by the root user and by the members of the docker group. 

Add current user to `docker` group.
```
james@lizard:/opt> sudo usermod -aG docker $USER
```

Enable and start Docker engine.
```
james@lizard:/opt> sudo systemctl enable docker.service 
Created symlink /etc/systemd/system/multi-user.target.wants/docker.service → /usr/lib/systemd/system/docker.service.

james@lizard:/opt> sudo systemctl start docker.service 

james@lizard:/opt> sudo systemctl status docker.service 
● docker.service - Docker Application Container Engine
     Loaded: loaded (/usr/lib/systemd/system/docker.service; enabled; vendor preset: disabled)
     Active: active (running) since Sat 2022-05-28 14:36:45 CST; 6s ago
       Docs: http://docs.docker.com
   Main PID: 31565 (dockerd)
      Tasks: 20
     CGroup: /system.slice/docker.service
             ├─31565 /usr/bin/dockerd --add-runtime oci=/usr/sbin/docker-runc
             └─31574 containerd --config /var/run/docker/containerd/containerd.toml --log-level warn

May 28 14:36:44 lizard systemd[1]: Starting Docker Application Container Engine...
May 28 14:36:44 lizard dockerd[31565]: time="2022-05-28T14:36:44+08:00" level=info msg="SUSE:secrets :: enabled"
May 28 14:36:44 lizard dockerd[31574]: time="2022-05-28T14:36:44+08:00" level=warning msg="deprecated version : `1`, please switch to version `2`"
May 28 14:36:44 lizard dockerd[31574]: time="2022-05-28T14:36:44.659346964+08:00" level=warning msg="failed to load plugin io.containerd.snapshotter.v1.devmapper" error="devmapper no>
May 28 14:36:44 lizard dockerd[31574]: time="2022-05-28T14:36:44.660040930+08:00" level=warning msg="could not use snapshotter devmapper in metadata plugin" error="devmapper not conf>
May 28 14:36:45 lizard dockerd[31565]: time="2022-05-28T14:36:45.018458102+08:00" level=warning msg="Your kernel does not support swap memory limit"
May 28 14:36:45 lizard dockerd[31565]: time="2022-05-28T14:36:45.018495482+08:00" level=warning msg="Your kernel does not support CPU realtime scheduler"
May 28 14:36:45 lizard dockerd[31565]: time="2022-05-28T14:36:45.018502682+08:00" level=warning msg="Your kernel does not support cgroup blkio weight"
May 28 14:36:45 lizard dockerd[31565]: time="2022-05-28T14:36:45.018506223+08:00" level=warning msg="Your kernel does not support cgroup blkio weight_device"
May 28 14:36:45 lizard systemd[1]: Started Docker Application Container Engine.
```

Let's download an image `alpine` to simulate an root file system under `/opt/test` folder.

```
james@lizard:/opt> mkdir test
james@lizard:/opt> cd test
james@lizard:/opt/test> wget https://dl-cdn.alpinelinux.org/alpine/v3.13/releases/x86_64/alpine-minirootfs-3.13.4-x86_64.tar.gz
james@lizard:/opt/test> tar zxvf alpine-minirootfs-3.13.4-x86_64.tar.gz -C alpine-minirootfs/

james@lizard:/opt> tree ./test -L 1
./test
├── alpine-minirootfs-3.13.4-x86_64.tar.gz
├── bin
├── dev
├── etc
├── home
├── lib
├── media
├── mnt
├── opt
├── proc
├── root
├── run
├── sbin
├── srv
├── sys
├── tmp
├── usr
└── var
```

Mount folder `/opt/test/proc` to a file and use command `unshare` to build a guest system.
```
james@lizard:/opt> sudo mount -t tmpfs tmpfs /opt/test/proc

james@lizard:/opt> sudo unshare --pid --mount-proc=$PWD/test/proc --fork chroot ./test/ /bin/sh
/ # ps -ef
PID   USER     TIME  COMMAND
    1 root      0:00 /bin/sh
    2 root      0:00 ps -ef
/ # touch 123
/ # ls 123
123
```

The file `123` created in guest system is accessable and writable from host system.
```
james@lizard:/opt> su -

lizard:/opt/test # ls 123
123

lizard:/opt/test # echo hello > 123
```

We will see above change in guest system.
```
/ # cat 123
hello
```

Let's create two folders `/opt/test-1` and `/opt/test-2`.
```
james@lizard:/opt> mkdir test-1
james@lizard:/opt> mkdir test-2
```

Create two guests system. Mount `/opt/test/home/` to different folders for different guests.
```
james@lizard:/opt> sudo mount --bind /opt/test-1 /opt/test/home/
james@lizard:/opt> sudo unshare --pid --mount-proc=$PWD/test/proc --fork chroot ./test/ /bin/sh
/ # cd /home
/home # echo "test-1" > 123.1
/home # cat 123.1
test-1

james@lizard:/opt> sudo mount --bind /opt/test-2 /opt/test/home/
james@lizard:/opt> sudo unshare --pid --mount-proc=$PWD/test/proc --fork chroot ./test/ /bin/sh
/ # cd /home
/home # echo "test-2" > 123.2
/home # cat 123.2
test-2

ames@lizard:/opt> ll test/home
-rw-r--r-- 1 root root 7 May 31 22:47 123.1
-rw-r--r-- 1 root root 7 May 31 22:47 123.2

james@lizard:/opt> ll test-1/
-rw-r--r-- 1 root root 7 May 31 22:47 123.1
-rw-r--r-- 1 root root 7 May 31 22:47 123.2

james@lizard:/opt> ll test-2/
-rw-r--r-- 1 root root 7 May 31 22:47 123.1
-rw-r--r-- 1 root root 7 May 31 22:47 123.2
```
With above demo, the conclusion is that two guests share same home folder on host system and will impact each other.






https://zhuanlan.zhihu.com/p/370869886

root@HomeDeb:~# mount -t tmpfs tmpfs alpine-minirootfs/proc
root@HomeDeb:~# unshare -m -p -f --mount-proc=$PWD/alpine-minirootfs/proc chroot ./alpine-minirootfs /bin/sh

root@HomeDeb:~# mkdir /tmp/container-1 
root@HomeDeb:~# mount --bind /tmp/container-1 alpine-minirootfs/home/
root@HomeDeb:~# unshare -m -p -f --mount-proc=$PWD/alpine-minirootfs/proc chroot ./alpine-minirootfs /bin/sh


root@HomeDeb:~# mkdir /tmp/container-2
root@HomeDeb:~# mount --bind /tmp/container-2 alpine-minirootfs/home/
root@HomeDeb:~# unshare -m -p -f --mount-proc=$PWD/alpine-minirootfs/proc chroot ./alpine-minirootfs /bin/sh
















## 3.Basic Concepts of Kubernetes

### Installing kubectl

Install kubectl by referring the [guidd](https://kubernetes.io/docs/tasks/tools/).

Download kubectl.
```
james@lizard:/opt> curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
```

Install kubectl.
```
james@lizard:/opt> sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

james@lizard:/opt> l /usr/local/bin/kubectl
-rwxr-xr-x 1 root root 45711360 May 28 14:49 /usr/local/bin/kubectl*
```

Test to ensure the version you installed is up-to-date:
```
james@lizard:/opt> kubectl version --client
WARNING: This version information is deprecated and will be replaced with the output from kubectl version --short.  Use --output=yaml|json to get the full version.
Client Version: version.Info{Major:"1", Minor:"24", GitVersion:"v1.24.1", GitCommit:"3ddd0f45aa91e2f30c70734b175631bec5b5825a", GitTreeState:"clean", BuildDate:"2022-05-24T12:26:19Z", GoVersion:"go1.18.2", Compiler:"gc", Platform:"linux/amd64"}
Kustomize Version: v4.5.4
```


### Installing Minikube

Install Minikube by referring to the [guide](https://minikube.sigs.k8s.io/docs/start/).

Installation.
```
james@lizard:/opt> curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 69.2M  100 69.2M    0     0  5720k      0  0:00:12  0:00:12 --:--:-- 6328k

james@lizard:/opt> sudo install minikube-linux-amd64 /usr/local/bin/minikube

james@lizard:/opt> ll /usr/local/bin/minikube
-rwxr-xr-x 1 root root 72651748 May 28 14:56 /usr/local/bin/minikube
```

Start start cluster.
```
james@lizard:/opt> minikube start
minikube v1.25.2 on Opensuse-Leap 15.3
Using the docker driver based on existing profile
docker is currently using the btrfs storage driver, consider switching to overlay2 for better performance
Starting control plane node minikube in cluster minikube
Pulling base image ...
Updating the running docker "minikube" container ...
Preparing Kubernetes v1.23.3 on Docker 20.10.12 ...
  ▪ kubelet.housekeeping-interval=5m
  ▪ Generating certificates and keys ...
  ▪ Booting up control plane ...
  ▪ Configuring RBAC rules ...
Verifying Kubernetes components...
  ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
Enabled addons: default-storageclass, storage-provisioner
Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
```

Two folders were created after `minikube start`. 

* `~/.kube` : default config file was created here.
* `~/.minikube` : configure files of Minikube.


Check what Docker images has been pulled down and what containers are up after Minikube start.
```
james@lizard:/opt> docker images --all
REPOSITORY       TAG       IMAGE ID       CREATED        SIZE
kicbase/stable   v0.0.30   1312ccd2422d   3 months ago   1.14GB

james@lizard:/opt> docker container ls -all
CONTAINER ID   IMAGE                    COMMAND                  CREATED          STATUS          PORTS                                                                                                                                  NAMES
5ec9c519d1e1   kicbase/stable:v0.0.30   "/usr/local/bin/entr…"   39 minutes ago   Up 39 minutes   127.0.0.1:49157->22/tcp, 127.0.0.1:49156->2376/tcp, 127.0.0.1:49155->5000/tcp, 127.0.0.1:49154->8443/tcp, 127.0.0.1:49153->32443/tcp   minikube
```

Get all nodes and namespaces deployed by default after Minikube installed.
```
james@lizard:/opt> kubectl get nodes
NAME       STATUS   ROLES                  AGE     VERSION

james@lizard:/opt> kubectl get ns
NAME              STATUS   AGE
default           Active   4h51m
kube-node-lease   Active   4h51m
kube-public       Active   4h51m
kube-system       Active   4h51m
```

Enbale Minikube addon - Dashboard.
```
james@lizard:/opt> minikube addons list
james@lizard:/opt> minikube addons enable dashboard
```

Get all the services in all the namespaces.
```
james@lizard:/opt> kubectl get service --all-namespaces
NAMESPACE              NAME                        TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                  AGE
default                kubernetes                  ClusterIP   10.96.0.1        <none>        443/TCP                  5h2m
kube-system            kube-dns                    ClusterIP   10.96.0.10       <none>        53/UDP,53/TCP,9153/TCP   5h2m
kubernetes-dashboard   dashboard-metrics-scraper   ClusterIP   10.110.44.98     <none>        8000/TCP                 49s
kubernetes-dashboard   kubernetes-dashboard        ClusterIP   10.108.121.183   <none>        80/TCP                   49s

james@lizard:/opt> kubectl get svc --all-namespaces
NAMESPACE              NAME                        TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                  AGE
default                kubernetes                  ClusterIP   10.96.0.1        <none>        443/TCP                  5h2m
kube-system            kube-dns                    ClusterIP   10.96.0.10       <none>        53/UDP,53/TCP,9153/TCP   5h2m
kubernetes-dashboard   dashboard-metrics-scraper   ClusterIP   10.110.44.98     <none>        8000/TCP                 49s
kubernetes-dashboard   kubernetes-dashboard        ClusterIP   10.108.121.183   <none>        80/TCP                   49s
```

Get details of deployment kubernetes-dashboard.
```
james@lizard:/opt> kubectl get deployment -n kubernetes-dashboard
NAME                        READY   UP-TO-DATE   AVAILABLE   AGE
dashboard-metrics-scraper   1/1     1            1           5m54s
kubernetes-dashboard        1/1     1            1           5m54s
```

Explore the dashboard, and verify it via `http://localhost:9090`
```
james@lizard:/opt> kubectl -n kubernetes-dashboard port-forward deployment/kubernetes-dashboard 9090
```

The dashboard looks like below.

![dashboard](./assets/003.png)




### Installing Helm

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
james@lizard:/opt> curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
james@lizard:/opt> chmod 700 get_helm.sh

james@lizard:/opt> ./get_helm.sh
Downloading https://get.helm.sh/helm-v3.9.0-linux-amd64.tar.gz
Verifying checksum... Done.
Preparing to install helm into /usr/local/bin
helm installed into /usr/local/bin/helm
```

Note:
[`helm init`](https://helm.sh/docs/helm/helm_init/) does not exist in Helm 3, following the removal of Tiller. You no longer need to install Tiller in your cluster in order to use Helm.

`helm search` can be used to search two different types of source:

* `helm search hub` searches the [Artifact Hub](https://artifacthub.io/), which lists helm charts from dozens of different repositories.
* `helm search repo` searches the repositories that you have added to your local helm client (with helm repo add). This search is done over local data, and no public network connection is needed.
















### nodes
### kubelet
### api server & rest API
### etcd
### kube-proxy
### kubectl
### yaml & json + basic structure of k8s resources
### namespaces
### pods - schedule, describe, logs, exec
### liveness & readiness probes
### labels
### replica sets, deployments
### cluster networking
### services (clusterIP, NodePort, Loadbalancer)
### communication via services



## Storage
### persistent volume
### persistent volume claims
### storage classes


## Configuration
### secrets
### config maps


## Further entities
### networking
### workloads
### administration
### Ingress
### controller & custom resources



## Stateful workloads
### StatefulSets and headless services



## Administration
### User management - service accounts
### Role based authorization (RBAC)
### Image pull secrets
### Network policies
### Node management
### Kubernetes Dashboard
### Scheduling pods on dedicated nodes
### get your own cluster | Gardener


## Troubleshooting





