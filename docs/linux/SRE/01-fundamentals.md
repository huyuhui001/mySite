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



### CPU信息

```
lscpu
cat /proc/cpuinfo
```

### 内存使用状态

```
free
cat /proc/meminfo
```

### 硬盘和分区情况

```
lsblk
```

openSUSE在VMWare默认安装的状态：
```
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
sda      8:0    0  200G  0 disk 
├─sda1   8:1    0    8M  0 part 
├─sda2   8:2    0  198G  0 part /home
│                               /var
│                               /opt
│                               /usr/local
│                               /root
│                               /tmp
│                               /srv
│                               /boot/grub2/x86_64-efi
│                               /boot/grub2/i386-pc
│                               /.snapshots
│                               /
└─sda3   8:3    0    2G  0 part [SWAP]
sr0     11:0    1  3.8G  0 rom 
```

Ubuntu在VMWare默认安装的状态：
```
NAME                      MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
loop0                       7:0    0 61.9M  1 loop /snap/core20/1405
loop1                       7:1    0 63.2M  1 loop /snap/core20/1623
loop2                       7:2    0 79.9M  1 loop /snap/lxd/22923
loop3                       7:3    0   48M  1 loop /snap/snapd/17029
loop4                       7:4    0  103M  1 loop /snap/lxd/23541
loop5                       7:5    0   48M  1 loop /snap/snapd/17336
sda                         8:0    0   50G  0 disk 
├─sda1                      8:1    0    1M  0 part 
├─sda2                      8:2    0    2G  0 part /boot
└─sda3                      8:3    0   48G  0 part 
  └─ubuntu--vg-ubuntu--lv 253:0    0   24G  0 lvm  /
sr0                        11:0    1  1.4G  0 rom 
```

Rocky在VMWare默认安装的状态：
```
NAME        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
sda           8:0    0   50G  0 disk 
├─sda1        8:1    0    1G  0 part /boot
└─sda2        8:2    0   49G  0 part 
  ├─rl-root 253:0    0 45.1G  0 lvm  /
  └─rl-swap 253:1    0  3.9G  0 lvm  [SWAP]
sr0          11:0    1  7.9G  0 rom
```


### 系统架构信息

```
arch
```
openSUSE，Ubuntu和Rocky的返回结果都是`x86_64`。


### 内核版本

```
uname -r
```
三个发行版返回的结果不尽相同：
```
# openSUSE
5.14.21-150400.24.21-default

# Ubuntu
5.15.0-52-generic

# Rocky
5.14.0-70.17.1.el9_0.x86_64
```


### 操作系统版本

```
cat /etc/os-release
cat /etc/issue

# Rocky 9
sudo cat /etc/redhat-release
```
```
lsb-release -a
lsb_release -cs
lsb_release -is
lsb_release -rs
```

在openSUSE中，需要安装`lsb-release`包。执行`lsb-release -a`和`lsb_release -a`返回的结果是一样的。
```
sudo zypper in lsb-release
```

在Ubuntu中，需要安装`lsb-release`包。只能执行`lsb_release -a`。
```
sudo apt install lsb-release
```

在Rocky 9中，找不到`lsb-release`相关的包。


### 日期和时间

显示默认格式的当前日期。
```
date
```
三个系统的默认日期格式略有不同。
```
# openSUSE
Mon 24 Oct 2022 09:28:06 AM CST

# Ubuntu
Mon Oct 24 01:28:09 AM UTC 2022

# Rocky
Mon Oct 24 09:24:01 AM CST 2022
```

显示自1970-01-01 00:00:00 UTC到当前的秒数。
```
date +%s
```

将上一命令中的描述转换为系统默认日期格式。
```
date -d @`date +%s`
date --date=@'1666575347'
```


显示硬件时钟。

`hwclock` 也被称为 Real Time Clock (RTC)。

在Rocky9中，`clock`有一个软连接指向`hwclock`：`/usr/sbin/clock -> hwclock`。在openSUSE和Ubuntu中只有`hwclock`。
```
ll /usr/sbin/clock
ll /usr/sbin/hwclock
```

读取RTC时间。
```
sudo hwclock --get
sudo hwclock -r
```

校准时间：

* `-s, –hctosys` : 以RTC硬件时间来校准系统时间。
* `-w, –systohoc` : 以系统时间来校准RTC硬件时间。


显示当前系统时区。
```
ll /etc/localtime
```
系统可能会返回不同结果，例如：
```
/etc/localtime -> /usr/share/zoneinfo/Asia/Shanghai
/etc/localtime -> /usr/share/zoneinfo/Etc/UTC
```

显示当前可以时区列表。
```
timedatectl list-timezones
timedatectl list-timezones | grep -i Asia
```

修改当前系统时区。
```
sudo timedatectl set-timezone Asia/Shanghai
```

显示日历。
```
cal -y
```
openSUSE和Rocky中，使用`cal`命令需要安装`util-linux`包。
Ubuntu中，使用`cal`命令需要安装`ncal`包。

```
sudo apt install ncal

sudo zypper se util-linux
sudo yum install util-linux
```



### 用户登录信息


* `whoami`：当前登录用户
* `who`：系统当前所有的登录会话
* `w`：系统当前所有的登录会话及所作的操作

MOTD is the abbreviation of "Message Of The Day", and it is used to display a message when a remote user login to the Linux Operating system using SSH. Linux administrators often need to display different messages on the login of the user, like displaying custom information about the server or any necessary information. 

编辑文件`/etc/motd`可以自定义"Message Of The Day"的信息。

Ubuntu 2204新安装后没有这个文件，需要自己创建。
openSUSE新安装后有预定义的信息。
Rocky9 新安装后有该文件，空白文件无内容。


### 会话管理工具

`screen`工具

* `screen -S <your_name>`  (Create new screen session)
* `screen -ls`             (list current screen sessions)
* `screen -x <your_name>`  (Attach to existing screeen session, sync between both)
* `screen -r <your_name>`  (Reattach existing screen session)


`tmux`工具

`tmux` 是指 *Terminal Multiplexer*.

安装`tmux`工具。
```
# Rocky
sudo yum install tmux

# Ubuntu
sudo apt install tmux

# openSUSE
sudo zypper in tmux
```

常用方法：

* `tmux new -s <your_name>`     (Create new session)
* `tmux detach`                 (Detach current session)
* `tmux ls`                     (list current sessions)
* `tmux attach -t <your_name>`  (Reattach existing session)
* `tmux switch -t <your_name>`  (Switch to another session)
* `tmux kill-session -t <your_name>`  (Kill existing session)
* `tmux list-keys`              (List all short keys)
* `tmux list-commands`          (List commands and parameters)
* `tmux info`                   (List all sessions info)
* `tmux split-window`           (Split window)



### `echo`命令

`echo`命令中可以输出变量，如果变量是用是单引号引起来，表示这个变量不用IFS替换！！

* `echo "Home=$HOME"`的输出结果是`Home=/home/vagrant`
* `echo 'Home=$HOME'`的输出结果是`Home=$HOME`


`echo -e`启用`\`字符的解释功能，比如：
* `echo -e "a\x0Ab"`，输出字符`a`和`b`，中间`\x0A`代表十六进制`OA`（即回车）
* `echo -e "\x4A \x41 \x4D \x45 \x53"`，输出结果是`J A M E S`

!!! Tips
    可以通过man 7 ascii来查看各进制的含义。



`echo -e`输出带颜色字符。

示例：

```
echo -e "\e[35m 紫色 \e[0m"
echo -e "\e[43m 黄底 \e[0m"
echo -e "\e[93m 黑底黄字 \e[0m"
```


!!! Reference
    字体颜色：

    * `\e[30m`： 黑色
    * `\e[31m`： 红色
    * `\e[32m`： 绿色
    * `\e[33m`： 黄色
    * `\e[34m`： 蓝色
    * `\e[35m`： 紫色
    * `\e[36m`： 青色
    * `\e[37m`： 白色
    * `\e[40m`： 黑底
    * `\e[41m`： 红底
    * `\e[42m`： 绿底
    * `\e[43m`： 黄底
    * `\e[44m`： 蓝底
    * `\e[45m`： 紫底
    * `\e[46m`： 青底
    * `\e[47m`： 白底

    背景颜色：

    * `\e[90m`： 黑底黑字
    * `\e[91m`： 黑底红字
    * `\e[92m`： 黑底绿字
    * `\e[93m`： 黑底黄字
    * `\e[94m`： 黑底蓝字
    * `\e[95m`： 黑底紫字
    * `\e[96m`： 黑底青字
    * `\e[97m`： 黑底白字

    控制属性：

    * `\e[0m` 关闭所有属性
    * `\e[1m` 设置高亮度
    * `\e[4m` 下划线
    * `\e[5m` 闪烁
    * `\e[7m` 反显，撞色显示，显示为白字黑底，或者显示为黑底白字
    * `\e[8m` 消影，字符颜色将会与背景颜色相同
    * `\e[nA` 光标上移 n 行
    * `\e[nB` 光标下移 n 行
    * `\e[nC` 光标右移 n 行
    * `\e[nD` 光标左移 n 行
    * `\e[y;xH` 设置光标位置
    * `\e[2J` 清屏
    * `\e[K` 清除从光标到行尾的内容
    * `\e[s` 保存光标位置
    * `\e[u` 恢复光标位置
    * `\e[?25` 隐藏光标
    * `\e[?25h` 显示光标


### `man`命令

安装包：
```
# openSUSE
sudo zypper install man-pages man-pages-zh_CN man-pages-posix

# Rocky
sudo yum install man-pages

# Ubuntu
sudo apt install man-db manpages-posix manpages manpages-zh
sudo apt install manpages-dev manpages-posix-dev
```

更新mandb
```
mandb
```

查找某个命令的man信息，例如查找`crontab`命令的信息。
```
# 精确查找
man -f crontab
whatis crontab

# 模糊查询
man -k crontab
apropos crontab
```
输出结果如下：
```
crontab (5)          - files used to schedule the execution of programs
crontab (1)          - maintains crontab files for individual users
crontab (1p)         - schedule periodic background work
```
查找crontab第5章的内容，则可以执行：
```
man 5 crontab
```

常用快捷键示例s：

* `1G` : go to the 1st line
* `10G` : go to the 10th line
* `G` : go to the end of the page
* `/^SELinux` : search the word SELinux
* `/section OPTIONS` : go to the section OPTIONS




### 语言环境LANG

安装语言包。
```
# Ubuntu
sudo apt install locales-all

# Rocky
sudo yum install glibc-langpack-zh.x86_64

# openSUSE
sudo zypper install glibc-locale glibc-locale-32bit glibc-locale-base
```

查看当前语言设置：
```
echo $LANG

locale -a
locale -k LC_TIME

localectl status
localectl list-locales
```

全局locale配置(Global locale settings)。
```
# openSUSE & Rocky
sudo cat /etc/locale.conf

# Ubuntu
sudo cat /etc/default/locale
```

临时修改当前session的locale。
```
LANG="zh_CN.utf8" 
```

永久修改locale设置。
```
sudo localectl set-locale LANG=zh_CN.utf8
```

修改回原设置。
```
sudo localectl set-locale LANG=en_US.utf8
```


### 符号`$`用法

符号`$`的用法：

* `$`，获取变零值。
```
x=1
echo $x
echo "$x"
```

建议使用"$x"，以避免shell编程中产生歧义。如下例：
```
s="this is a string"
echo $s
echo "this is a string"
```
执行`[ $s == "this is a string" ]`会报错，这是实际生成的比较式`this is a string == "this is a string"`。
我们预期的是`"this is a string" == "this is a string"`，所以需要改成`[ "$s" == "this is a string" ]`。


* `$0`, `$1`, `$n`, `$#`：

生成一个测试脚本。
```
echo 'echo $0 $1 $2 $#' > test.sh
chmod 755 test.sh
```

验证各个参数位置。
```
./test.sh a b c d e
```
输出结果：
```
./test.sh a b 5
```

结论：

* `$0`输出脚本文件名；
* `$1`输出第一个参数；
* `$2`输出第二个参数；
* `$#`输出参数个数。


* `${}`

`${}`用于区分变量的边界。

下面例子中，`$abc`无结果输出，`${a}bc`输出结果`stringbc`，通过{}指定了某个字符属于变量。
```
a="string"
echo ${a}bc
echo $abc
```


* `${#}`

`${#}`是返回变量值的长度。
```
s='this is a string'
echo "$s"
echo "${#s}"
```
命令`echo "${#s}"`输出结果是字串`this is a string`的长度`16`。


* `$?`

`$?`是返回上一命令是否成功的状态，`0`代表成功，非零代表失败。

`ls`是一个命令，所以返回值是`0`。`tom`是一个不存在的命令，则返回`127`。
```
ls
echo $?

tom
echo $?
```

* `$()`

`$()`等同于反引号。`echo $(ls)`等同于执行`ls`命令。

`$()`的弊端是，不是所有的类unix系统都支持，反引号是肯定支持的。

`$()`的优势是直观，在转移处理时，比反引号直观容易些。
```
echo $(ls)
# test.sh

echo $(cat $(ls))
# echo $0 $1 $2 $#
```
上述嵌套格式中，ls命令的输出，是cat命令的输入，可以进行多层嵌套，内层命令的输出是外层命令的输入。


* `$[]`

`$[]`是表达式计算。
```
echo $[3 + 2]
```

* `$-`

`$-`显示shell当前所使用的选项。

执行`echo $-`，输出结果`himBHs`。himBH每一个字符是一个shell的选项。


* `$!`

`$!`获取最后一个运行的后台进程的pid。

比如执行`cat test.sh &`，结果中会包含一个pid号，马上着执行`echo $!`，如果2个命令间隔之间没有其他后台进程执行，则可以得到和前面一致的pid号。

* `!$`

`!$`返回上一条命令的最后一个参数。

执行`./test.sh a b c iamhere`，得到结果`./test.sh a b 4`。
执行`echo !$`，得到2个结果，`echo iamhere`和`iamhere`。


* `!!`

`!!`输出上一条命令，并执行。

`!!`会先输出上一条命令`cat test.sh`，然后再执行这条命令，第二行即执行结果。
```
[vagrant@lizard:~]$ cat test.sh 
echo $0 $1 $2 $#
[vagrant@lizard:~]$ !!
cat test.sh 
echo $0 $1 $2 $#
```

* `$$`

`$$` 输出当前进程的pid。
```
echo $$
```



* `$@` & `$*`

`$@`和`$*`是对传入参数的不同体现，`$@`是以变量形式引用传入参数，`$*`是以数组的形式引用传入参数。

创建一个文件`script.sh`包含下面的脚本。并添加执行权限`chmod 755 script.sh`。
```
echo '$@以变量方式引用传入参数：'

for x in "$@"
do
  echo $x
done

echo '$*以数组的形式引用传入参数：'

for x in "$*"
do
  echo $x
done
```
输出结果：
```
$@以变量方式引用传入参数：
a
b
3
5
d
$*以数组的形式引用传入参数：
a b 3 5 d
```



## 文件系统

文件系统层次标准（Filesystem Hierarchy Standard, FHS），它是Linux 标准库（Linux Standards Base, LSB）规范的一部分。

根目录`/`指文件系统树的最高层。 根分区在系统启动时首先挂载。
系统启动时运行的所有程序都必须在此分区中。

### 主要目录

以下目录必须在根分区中：

* `/bin` - 用户基本程序。
    * 包含未挂载其他文件系统时所需的可执行文件。 例如，系统启动、处理文件和配置所需的程序。
    * `/bin/bash` - `bash`脚本处理
    * `/bin/cat` - 显示文件内容
    * `/bin/cp` - 拷贝文件
    * `/bin/dd` - 拷贝文件（基于字节byte）
    * `/bin/gzip` - 压缩文件
    * `/bin/mount` - 挂载文件系统
    * `/bin/rm` - 删除文件
    * `/bin/vi` - 文件编辑
* `/sbin` - 系统基本程序。
	* 包含基本系统管理的程序。
	* 默认是root用户有权限执行，因此它不在常规用户路径中。 
	* 一些重要管理程序：
	    * `/sbin/fdisk*` - 管理硬盘分区
	    * `/sbin/fsck*` - 文件系统检查。不能在运行的系统上面直接执行`fsck`，损坏根文件系统，执行前需要`umount`。
	    * `/sbin/mkfs` - 创建文件系统
	    * `/sbin/shutdown` - 关闭系统
* `/dev` - 设备文件
	* 以太网卡是内核模块，其他硬件都以设备dev的方式展现。
	* 应用程序读取和写入这些文件以操作使用硬件组件。
	* 两种类型设备文件：
		* 字符设备（Character-oriented）– 序列设备（打印机，磁带机，鼠标等） 
		* 块设备（Block-oriented）– 硬盘，DVD等 
	* 与设备驱动程序的连接通过内核中称为主设备号的通道实现。
	* 过去，这些文件是使用`mknod`命令手动创建的。 现在当内核发现设备时，它们会由`udev`自动创建。
	* 一些重要的设备文件：
		* Null设备: - `/dev/null`
		* Zero设备: - `/dev/zero`
		* 系统终端: - `/dev/console`
		* 虚拟终端: - `/dev/tty1`
		* 串行端口 - `/dev/ttyS0`
		* 并行端口: - `/dev/lp0`
		* 软盘驱动器: - `/dev/fd0`
		* 硬盘驱动器: - `/dev/sda`
		* 硬盘分区: - `/dev/sda1`
		* CD-ROM驱动器: - `/dev/scd0`
* `/etc` - 配置文件
	* 存放系统和服务的配置文件。
	* 大部分都是ASCII文件
	* 普通用户可以默认读取其中的大部分内容。 这会带来一个潜在的全问题，因为其中一些文件包含密码，因此重要的是要确保这些文件只能由root用户读取。
	* 根据FHS标准，此处不能放置任何可执行文件，但子目录可能包含shell脚本。
	* 几乎每个已安装的服务在`/etc`或其子目录中至少有一个配置文件。
	* 一些重要的配置文件:
	    * `/etc/os-release` - 系统版本信息
	    * `/etc/DIR_COLORS` - `ls`命令中的颜色配置信息（openSUSE和Rocky）
	    * `/etc/fstab` - 配置要挂载的文件系统
	    * `/etc/profile` - Shell登录脚本
	    * `/etc/passwd` - 用户信息集合（不含密码）
	    * `/etc/shadow` - 密码和相关信息
	    * `/etc/group` - 用户组信息集合
	    * `/etc/cups/*` - 用于CUPS打印系统（CUPS=Common UNIX Printing System）
	    * `/etc/hosts` - 主机名机器IP地址
	    * `/etc/motd` - 登录后显示的欢迎信息
	    * `/etc/issue` - 登录前显示的欢迎信息
	    * `/etc/sysconfig/*` - 系统配置文件
* `/lib` - 库（Libraries）
	* 许多程序都具有一些通用功能。 这些通用功能可以保存在共享库中。
	* 共享库中文件的扩展名是`.so`。 
	* 目录`/lib`包含的共享库文件主要是被`/bin`和`/sbin`目录包含的程序所调用。 
	* 目录`/lib`的子目录包含一些额外需要的共享库。 
	* 内核模块存储在目录`/lib/modules`。
* `/lib64` - 64位共享库（64-Bit Libraries），类似目录`/lib`。 
	* 这个目录因系统架构不同而不同。 
	* 一些系统支持不同的二进制格式并保留同一个共享库的不同版本。
* `/usr` - 包含应用程序、图形界面文件、库、本地程序、文档等。
	* `/usr` 即 Unix System Resources. 例如：
	* `/usr/X11R6/` - X Window 系统文件
	* `/usr/bin/` - 几乎包含所有可执行文件
	* `/usr/lib/` - 包含库和应用程序
	* `/usr/local/` - 包含本地安装程序。这个目录下的内容不会被系统升级所覆盖。下面3个目录在初始安装后是空的。
		* `/usr/local/bin`- 
		* `/usr/local/sbin`- 
		* `/usr/local/lib`- 
	* `/usr/sbin/` - 系统管理程序
	* `/usr/share/doc/` - 文档
	* `/usr/src/` - 内核和应用程序的源代码
		* `/usr/src/linux`- 
	* `/usr/share/man/` - `man`命令使用的内容
* `/opt` - 可选应用程序目录
	* 各发行版包含的应用程序一般存储在目录`/usr/lib/`，各发行版可选程序，或第三方应用程序则存储在目录`/opt`. 
	* 在安装时，会为每个应用程序的文件创建一个目录，其中包含应用程序的名称。比如：
	    * `/opt/novell`- 
* `/boot` - 引导目录
	* `/boot/grub2` - 包含 GRUB2 的静态引导加载程序文件。（GRUB = Grand Unified Boot Loader）
	* 包含以链接 vmlinuz 和 initrd 标识的内核和 initrd 文件。
* `/root` - 管理员的主目录（home directory）。
	* `root`用户的主目录。其他用户的主目录是在目录`/home`下。
	* `root`用户的登录环境配置保存至`/root`分区中。
* `/home` - 用户主目录
	* 每个系统用户都有一个分配的文件区域，该文件区域在登录后成为当前工作目录。 默认情况下，它们存在于`/home`中。
	* `/home`中的文件和目录可以位于单独的分区中，也可以位于网络上的另一台计算机上。
	* 用户配置信息和配置文件（user profile and configuration files）主要有：
	    * .profile - 用户私有登录脚本
	    * .bashrc - `bash`的配置文件
	    * .bash_history - `bash`环境下保持命令历史记录
* `/run/media/<user>/*` - 可移动设备的挂载点，例如：
	  * `/run/media/media_name/`
	  * `/run/media/cdrom/`- 
	  * `/run/media/dvd/`- 
	  * `/run/media/usbdisk/`- 
* `/mnt` - 文件系统临时挂载点
	* 用于挂载临时使用的文件系统的目录。
	* 文件系统使用 mount 命令挂载，使用 umount 命令删除。
	* 子目录默认不存在，也不会自动创建。
* `/srv` - 服务数据目录
	* 存放各种服务的数据，比如：
	    * `/srv/www` - 用于存放 Apache Web Server 的数据
	    * `/srv/ftp` - 用于存放 FTP server 的数据
* `/var` - 可变文件（Variable Files）
	* 在系统运行过程中会被修改的文件
	* Important subdirectories:
	    * `/var/lib/` - 可变库文件
	    * `/var/log/` - 日志文件
	    * `/var/run/` - 运行中的线程的信息
	    * `/var/spool/` - 对列（打印机，邮件）
	    	* `/var/spool/mail`- 
	    	* `/var/spool/cron`- 
	    * `/var/lock/` - 多用户访问锁文件
	    * `/var/cache`- 
	    * `/var/mail`- 
* `/tmp` - 临时文件
	* 程序在运行时创建临时文件的位置
* `/proc` - 进程文件
	* 虚拟文件系统，不占空间，大小始终为零，保持当前进程的状态信息
	* 包含有关各个进程的信息的目录，根据进程的 PID 号命名。
	* 有些值可以临时在线更改生效，但重启后丢失
	    * `/proc/cpuinfo/` - Processor information
	    * `/proc/dma/` - Use of DMA ports
	    * `/proc/interrupts/` - Use of interrupts
	    * `/proc/ioports/` - Use of I/O ports
	    * `/proc/filesystems/` - File system formats the kernel knows
	    * `/proc/modules/` - Active modules
	    * `/proc/mounts/` - Mounted file systems
	    * `/proc/net/*` - Network information and statistics
	    * `/proc/partitions/` - Existing partitions
	    * `/proc/bus/pci/` - Connected PCI devices
	    * `/proc/bus/scsi/` - Connected SCSI devices
	    * `/proc/sys/*` - System and kernel information
	    * `/proc/version` - Kernel version
* `/sys` - 系统信息目录
	* 虚拟文件系统，仅存在于内存中，文件大小为零。主要提供如下信息：
	  - 硬件总线（hardware buses）
	  - 硬件设备（hardware devices）
	  - 有源设备（active devices）
	  - 驱动程序（drivers）


### 七种不同类型的文件

* 普通文件（Normal Files）
  * ASCII 文本文件
  * 可执行文件
  * 图形文件
* 目录（Directories）
  * 组织规划磁盘上的文件
  * 包含文件和子目录
  * 实现分层文件系统
* 链接（Links）
  * 硬链接（Hard links）
       * 磁盘上文件的辅助文件名
       * 多个文件名引用单个`inode`
       * 引用的文件必须存在于同一个文件系统中
  * 符号链接（Symbolic links）
       * 对磁盘上其他文件的引用
       * `inode`包含对另一个文件名的引用
       * 被引用的文件可以存在于同一个文件系统中，也可以存在于其他文件系统中
       * 符号链接可以引用不存在的文件（断开的链接）
* 套接字Sockets - 用于进程之间的双向通信。
* 管道（Pipes）(FIFOs) - 用于从一个进程到另一个进程的单向通信。
* 块设备（Block Devices）
* 字符设备（Character Devices）


#### 链接类型 

**硬链接**（Hard links）硬链接是存储卷上文件的目录引用或指针。 文件名是存储在目录结构中的标签，目录结构指向文件数据。 因此，可以将多个文件名与同一文件关联。 通过不同的文件名访问时，所做的任何更改都是针对源文件数据。

**符合链接**（Symbolic links）: 符号链接包含一个文本字符串，操作系统将其解释并作为另一个文件或目录的路径。 它本身就是一个文件，可以独立于目标而存在。 如果删除了符号链接，则其目标文件或目录不受影响。 如果移动，重命名或删除目标文件或目录，则用于指向它的任何符号链接将继续存在，但指向的是现在不存在的文件。

仅当文件和链接文件位于同一文件系统（在同一分区上）时，才能使用硬链接，因为inode编号在同一文件系统中仅是唯一的。 可以使用`ln`命令创建硬链接，`ln`命令指向已存在文件的inode。 以后可以在文件的名称和链接的名称下访问文件，并且无法再识别首先存在的名称或原始文件和链接的不同之处。 

可以使用`ln`命令和`-s`选项创建符号链接。 一个符号链接被分配了它自己的inode，一个链接指向一个文件，所以总是可以区分链接和实际文件。 
 
文件系统本质上是一个用于跟踪分区卷中的文件的数据库。 对于普通文件，分配数据块以存储文件的数据，分配inode以指向数据块以及存储关于文件的元数据，然后将文件名分配给inode。 硬链接是与现有inode关联的辅助文件名。 对于符号链接，将为新的inode分配一个与之关联的新文件名，但inode引用另一个文件名而不是引用数据块。

查看文件名和inode之间关系的一个方法是使用`ls -il`命令。inode的典型大小为128位，数据块的大小范围可以是1k，2k，4k或更大，具体取决于文件系统类型。

软连接可以针对目录，硬连接只能针对文件。
	
硬链接相当于增加了一个登记项，使得原来的文件多了一个名字，至于inode都没变。所谓的登记项其实是目录文件中的一个条目(目录项)，使用hard link 是让多个不同的目录项指向同一个文件的inode，没有多余的内容需要存储在磁盘扇区中，所以hardlink不占用额外的空间。

符号链接有单独的inode，在inode中存放另一个文件的路径而不是文件数据，所以符号链接会占用额外的空间。


#### 设备文件

**设备文件**（Device File）表示硬件（网卡除外）。 每个硬件都由一个设备文件表示。 网卡是接口。

设备文件把内核驱动和物理硬件设备连接起来。
内核驱动程序通过对设备文件进行读写（正确的格式）来实现对硬件的读写。

类型：

* 块设备（Block Devices）：块设备（通常）在512字节的大块中读取/写入信息。
* 字符设备（Character Devices）：字符设备以字符方式读取/写入信息。 字符设备直接提供对硬件设备的无缓冲访问。
  * 有时称为裸设备（raw devices）。（注意：裸设备被视为字符设备，不是块设备）
  * 通过辅以不同选项，可以广泛而多样地应用和使用字符设备。
* 当内核发现设备时由操作系统`udev`自动创建。


#### 练习

以Rocky 9为例。

创建练习目录。
```
mkdir data
mkdir -p data/typelink
cd data
```

创建硬链接。注意：`file`、`hardlinkfile1`、`hardlinkfile2` 文件的链接位置的数值的变化)
```
echo "it's original file" > file
ln file hardlinkfile1
ln -s file symlinkfile1
ln -s file symlinkfile2
```
执行`ls -l`命令可以得到下面的结果：
```
-rw-r--r--. 2 vagrant wheel 19 Nov  1 10:42 file
-rw-r--r--. 2 vagrant wheel 19 Nov  1 10:42 hardlinkfile1
lrwxrwxrwx. 1 vagrant wheel  4 Nov  1 10:43 symlinkfile1 -> file
lrwxrwxrwx. 1 vagrant wheel  4 Nov  1 10:43 symlinkfile2 -> file
```

创建硬链接。
```
ln file hardlinkfile1
ln file hardlinkfile2
```
执行`ls -l`命令可以得到下面的结果：
```
-rw-r--r--. 3 vagrant wheel  19 Nov  1 10:42 file
-rw-r--r--. 3 vagrant wheel  19 Nov  1 10:42 hardlinkfile1
-rw-r--r--. 3 vagrant wheel  19 Nov  1 10:42 hardlinkfile2
lrwxrwxrwx. 1 vagrant wheel   4 Nov  1 10:43 symlinkfile1 -> file
lrwxrwxrwx. 1 vagrant wheel   4 Nov  1 10:43 symlinkfile2 -> file
```

修改`file`文件的内容。
```
echo "add oneline" >> file
```
通过命令`cat file`查看当前`file`的内容。
```
it's original file
add oneline
```
通过下面的命令，可以看到所以软/硬链接文件内容都更新了，和`file`文件更新后的内容保持一致。
```
cat hardlinkfile1
cat hardlinkfile2
cat symlinkfile1
cat symlinkfile2
```

对文件`symlinkfile1`再创建新的软连接。
```
ln -s symlinkfile1 symlinkfile1-1
```

通过命令`ls -il`查看现在的目录信息。
```
67274680 -rw-r--r--. 3 vagrant wheel 31 Nov  1 11:14 file
67274680 -rw-r--r--. 3 vagrant wheel 31 Nov  1 11:14 hardlinkfile1
67274680 -rw-r--r--. 3 vagrant wheel 31 Nov  1 11:14 hardlinkfile2
67274681 lrwxrwxrwx. 1 vagrant wheel  4 Nov  1 10:43 symlinkfile1 -> file
67274683 lrwxrwxrwx. 1 vagrant wheel 12 Nov  1 11:20 symlinkfile1-1 -> symlinkfile1
67274682 lrwxrwxrwx. 1 vagrant wheel  4 Nov  1 10:43 symlinkfile2 -> file
```

读取软链接文件的源文件信息
```
readlink symlinkfile1
readlink symlinkfile2
```

注意，对于`symlinkfile1-1`的情况有些不同。
```
readlink symlinkfile1-1
```
上面命令返回结果`symlinkfile1`仍然是一个符号链接文件。通过`readlink -f`可以直接定位真正的源文件。
```
readlink -f symlinkfile1-1
```
上面的返回结果`/data/linktype/file`是`symlinkfile1-1`真正的源文件。


显示`data`目录下的文件和子目录：
```
cd ~
tree ./data
```
运行结果：
```
./data
├── file
├── hardlinkfile1
├── hardlinkfile2
├── symlinkfile1 -> file
├── symlinkfile1-1 -> symlinkfile1
├── symlinkfile2 -> file
└── typelink
```

只显示`data`目录下的子目录：
```
tree -d ./data
```
运行结果：
```
./data
└── typelink
```

显示`data`目录下的文件和子目录，包含全目录：
```
tree -f ./data
```
运行结果：
```
./data
├── ./data/file
├── ./data/hardlinkfile1
├── ./data/hardlinkfile2
├── ./data/symlinkfile1 -> file
├── ./data/symlinkfile1-1 -> symlinkfile1
├── ./data/symlinkfile2 -> file
└── ./data/typelink
```



















