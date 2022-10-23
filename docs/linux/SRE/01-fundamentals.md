# Linux 基础

## 系统环境

### Rocky

使用版本：`Rocky 9.0`。

从网站下载Rocky系统ISO镜像：
```
https://www.rockylinux.org/download/
```

通过`wget`命令下载Rocky系统ISO镜像。
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

刷新缓存。
```
dnf makecache
```






### Ubuntu

使用版本：`Ubuntu 2204`。

设定root用户的密码。
```
sudo passwd root
```

通过安装时已创建的用户`vagrant`登录。执行下面命令修改`sudo`权限。
```
sudo visudo
```
添加`vagrant`到特权用户（Rocky和openSUSE不需要添加），并激活sudo一行（不设密码，方便练习）：
```
# User privilege specification
root    ALL=(ALL:ALL) ALL
vagrant ALL=(ALL:ALL) ALL

# Allow members of group sudo to execute any command
sudo    ALL=(ALL:ALL) NOPASSWD: ALL
```

修改用户`vagrant`的主要组为`sudo`。
```
sudo usermod -g sudo vagrant
```

修改主机名和别名。
```
sudo hostnamectl set-hostname ubuntu2204
sudo hostnamectl set-hostname ubuntu2204 --pretty
```


!!! Tips
    如何处理`Username is not in the sudoers file. This incident will be reported`问题。

    如果没有初始化`root`用户的密码，且当前用户也无法执行`sudo`命令，可以通过下面步骤通过recovery救援模式进行恢复。

    * 按`shift`键开机，进入grub启动菜单。（VMWare也适用）
    * 向下移动高亮条，选择菜单`Advanced options for Ubuntu`，并确认回车。
    * 选择带有`recovery mode`的内核，确认回车。
    * 向下移动高亮条，选择菜单`root   Drop to root shell prompt`，并确认回车。
    * 回车确认`press Enter for maintenance`。
    * 出现`root`的命令提示符后，执行命令`mount -o rw,remount /`。
    * 执行命令`passwd`给`root`设定密码。
    * 执行命令`adduser username sudo`把指定用户加入`sudo`组。
    * 执行命令`visudo`进行必要的修正或修改。







### openSUSE

使用版本：`Leap 15.4`。

选择服务器模式安装，无图形界面。安装中不创建用户。

创建用户`vagrant`，并设置`wheel`为主要组。
```
useradd -m -g wheel -G root -c "vagrant" vagrant
passwd vagrant
```

执行`visudo`命令，激活下面一行，添加`sudo`权限。
```
%wheel ALL=(ALL) NOPASSWD: ALL
```

修改主机名和别名。
```
sudo hostnamectl set-hostname lizard
sudo hostnamectl set-hostname lizard --pretty
```








## 常用命令

!!! info
    默认当前操作用户为`vagrant`。


### 修改提示符风格

bash可识别的转义序列有下面这些：

* `\u` 用户名
* `\h` 主机名第一部分
* `\H` 主机名全称
* `\w` 当前工作目录（如 "/home/username/mywork"）
* `\W` 当前工作目录的"基名 (basename)"（如 "mywork")
* `\t` 24 小时制时间
* `\T` 12 小时制时间
* `\@` 带有 am/pm 的 12 小时制时间
* `\d` "Sat Dec 18" 格式的日期
* `\s` shell 的名称（如 "bash")
* `\v` bash 的版本（如 2.04）
* `\V` Bash 版本（包括补丁级别）
* `\n` 换行符
* `\r` 回车符
* `\\` 反斜杠
* `\a` ASCII 响铃字符（也可以键入 07）
* `\e` ASCII 转义字符（也可以键入 33)
* `\[` 这个序列应该出现在不移动光标的字符序列（如颜色转义序列）之前。它使 bash 能够正确计算自动换行。
* `\]` 这个序列应该出现在非打印字符序列之后。




执行下面命令可以看到当前系统的命令提示符格式。
```
echo $PS1
```
各系统设置是有差异的。
```
# Rocky
[\u@\h \W]\$

# Ubuntu
\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$

# openSUSE
\u@\h:\w>
```


PS1="\[\e[1;35m\]\u@\h:\w>"
PS1="\[\e[1;35m\]\u@\h:\w>"





