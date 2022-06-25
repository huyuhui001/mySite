# Kubernetes Foundation

## **1.Demo environment**

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

### Linux Primitives

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

james@lizard:/opt> ll test/home
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





### Container lifecycle


#### Overview

Pull down below images in advance.
```
james@lizard:~> docker image pull busybox
james@lizard:~> docker image pull nginx
james@lizard:~> docker image pull alpine
james@lizard:~> docker image pull jenkins/jenkins:lts
james@lizard:~> docker image pull golang:1.12-alpine
james@lizard:~> docker image pull golang
```

Download some docker images.
Create and run a new busybox container interactively and connect a pseudo terminal to it.
Inside the container, use the top command to find out that `/bin/sh` is running as process with the PID 1 and `top` process is also running. 
After that, just exit.
```
james@lizard:~> docker image ls  (or docker images)
REPOSITORY        TAG           IMAGE ID       CREATED         SIZE
golang            latest        80d9a75ccb38   5 days ago      941MB
nginx             latest        c316d5a335a5   6 days ago      141MB
jenkins/jenkins   lts           9aee0d53624f   2 weeks ago     441MB
busybox           latest        beae173ccac6   4 weeks ago     1.24MB
alpine            latest        c059bfaa849c   2 months ago    5.58MB
golang            1.12-alpine   76bddfb5e55e   23 months ago   346MB

james@lizard:~> docker run -d -it --name busybox_v1 -v /opt/test:/docker busybox:latest /bin/sh

james@lizard:~> docker container ps -a
CONTAINER ID   IMAGE            COMMAND     CREATED          STATUS         PORTS     NAMES
185efe490507   busybox:latest   "/bin/sh"   11 seconds ago   Up 9 seconds             busybox_v1

james@lizard:~> docker exec -it 185efe490507 /bin/sh
/ # top
Mem: 3627396K used, 12731512K free, 10080K shrd, 2920K buff, 2999340K cached
CPU:  0.0% usr  0.1% sys  0.0% nic 99.8% idle  0.0% io  0.0% irq  0.0% sirq
Load average: 0.38 1.09 1.29 2/277 14
  PID  PPID USER     STAT   VSZ %VSZ CPU %CPU COMMAND
    1     0 root     S     1332  0.0   1  0.0 /bin/sh
    8     0 root     S     1332  0.0   2  0.0 /bin/sh
   14     8 root     R     1328  0.0   1  0.0 top
/ # exitbuild 
```

Start a new nginx container in detached mode.
Use the `docker exec` command to start another shell (`/bin/sh`) in the nginx container. 
Use ps to find out that `sh` and `ps` commands are running in your container.
```
james@lizard:~> docker run -d -it --name nginx_v1 -v /opt/test:/docker nginx:latest /bin/sh

james@lizard:~> docker container ps -a
CONTAINER ID   IMAGE            COMMAND                  CREATED         STATUS         PORTS     NAMES
edb640127a0d   nginx:latest     "/docker-entrypoint.…"   3 seconds ago   Up 2 seconds   80/tcp    nginx_v1
185efe490507   busybox:latest   "/bin/sh"                2 minutes ago   Up 2 minutes             busybox_v1

james@lizard:~> docker exec -it edb640127a0d /bin/sh
# ps
/bin/sh: 2: ps: not found
# apt-get update && apt-get install -y procps
# ps
   PID TTY          TIME CMD
     8 pts/1    00:00:00 sh
   351 pts/1    00:00:00 ps
# exit
```

Now we have two running containers below.
```
james@lizard:~> docker container ps -a
CONTAINER ID   IMAGE            COMMAND                  CREATED          STATUS          PORTS     NAMES
edb640127a0d   nginx:latest     "/docker-entrypoint.…"   7 minutes ago    Up 7 minutes    80/tcp    nginx_v1
185efe490507   busybox:latest   "/bin/sh"                10 minutes 
Let's make use of this to create a new stage:ago   Up 10 minutes             busybox_v1
```

Let's use `docker logs` to display the logs of the container we just exited from. 
The option `--since 35m` means display log in last 35 minutes.
```
james@lizard:~> docker logs nginx_v1 --details --since 35m
james@lizard:~> docker logs busybox_v1 --details --since 35m
```
Let's make use of this to create a new stage:

Use the `docker stop` command to end your nginx container.
```
james@lizard:~> docker stop busybox_v1
busybox_v1
james@lizard:~> docker stop nginx_v1 
nginx_v1

james@lizard:~> docker container ps -a
CONTAINER ID   IMAGE            COMMAND                  CREATED          STATUS                        PORTS     NAMES
edb640127a0d   nginx:latest     "/docker-entrypoint.…"   10 minutes ago   Exited (137) 4 seconds ago              nginx_v1
185efe490507   busybox:latest   "/bin/sh"                13 minutes ago   Exited (137) 16 seconds ago             busybox_v1
```

With above command `docker container ps -a`, we get a list of all running and exited containers. 
Remove them with docker rm.
Use `docker rm $(docker ps -aq)` to clean up all containers on your host. Use it with caution!
```
james@lizard:~> docker rm busybox_v1
busybox_v1

james@lizard:~> docker container ps -a
CONTAINER ID   IMAGE          COMMAND                  CREATED          STATUS                        PORTS     NAMES
edb640127a0d   nginx:latest   "/docker-entrypoint.…"   11 minutes ago   Exited (137) 53 seconds ago             nginx_v1
```

#### Ports and volumes

Now, let's run an nginx webserver in a container and serve a website to the outside world.

Start a new nginx container and export the port of the nginx webserver to a random port that is chosen by Docker. 

Use command `docker ps` to find you which port the webserver is forwarded. Access the docker with the forwarded port number on host `http://localhost:<port#>`.
```
james@lizard:~> docker container ps -a
CONTAINER ID   IMAGE          COMMAND                  CREATED          STATUS                        PORTS     NAMES
edb640127a0d   nginx:latest   "/docker-entrypoint.…"   11 minutes ago   Exited (137) 53 seconds ago             nginx_v1

james@lizard:~> docker run -d -P --name nginx_v2 nginx:latest

james@lizard:~> docker container ps -a
CONTAINER ID   IMAGE          COMMAND                  CREATED          STATUS                       PORTS                                     NAMES
3349a84e5024   nginx:latest   "/docker-entrypoint.…"   15 seconds ago   Up 14 seconds                0.0.0.0:49153->80/tcp, :::49153->80/tcp   nginx_v2
edb640127a0d   nginx:latest   "/docker-entrypoint.…"   13 minutes ago   Exited (137) 3 minutes ago                                             nginx_v1
```

Start another nginx container and expose port to `1080` on host as an example via `http://localhost:1080`.
```
james@lizard:~> docker run -d -p 1080:80 --name nginx_v3 nginx:latest

james@lizard:~> docker container ps -a
CONTAINER ID   IMAGE          COMMAND                  CREATED          STATUS              PORTS                                     NAMES
214ded9b8645   nginx:latest   "/docker-entrypoint.…"   30 seconds ago   Up 28 seconds       0.0.0.0:1080->80/tcp, :::1080->80/tcp     nginx_v3
3349a84e5024   nginx:latest   "/docker-entrypoint.…"   3 hours ago      Up About a minute   0.0.0.0:49153->80/tcp, :::49153->80/tcp   nginx_v2
edb640127a0d   nginx:latest   "/docker-entrypoint.…"   3 hours ago      Up 3 seconds        80/tcp                                    nginx_v1
```
Let's make use of this to create a new stage:

Use command `docker inspect` to find out which port is exposed by the image. Network information (ip, gateway, ports, etc.) is part of the output JSON format.
```
james@lizard:~> docker inspect nginx_v3 
```

Create a file `index.html` in folder `/opt/test` with below sample content. 

    <html>
    <head>
        <title>Sample Website from my container</title>
    </head>
    <body>
        <h1>This is a custom website.</h1>
        <p>This website is served from my <a href="http://www.docker.com" target="_blank">Docker</a> container.</p>
    </body>
    </html>


Start a new container that bind-mounts host directory `/opt/test` to container directory `/usr/share/nginx/html` as a volume, so that NGINX will publish the HTML file wee just created instead of its default message via `http://localhost:49159/` below.
```
james@lizard:~> docker run -d -P --mount type=bind,source=/opt/test/,target=/usr/share/nginx/html --name nginx_v3-1 nginx:latest

james@lizard:~> docker container ps -a
CONTAINER ID   IMAGE          COMMAND                  CREATED          STATUS              PORTS                                     NAMES
bd94e4df65cf   nginx:latest   "/docker-entrypoint.…"   30 seconds ago   Up About a minute   0.0.0.0:49159->80/tcp, :::49154->80/tcp   nginx_v3-1                                                                                                
214ded9b8645   nginx:latest   "/docker-entrypoint.…"   30 seconds ago   Up 28 seconds       0.0.0.0:1080->80/tcp, :::1080->80/tcp     nginx_v3
3349a84e5024   nginx:latest   "/docker-entrypoint.…"   3 hours ago      Up About a minute   0.0.0.0:49153->80/tcp, :::49153->80/tcp   nginx_v2
edb640127a0d   nginx:latest   "/docker-entrypoint.…"   3 hours ago      Up 3 seconds        80/tcp                                    nginx_v1
```

Check nginx config file on where is the html home page stored in container.
```
james@lizard:~> docker exec -it nginx_v3-1 /bin/sh
# cd /etc/nginx/conf.d
# ls
default.conf
# cat default.conf
server {
    listen       80;
    listen  [::]:80;
    server_name  localhost;

    #access_log  /var/log/nginx/host.access.log  main;

    location / {
        root   /usr/share/nginx/html;  <--
        index  index.html index.htm;
    }

    #error_page  404              /404.html;

    # redirect server error pages to the static page /50x.html
    #
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }

    # proxy the PHP scripts to Apache listening on 127.0.0.1:80
    #
    #location ~ \.php$ {
    #    proxy_pass   http://127.0.0.1;
    #}

    # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
    #
    #location ~ \.php$ {
    #    root           html;
    #    fastcgi_pass   127.0.0.1:9000;
    #    fastcgi_index  index.php;
    #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
    #    include        fastcgi_params;
    #}

    # deny access to .htaccess files, if Apache's document root
    # concurs with nginx's one
    #
    #location ~ /\.ht {
    #    deny  all;
    #}
}
# cd /usr/share/nginx/html
# cat index.html              
  <html>
  <head>
      <title>Sample Website from my container</title>
  </head>
  <body>
      <h1>This is a custom website.</h1>
      <p>This website is served from my <a href="http://www.docker.com" target="_blank">Docker</a> container.</p>
  </body>
  </html>
# 
```


It's recommendable to add a persistence with volumes API, instead of storing data in a docker container. Docker supports 2 ways of mount:

* Bind mounts: 
    * mount a local host directory onto a certain path in the container. 
    * Everything that was present before in the target directory is hidden (nature of the bind mount). 
    * For example, if you have some configuration you want to inject, write your config file, store it on your docker host at `/home/container/config` and mount the content of this directory to `/usr/application/config` (assuming the application reads config from there). 
    * Command: `docker run --mount type=bind,source=<source path>,target=<container path> …`
* Named volumes: 
    * docker can create a separated storage volume. 
    * Its lifecycle is independent from the container but still managed by docker. 
    * Upon creation, the content of the mount target is merged into the volume. 
    * Command: `docker run --mount source=<vol name>,target=<container path> …`


How to differentiate between bind mountbuild s and named volumes? 

* When specifying an absolute path, docker assumes a bind mount. 
* When you just give a name (like in a relative path “config”), it will assume a named volume and create a volume “config”.
* Note: Persistent storage is 'provided' by the host. It can be a part of the file system on the host directly but also an NFS mount. 



#### Dockerfile

Let's build an image with a Dockerfile,build  tag it and upload it to a registry. 

Get docker image build history.
```
james@lizard:~> docker image history nginx:latest 
IMAGE          CREATED      CREATED BY                                      SIZE      COMMENT
c316d5a335a5   6 days ago   /bin/sh -c #(nop)  CMD ["nginx" "-g" "daemon…   0B
<missing>      6 days ago   /bin/sh -c #(nop)  STOPSIGNAL SIGQUIT           0B
<missing>      6 days ago   /bin/sh -c #(nop)  EXPOSE 80                    0B
<missing>      6 days ago   /bin/sh -c #(nop)  ENTRYPOINT ["/docker-entr…   0B
<missing>      6 days ago   /bin/sh -c #(nop) COPY file:09a214a3e07c919a…   4.61kB
<missing>      6 days ago   /bin/sh -c build #(nop) COPY file:0fd5fca330dcd6a7…   1.04kB
<missing>      6 days ago   /bin/sh -c #(nop) COPY file:0b866ff3fc1ef5b0…   1.96kB
<missing>      6 days ago   /bin/sh -c #(nop) COPY file:65504f71f5855ca0…   1.2kB
<missing>      6 days ago   /bin/sh -c set -x     && addgroup --system -…   61.1MB
<missing>      6 days ago   /bin/sh -c #(nop)  ENV PKG_RELEASE=1~bullseye   0B
<missing>      6 days ago   /bin/sh -c #(nop)  ENV NJS_VERSION=0.7.2        0B
<missing>      6 days ago   /bin/sh -c #(nop)  ENV NGINX_VERSION=1.21.6     0B
<missing>      6 days ago   /bin/sh -c #(nop)  LABEL maintainer=NGINX Do…   0B
<missing>      7 days ago   /bin/sh -c #(nop)  CMD ["bash"]                 0B
<missing>      7 days ago   /bin/sh -c #(nop) ADD file:90495c24c897ec479…   80.4MB
```


Create an empty directory `/opt/tmp-1`, change to the directory and create an sample `index.html` file in `/opt/tmp-1`.
```
james@lizard:/opt/tmp-1> cat index.html 
  <html>
  <head>
      <title>Sample Website from my container</title>
  </head>
  <body>
      <h1>This is a custom website.</h1>
      <p>This website is served from my <a href="http://www.docker.com" target="_blank">Docker</a> container.</p>
  </body>
  </html>
```

Use `FROM` to extend an existing image, specify the release number.

Use `COPY` to copy a new default website into the image, e.g., `/usr/share/nginx/html`

Create SSL configuration `/opt/tmp-1/ssl.conf` for nginx.

    server {
        listen       443 ssl;
        server_name  localhost;
    
        ssl_certificate /etc/nginx/ssl/nginx.crt;
        ssl_certificate_key /etc/nginx/ssl/nginx.key;
    
        location / {
            root   /usr/share/nginx/html;
            index  index.html index.htm;
        }
    }



Use OpenSSL to create a self-signed certificate so SSL/TLS to work would work.

Use the following command to create an encryption key and a certificate.
```
james@lizard:/opt/tmp-1> openssl req -x509 -nodes -newkey rsa:4096 -keyout nginx.key -out nginx.crt -days 365 -subj "/CN=$(hostname)"
Generating a RSA private key
........++++
................................++++
writing new private key to 'nginx.key'
-----
```

To enable encrypted HTTPS, we need to expose port 443 with the EXPOSE directive. The default nginx image only exposes port 80 for unencrypted HTTP.

In summary, we create below Dockerfile in foder `/opt/tmp-1`. 
```
james@lizard:/opt/tmp-1> cat Dockerfile 
FROM nginx:latest

# copy the custom website into the image
COPY index.html /usr/share/nginx/html

# copy the SSL configuration file into the image
COPY ssl.conf /etc/nginx/conf.d/ssl.conf

# download the SSL key and certificate into the image
COPY nginx.key /etc/nginx/ssl/
COPY nginx.crt /etc/nginx/ssl/

# expose the HTTPS port
EXPOSE 443
```

We have five files in foder `/opt/tmp-1` till now.
```
james@lizard:/opt/tmp-1> ls
Dockerfile  index.html  nginx.crt  nginx.key  ssl.conf
```

Now let's use the `docker build` command to build the image, forward the containers ports 80 and 443.
```
james@lizard:~> docker build -t nginx:my1 /opt/tmp-1/
Sending build context to Docker daemon  62.98kB
Let's make use of this to create a new stage:
Step 1/6 : FROM nginx:latest
 ---> c316d5a335a5
Step 2/6 : COPY index.html /usr/share/nginx/html
 ---> 4a71ac8a2624
Step 3/6 : COPY ssl.conf /etc/nginx/conf.d/ssl.conf
 ---> ad574bc8080c
Step 4/6 : COPY nginx.key /etc/nginx/ssl/
 ---> 90c41ec98809
Step 5/6 : COPY nginx.crt /etc/nginx/ssl/
 ---> 5801c1e5e02f
Step 6/6 : EXPOSE 443
 ---> Running in 0db1bffe7eb3
Removing intermediate container 0db1bffe7eb3
 ---> 748439b24876
Successfully built 748439b24876
Successfully tagged nginx:my1

james@lizard:~> docker image ls
REPOSITORY        TAG           IMAGE ID       CREATED          SIZE
nginx             my1           748439b24876   44 seconds ago   142MB
golang            latest        80d9a75ccb38   5 days ago       941MB
nginx             latest        c316d5a335a5   6 days ago       141MB
jenkins/jenkins   lts           9aee0d53624f   2 weeks ago      441MB
busybox           latest        beae173ccac6   4 weeks ago      1.24MB
alpine            latest        c059bfaa849c   2 months ago     5.58MB
golang            1.12-alpine   76bddfb5e55e   23 months ago    346MB


james@lizard:~> docker run -d -p 1086:80 -p 1088:443 --name nginx_v5 nginx:my1

james@lizard:~> docker container ps -a
CONTAINER ID   IMAGE          COMMAND  build                 CREATED             STATUS                           PORTS                                                                            NAMES
70126d22e48b   nginx:my1      "/docker-entrypoint.…"   7 seconds ago       Up 6 seconds                     0.0.0.0:1086->80/tcp, :::1086->80/tcp, 0.0.0.0:1088->443/tcp, :::1088->443/tcp   nginx_v5
7714058076c0   nginx:latest   "/docker-entrypoint.…"   About an hour ago   Exited (0) 48 seconds ago                                                                                         nginx_v4
214ded9b8645   nginx:latest   "/docker-entrypoint.…"   2 hours ago         Exited (0) About an hour ago                                                                                      nginx_v3
3349a84e5024   nginx:latest   "/docker-entrypoint.…"   5 hours ago         Exited (0) About an hour ago                                                                                      nginx_v2
edb640127a0d   nginx:latest   "/docker-entrypoint.…"   5 hours ago         Exited (137) About an hour ago                                                                                    nginx_v1
```


Above changes can be validated via below links:

    http://localhost:1086/
    https://localhost:1088/




Register an account in [DockerHub](https://hub.docker.com/) and enable access token in Docker Hub for CLI client authentication.
```
james@lizard:~> docker login
Username: <your account id>
Password: <token>
```

Tag the image to give image a nice name and a release number as tag, e.g., name is `secure_nginx_0001`, tag is `v1`.
```
james@lizard:~> docker tag nginx:my1 <your account id>secure_nginx_0001:v1

james@lizard:~> docker push <your account id>secure_nginx_0001:v1

james@lizard:~> docker image ls
REPOSITORY                            TAG           IMAGE ID       CREATED         SIZE
nginx                                 my1           748439b24876   7 minutes ago   142MB
<your account id>secure_nginx_0001    v1            748439b24876   7 minutes ago   142MB
golang                                latest        80d9a75ccb38   5 days ago      941MB
nginx                                 latest        c316d5a335a5   6 days ago      141MB
jenkins/jenkins                       lts           9aee0d53624f   2 weeks ago     441MB
busybox                               latest        beae173ccac6   4 weeks ago     1.24MB
alpine                                latest        c059bfaa849c   2 months ago    5.58MB
golang                                1.12-alpine   76bddfb5e55e   23 months ago   346MB
```


#### Multi-stage Dockerfile

Let's show an example of multi-stage build. The multi-stage in the context of Docker means, we can have more than one line with a FROM keyword. 

Create folder `/opt/tmp-2` and `/opt/tmp-2/tmpl`. 

Create files [edit.html](./assets/edit.html), [view.html](./assets/view.html), [wiki.go](./assets/wiki.go) and structure likes below.
```
james@lizard:/opt/tmp-2> tree -l
.
├── tmpl
│   ├── edit.html
│   └── view.html
└── wiki.go
```


Create an new Dockerfile that starts 
```
james@lizard:/opt/tmp-2> cat Dockerfile
# app builder stage
FROM golang:1.12-alpine as builder

## copy the go source code over and build the binary
WORKDIR /go/src
COPY wiki.go /go/src/wiki.go
RUN go build wiki.go

# app exec stage
# separate & new image starts here!#
FROM alpine:3.9

# prepare file system etc
RUN mkdir -p /app/data /app/tmpl && adduser -S -D -H -h /app appuser
COPY tmpl/* /app/tmpl/

# get the compiled binary from the previous stage
COPY --from=builder /go/src/wiki /app/wiki

# prepare runtime env
RUN chown -R appuser /app
USER appuser
WORKDIR /app

# expose app port & set default command
EXPOSE 8080
CMD ["/app/wiki"]
```

Build the images by Dockerfile we created above.
```
james@lizard:~> docker build -t lizard/golang:my1 /opt/tmp-2/
Sending build context to Docker daemon  9.728kB
Step 1/13 : FROM golang:1.12-alpine as builder
 ---> 76bddfb5e55e
Step 2/13 : WORKDIR /go/src
 ---> Running in 279957765a67
Removing intermediate container 279957765a67
 ---> d74f3297387b
Step 3/13 : COPY wiki.go /go/src/wiki.go
 ---> f14f358f10c0
Step 4/13 : RUN go build wiki.go
 ---> Running in af4a9d2d1dcc
Removing intermediate container af4a9d2d1dcc
 ---> 101e734099a3
Step 5/13 : FROM alpine:3.9
3.9: Pulling from library/alpine
31603596830f: Pull complete
Digest: sha256:414e0518bb9228d35e4cd5165567fb91d26c6a214e9c95899e1e056fcd349011
Status: Downloaded newer image for alpine:3.9
 ---> 78a2ce922f86
Step 6/13 : RUN mkdir -p /app/data /app/tmpl && adduser -S -D -H -h /app appuser
 ---> Running in c7a8793fc95d
Removing intermediate container c7a8793fc95d
 ---> a6e83922a81f
Step 7/13 : COPY tmpl/* /app/tmpl/
 ---> e48d44caf735
Step 8/13 : COPY --from=builder /go/src/wiki /app/wiki
 ---> 26cc829fe32b
Step 9/13 : RUN chown -R appuser /app
 ---> Running in 22f3af57f969
Removing intermediate container 22f3af57f969
 ---> ea7d678adf67
Step 10/13 : USER appuser
 ---> Running in 03c5d8e9ad45
Removing intermediate container 03c5d8e9ad45
 ---> 40a692198491
Step 11/13 : WORKDIR /app
 ---> Running in 7c1b04e38306
Removing intermediate container 7c1b04e38306
 ---> 45eaaebb0c12
Step 12/13 : EXPOSE 8080
 ---> Running in 84f06d2e5f90
Removing intermediate container 84f06d2e5f90
 ---> 3750bfa8c032
Step 13/13 : CMD ["/app/wiki"]
 ---> Running in 9ce20ca3a834
Removing intermediate container 9ce20ca3a834
 ---> 8621174bab0d
Successfully built 8621174bab0d
Successfully tagged lizard/golang:my1
```

Run the image in detached mode, create a port forwarding from port 8080 in the container to port 1090 on the host.
```
james@lizard:~> docker run -d -p 1090:8080 --name golan_v1 lizard/golang:my1
```

Access the container via link http://localhost:1090

Tab the golang image we created and push it to DockerHub.
```
james@lizard:~> docker tag lizard/golang:my1 <your acccount id>/golang_0001:v1

james@lizard:~> docker push <your acccount id>/golang_0001:v1
```










## 3.Basic Concepts of Kubernetes

### Kubernetes Components

A Kubernetes cluster consists of the components that represent the **control plane** and a set of machines called **nodes**.

![The components of a Kubernetes cluster](https://d33wubrfki0l68.cloudfront.net/2475489eaf20163ec0f54ddc1d92aa8d4c87c96b/e7c81/images/docs/components-of-kubernetes.svg)


**Kubernetes Components**: 

* **Control Plane Components**
    * **kube-apiserver**: query and manipulate the state of objects in Kubernetes.
    * **etcd**: all Kubernetes objects are stored on etcd. Kubernetes objects are persistent **entities** in the Kubernetes system, which are used to represent the state of your cluster.
    * **kube-scheduler**: watches for newly created Pods with no assigned node, and selects a node for them to run on.
    * **kube-controller-manager**: runs controller processes.
        * *Node controller*: Responsible for noticing and responding when nodes go down.
        * *Job controller*: Watches for Job objects that represent one-off tasks, then creates Pods to run those tasks to completion.
        * *Endpoints controller*: Populates the Endpoints object (that is, joins Services & Pods).
        * *Service Account & Token controllers*: Create default accounts and API access tokens for new namespaces.
    * **cloud-controller-manager**: embeds cloud-specific control logic and only runs controllers that are specific to your cloud provider, no need for own premises and learning environment.
        * *Node controller*: For checking the cloud provider to determine if a node has been deleted in the cloud after it stops responding
        * *Route controller*: For setting up routes in the underlying cloud infrastructure
        * *Service controller*: For creating, updating and deleting cloud provider load balancers
* **Node Components**
    * **kubelet**: An agent that runs on each node in the cluster. It makes sure that containers are running in a Pod.
    * **kube-proxy**: maintains network rules on nodes.
    * **Container runtime**: is the software that is responsible for running containers.
* Addons
    * DNS: is a DNS server and required by all Kubernetes clusters.
    * Web UI (Dashboard): web-based UI for Kubernetes clusters. 
    * Container Resource Monitoring: records generic time-series metrics about containers in a central database
    * Cluster-level Logging: is responsible for saving container logs to a central log store with search/browsing interface.


Scalability:

* **Scaling out** (horizontal scaling) by adding more servers to your architecture to spread the workload across more machines.
* **Scaling up** (vertical scaling) by adding more hard drives and memory to increase the computing capacity of physical servers. 





### Kubernetes Objects

Objects Overview:

* Object Spec:
    * providing a description of the characteristics the resource created to have: *its desired state*.
* Object Status:
    * describes the current state of the object.

Example of Deployment as an object that can represent an application running on cluster.

    apiVersion: apps/v1  # Which version of the Kubernetes API you're using to create this object
    kind: Deployment     # What kind of object you want to create
    metadata:            # Data that helps uniquely identify the object, including a name string, UID, and optional namespace
      name: nginx-deployment
    spec:                # What state you desire for the object
      selector:
        matchLabels:
          app: nginx
      replicas: 2 # tells deployment to run 2 pods matching the template
      template:
        metadata:
          labels:
            app: nginx
        spec:
          containers:
          - name: nginx
            image: nginx:1.14.2
            ports:
            - containerPort: 80



Object Management:

The `kubectl` command-line tool supports several different ways to create and manage Kubernetes objects. Read the [Kubectl book](https://kubectl.docs.kubernetes.io/) for details.

A Kubernetes object should be managed using ONLY one technique. Mixing and matching techniques for the same object results in undefined behavior. 

Three management techniques:

* Imperative commands
    * operates directly on live objects in a cluster. 
    * `kubectl create deployment nginx --image nginx`
* Imperative object configuration
    * `kubectl create -f nginx.yaml`
    * `kubectl delete -f nginx.yaml -f redis.yaml`
    * `kubectl replace -f nginx.yaml`
* Declarative object configuration
    * `kubectl diff -f configs/`
    * `kubectl apply -f configs/`





#### Object Names and IDs

Each object in your cluster has a *Name* that is unique for that type of resource.

* DNS Subdomain Names
* Label Names
* Path Segment Names

Every Kubernetes object also has a *UID* that is unique across the whole cluster.





#### Namespaces

In Kubernetes, namespaces provides a mechanism for isolating groups of resources within a single cluster. 

Names of resources need to be unique within a namespace, but not across namespaces. 

Namespace-based scoping is applicable only for namespaced objects (e.g. Deployments, Services, etc) and not for cluster-wide objects (e.g. StorageClass, Nodes, PersistentVolumes, etc)

Not All Objects are in a Namespace.


Kubernetes starts with four initial namespaces:

* `default` 
    The default namespace for objects with no other namespace
* `kube-system` 
    The namespace for objects created by the Kubernetes system
* `kube-public` 
    This namespace is created automatically and is readable by all users (including those not authenticated). 
    This namespace is mostly reserved for cluster usage, in case that some resources should be visible and readable publicly throughout the whole cluster. 
    The public aspect of this namespace is only a convention, not a requirement.
* `kube-node-lease` This namespace holds Lease objects associated with each node. Node leases allow the kubelet to send heartbeats so that the control plane can detect node failure.


Viewing namespaces: 

* `kubectl get namespace`

Setting the namespace for a request

* `kubectl run nginx --image=nginx --namespace=<insert-namespace-name-here>`
* `kubectl get pods --namespace=<insert-namespace-name-here>`






#### Labels and Selectors

Labels are key/value pairs that are attached to objects, such as pods. 
Valid label keys have two segments: an optional prefix and name, separated by a slash (`/`).

Labels are intended to be used to specify identifying attributes of objects that are meaningful and relevant to users.

Labels can be used to organize and to select subsets of objects. 
Labels can be attached to objects at creation time and subsequently added and modified at any time. 
Each object can have a set of key/value labels defined. 
Each Key must be unique for a given object.

Example of labels:
```
"metadata": {
    "labels": {
        "key1" : "value1",
        "key2" : "value2"
    }
}
```


Unlike names and UIDs, labels do not provide uniqueness. In general, we expect many objects to carry the same label(s).

The API currently supports two types of selectors: 

* equality-based, e.g., `environment = production`, `tier != frontend`
* set-based, e.g., `environment in (production, qa)`, `tier notin (frontend, backend)`

Sample commands:
```
kubectl get pods -l environment=production,tier=frontend
kubectl get pods -l 'environment in (production),tier in (frontend)'
kubectl get pods -l 'environment in (production, qa)'
kubectl get pods -l 'environment,environment notin (frontend)'
```





#### Annotations

Use Kubernetes annotations to attach arbitrary non-identifying metadata to objects. 
Clients such as tools and libraries can retrieve this metadata.

Use either labels or annotations to attach metadata to Kubernetes objects. 

* Labels can be used to select objects and to find collections of objects that satisfy certain conditions. 
* Annotations are not used to identify and select objects. 


Annotations, like labels, are key/value maps. The keys and the values in the map must be strings. 
```
"metadata": {
    "annotations": {
      "key1" : "value1",
      "key2" : "value2"
    }
}
```

Valid annotation keys have two segments: an optional prefix and name, separated by a slash (`/`). 






#### Field Selectors

Field selectors let you select Kubernetes resources based on the value of one or more resource fields. 

Here are some examples of field selector queries:
```
metadata.name=my-service
metadata.namespace!=default
status.phase=Pending
```

This kubectl command selects all Pods for which the value of the status.phase field is Running:
`kubectl get pods --field-selector status.phase=Running`


Supported field selectors vary by Kubernetes resource type. All resource types support the `metadata.name` and `metadata.namespace` fields. 

Use the `=`, `==`, and `!=` operators with field selectors (`=` and `==` mean the same thing). 

For example:

`kubectl get ingress --field-selector foo.bar=baz`

With operators, 
`kubectl get services  --all-namespaces --field-selector metadata.namespace!=default`

Chained selectors, 
`kubectl get pods --field-selector=status.phase!=Running,spec.restartPolicy=Always`

Multiple resource types, 
`kubectl get statefulsets,services --all-namespaces --field-selector metadata.namespace!=default`






#### Finalizers

Finalizers are *namespaced keys* that tell Kubernetes to wait until specific conditions are met before it fully deletes resources marked for *deletion*. 
*Finalizers alert controllers* to clean up resources the deleted object owned.

Finalizers are usually added to resources for a reason, so forcefully removing them can lead to issues in the cluster.

Like labels, *owner references* describe the relationships between objects in Kubernetes, but are used for a different purpose.

Kubernetes uses the owner references (not labels) to determine which Pods in the cluster need cleanup.

Kubernetes processes finalizers when it identifies owner references on a resource targeted for deletion.





#### Owners and Dependents

In Kubernetes, some objects are owners of other objects. For example, a ReplicaSet is the owner of a set of Pods. 
These owned objects are dependents of their owner.

Dependent objects have a `metadata.ownerReferences` field that references their owner object.

A valid owner reference consists of the object name and a UID within the same namespace as the dependent object.

Dependent objects also have an `ownerReferences.blockOwnerDeletion` field that takes a boolean value and controls whether specific dependents can block garbage collection from deleting their owner object. 





## 4.Tutorials

* [Tutorials: local deployment](KubernetesTutorials-Local-Deploy.md)

* [Tutorials: SAP BTP trail account](KubernetesTutorials-BTP-trail.md)

* [Tutorials: Aliyun Account](KubernetesTutorials-Aliyun.md)









