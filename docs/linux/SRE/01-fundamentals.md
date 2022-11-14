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
各系统默认设置是有差异的。
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




### `tr`命令

`tr`命令可以对来自标准输入的字符进行替换、压缩和删除。它可以将一组字符变成另一组字符。

格式：`tr [OPTION]... SET1 [SET2]`

举例：
```
# 将输入字符由大写转换为小写
$ echo "HELLO WORLD" | tr 'A-Z' 'a-z'
hello world

# 删除出现的数字
$ echo "HELLO 1234 WORLD 4567" | tr -d '0-9'
HELLO  WORLD

# 从输入文本中将不在补集中的所有字符删除（只保留数字1，2，3，4，5）
$ echo "HELLO 1234 WORLD 4567" | tr -d -c '1-5'
123445

# 将连续重复的字符以单独一个字符表示
$ echo "HELLOOO 1222235555555554" | tr -s 'O215'
HELLO 12354

# 删除由于Windows文件造成的'^M'字符
$ cat file.txt | tr -s '\r' '\n' > new.txt
$ cat file.txt | tr -d '\r' > new.txt

# 将换行符替换成制表符
$ cat file.txt | tr '\n' '\t' > new.txt

# 将大写字母转换为小写字母
$ echo "HELLO 1234 WORLD 4567" | tr '[:upper:]' '[:lower:]'
hello 1234 world 4567

```




### `tee`命令

`tee`命令基于标准输入读取数据，标准输出或文件写入数据。

举例：
```
# ping命令的输出，不仅输出到屏幕，也同时写入文件output.txt中（覆盖式写入）。
$ ping www.baidu.com | tee output.txt

# ping命令的输出，不仅输出到屏幕，也同时写入文件output.txt中（追加式写入）。
$ ping www.baidu.com | tee -a output.txt

# ping命令的输出，不仅输出到屏幕，也同时写入多个文件中（覆盖式写入）。
$ ping www.baidu.com | tee output1.txt output2.txt output3.txt

# ls命令的输出写入文件output.txt中，并作为wc命令的输入。
$ ls *.txt | tee output.txt | wc -l
4
# cat output.txt
f1.txt
f2.txt
output.txt
test.txt
```

技巧：在vi使用中，通过`tee`命令提升文件写入权限。

比如非root用户执行`vi /etc/hosts`，在vi中使用`:w !sudo tee %`可以提高权限保存这个文件。




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

!!! Tips
    Mac OS ssh登陆Linux是终端提示`/usr/bin/manpath: can't set the locale; make sure $LC_* and $LANG are correct`

    解决方法：在本地mac电脑上修改/etc/ssh/ssh_config或者/etc/ssh/ssh_config文件，删除掉或者注释掉以下配置内容：

    `#    SendEnv LANG LC_*`

    如果使用的是`Iterm2`，可以打开`iterm2`的`preferences` -> `Profiles` -> `Terminal`菜单里关闭`Set locale variables automatically`选项。




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
    * 不能关联到独立分区，操作系统启动即会调用的程序。
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
    * 不能关联到独立分区，操作系统启动即会调用的程序
	* 一些重要管理程序：
	    - `/sbin/fdisk*` - 管理硬盘分区
	    - `/sbin/fsck*` - 文件系统检查。不能在运行的系统上面直接执行`fsck`，损坏根文件系统，执行前需要`umount`。
	    - `/sbin/mkfs` - 创建文件系统
	    - `/sbin/shutdown` - 关闭系统
* `/dev` - 设备文件
	* 以太网卡是内核模块，其他硬件都以设备dev的方式展现。
	* 应用程序读取和写入这些文件以操作使用硬件组件。
	* 两种类型设备文件：
		- 字符设备（Character-oriented）– 序列设备（打印机，磁带机，鼠标等） 
		- 块设备（Block-oriented）– 硬盘，DVD等 
	* 与设备驱动程序的连接通过内核中称为主设备号的通道实现。
	* 过去，这些文件是使用`mknod`命令手动创建的。 现在当内核发现设备时，它们会由`udev`自动创建。
	* 一些重要的设备文件：
		- Null设备: - `/dev/null`
		- Zero设备: - `/dev/zero`
		- 系统终端: - `/dev/console`
		- 虚拟终端: - `/dev/tty1`
		- 串行端口 - `/dev/ttyS0`
		- 并行端口: - `/dev/lp0`
		- 软盘驱动器: - `/dev/fd0`
		- 硬盘驱动器: - `/dev/sda`
		- 硬盘分区: - `/dev/sda1`
		- CD-ROM驱动器: - `/dev/scd0`
* `/etc` - 配置文件
	* 存放系统和服务的配置文件。
	* 大部分都是ASCII文件
	* 普通用户可以默认读取其中的大部分内容。 这会带来一个潜在的全问题，因为其中一些文件包含密码，因此重要的是要确保这些文件只能由root用户读取。
	* 根据FHS标准，此处不能放置任何可执行文件，但子目录可能包含shell脚本。
	* 几乎每个已安装的服务在`/etc`或其子目录中至少有一个配置文件。
	* 一些重要的配置文件:
	    - `/etc/os-release` - 系统版本信息
	    - `/etc/DIR_COLORS` - `ls`命令中的颜色配置信息（openSUSE和Rocky）
	    - `/etc/fstab` - 配置要挂载的文件系统
	    - `/etc/profile` - Shell登录脚本
	    - `/etc/passwd` - 用户信息集合（不含密码）
	    - `/etc/shadow` - 密码和相关信息
	    - `/etc/group` - 用户组信息集合
	    - `/etc/cups/*` - 用于CUPS打印系统（CUPS=Common UNIX Printing System）
	    - `/etc/hosts` - 主机名机器IP地址
	    - `/etc/motd` - 登录后显示的欢迎信息
	    - `/etc/issue` - 登录前显示的欢迎信息
	    - `/etc/sysconfig/*` - 系统配置文件
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
    * `/usr/lib64/` - 包含64位库和应用程序
    * `/usr/include/` - 包含C程序的头文件（head file）
	* `/usr/local/` - 包含本地安装程序。这个目录下的内容不会被系统升级所覆盖。下面3个目录在初始安装后是空的。
		- `/usr/local/bin`- 
		- `/usr/local/sbin`- 
		- `/usr/local/lib`- 
	* `/usr/sbin/` - 系统管理程序
	* `/usr/src/` - 内核和应用程序的源代码
		- `/usr/src/linux`- 
    * `/usr/share/` - 结构化独立数据
        - `/usr/share/doc/` - 文档
	    - `/usr/share/man/` - `man`命令使用的内容
* `/opt` - 第三方应用程序目录
	* 各发行版包含的应用程序一般存储在目录`/usr/lib/`。
    * 各发行版可选程序，或第三方应用程序则存储在目录`/opt`。
	* 在安装时，会为每个应用程序的文件创建一个目录，其中包含应用程序的名称。比如：
	    - `/opt/novell`- 
* `/boot` - 引导目录
	* `/boot/grub2` - 包含GRUB2的静态引导加载程序文件（GRUB = Grand Unified Boot Loader）。
	* 包含以链接 vmlinuz 和 initrd 标识的内核和 initrd 文件。
* `/root` - 管理员的主目录（home directory）。
	* `root`用户的主目录。其他用户的主目录是在目录`/home`下。
	* `root`用户的登录环境配置保存至`/root`分区中。
* `/home` - 用户主目录
	* 每个系统用户都有一个分配的文件区域，该文件区域在登录后成为当前工作目录。 默认情况下，它们存在于`/home`中。
	* `/home`中的文件和目录可以位于单独的分区中，也可以位于网络上的另一台计算机上。
	* 用户配置信息和配置文件（user profile and configuration files）主要有：
	    - .profile - 用户私有登录脚本
	    - .bashrc - `bash`的配置文件
	    - .bash_history - `bash`环境下保持命令历史记录
* `run` - 应用程序状态文件
    * 为应用程序提供了一个标准位置来存储它们需要的临时文件，例如套接字和进程ID。 这些文件不能存储在`/tmp`中，因为`/tmp`中的文件可能会被删除。
    * `/run/media/<user>/*` - 可移动设备的挂载点，例如：
	    - `/run/media/media_name/`
	    - `/run/media/cdrom/`- 
	    - `/run/media/dvd/`- 
	    - `/run/media/usbdisk/`- 
* `/mnt` - 文件系统临时挂载点
	* 用于挂载临时使用的文件系统的目录。
	* 文件系统使用 mount 命令挂载，使用 umount 命令删除。
	* 子目录默认不存在，也不会自动创建。
* `/srv` - 服务数据目录
	* 存放各种服务的数据，比如：
	    - `/srv/www` - 用于存放 Apache Web Server 的数据
	    - `/srv/ftp` - 用于存放 FTP server 的数据
* `/var` - 可变文件（Variable Files）
	* 在系统运行过程中会被修改的文件
	* Important subdirectories:
	    - `/var/lib/` - 可变库文件，应用程序状态信息数据
	    - `/var/log/` - 日志文件
	    - `/var/run/` - 运行中的进程的信息
	    - `/var/lock/` - 多用户访问时的锁文件
	    - `/var/cache`- 应用程序缓存数据目录
        - `/var/opt` - 专为`/opt`下的应用程序存储可变数据
	    - `/var/mail`- 
        - `/var/spool/` - 应用程序数据池，比如：打印机，邮件
	    	* `/var/spool/mail`- 
	    	* `/var/spool/cron`- 
* `/tmp` - 临时文件
	* 程序在运行时创建临时文件的位置
* `/proc` - 进程文件
	* 虚拟文件系统，不占空间，大小始终为零，保持当前进程的状态信息
	* 包含有关各个进程的信息的目录，根据进程的 PID 号命名
	* 有些值可以临时在线更改生效，但重启后丢失
	    - `/proc/cpuinfo/` - Processor information
	    - `/proc/dma/` - Use of DMA ports
	    - `/proc/interrupts/` - Use of interrupts
	    - `/proc/ioports/` - Use of I/O ports
	    - `/proc/filesystems/` - File system formats the kernel knows
	    - `/proc/modules/` - Active modules
	    - `/proc/mounts/` - Mounted file systems
	    - `/proc/net/*` - Network information and statistics
	    - `/proc/partitions/` - Existing partitions
	    - `/proc/bus/pci/` - Connected PCI devices
	    - `/proc/bus/scsi/` - Connected SCSI devices
	    - `/proc/sys/*` - System and kernel information
	    - `/proc/version` - Kernel version
* `/sys` - 系统信息目录
	* 虚拟文件系统，仅存在于内存中，文件大小为零。主要提供如下信息：
	    - 硬件总线（hardware buses）
	    - 硬件设备（hardware devices）
	    - 有源设备（active devices）
	    - 驱动程序（drivers）





### 文件操作命令

#### 显示当前工作目录

pwd命令（print working directory）:

* -L: 显示链接路径
* -P：显示真实物理路径


#### 相对和绝对路径

对于绝对路径`/etc/firewalld/policies`，可以通过下面命令得到该路径的基名`policies`和目录名`/etc/firewalld`。
```
basename /etc/firewalld/policies
dirname /etc/firewalld/policies
```

#### 更改目录

`.`指当前目录，即`pwd`命令所返回的目录。

`..`指当前目录的上一级目录，及当前目录的父目录。

* 切换至父目录：`cd ..`
* 切换至当前用户主目录：`cd ~`
* 切换至上次工作目录：`cd -`

* `echo $PWD`：当前工作目录
* `echo $OLDPWD`：上次工作目录


#### 列出目录内容

`ls`命令：

* `-a` 显示所有文件及目录 (. 开头的隐藏文件也会列出)
* `-A` 同 `-a` ，但不列出 `.` (目前目录) 及 `..` (父目录)
* `-l` 除文件名称外，亦将文件型态、权限、拥有者、文件大小等资讯详细列出
* `-r` 将文件以相反次序显示(原定依英文字母次序)
* `-t` 将文件依建立时间之先后次序列出
* `-F` 在列出的文件名称后加一符号；例如可执行档则加 "*", 目录则加 "/"
* `-R` 递归列出子目录
* `-S` 按文件大小排序，从大到小
* `-1` 按一个文件一行列出
* `-t` 按文件时间排序，最新的在前
* `-U` 不排序输出，按目录存放顺序列出
* `-u` 配合`-lt`，按访问时间排序并显示；配合`-l`，显示访问时间并按名称排序； 否则按访问时间排序，最新的在前
* `-X` 按文件扩展名字母顺序排序输出
* `-F` 对不同类型文件显示时附加不同的符号，`* / = > @ |`之一

`ls`命令查看不同文件是的颜色，由`/etc/DIR_COLORS`和变量`@LS_COLORS`定义。


#### 文件状态stat

每个文件有三个时间戳：

* 访问时间 Access Time `atime` : 读取文件内容。
* 修改时间 Modify Time `mtime` : 改变文件内容（数据）。
* 改变时间 Change Time `ctime` : 元数据发生改变。

读取三个时间戳的命令`stat`：
```
stat /etc/fstab
```
输出结果：
```
  File: /etc/fstab
  Size: 927             Blocks: 8          IO Block: 4096   regular file
Device: 30h/48d Inode: 263         Links: 1
Access: (0644/-rw-r--r--)  Uid: (    0/    root)   Gid: (    0/    root)
Access: 2022-10-31 10:26:34.987466959 +0800
Modify: 2022-06-24 14:50:24.387992912 +0800
Change: 2022-06-24 14:50:24.387992912 +0800
 Birth: 2022-06-24 14:50:23.755992937 +0800
```


#### 确定文件类型

命令`file`检查文件类型。

* `-b`：列出辨识结果时，不显示文件名称。
* `-c`：详细显示指令执行过程，便于排错或分析程序执行的情形。
* `-f <名称文件>`：指定名称文件，其内容有一个或多个文件名称时，让file依序辨识这些文件，格式为每列一个文件名称。
* `-L`： 直接显示符号连接所指向的文件的类别。
* `-v`： 显示版本信息。
* `-z`： 尝试去解读压缩文件的内容。

编辑文件`list.txt`包含一下内容：
```
/etc/
/bin
/etc/issue
```
运行命令`file -f list.txt`，结果如下：
```
/etc/:      directory
/bin:       directory
/etc/issue: symbolic link to ../run/issue
```



#### 文件编码转换

`iconv`命令用于将一种编码中的某些文本转换为另一种编码。 如果没有提供输入文件，则它从标准输入中读取。 同样，如果没有给出输出文件，那么它会写入标准输出。 如果没有提供 `from-encoding` 或 `to-encoding`，则它使用当前本地的字符编码。


将文本从 ISO 8859-15 字符编码转换为 UTF-8，读入`input.txt`，输出`output.txt`。
```
iconv -f ISO-8859-15 -t UTF-8 < input.txt > output.txt
```

从 UTF-8 转换为 ASCII，尽可能进行音译（transliterating）：
```
echo abc ß α € àḃç | iconv -f UTF-8 -t ASCII//TRANSLIT
```
运行结果：
```
abc ss ? EUR abc
```



#### 通配符

通配符，指包含这些字符的字符串

* `?`  ：表示任意一个字符
* `*`  ：表示任意长度的任意字符
* `[]` ：匹配指定范围内任意一个字符
  * `[abcd]`：匹配abcd中的任何一个字符
  * `[a-z]`：匹配范围a到z内任意一个字符
  * `[!abcd]`：不匹配括号里面任何一个字符
* `{}` ：表示生成序列，以逗号分割，不能有空格

示例：
```
$ touch file_{a..z}.txt
$ touch file_{A..Z}.txt

$ ls
file_a.txt  file_C.txt  file_f.txt  file_H.txt  file_k.txt  file_M.txt  file_p.txt  file_R.txt  file_u.txt  file_W.txt  file_z.txt
file_A.txt  file_d.txt  file_F.txt  file_i.txt  file_K.txt  file_n.txt  file_P.txt  file_s.txt  file_U.txt  file_x.txt  file_Z.txt
file_b.txt  file_D.txt  file_g.txt  file_I.txt  file_l.txt  file_N.txt  file_q.txt  file_S.txt  file_v.txt  file_X.txt
file_B.txt  file_e.txt  file_G.txt  file_j.txt  file_L.txt  file_o.txt  file_Q.txt  file_t.txt  file_V.txt  file_y.txt
file_c.txt  file_E.txt  file_h.txt  file_J.txt  file_m.txt  file_O.txt  file_r.txt  file_T.txt  file_w.txt  file_Y.txt

$ ls file_[a..d].*
file_a.txt  file_d.txt
 
$ ls file_[a...d].*
file_a.txt  file_d.txt

$ ls file_[ad].*
file_a.txt  file_d.txt

$ ls file_[a-c].*
file_a.txt  file_A.txt  file_b.txt  file_B.txt  file_c.txt

$ ls file_[a-C].*
file_a.txt  file_A.txt  file_b.txt  file_B.txt  file_c.txt  file_C.txt

$ ls file_[!d-W].*
file_a.txt  file_b.txt  file_c.txt  file_x.txt  file_y.txt  file_z.txt
file_A.txt  file_B.txt  file_C.txt  file_X.txt  file_Y.txt  file_Z.txt
```

比较有无`*`的区别：
```
$ ls -a *
file_a.txt  file_D.txt  file_h.txt  file_K.txt  file_o.txt  file_R.txt  file_v.txt  file_Y.txt
file_A.txt  file_e.txt  file_H.txt  file_l.txt  file_O.txt  file_s.txt  file_V.txt  file_z.txt
file_b.txt  file_E.txt  file_i.txt  file_L.txt  file_p.txt  file_S.txt  file_w.txt  file_Z.txt
file_B.txt  file_f.txt  file_I.txt  file_m.txt  file_P.txt  file_t.txt  file_W.txt
file_c.txt  file_F.txt  file_j.txt  file_M.txt  file_q.txt  file_T.txt  file_x.txt
file_C.txt  file_g.txt  file_J.txt  file_n.txt  file_Q.txt  file_u.txt  file_X.txt
file_d.txt  file_G.txt  file_k.txt  file_N.txt  file_r.txt  file_U.txt  file_y.txt

$ ls -a
.           file_C.txt  file_g.txt  file_J.txt  file_n.txt  file_Q.txt  file_u.txt  file_X.txt
..          file_d.txt  file_G.txt  file_k.txt  file_N.txt  file_r.txt  file_U.txt  file_y.txt
file_a.txt  file_D.txt  file_h.txt  file_K.txt  file_o.txt  file_R.txt  file_v.txt  file_Y.txt
file_A.txt  file_e.txt  file_H.txt  file_l.txt  file_O.txt  file_s.txt  file_V.txt  file_z.txt
file_b.txt  file_E.txt  file_i.txt  file_L.txt  file_p.txt  file_S.txt  file_w.txt  file_Z.txt
file_B.txt  file_f.txt  file_I.txt  file_m.txt  file_P.txt  file_t.txt  file_W.txt
file_c.txt  file_F.txt  file_j.txt  file_M.txt  file_q.txt  file_T.txt  file_x.txt
```


#### 字符集

* [:alpha:] 表示所有的字母（不区分大小写），效果同[a-z]
* [:digit:] 表示任意单个数字，效果同[0-9]
* [:lower:] 表示任意单个小写字母
* [:upper:] 表示任意单个大写字母
* [:alnum:] 表示任意单个字母或数字


举例：

* `ls -d [[:alpha:]]`即`ls -d [a-Z]`：显示当前目录下所有单个字母的目录和文件
* `ls -d *[[:digit:]]`即`ls -d *[0-9]`：显示当前目录下所有以数字结尾的目录和文件
* `ls [[:lower:]].txt`：显示当前目录下所有以单个小写字母为名的.txt格式的文件
* `ls -d [[:alnum:]]`：显示当前目录下所有单个字母（不区分大小写）或数字为名的目录或文件






#### 特殊符号

* `|`   ：管道符，或者（正则）
* `>`   ：输出重定向
* `>>`  ：输出追加重定向
* `<`   ：输入重定向
* `<<`  ：追加输入重定向
* `~`   ：当前用户家目录
* `$()` ：引用命令被执行后的结果
* `$`   ：以...结尾（正则）
* `^`   ：以...开头（正则）
* `*`   ：匹配全部字符，通配符
* `?`   ：任意一个字符，通配符
* `#`   ：注释
* `&`   ：让程序或脚本切换到后台执行
* `&&`  ：并且，同时成立
* `[]`  ：表示一个范围（正则，通配符）
* `{}`  ：产生一个序列（通配符）
* `.`   ：当前目录的硬链接
* `..`  ：上级目录的硬链接



#### 刷新文件时间

`touch`命令可以创建空文件，也可以刷新文件时间。参数如下：

* `-a`：仅改变`atime`和`ctime`
* `-m`：仅改变`mtime`和`ctime`
* `-t [[CC]YY]MMDDhhmm[.ss]`：指定`atime`和`mtime`
* `-c`：如果文件不存在，则不创建


```
$ touch file1
$ touch file2

$ ll
-rw-r--r--. 1 vagrant wheel 5 Nov  8 20:49 file1
-rw-r--r--. 1 vagrant wheel 0 Nov  8 20:28 file2
```

创建文件file-non.log，如果不存在则不创建。
```
touch -c file-non.log
```

更新`file1`的时间和`file2`一致。
```
$ touch -r file1 file2

$ ll
-rw-r--r--. 1 vagrant wheel 5 Nov  8 20:49 file1
-rw-r--r--. 1 vagrant wheel 0 Nov  8 20:49 file2
```

指定`file2`的时间。`202210012135.25`代表`YYYYMMDDHHMM.SS`。
```
$ touch -t 202210012135.25 file2

$ ll
-rw-r--r--. 1 vagrant wheel 5 Nov  8 20:49 file1
-rw-r--r--. 1 vagrant wheel 0 Oct  1 21:35 file2

$ stat file2
  File: file2
  Size: 0               Blocks: 0          IO Block: 4096   regular empty file
Device: fd02h/64770d    Inode: 140         Links: 1
Access: (0644/-rw-r--r--)  Uid: ( 1000/ vagrant)   Gid: (   10/   wheel)
Context: unconfined_u:object_r:user_home_t:s0
Access: 2022-10-01 21:35:25.000000000 +0800
Modify: 2022-10-01 21:35:25.000000000 +0800
Change: 2022-11-08 20:56:18.306315887 +0800
 Birth: 2022-11-08 20:28:37.809551441 +0800
```



#### 复制文件和目录

`cp`命令：Copy SOURCE to DEST, or multiple SOURCE(s) to DIRECTORY.

常用参数：

* `-a`：归档，相当于`-dR --preserv=all`参数组合，常用于备份。
* `-d`：不复制原文件，只复制链接名。相当于`--no-dereference --preserve=links`参数组合。
* `-f`：覆盖已经存在的目标文件。
* `-i`：覆盖目标文件之前给出提示。
* `-p`：除复制文件的内容外，也复制文件权限，时间戳，属主属组。相当于`--preserve=mode,ownership,timestamps`。
* `-r, -R, --recursive`：递归复制目录所包含的全部内容。
* `-l`：不复制文件，只是生成硬链接文件。


参数`--preserv`可选项：

* mode：权限
* ownership：属主属组
* timestamp
* links
* xattr
* context
* all

创建测试目录。
```
$ cd ~
$ mkdir test
```

对比参数`-p`的差别。
```
$ cp /etc/issue ~/test/issue1
$ cp -p /etc/issue ~/test/issue1
$ sudo cp /etc/issue ~/test/issue3
$ sudo cp -p /etc/issue ~/test/issue4

$ ll ~/test
-rw-r--r--. 1 vagrant wheel 23 Nov  8 22:25 issue1
-rw-r--r--. 1 vagrant wheel 23 Jul 21 01:10 issue2
-rw-r--r--. 1 root    root  23 Nov  8 22:43 issue3
-rw-r--r--. 1 root    root  23 Jul 21 01:10 issue4

$ ll /etc/issue
-rw-r--r--. 1 root root 23 Jul 21 01:10 /etc/issue
```

对比参数`-r`。
```
$ sudo cp /etc/sysconfig/ ~/test
cp: -r not specified; omitting directory '/etc/sysconfig/'

$ sudo cp -r /etc/sysconfig/ ~/test

$ tree -L 2 ~/test
/home/vagrant/test
├── issue1
├── issue2
├── issue3
├── issue4
└── sysconfig
    ├── anaconda
    ├── atd
    ├── chronyd
    ├── cpupower
    ├── crond
    ├── firewalld
    ├── irqbalance
    ├── kdump
    ├── kernel
    ├── man-db
    ├── network
    ├── network-scripts
    ├── nftables.conf
    ├── raid-check
    ├── rsyslog
    ├── run-parts
    ├── samba
    ├── selinux -> ../selinux/config
    ├── smartmontools
    └── sshd
```

参数`-b`，如果目标文件存在，复制前先将原文件复制并以`~`结尾。
```
$ ll /etc/motd
-rw-r--r--. 1 root root 0 Jun 23  2020 /etc/motd

$ ll ~/test/issue1
-rw-r--r--. 1 vagrant wheel 23 Nov  8 22:25 /home/vagrant/test/issue1

$ cp -b /etc/motd ~/test/issue
$ cp -b /etc/motd ~/test/issue1 

$ ll ~/test
-rw-r--r--. 1 vagrant wheel    0 Nov  8 23:00 issue
-rw-r--r--. 1 vagrant wheel    0 Nov  8 22:57 issue1
-rw-r--r--. 1 vagrant wheel   23 Nov  8 22:25 issue1~
-rw-r--r--. 1 vagrant wheel   23 Jul 21 01:10 issue2
-rw-r--r--. 1 root    root    23 Nov  8 22:43 issue3
-rw-r--r--. 1 root    root    23 Jul 21 01:10 issue4
drwxr-xr-x. 3 root    root  4096 Nov  8 22:49 sysconfig
```

参数`--backup=numbered`会在复制原文件时加上数字序号，序号1代表原始的文件。
```
$ cp --backup=numbered /etc/motd ~/test/issue2
$ cp --backup=numbered /etc/motd ~/test/issue2
$ cp --backup=numbered /etc/motd ~/test/issue2

$ ll ~/test
-rw-r--r--. 1 vagrant wheel    0 Nov  8 23:00 issue
-rw-r--r--. 1 vagrant wheel    0 Nov  8 22:57 issue1
-rw-r--r--. 1 vagrant wheel   23 Nov  8 22:25 issue1~
-rw-r--r--. 1 vagrant wheel    0 Nov  8 23:09 issue2
-rw-r--r--. 1 vagrant wheel   23 Jul 21 01:10 issue2.~1~
-rw-r--r--. 1 vagrant wheel    0 Nov  8 23:09 issue2.~2~
-rw-r--r--. 1 vagrant wheel    0 Nov  8 23:09 issue2.~3~
-rw-r--r--. 1 root    root    23 Nov  8 22:43 issue3
-rw-r--r--. 1 root    root    23 Jul 21 01:10 issue4
drwxr-xr-x. 3 root    root  4096 Nov  8 22:49 sysconfig
```


#### 移动文件和目录

`mv`命令。Rename SOURCE to DEST, or move SOURCE(s) to DIRECTORY.

常用参数：

* `-v`：显示命令执行的信息。
* `-i`：交互式，比如，重名覆盖时会提升是否确认。
* `-b`：覆盖时创建备份。默认情况下，移动文件将会覆盖已存在的目标文件。


移动多个文件到某个目录。
```
$ mv file1 file2 file3 ~/dest
$ mv file* ~/dest
```

移动目录。
```
mv ~/test ~/dest/new/one/
```

重命名文件和目录。
```
$ mv file1 file2
$ mv ~/test ~/dest
```



#### 重命名文件和目录

`rename`命令。分为perl版本和C语言版本。
区分方法: `rename --version`。如果返回结果中包含 `util-linux`，说明是C语言版本, 反之是Perl版本。
openSUSE和Rocy是C语言版本，Ubuntu是Perl版本。

举例：修改当前目录所有扩展名为`s`的文件改为扩展名为`gz`。
```
$ touch file{1..3}.s

$ rename -v '.s' '.gz' *.s
$ rename -v ".s" ".gz" *.s
`file1.txt' -> `file1.html'
`file2.txt' -> `file2.html'
`file3.txt' -> `file3.html'
```

在Ubuntu上完成同样任务，则需要使用正则。
```
rename -v "s/s/gz/g" *.s
```


#### 删除文件

`rm`命令。建议使用`mv`命令代替`rm`命令。



#### 目录操作命令

创建目录：`mkdir`
删除空目录：`rmdir`
删除非空目录：`rm -r`
显示目录树：`tree`




#### 练习

1. 显示`/etc`目录下所有以`l`开头，以一个小写字母结尾，且中间出现至少一位数字的文件或目录列表。
```
ls -d /etc/l*[0-9]*[a-z]
ls -d /etc/l*[[:digit:]]*[[:lower:]]
```
如果无符合条件的记录返回，可以手工创建一个符合条件的文件和目录。
```
sudo touch /etc/lam4you
sudo mkdir /etc/lam5you
```
验证后删除。
```
sudo rm /etc/lam4you
sudo rm -rf /etc/lam5you
```


2. 显示`/etc`目录下以任意一位数字开头，且以非数字结尾的文件或目录列表。
```
ls /etc/[0-9]*[!0-9]
ls /etc/[[:digit:]]*[^[:digit:]]
```
如果无符合条件的记录返回，可以手工创建一个符合条件的文件和目录。
```
sudo touch /etc/5am4yo.
sudo mkdir /etc/5am5yo.
```
验证后删除。
```
sudo rm /etc/5am4yo.
sudo rm -rf /etc/5am5yo.
```


3. 显示`/etc`目录下以非字母开头，后面跟了一个字母及其它任意长度任意字符的文件或目录列表。
```
ls /etc/[!a-zA-Z][a-zA-Z]*
ls /etc/[^[:alpha:]][[:alpha:]]*
```
如果无符合条件的记录返回，可以手工创建一个符合条件的文件和目录。
```
sudo touch /etc/5Ato3
sudo mkdir /etc/6dog6
```
验证后删除。
```
sudo rm /etc/5Ato3
sudo rm -rf /etc/6dog6
```


4. 显示`/etc`目录下，所有以`rc`开头，并后面是0-6之间的数字，其它为任意字符的文件或目录列表。
```
ls /etc/rc[0-6]*
```
如果无符合条件的记录返回，可以手工创建一个符合条件的文件和目录。
```
sudo touch /etc/rc5come
sudo mkdir /etc/rc0123
```
验证后删除。
```
sudo rm /etc/rc5come
sudo rm -rf /etc/rc0123
```


5. 显示`/etc`目录下，所有以`.conf`结尾，且以`m`、`n`、`r`、`p`开头的文件或目录列表。
```
ls /etc/[mnrp]*.conf
```


6. 只显示`/root`下的隐藏文件和目录列表。
```
ls .*
```


7. 只显示/etc下非隐藏目录列表。
```
ls /etc/[^.]*/
```


8. 将`/etc`目录下所有文件，备份到`~/test/`目录下，并要求子目录格式为`backupYYYY-mm-dd`，备份过程可见。
```
$ sudo cp -av /etc/ ~/test/backup`date +%F`
$ sudo cp -av /etc/ ~/test/backup`date +%F_%H-%M-%S`
```


9. 创建目录`~/testdir/dir1/x`，`~/testdir/dir1/y`，`~/testdir/dir1/x/a`，`~/testdir/dir1/x/b`，`~/testdir/dir1/y/a`，`~/testdir/dir1/y/b`。
```
$ mkdir -p ~/testdir/dir1/{x,y}/{a,b}

$ tree ~/testdir/dir1/
/home/vagrant/testdir/dir1/
├── x
│   ├── a
│   └── b
└── y
    ├── a
    └── b
```

10. 创建目录`~/testdir/dir2/x`，`~/testdir/dir2/y`，`~/testdir/dir2/x/a`，`~/testdir/dir2/x/b`。
```
$ mkdir -p ~/testdir/dir2/{x/{a,b},y}

$ tree ~/testdir/dir2/
/home/vagrant/testdir/dir2/
├── x
│   ├── a
│   └── b
└── y
```


11. 创建目录`~/testdir/dir3`、`~/testdir/dir4`、`~/testdir/dir5`、`~/testdir/dir5/dir6`、`~/testdir/dir5/dir7`。
```
$ mkdir -p ~/testdir/dir{3,4,5/dir{6,7}}

$ tree ~/testdir
/home/vagrant/testdir
├── dir1
│   ├── x
│   │   ├── a
│   │   └── b
│   └── y
│       ├── a
│       └── b
├── dir2
│   ├── x
│   │   ├── a
│   │   └── b
│   └── y
├── dir3
├── dir4
└── dir5
    ├── dir6
    └── dir7
```




### 七种文件类型

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



#### inode结构

文件储存在硬盘上，硬盘的最小存储单位叫做“扇区”（Sector）。每个扇区储存512字节（相当于0.5KB）。

操作系统读取硬盘的时候，不是一个一个扇区读取，而是一次性连续读取多个扇区，我们称为读取一个“块”（block）。

常见的block的大小是4KB（连续八个sector组成一个block）。

多个扇区组成的block是文件存取的*最小单位*。

文件数据储存在block中，文件的元信息，比如文件的创建者、创建日期、文大小等，存储在inode，即“索引节点”。

每一个文件都有对应的inode，里面包含了与该文件有关的一些信息。注意，除了文件名以外的其它文件信息，都存在inode之中。

inode包含文件的元信息主要有：

* 文件的字节数
* 文件拥有者的 User ID
* 文件的 Group ID
* 文件的读、写、执行权限
* 文件的时间戳，共有三个：ctime指inode上一次变动的时间，mtime指文件内容上一次变动的时间，atime指文件上一次打开的时间。
* 链接数，即有多少文件名指向这个inode
* 文件数据block的位置

查看inode信息的命令`stat`：
```
$ stat file1
  File: file1
  Size: 5               Blocks: 8          IO Block: 4096   regular file
Device: fd02h/64770d    Inode: 143         Links: 1
Access: (0644/-rw-r--r--)  Uid: ( 1000/ vagrant)   Gid: (   10/   wheel)
Context: unconfined_u:object_r:user_home_t:s0
Access: 2022-11-08 20:49:26.019678244 +0800
Modify: 2022-11-08 20:49:26.019678244 +0800
Change: 2022-11-08 20:49:26.028678455 +0800
 Birth: 2022-11-08 20:49:26.019678244 +0800
```

格式化硬盘时，操作系统会自动将硬盘分成两个区域。一个是数据区，存放文件数据。另一个是inode区（inode table），存放inode所包含的文件的元信息。

每个inode节点的大小，一般是128字节或256字节。inode节点的总数，在格式化时就确定了，一般是每1KB或每2KB就设置一个inode。

假定一块1GB的硬盘，如果每个inode节点的大小为128字节，且每1KB就设置一个inode，则inode table的大小就会达到128MB，占整块硬盘的12.8%。

通过`df`命令查看每个硬盘分区的inode总数和已经使用的数量。
由于每个文件都必须有一个inode，因此有可能发生inode已经用光，但是硬盘还未存满的情况，也就无法在硬盘上创建新文件。

```
$ df -i
Filesystem                         Inodes IUsed   IFree IUse% Mounted on
tmpfs                              497897   872  497025    1% /run
/dev/mapper/ubuntu--vg-ubuntu--lv 3211264 81473 3129791    3% /
tmpfs                              497897     1  497896    1% /dev/shm
tmpfs                              497897     3  497894    1% /run/lock
/dev/sda2                          131072   316  130756    1% /boot
tmpfs                               99579    25   99554    1% /run/user/1000
```

下面命令可以查看每个inode节点的大小：
```
$ sudo dumpe2fs -h /dev/sda2 | grep "Inode size"
dumpe2fs 1.46.5 (30-Dec-2021)
Inode size:               256
```

每个inode都有一个号码，操作系统用inode号码来识别不同的文件，注意，不是通过文件名来识别不同文件。从操作系统角度看，文件名只是inode号码对一个别名。

用户通过文件名，打开某个文件的过程，操作系统分成三步完成：
首先，系统找到这个文件名对应的inode号码。
其次，通过inode号，获取inode信息。
第三，通过inode信息，找到文件数据所在的block，读出数据。

通过`ls -i`命令，可以得到文件对应的inode号：
```
$ ls -i file1
143 file1
```

目录（directory）也是一种文件。打开目录，实际上就是打开目录文件。

目录文件的结构是由一个包含一系列目录项（dirent）的列表组成。
每个目录项由两部分组成：所包含文件的文件名，以及该文件名对应的inode号。

命令`ls -i`列出整个目录文件，即文件名和inode号：
```
$ ls -i
143 file1  140 file2  139 test

$ ls -il
143 -rw-r--r--. 1 vagrant wheel    5 Nov  8 20:49 file1
140 -rw-r--r--. 1 vagrant wheel    0 Oct  1 21:35 file2
139 drwxr-xr-x. 5 vagrant wheel 4096 Nov  9 22:00 test
```




#### 链接类型 

**硬链接**（Hard links）硬链接是存储卷上文件的目录引用或指针。 文件名是存储在目录结构中的标签，目录结构指向文件数据。 因此，可以将多个文件名与同一文件关联。 通过不同的文件名访问时，所做的任何更改都是针对源文件数据。

**符号链接**（Symbolic links）: 符号链接包含一个文本字符串，操作系统将其解释为另一个文件或目录。 它本身就是一个文件，可以独立于目标而存在。 如果删除了符号链接，则其目标文件或目录不受影响。 如果移动，重命名或删除目标文件或目录，则用于指向它的任何符号链接将继续存在，但指向的是一个不存在的文件。

仅当文件和链接文件位于同一文件系统（在同一分区上）时，才能使用硬链接，因为inode编号在同一文件系统中仅是唯一的。 
可以使用`ln`命令创建硬链接，指向已存在文件的inode，可以通过文件名或者硬链接名访问文件。 

可以使用`ln -s`选项创建符号链接。 一个符号链接会被分配一个单独的inode，并指向一个文件，所以可以明显区分符号链接文件和实际文件。 
 
文件系统本质上是一个用于跟踪分区卷中的文件的数据库。 对于普通文件，分配数据块以存储文件的数据，分配inode以指向数据块以及存储关于文件的元数据，然后将文件名分配给inode。 硬链接是与现有inode关联的辅助文件名。 对于符号链接，将为新的inode分配一个与之关联的新文件名，但inode引用另一个文件名而不是引用数据块。

查看文件名和inode之间关系的一个方法是使用`ls -il`命令。inode的典型大小为128位，数据块的大小范围可以是1k，2k，4k或更大，具体取决于文件系统类型。

软连接可以针对目录，硬连接只能针对文件。
	
硬链接相当于增加了一个登记项，使得原来的文件多了一个名字，至于inode都没变。所谓的登记项其实是目录文件中的一个条目(目录项)，使用hard link 是让多个不同的目录项指向同一个文件的inode，没有多余的内容需要存储在磁盘扇区中，所以hardlink不占用额外的空间。

符号链接有单独的inode，在inode中存放另一个文件的路径而不是文件数据，所以符号链接会占用额外的空间。

特征      | 硬链接                             | 符号链接
----------|-----------------------------------|------------
本质       | 同一个文件                         | 不是同一个文件
跨设备     | 不支持                            | 支持
inode     | 相同                              | 不同
链接数     | 创建硬链接，链接数会增加，删除则减少   | 创建或删除，链接数都不变
文件夹     | 不支持                            | 支持
相对路径   | 原始文件的相对路径是相对于当前工作目录 | 原始文件的相对路径是相对于链接文件的相对路径
删除源文件 | 只是链接数减少，链接文件访问不受影响   | 链接文件将无法访问
文件类型   | 和源文件相同                       | 链接文件，和源文件无关
文件大小   | 和源文件相同                       | 源文件的路径的长度











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

!!! 目标

    以Rocky 9为例。

    * 查看软/硬链接文件的特征。
    * 查看目录结构。


可以通过下面命令得到当前系统的2级目录的结构。
```
$ tree -L 2 -d /
```

创建练习目录。
```
$ mkdir data
$ mkdir -p data/typelink
$ cd data
```

创建硬链接。注意：`file`、`hardlinkfile1`、`hardlinkfile2` 文件的链接位置的数值的变化)
```
$ echo "it's original file" > file
$ ln file hardlinkfile1
$ ln -s file symlinkfile1
$ ln -s file symlinkfile2
```
执行`ls -l`命令可以得到下面的结果：
```
-rw-r--r--. 2 vagrant wheel 19 Nov  1 10:42 file
-rw-r--r--. 2 vagrant wheel 19 Nov  1 10:42 hardlinkfile1
lrwxrwxrwx. 1 vagrant wheel  4 Nov  1 10:43 symlinkfile1 -> file
lrwxrwxrwx. 1 vagrant wheel  4 Nov  1 10:43 symlinkfile2 -> file
```

创建另外一个硬链接。
```
$ ln file hardlinkfile2
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
$ echo "add oneline" >> file
```
通过命令`cat file`查看当前`file`的内容。
```
it's original file
add oneline
```
通过下面的命令，可以看到所以软/硬链接文件内容都更新了，和`file`文件更新后的内容保持一致。
```
$ cat hardlinkfile1
$ cat hardlinkfile2
$ cat symlinkfile1
$ cat symlinkfile2
```

对文件`symlinkfile1`再创建新的软连接。
```
$ ln -s symlinkfile1 symlinkfile1-1
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
$ readlink symlinkfile1
$ readlink symlinkfile2
```

注意，对于`symlinkfile1-1`的情况有些不同。
```
$ readlink symlinkfile1-1
```
上面命令返回结果`symlinkfile1`仍然是一个符号链接文件。通过`readlink -f`可以直接定位真正的源文件。
```
$ readlink -f symlinkfile1-1
```
上面的返回结果`/data/linktype/file`是`symlinkfile1-1`真正的源文件。


显示`data`目录下的文件和子目录：
```
$ cd ~
$ tree ./data
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
$ tree -d ./data
```
运行结果：
```
./data
└── typelink
```

显示`data`目录下的文件和子目录，包含全目录：
```
$ tree -f ./data
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

### 文件属性说明

执行命令`ls -ihl`，可以得到下面的输出结果（Rocky 9）。
```
67274680 -rw-r--r--. 3 vagrant wheel 31 Nov  1 11:14 file
67274680 -rw-r--r--. 3 vagrant wheel 31 Nov  1 11:14 hardlinkfile1
67274680 -rw-r--r--. 3 vagrant wheel 31 Nov  1 11:14 hardlinkfile2
67274681 lrwxrwxrwx. 1 vagrant wheel  4 Nov  1 10:43 symlinkfile1 -> file
67274683 lrwxrwxrwx. 1 vagrant wheel 12 Nov  1 11:20 symlinkfile1-1 -> symlinkfile1
67274682 lrwxrwxrwx. 1 vagrant wheel  4 Nov  1 10:43 symlinkfile2 -> file
33555262 drwxr-xr-x. 2 vagrant wheel  6 Nov  1 11:30 typelink
```

以`67274680 -rw-r--r--. 3 vagrant wheel 31 Nov  1 11:14 file`为例：

* `67274680`: inode 索引节点编号。
* `-rw-r--r--`：文件类型及权限
  * `-`：文件类型，例子中出现了三种，`-`，`l`和`d`。
    * `-`：普通文件
    * `d`：目录
    * `l`：符号链接文件（link）
    * `b`：块设备（block）
    * `c`：字符设备（character）
    * `p`：管道文件（pipe）
    * `s`：套接字文件（socket）
  * `rw-r--r--`：文件权限，从左到右依次为：
    * `rw-`：文件属主权限，例子中是`vagrant`。
    * `r--`：文件属组的权限，例子中是`wheel`。
    * `r--`：其他组的权限。
* `.`：这个点表示文件带有SELinux的安全上下文（SELinux Contexts）。关闭SELinux，新创建的文件就不会再有这个点了。但是，以前创建的文件本来有这个点的还会显示这个点（虽然SELinux不起作用了）。
* `3`：硬链接数，例子中`file`和`hardlinkfile1`和`hardlinkfile2`之间是硬链接，所以这三个文件的硬链接数都是`3`。
* `vagrant`：文件属主
* `wheel`：文件属组
* `31`：文件或目录的大小
* `Nov  1 11:14`：文件或目录的创建日期和时间
* `file`：文件或目录名称


下面是命令`ls -ihl`在openSUSE和Ubuntu上的显示结果。
```
$ ls -ihl
233647 -rw-r--r-- 3 vagrant wheel 31 Nov  1 15:52 file
233647 -rw-r--r-- 3 vagrant wheel 31 Nov  1 15:52 hardlinkfile1
233647 -rw-r--r-- 3 vagrant wheel 31 Nov  1 15:52 hardlinkfile2
233648 lrwxrwxrwx 1 vagrant wheel  4 Nov  1 15:52 symlinkfile1 -> file
233650 lrwxrwxrwx 1 vagrant wheel 12 Nov  1 15:52 symlinkfile1-1 -> symlinkfile1
233649 lrwxrwxrwx 1 vagrant wheel  4 Nov  1 15:52 symlinkfile2 -> file
233646 drwxr-xr-x 1 vagrant wheel  0 Nov  1 15:51 typelink
```



#### SELinux & ACL

Security-Enhanced Linux (SELinux) 是一种Linux系统的安全架构，它允许管理员更好地控制谁可以访问系统。 
SELinux于2000年向开源社区发布，并于2003年集成到上游 Linux 内核中。

SELinux为系统上的应用程序、进程和文件定义了访问控制。 它使用安全策略（一组规则告诉SELinux什么可以访问或不可以访问）来强制执行策略允许的访问。

当称为主体（subject）的应用程序或进程请求访问对象（如文件）时，SELinux会检查访问向量缓存(AVC, Access Vector Cache)，其中缓存了主体和对象的权限。

如果 SELinux 无法根据缓存的权限做出访问决定，它会将请求发送到安全服务器。安全服务器检查应用程序或进程和文件的安全上下文。从SELinux策略数据库应用安全上下文（Security context），然后授予或拒绝许可。如果权限被拒绝，`avc: denied`消息将在`/var/log.messages`中体现。

传统上，Linux和UNIX系统都使用DAC（Discretionary Access Control）。 SELinux是Linux的MAC（Mandatory Access Control）系统的一个示例。

在DAC方式下，文件和进程有自己的属主（所有者）。 用户可以拥有一个文件，一个组也可以拥有一个文件，或者其他人。 用户可以更改自己文件的权限。`root`用户对DAC系统具有完全访问控制权。 

但是在像SELinux这样的MAC系统上，对于访问的管理是通过设置策略来实现的。即使用户主目录上的DAC设置发生更改，用于防止其他用户或进程访问该目录的SELinux策略也将继续确保系统安全。

MAC方式是控制一个进程对具体文件系统上面的文件或目录是否拥有访问权限。判断进程是否可以访问文件或目录的依据，取决于SELinux中设定的很多策略规则。

可以通过编辑 `/etc/selinux/config` 并设置 `SELINUX=permissive` 来启用 SElinux。

访问控制列表 (ACL，Access Control List) 为文件系统提供了一种额外的、更灵活的权限机制。 它旨在协助 UNIX 文件权限。ACL允许授予任何用户或组对任何磁盘资源的权限。ACL适用于在不使某个用户成为组成员的情况下，仍旧授予一些读或写访问权限。

下面示例对比说明了SELinux和ACL在文件属性展现上的特点。

* `-rwxr-xr--  vagrant wheel` ：没有selinux上下文，没有ACL
* `-rwx--xr-x+ vagrant wheel` ：只有ACL，没有selinux上下文
* `-rw-r--r--. vagrant wheel` ：只有selinux上下文，没有ACL
* `-rwxrwxr--+ vagrant wheel` ：有selinux上下文，有ACL



## 标准输入输出

标准输入输出，即I/O，I/O的I是Input，O是output。

* I：从外部设备输入到内存
* O：从内存输出到外部设备

标准输入和标准输出是用于IO的，它们属于外部设备（逻辑上的外部设备），不是内存。

linux中一切设备皆是文件！因此标准输入和输出本质就是文件，外部设备以文件形式表现。

在Linux系统中，标准输入和标准输出对应的文件是`/dev/stdin`和`/dev/stdout`这两个文件。

从标准输入读，从逻辑上讲，就是打开`/dev/stdin`这个文件，并读入文件内容。
输出到标准输出，从逻辑上讲，就是打开`/dev/stdout`这个文件，并把内容输出到这个文件里去。

这里强调的是“逻辑上”，因为`/dev/stdin`和`/dev/stdout`这2个文件本身不是设备文件。Linux中设备是文件，但是文件不一定是设备。
因此，操作`/dev/stdin`和/dev/stdout`这2个文件，实际上是操作两个文件存放地址对应的设备文件。

通过下面命令可以看到标准输入输出文件的特点，他们虽然在`/dev`目录下，都是以`l`开头的链接文件，指向的是另一个文件的地址。
```
$ ls -l /dev/std*
lrwxrwxrwx 1 root root 15 Nov 13 10:39 /dev/stderr -> /proc/self/fd/2
lrwxrwxrwx 1 root root 15 Nov 13 10:39 /dev/stdin -> /proc/self/fd/0
lrwxrwxrwx 1 root root 15 Nov 13 10:39 /dev/stdout -> /proc/self/fd/1

# Rocky
$ ll /proc/self/fd/
lrwx------. 1 vagrant wheel 64 Nov 13 22:38 0 -> /dev/pts/0
lrwx------. 1 vagrant wheel 64 Nov 13 22:38 1 -> /dev/pts/0
lrwx------. 1 vagrant wheel 64 Nov 13 22:38 2 -> /dev/pts/0
lr-x------. 1 vagrant wheel 64 Nov 13 22:38 3 -> /proc/1702/fd

# Ubuntu
$ ll /proc/self/fd/
lrwx------ 1 vagrant sudo 64 Nov 13 14:38 0 -> /dev/pts/0
lrwx------ 1 vagrant sudo 64 Nov 13 14:38 1 -> /dev/pts/0
lrwx------ 1 vagrant sudo 64 Nov 13 14:38 2 -> /dev/pts/0
lr-x------ 1 vagrant sudo 64 Nov 13 14:38 3 -> /proc/2062/fd/

# openSUSE
$ ll /proc/self/fd/*
ls: cannot access '/proc/self/fd/255': No such file or directory
ls: cannot access '/proc/self/fd/3': No such file or directory
lrwx------ 1 vagrant wheel 64 Nov 13 22:37 /proc/self/fd/0 -> /dev/pts/0
lrwx------ 1 vagrant wheel 64 Nov 13 22:37 /proc/self/fd/1 -> /dev/pts/0
lrwx------ 1 vagrant wheel 64 Nov 13 22:37 /proc/self/fd/2 -> /dev/pts/0
```

Linux进程默认会打开的三个文件：

* 标准输入`/dev/stdin`，描述符为 0，默认是键盘输入。
* 标准输出`/dev/stdout`，描述符为 1，默认是输出到屏幕。
* 标准输出`/dev/stderr`，描述符为 2，默认是输出到屏幕。


以Rocky为例，创建`file.py`文件。
```
$ cat > file.py <<EOF
import time
f = open('test.txt', 'r')
time.sleep(1000)
EOF
```
创建`test.txt`文件。
```
$ echo "hello" > test.txt
```
运行`file.py`程序。
```
$ python3 file.py
```
打开新的终端窗口，执行下面命令，得到python3这个程序运行的process ID。其中可以看到有一个来自文件test.txt被程序file.py打开（输入）。
```
$ pidof python3
1739 788

$ sudo ls -l /proc/788/fd/
lr-x------. 1 root root 64 Nov 13 23:00 0 -> /dev/null
l-wx------. 1 root root 64 Nov 13 23:00 1 -> /dev/null
lrwx------. 1 root root 64 Nov 13 23:00 10 -> 'socket:[24677]'
lrwx------. 1 root root 64 Nov 13 23:00 11 -> 'socket:[24678]'
l-wx------. 1 root root 64 Nov 13 23:00 2 -> /dev/null
l-wx------. 1 root root 64 Nov 13 10:41 3 -> /var/log/firewalld
lrwx------. 1 root root 64 Nov 13 23:00 4 -> 'socket:[23421]'
lrwx------. 1 root root 64 Nov 13 23:00 5 -> 'anon_inode:[eventfd]'
lrwx------. 1 root root 64 Nov 13 23:00 6 -> 'socket:[24586]'
lr-x------. 1 root root 64 Nov 13 23:00 7 -> anon_inode:inotify
lrwx------. 1 root root 64 Nov 13 23:00 8 -> 'anon_inode:[eventfd]'
lrwx------. 1 root root 64 Nov 13 23:00 9 -> '/memfd:libffi (deleted)'

$ sudo ls -l /proc/1739/fd/
lrwx------. 1 vagrant wheel 64 Nov 13 23:00 0 -> /dev/pts/0
lrwx------. 1 vagrant wheel 64 Nov 13 23:00 1 -> /dev/pts/0
lrwx------. 1 vagrant wheel 64 Nov 13 23:00 2 -> /dev/pts/0
lr-x------. 1 vagrant wheel 64 Nov 13 23:00 3 -> /home/vagrant/test.txt
```

在Ubuntu中运行`file.py`程序，pidof会取得3个process IDs。
```
$ pidof python3
2128 924 873

$ sudo ls -l /proc/2128/fd/
lrwx------ 1 vagrant sudo 64 Nov 13 15:10 0 -> /dev/pts/0
lrwx------ 1 vagrant sudo 64 Nov 13 15:10 1 -> /dev/pts/0
lrwx------ 1 vagrant sudo 64 Nov 13 15:10 2 -> /dev/pts/0
lr-x------ 1 vagrant sudo 64 Nov 13 15:10 3 -> /home/vagrant/test.txt

$ sudo ls -l /proc/924/fd/
lr-x------ 1 root root 64 Nov 13 15:11 0 -> /dev/null
lrwx------ 1 root root 64 Nov 13 15:11 1 -> 'socket:[31593]'
lrwx------ 1 root root 64 Nov 13 15:11 2 -> 'socket:[31593]'
l-wx------ 1 root root 64 Nov 13 02:40 3 -> /var/log/unattended-upgrades/unattended-upgrades-shutdown.log
lrwx------ 1 root root 64 Nov 13 15:11 4 -> 'socket:[31652]'
lrwx------ 1 root root 64 Nov 13 15:11 5 -> 'anon_inode:[eventfd]'
lrwx------ 1 root root 64 Nov 13 15:11 6 -> 'anon_inode:[eventfd]'
lrwx------ 1 root root 64 Nov 13 15:11 7 -> 'socket:[31657]'
l-wx------ 1 root root 64 Nov 13 15:11 8 -> /run/systemd/inhibit/1.ref
lrwx------ 1 root root 64 Nov 13 15:11 9 -> 'socket:[31658]'

$ sudo ls -l /proc/873/fd/
lr-x------ 1 root root 64 Nov 13 15:11 0 -> /dev/null
lrwx------ 1 root root 64 Nov 13 15:11 1 -> 'socket:[31412]'
lrwx------ 1 root root 64 Nov 13 15:11 2 -> 'socket:[31412]'
lrwx------ 1 root root 64 Nov 13 02:40 3 -> 'socket:[31650]'
lrwx------ 1 root root 64 Nov 13 15:11 4 -> 'anon_inode:[eventfd]'
lrwx------ 1 root root 64 Nov 13 15:11 5 -> 'socket:[31663]'
lrwx------ 1 root root 64 Nov 13 15:11 6 -> 'socket:[31664]'
```

openSUSE需要安装包`sysvinit-tools`才能使用`pidof`命令。
```
$ sudo zypper in sysvinit-tools
```

由于openSUSE中pidof python3只返回一个process ID，所以可以简化命令行得到process ID的详细信息。
```
$ sudo ls -l /proc/`pidof python3`/fd/
lrwx------ 1 vagrant wheel 64 Nov 13 23:21 0 -> /dev/pts/0
lrwx------ 1 vagrant wheel 64 Nov 13 23:21 1 -> /dev/pts/0
lrwx------ 1 vagrant wheel 64 Nov 13 23:21 2 -> /dev/pts/0
lr-x------ 1 vagrant wheel 64 Nov 13 23:21 3 -> /home/vagrant/test.txt
```

!!! Reference
    当键盘和鼠标等设备通过串口直接连接到计算机时，这种连接称为TTY。
    伪终端pseudoterminal（缩写为“pty”）是一对提供双向通信通道的虚拟字符设备。 通道的一端称为主端master； 另一端称为从端slave。 

    `/dev/pts`表示与伪终端pseudoterminal的主端master或从端slave相关的master文件，操作系统将其保存为`/dev/ptmx`文件。 `telnet`和`ssh`等程序能够仿真终端，用户与它们的交互，虽然本质上是与文件`/dev/ptmx`进行交互，但呈现给用户的却是好像运行在真正的终端窗口一样，从端的文件是主端的输入。

    伪终端进程在Linux中被存储在`/dev/pts/`目录下。`/dev/pts/`目录下的内容是一些特殊的目录，由Linux内核所创建。
    
    每个唯一的终端窗口都与`/dev/pts`系统中的一个Linux`pts`条目相关。

    下面返回的结果说明有2个远程终端连接到当前的机器。
    ```
    $ ll /dev/pts/
    crw--w----. 1 vagrant tty  136, 0 Nov 13 23:18 0
    crw--w----. 1 vagrant tty  136, 1 Nov 13 23:48 1
    c---------. 1 root    root   5, 2 Nov 13 10:41 ptmx
    ```

    也可以通过`w`命令看到2个终端进程。
    ```
    $ w
     23:55:05 up 13:14,  2 users,  load average: 0.00, 0.00, 0.00
    USER     TTY        LOGIN@   IDLE   JCPU   PCPU WHAT
    vagrant  pts/0     10:51   37:03   0.05s  0.05s -bash
    vagrant  pts/1     23:48    0.00s  0.03s  0.00s w
    ```

    单个伪终端pseudoterminal可以同时接收来自不同的程序的输出。
    多个程序同时对一个伪终端pseudoterminal进行读取会引起混淆。

    存储在`/dev/pts`目录中的文件是抽象文件而不是真实文件，是伪终端中执行程序时临时存储的数据。 打开`/dev/pts`下的文件通常没有什么实际意义。





## 重定向和管道

### 输入重定向

常用命令格式：

* `command < file`：将指定文件`file`作为命令的输入设备。
* `command << delimiter`：表示从标准输入设备（键盘）中读入，直到遇到分界符`delimiter`停止（读入的数据不包括分界符），这里的分界符可以理解为自定义的字符串。
* `command < file1 > file2`：将`file1`作为命令的输入设备，该命令的执行结果输出到`file2`中。


```
# 输出文件file.py内容（输入设备是键盘）
$ cat file.py

# 输出文件file.py内容（输入设备是文件file.py）
$ cat < file.py

# 指定分界符（这里是EOF），读取键盘输入内容，直到遇到指定分界符为止，将所读取的内容输出到文件file.py。
$ cat > file.py <<EOF
import time
f = open('test.txt', 'r')
time.sleep(1000)
EOF

# 读取文件file.py内容，输出到新文件new.py。
$ cat < file.py > new.py
```


### 输出重定向

输出重定向分为标准输出重定向和错误输出重定向两种。

常用命令格式：

* `command > file`：将命令`command`执行的标准输出结果重定向输出到指定的文件`file`中，如果该文件已包含数据，会清空原有数据，再写入新数据。
* `command 2> file`：将命令`command`执行的错误输出结果重定向到指定的文件`file`中，如果该文件中已包含数据，会清空原有数据，再写入新数据。
* `command >> file`：将命令`command`执行的标准输出结果重定向输出到指定的文件`file`中，如果该文件已包含数据，新数据将追加写入到原有内容的后面。
* `command 2>> file`：将命令`command`执行的错误输出结果重定向到指定的文件`file`中，如果该文件中已包含数据，新数据将追加写入到原有内容的后面。
* `command >> file 2>&1` 或者 `command &>> file`：将标准输出或者错误输出写入到指定文件`file`中，如果该文件中已包含数据，新数据将追加写入到原有内容的后面。

注意：上面的`file`可以是一个普通文件，也可以使用一个特殊的文件`/dev/null`。`/dev/null`并不保存数据，被写入`/dev/null`的数据最终都会丢失。

举例：2个python文件存在，其他2个无扩展名的文件不存在。
```
$ ls file.py > out
$ ls file 2> out.err

$ ls new.py >> out
$ ls new 2>> out.err
```
可以得到预期的结果。两个错误记录都被追加到`out.err`文件中。两个成功执行的命令的返回结果也输出到`out`文件中。
```
$ccat out
file.py
new.py

$ cat out.err
ls: cannot access 'file': No such file or directory
ls: cannot access 'new': No such file or directory
```

上例命令也可以合并。
```
$ ls file.py > out 2> out.err
$ ls file >> out 2>> out.err
```

`2>&1`格式举例：
```
$ ls file >> out.txt 2>&1
$ cat out.txt
ls: cannot access 'file': No such file or directory

$ ls file.py &>> out.txt
$ cat out.txt
ls: cannot access 'file': No such file or directory
file.py
```

### 特殊重定向

格式：`command1 < <(command2)`
```
tr 'a-z' 'A-Z' < <(echo "Hello World")
```


应用：修改密码

密码保存在`passwd.txt`文件中，并严格限制改文件的权限。
通过参数`--stdin`实现模拟键盘输入操作输入用户名。

```
passwd --stdin vagrant < passwd.txt
```






!!! Reference
    Here-document(Here-doc)：输入的文本块重定向至标准输入流，直至遇到特殊的文件结束标记符为止（文件结束标记符可以是任意的唯一的字符串，但大部分人都默认使用 `EOF`）。

    ```
    cat <<EOF
    This is line1
    Another line
    Finally 3rd line
    EOF
    ```
    文本块中含有tab键。
    ```
    cat <<-EOF
        This message is indented
            This message is double indented
    EOF
    ```

    文本块中含有参数。
    ```
    cat <<EOF
    Hello ${USER}
    EOF
    ```

    文本块中含有命令。
    ```
    cat <<EOF
    Hello! It is currently: $(date)
    EOF
    ```

    Here-string：与`Here-doc`相似，但是它只有一个字符串，或者几个被引号括起来的字符串。

    基本用法。
    ```
    cat <<< "This is a string"
    ```
    使用变量。
    ```
    WELCOME_MESSAGE="Welcome!"
    cat <<< $WELCOME_MESSAGE
    ```
    使用参数。
    ```
    cat <<< "Welcome! ${USER}"
    ```


### 管道

Linux中使用竖线`|`连接多个命令，这被称为管道符。

当在两个命令之间设置管道时，管道符`|`左边命令的输出就变成了右边命令的输入。管道符`|`左边正确的输出才能被右边处理，管道符`|`右边不能处理左边错误的输出。


重定向和管道的区别：重定向操作符`>`将命令与文件连接起来，用文件来接收命令的输出；而管道符`|`将命令与命令连接起来，用右边命令来接收左边命令的输出。

```
$ ls | tr 'a-z' 'A-Z'
BIN
F1.TXT
F2.TXT
FILE.PY
NEW.PY
OUT
OUT.ERR
TEST.TXT
```







