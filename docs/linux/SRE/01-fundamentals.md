# Linux 基础

## 官方文档

[Rocky Linux Instructional Books](https://docs.rockylinux.org/books/)

[openSUSE Documentation](https://doc.opensuse.org/)

[Ubuntu Documentation](https://docs.ubuntu.com/)




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












