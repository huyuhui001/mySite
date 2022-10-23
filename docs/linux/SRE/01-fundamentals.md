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

!!! reference

    bash可识别的转义序列有下面这些：

    * `\u` : 当前用户的账号名称
    * `\h` : 主机名第一部分
    * `\H` : 完整的主机名称
    * `\w` : 完整的工作目录名称（如 "/home/username/mywork"）
    * `\W` : 当前工作目录的"基名 (basename)"（如 "mywork")
    * `\t` : 显示时间为24小时格式，如：HH:MM:SS
    * `\T` : 显示时间为12小时格式
    * `\A` : 显示时间为24小时格式：HH:MM
    * `\@` : 带有 am/pm 的 12 小时制时间
    * `\d` : 代表日期，格式为weekday month date，例如："Mon Aug 1"
    * `\s` : shell 的名称（如 "bash")
    * `\v` : bash的版本（如 2.04）
    * `\V` : bash的版本（包括补丁级别）
    * `\n` : 换行符
    * `\r` : 回车符
    * `\\` : 反斜杠
    * `\a` : ASCII 响铃字符（也可以键入`07`）
    * `\e` : ASCII 转义字符（也可以键入`33`)
    * `\[` : 这个序列应该出现在不移动光标的字符序列（如颜色转义序列）之前。它使bash能够正确计算自动换行
    * `\]` : 这个序列应该出现在非打印字符序列之后
    * `\#` : 下达的第几个命令
    * `\$` : 提示字符，如果是root用户，提示符为`#` ，普通用户则为`$`


在PS1中设置字符颜色的格式为：`[\e[F;Bm]........[\e[0m]`，其中`[\e[0m]`作为颜色设定的结束。
其中"F"为字体颜色，编号为30-37，"B"为背景颜色，编号为40-47。

!!! info
    颜色对照表:

    * F:30 , B:40 : 黑色
    * F:31 , B:41 : 红色
    * F:32 , B:42 : 绿色
    * F:33 , B:43 : 黄色
    * F:34 , B:44 : 蓝色
    * F:35 , B:45 : 紫红色
    * F:36 , B:46 : 青蓝色
    * F:37 , B:47 : 白色

以下面的PS1设定为例说明颜色设定。
```
PS1="\[\e[37;40m\][\[\e[32;40m\]\u\[\e[37;40m\]@\h:\[\e[36;40m\]\w\[\e[0m\]]\$ "
```
拆解分析：
```
PS1="
  \[\e[37;40m\]  # 整个提示符区域前景白色，背景黑色
  [              # 显示字符[
  \[\e[32;40m\]  # 修饰后面的\u，前景绿色，背景黑色
  \u             # 显示当前用户的账号名称
  \[\e[37;40m\]  # 修饰后面的字符@和主机名
  @              # 显示字符@
  \h             # 显示主机名
  :              # 显示字符:
  \[\e[36;40m\]  # 修饰后面的\w，前景青蓝色，背景黑色
  \w             # 显示完整工作目录
  \[\e[0m\]      # 结束颜色设定
  ]              # 显示字符]
  \$"            # 如果是root用户，提示符为# ，普通用户则为$
```

对不同主机做不同设置：
```
# Rocky
PS1="\[\e[37;40m\][\[\e[32;40m\]\u\[\e[37;40m\]@\h:\[\e[36;40m\]\w\[\e[0m\]]\$ "

# Ubuntu
PS1="\[\e[37;40m\][\[\e[32;40m\]\u\[\e[33;40m\]@\h:\[\e[36;40m\]\w\[\e[0m\]]\$ "

# openSUSE
PS1="\[\e[37;40m\][\[\e[32;40m\]\u\[\e[35;40m\]@\h:\[\e[36;40m\]\w\[\e[0m\]]\$ "
```

将上述PS1的设定，追加到当前用户的`~/.bashrc`文件末尾，以实现对当前用户的提示符风格做持久保存。



### Linux的内外部命令

*内部命令* (internal command)实际上是shell程序的一部分，包含的是一些比较简单的linux系统命令，这些命令由shell程序识别并在shell程序内部完成运行，通常在linux系统加载运行时shell就被加载并驻留在系统内存中。

*外部命令* (external command)是linux系统中的实用程序部分，系统加载时并不随系统一起被加载到内存中，而是在需要时才将其调用内存。通常外部命令的实体并不包含在shell中，但是其命令执行过程是由shell程序控制的。

比如：

执行命令`type -t cp`，系统返回结果是`file`，外部命令。

执行命令`type -t cd`，系统返回结果`builtin`，内部命令。

执行命令`enable -a cp`，系统返回`-bash: enable: cp: not a shell builtin`，也可以判断是否为内部命令。

对于内部命令，可以通过enable命令来启用或者禁用。
```
# 禁用cd命令
enable -n cd

# 查看所有被禁用的命令
enable -n

# 启用cd命令
enable cd
```

对于命令，可以通过`whereis`命令来查看路径。
```
whereis cp
whereis cd
```






