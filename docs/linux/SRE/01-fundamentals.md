# Linux 基础

## 系统环境

### Rocky

从网站下载Rocky系统ISO镜像：
```
https://www.rockylinux.org/download/
```

通过`wget`命令下载Rocky系统ISO镜像。这里我们使用`Rocky 9.0`。
```
wget https://download.rockylinux.org/pub/rocky/9.0/isos/x86_64/Rocky-9.0-x86_64-dvd.iso
```

安装时我选择了激活`root`用户，选择了Server模式安装（没有GUI）。

以`root`登录，执行下面命令修改`sudo`权限。
```
visudo
```
并激活下面一行（不设密码，方便练习）：
```
%wheel  ALL=(ALL)       NOPASSWD: ALL
```

创建用户`vagrant`，并设置`wheel`为主要组和修改密码。
```
adduser vagrant
usermod -g wheel vagrant
passwd vagrant
```

设定hostname（包括别名），并查看结果。
```
hostnamectl set-hostname --static "rocky9"
hostnamectl set-hostname --pretty "rocky9"

hostnamectl
cat /etc/hostname
```

!!! Info
    由systemd控制的主机名的服务配置信息：`/usr/lib/systemd/system/systemd-hostnamed.service`


Rocky的软件源的配置信息保存在目录`/etc/yum.repos.d/`下。如果访问默认源比较慢，可以更新阿里源或者科大源。

更换阿里源。
```
sed -e 's|^mirrorlist=|#mirrorlist=|g' \
    -e 's|^#baseurl=http://dl.rockylinux.org/$contentdir|baseurl=https://mirrors.aliyun.com/rockylinux|g' \
    -i.bak \
    /etc/yum.repos.d/Rocky-*.repo
```
更换科大源。
```
sed -e 's|^mirrorlist=|#mirrorlist=|g' \
    -e 's|^#baseurl=http://dl.rockylinux.org/$contentdir|baseurl=https://mirrors.ustc.edu.cn/rocky|g' \
    -i.bak \
    /etc/yum.repos.d/rocky-extras.repo \
    /etc/yum.repos.d/rocky.repo
```

```
dnf makecache
```






### Ubuntu


### openSUSE
















