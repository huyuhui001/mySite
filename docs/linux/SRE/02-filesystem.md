# 第二章 文件系统

文件系统层次标准（Filesystem Hierarchy Standard, FHS），它是Linux 标准库（Linux Standards Base, LSB）规范的一部分。

根目录`/`指文件系统树的最高层。 根分区在系统启动时首先挂载。
系统启动时运行的所有程序都必须在此分区中。

## 1.主要目录

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
  * `/usr/lib64/` - 包含64位库和应用程序
  * `/usr/include/` - 包含C程序的头文件（head file）
  * `/usr/local/` - 包含本地安装程序。这个目录下的内容不会被系统升级所覆盖。下面3个目录在初始安装后是空的。
    * `/usr/local/bin`-
    * `/usr/local/sbin`-
    * `/usr/local/lib`-
  * `/usr/sbin/` - 系统管理程序
  * `/usr/src/` - 内核和应用程序的源代码
    * `/usr/src/linux`-
  * `/usr/share/` - 结构化独立数据
    * `/usr/share/doc/` - 文档
    * `/usr/share/man/` - `man`命令使用的内容
* `/opt` - 第三方应用程序目录
  * 各发行版包含的应用程序一般存储在目录`/usr/lib/`。
  * 各发行版可选程序，或第三方应用程序则存储在目录`/opt`。
  * 在安装时，会为每个应用程序的文件创建一个目录，其中包含应用程序的名称。比如：
    * `/opt/novell`-
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
    * .profile - 用户私有登录脚本
    * .bashrc - `bash`的配置文件
    * .bash_history - `bash`环境下保持命令历史记录
* `run` - 应用程序状态文件
  * 为应用程序提供了一个标准位置来存储它们需要的临时文件，例如套接字和进程ID。 这些文件不能存储在`/tmp`中，因为`/tmp`中的文件可能会被删除。
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
    * `/var/lib/` - 可变库文件，应用程序状态信息数据
    * `/var/log/` - 日志文件
    * `/var/run/` - 运行中的进程的信息
    * `/var/lock/` - 多用户访问时的锁文件
    * `/var/cache`- 应用程序缓存数据目录
    * `/var/opt` - 专为`/opt`下的应用程序存储可变数据
    * `/var/mail`-
    * `/var/spool/` - 应用程序数据池，比如：打印机，邮件
      * `/var/spool/mail`-
      * `/var/spool/cron`-
* `/tmp` - 临时文件
  * 程序在运行时创建临时文件的位置
* `/proc` - 进程文件
  * 虚拟文件系统，不占空间，大小始终为零，保持当前进程的状态信息
  * 包含有关各个进程的信息的目录，根据进程的 PID 号命名
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
    * 硬件总线（hardware buses）
    * 硬件设备（hardware devices）
    * 有源设备（active devices）
    * 驱动程序（drivers）

## 2.文件操作命令

### 2.1.显示当前工作目录

pwd命令（print working directory）:

* -L: 显示链接路径
* -P：显示真实物理路径

### 2.2.相对和绝对路径

对于绝对路径`/etc/firewalld/policies`，可以通过下面命令得到该路径的基名`policies`和目录名`/etc/firewalld`。

```bash
basename /etc/firewalld/policies
dirname /etc/firewalld/policies
```

### 2.3.更改目录

`.`指当前目录，即`pwd`命令所返回的目录。

`..`指当前目录的上一级目录，及当前目录的父目录。

* 切换至父目录：`cd ..`

* 切换至当前用户主目录：`cd ~`

* 切换至上次工作目录：`cd -`

* `echo $PWD`：当前工作目录

* `echo $OLDPWD`：上次工作目录

### 2.4.列出目录内容

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

### 2.5.文件状态stat

每个文件有三个时间戳：

* 访问时间 Access Time `atime` : 读取文件内容。
* 修改时间 Modify Time `mtime` : 改变文件内容（数据）。
* 改变时间 Change Time `ctime` : 元数据发生改变。

读取三个时间戳的命令`stat`：

```bash
stat /etc/fstab
```

输出结果：

```console
  File: /etc/fstab
  Size: 927             Blocks: 8          IO Block: 4096   regular file
Device: 30h/48d Inode: 263         Links: 1
Access: (0644/-rw-r--r--)  Uid: (    0/    root)   Gid: (    0/    root)
Access: 2022-10-31 10:26:34.987466959 +0800
Modify: 2022-06-24 14:50:24.387992912 +0800
Change: 2022-06-24 14:50:24.387992912 +0800
 Birth: 2022-06-24 14:50:23.755992937 +0800
```

### 2.6.确定文件类型

命令`file`检查文件类型。

* `-b`：列出辨识结果时，不显示文件名称。
* `-c`：详细显示指令执行过程，便于排错或分析程序执行的情形。
* `-f <名称文件>`：指定名称文件，其内容有一个或多个文件名称时，让file依序辨识这些文件，格式为每列一个文件名称。
* `-L`： 直接显示符号连接所指向的文件的类别。
* `-v`： 显示版本信息。
* `-z`： 尝试去解读压缩文件的内容。

编辑文件`list.txt`包含一下内容：

```console
/etc/
/bin
/etc/issue
```

运行命令`file -f list.txt`，结果如下：

```console
/etc/:      directory
/bin:       directory
/etc/issue: symbolic link to ../run/issue
```

### 2.7.文件编码转换

`iconv`命令用于将一种编码中的某些文本转换为另一种编码。 如果没有提供输入文件，则它从标准输入中读取。 同样，如果没有给出输出文件，那么它会写入标准输出。 如果没有提供 `from-encoding` 或 `to-encoding`，则它使用当前本地的字符编码。

将文本从 ISO 8859-15 字符编码转换为 UTF-8，读入`input.txt`，输出`output.txt`。

```bash
iconv -f ISO-8859-15 -t UTF-8 < input.txt > output.txt
```

从 UTF-8 转换为 ASCII，尽可能进行音译（transliterating）：

```bash
echo abc ß α € àḃç | iconv -f UTF-8 -t ASCII//TRANSLIT
```

运行结果：

```console
abc ss ? EUR abc
```

### 2.8.通配符

通配符，指包含这些字符的字符串

* `?`  ：表示任意一个字符
* `*`  ：表示任意长度的任意字符
* `[]` ：匹配指定范围内任意一个字符
  * `[abcd]`：匹配abcd中的任何一个字符
  * `[a-z]`：匹配范围a到z内任意一个字符
  * `[!abcd]`：不匹配括号里面任何一个字符
* `{}` ：表示生成序列，以逗号分割，不能有空格

示例：

```bash
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

```bash
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

### 2.9.字符集

* `[:alpha:]`：表示所有的字母（不区分大小写），效果同`[a-z]`
* `[:digit:]`：表示任意单个数字，效果同`[0-9]`
* `[:xdigit:]`：表示十六进制数字
* `[:lower:]`：表示任意单个小写字母
* `[:upper:]`：表示任意单个大写字母
* `[:alnum:]`：表示任意单个字母或数字
* `[:blank:]`：表示空白字符（空格和制表符）
* `[:space:]`：表示包括空格、制表符（水平和垂直）、换行符、回车符等各种类型的空白，比`[:blank:]`范围更广
* `[:cntrl:]`：表示不可打印的控制字符（退格、删除、警铃等）
* `[:graph:]`：表示可打印的非空白字符
* `[:print:]`：表示可打印字符
* `[:punct:]`：表示标点符号

举例：

* `ls -d [[:alpha:]]`即`ls -d [a-Z]`：显示当前目录下所有单个字母的目录和文件
* `ls -d *[[:digit:]]`即`ls -d *[0-9]`：显示当前目录下所有以数字结尾的目录和文件
* `ls [[:lower:]].txt`：显示当前目录下所有以单个小写字母为名的.txt格式的文件
* `ls -d [[:alnum:]]`：显示当前目录下所有单个字母（不区分大小写）或数字为名的目录或文件

### 2.10.特殊符号

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

### 2.11.刷新文件时间`touch`

`touch`命令可以创建空文件，也可以刷新文件时间。参数如下：

* `-a`：仅改变`atime`和`ctime`
* `-m`：仅改变`mtime`和`ctime`
* `-t [[CC]YY]MMDDhhmm[.ss]`：指定`atime`和`mtime`
* `-c`：如果文件不存在，则不创建

```bash
$ touch file1
$ touch file2

$ ll
-rw-r--r--. 1 vagrant wheel 5 Nov  8 20:49 file1
-rw-r--r--. 1 vagrant wheel 0 Nov  8 20:28 file2
```

创建文件file-non.log，如果不存在则不创建。

```bash
touch -c file-non.log
```

更新`file1`的时间和`file2`一致。

```bash
$ touch -r file1 file2

$ ll
-rw-r--r--. 1 vagrant wheel 5 Nov  8 20:49 file1
-rw-r--r--. 1 vagrant wheel 0 Nov  8 20:49 file2
```

指定`file2`的时间。`202210012135.25`代表`YYYYMMDDHHMM.SS`。

```bash
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

### 2.12.复制文件和目录`cp`

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

```bash
cd ~
mkdir test
```

对比参数`-p`的差别。

```bash
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

```bash
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

```bash
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

```bash
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

### 2.13.移动文件和目录`mv`

`mv`命令。Rename SOURCE to DEST, or move SOURCE(s) to DIRECTORY.

常用参数：

* `-v`：显示命令执行的信息。
* `-i`：交互式，比如，重名覆盖时会提升是否确认。
* `-b`：覆盖时创建备份。默认情况下，移动文件将会覆盖已存在的目标文件。

移动多个文件到某个目录。

```bash
mv file1 file2 file3 ~/dest
mv file* ~/dest
```

移动目录。

```bash
mv ~/test ~/dest/new/one/
```

重命名文件和目录。

```bash
mv file1 file2
mv ~/test ~/dest
```

### 2.14.重命名文件和目录`rename`

`rename`命令。分为perl版本和C语言版本。
区分方法: `rename --version`。如果返回结果中包含 `util-linux`，说明是C语言版本, 反之是Perl版本。
openSUSE和Rocy是C语言版本，Ubuntu是Perl版本。

举例：修改当前目录所有扩展名为`s`的文件改为扩展名为`gz`。

```bash
$ touch file{1..3}.s

$ rename -v '.s' '.gz' *.s
$ rename -v ".s" ".gz" *.s
`file1.txt' -> `file1.html'
`file2.txt' -> `file2.html'
`file3.txt' -> `file3.html'
```

在Ubuntu上完成同样任务，则需要使用正则。

```bash
rename -v "s/s/gz/g" *.s
```

### 2.15.删除文件`rm`

`rm`命令。建议使用`mv`命令代替`rm`命令。

### 2.16.目录操作命令

创建目录：`mkdir`

删除空目录：`rmdir`

删除非空目录：`rm -r`

显示目录树：`tree`

### 2.17.练习

* 显示`/etc`目录下所有以`l`开头，以一个小写字母结尾，且中间出现至少一位数字的文件或目录列表。

```bash
ls -d /etc/l*[0-9]*[a-z]
ls -d /etc/l*[[:digit:]]*[[:lower:]]
```

如果无符合条件的记录返回，可以手工创建一个符合条件的文件和目录。

```bash
sudo touch /etc/lam4you
sudo mkdir /etc/lam5you
```

验证后删除。

```bash
sudo rm /etc/lam4you
sudo rm -rf /etc/lam5you
```

* 显示`/etc`目录下以任意一位数字开头，且以非数字结尾的文件或目录列表。

```bash
ls /etc/[0-9]*[!0-9]
ls /etc/[[:digit:]]*[^[:digit:]]
```

如果无符合条件的记录返回，可以手工创建一个符合条件的文件和目录。

```bash
sudo touch /etc/5am4yo.
sudo mkdir /etc/5am5yo.
```

验证后删除。

```bash
sudo rm /etc/5am4yo.
sudo rm -rf /etc/5am5yo.
```

* 显示`/etc`目录下以非字母开头，后面跟了一个字母及其它任意长度任意字符的文件或目录列表。

```bash
ls /etc/[!a-zA-Z][a-zA-Z]*
ls /etc/[^[:alpha:]][[:alpha:]]*
```

如果无符合条件的记录返回，可以手工创建一个符合条件的文件和目录。

```bash
sudo touch /etc/5Ato3
sudo mkdir /etc/6dog6
```

验证后删除。

```bash
sudo rm /etc/5Ato3
sudo rm -rf /etc/6dog6
```

* 显示`/etc`目录下，所有以`rc`开头，并后面是0-6之间的数字，其它为任意字符的文件或目录列表。

```bash
ls /etc/rc[0-6]*
```

如果无符合条件的记录返回，可以手工创建一个符合条件的文件和目录。

```bash
sudo touch /etc/rc5come
sudo mkdir /etc/rc0123
```

验证后删除。

```bash
sudo rm /etc/rc5come
sudo rm -rf /etc/rc0123
```

* 显示`/etc`目录下，所有以`.conf`结尾，且以`m`、`n`、`r`、`p`开头的文件或目录列表。

```bash
ls /etc/[mnrp]*.conf
```

* 只显示`/root`下的隐藏文件和目录列表。

```bash
ls .*
```

* 只显示/etc下非隐藏目录列表。

```bash
ls /etc/[^.]*/
```

* 将`/etc`目录下所有文件，备份到`~/test/`目录下，并要求子目录格式为`backupYYYY-mm-dd`，备份过程可见。

```bash
sudo cp -av /etc/ ~/test/backup`date +%F`
sudo cp -av /etc/ ~/test/backup`date +%F_%H-%M-%S`
```

* 创建目录`~/testdir/dir1/x`，`~/testdir/dir1/y`，`~/testdir/dir1/x/a`，`~/testdir/dir1/x/b`，`~/testdir/dir1/y/a`，`~/testdir/dir1/y/b`。

```bash
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

* 创建目录`~/testdir/dir2/x`，`~/testdir/dir2/y`，`~/testdir/dir2/x/a`，`~/testdir/dir2/x/b`。

```bash
$ mkdir -p ~/testdir/dir2/{x/{a,b},y}

$ tree ~/testdir/dir2/
/home/vagrant/testdir/dir2/
├── x
│   ├── a
│   └── b
└── y
```

* 创建目录`~/testdir/dir3`、`~/testdir/dir4`、`~/testdir/dir5`、`~/testdir/dir5/dir6`、`~/testdir/dir5/dir7`。

```bash
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

## 3.七种文件类型

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

### 3.1.inode结构

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

```bash
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

```bash
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

```bash
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

```bash
$ ls -i file1
143 file1
```

目录（directory）也是一种文件。打开目录，实际上就是打开目录文件。

目录文件的结构是由一个包含一系列目录项（dirent）的列表组成。
每个目录项由两部分组成：所包含文件的文件名，以及该文件名对应的inode号。

命令`ls -i`列出整个目录文件，即文件名和inode号：

```bash
$ ls -i
143 file1  140 file2  139 test

$ ls -il
143 -rw-r--r--. 1 vagrant wheel    5 Nov  8 20:49 file1
140 -rw-r--r--. 1 vagrant wheel    0 Oct  1 21:35 file2
139 drwxr-xr-x. 5 vagrant wheel 4096 Nov  9 22:00 test
```

### 3.2.链接类型

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

| 特征    | 硬链接                 | 符号链接                   |
| ----- | ------------------- | ---------------------- |
| 本质    | 同一个文件               | 不是同一个文件                |
| 跨设备   | 不支持                 | 支持                     |
| inode | 相同                  | 不同                     |
| 链接数   | 创建硬链接，链接数会增加，删除则减少  | 创建或删除，链接数都不变           |
| 文件夹   | 不支持                 | 支持                     |
| 相对路径  | 原始文件的相对路径是相对于当前工作目录 | 原始文件的相对路径是相对于链接文件的相对路径 |
| 删除源文件 | 只是链接数减少，链接文件访问不受影响  | 链接文件将无法访问              |
| 文件类型  | 和源文件相同              | 链接文件，和源文件无关            |
| 文件大小  | 和源文件相同              | 源文件的路径的长度              |

### 3.3.设备文件

**设备文件**（Device File）表示硬件（网卡除外）。 每个硬件都由一个设备文件表示。 网卡是接口。

设备文件把内核驱动和物理硬件设备连接起来。
内核驱动程序通过对设备文件进行读写（正确的格式）来实现对硬件的读写。

类型：

* 块设备（Block Devices）：块设备（通常）在512字节的大块中读取/写入信息。
* 字符设备（Character Devices）：字符设备以字符方式读取/写入信息。 字符设备直接提供对硬件设备的无缓冲访问。
  * 有时称为裸设备（raw devices）。（注意：裸设备被视为字符设备，不是块设备）
  * 通过辅以不同选项，可以广泛而多样地应用和使用字符设备。
* 当内核发现设备时由操作系统`udev`自动创建。

### 3.4.练习

目标：以Rocky 9为例。

* 查看软/硬链接文件的特征。
* 查看目录结构。

可以通过下面命令得到当前系统的2级目录的结构。

```bash
tree -L 2 -d /
```

创建练习目录。

```bash
mkdir data
mkdir -p data/typelink
cd data
```

创建硬链接。注意：`file`、`hardlinkfile1`、`hardlinkfile2` 文件的链接位置的数值的变化)

```bash
echo "it's original file" > file
ln file hardlinkfile1
ln -s file symlinkfile1
ln -s file symlinkfile2
```

执行`ls -l`命令可以得到下面的结果：

```bash
-rw-r--r--. 2 vagrant wheel 19 Nov  1 10:42 file
-rw-r--r--. 2 vagrant wheel 19 Nov  1 10:42 hardlinkfile1
lrwxrwxrwx. 1 vagrant wheel  4 Nov  1 10:43 symlinkfile1 -> file
lrwxrwxrwx. 1 vagrant wheel  4 Nov  1 10:43 symlinkfile2 -> file
```

创建另外一个硬链接。

```bash
ln file hardlinkfile2
```

执行`ls -l`命令可以得到下面的结果：

```bash
-rw-r--r--. 3 vagrant wheel  19 Nov  1 10:42 file
-rw-r--r--. 3 vagrant wheel  19 Nov  1 10:42 hardlinkfile1
-rw-r--r--. 3 vagrant wheel  19 Nov  1 10:42 hardlinkfile2
lrwxrwxrwx. 1 vagrant wheel   4 Nov  1 10:43 symlinkfile1 -> file
lrwxrwxrwx. 1 vagrant wheel   4 Nov  1 10:43 symlinkfile2 -> file
```

修改`file`文件的内容。

```bash
echo "add oneline" >> file
```

通过命令`cat file`查看当前`file`的内容。

```bash
it's original file
add oneline
```

通过下面的命令，可以看到所以软/硬链接文件内容都更新了，和`file`文件更新后的内容保持一致。

```bash
cat hardlinkfile1
cat hardlinkfile2
cat symlinkfile1
cat symlinkfile2
```

对文件`symlinkfile1`再创建新的软连接。

```bash
ln -s symlinkfile1 symlinkfile1-1
```

通过命令`ls -il`查看现在的目录信息。

```bash
67274680 -rw-r--r--. 3 vagrant wheel 31 Nov  1 11:14 file
67274680 -rw-r--r--. 3 vagrant wheel 31 Nov  1 11:14 hardlinkfile1
67274680 -rw-r--r--. 3 vagrant wheel 31 Nov  1 11:14 hardlinkfile2
67274681 lrwxrwxrwx. 1 vagrant wheel  4 Nov  1 10:43 symlinkfile1 -> file
67274683 lrwxrwxrwx. 1 vagrant wheel 12 Nov  1 11:20 symlinkfile1-1 -> symlinkfile1
67274682 lrwxrwxrwx. 1 vagrant wheel  4 Nov  1 10:43 symlinkfile2 -> file
```

读取软链接文件的源文件信息

```bash
readlink symlinkfile1
readlink symlinkfile2
```

注意，对于`symlinkfile1-1`的情况有些不同。

```bash
readlink symlinkfile1-1
```

上面命令返回结果`symlinkfile1`仍然是一个符号链接文件。通过`readlink -f`可以直接定位真正的源文件。

```bash
readlink -f symlinkfile1-1
```

上面的返回结果`/data/linktype/file`是`symlinkfile1-1`真正的源文件。

显示`data`目录下的文件和子目录：

```bash
cd ~
tree ./data
```

运行结果：

```bash
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

```bash
tree -d ./data
```

运行结果：

```bash
./data
└── typelink
```

显示`data`目录下的文件和子目录，包含全目录：

```bash
tree -f ./data
```

运行结果：

```bash
./data
├── ./data/file
├── ./data/hardlinkfile1
├── ./data/hardlinkfile2
├── ./data/symlinkfile1 -> file
├── ./data/symlinkfile1-1 -> symlinkfile1
├── ./data/symlinkfile2 -> file
└── ./data/typelink
```

## 4.文件属性说明

执行命令`ls -ihl`，可以得到下面的输出结果（Rocky 9）。

```bash
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

```bash
$ ls -ihl
233647 -rw-r--r-- 3 vagrant wheel 31 Nov  1 15:52 file
233647 -rw-r--r-- 3 vagrant wheel 31 Nov  1 15:52 hardlinkfile1
233647 -rw-r--r-- 3 vagrant wheel 31 Nov  1 15:52 hardlinkfile2
233648 lrwxrwxrwx 1 vagrant wheel  4 Nov  1 15:52 symlinkfile1 -> file
233650 lrwxrwxrwx 1 vagrant wheel 12 Nov  1 15:52 symlinkfile1-1 -> symlinkfile1
233649 lrwxrwxrwx 1 vagrant wheel  4 Nov  1 15:52 symlinkfile2 -> file
233646 drwxr-xr-x 1 vagrant wheel  0 Nov  1 15:51 typelink
```

## 5.标准输入输出

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

```bash
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

```bash
$ cat > file.py <<EOF
import time
f = open('test.txt', 'r')
time.sleep(1000)
EOF
```

创建`test.txt`文件。

```bash
echo "hello" > test.txt
```

运行`file.py`程序。

```bash
python3 file.py
```

打开新的终端窗口，执行下面命令，得到python3这个程序运行的process ID。其中可以看到有一个来自文件test.txt被程序file.py打开（输入）。

```bash
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

```bash
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

```bash
sudo zypper in sysvinit-tools
```

由于openSUSE中pidof python3只返回一个process ID，所以可以简化命令行得到process ID的详细信息。

```bash
$ sudo ls -l /proc/`pidof python3`/fd/
lrwx------ 1 vagrant wheel 64 Nov 13 23:21 0 -> /dev/pts/0
lrwx------ 1 vagrant wheel 64 Nov 13 23:21 1 -> /dev/pts/0
lrwx------ 1 vagrant wheel 64 Nov 13 23:21 2 -> /dev/pts/0
lr-x------ 1 vagrant wheel 64 Nov 13 23:21 3 -> /home/vagrant/test.txt
```

参考：

> 当键盘和鼠标等设备通过串口直接连接到计算机时，这种连接称为TTY。
> 伪终端pseudoterminal（缩写为“pty”）是一对提供双向通信通道的虚拟字符设备。 通道的一端称为主端master； 另一端称为从端slave。
>
> `/dev/pts`表示与伪终端pseudoterminal的主端master或从端slave相关的master文件，操作系统将其保存为`/dev/ptmx`文件。 `telnet`和`ssh`等程序能够仿  端用户> 与它们的交互，虽然本质上是与文件`/dev/ptmx`进行交互，但呈现给用户的却是好像运行在真正的终端窗口一样，从端的文件是主端的输入。
>
> 伪终端进程在Linux中被存储在`/dev/pts/`目录下。`/dev/pts/`目录下的内容是一些特殊的目录，由Linux内核所创建。
>
> 每个唯一的终端窗口都与`/dev/pts`系统中的一个Linux`pts`条目相关。
>
> 下面返回的结果说明有2个远程终端连接到当前的机器。
>
> ```bash
> $ ll /dev/pts/
> crw--w----. 1 vagrant tty  136, 0 Nov 13 23:18 0
> crw--w----. 1 vagrant tty  136, 1 Nov 13 23:48 1
> c---------. 1 root    root   5, 2 Nov 13 10:41 ptmx
> ```
>
> 也可以通过`w`命令看到2个终端进程。
>
> ```bash
> $ w
>  23:55:05 up 13:14,  2 users,  load average: 0.00, 0.00, 0.00
> USER     TTY        LOGIN@   IDLE   JCPU   PCPU WHAT
> vagrant  pts/0     10:51   37:03   0.05s  0.05s -bash
> vagrant  pts/1     23:48    0.00s  0.03s  0.00s w
> ```
>
> 单个伪终端pseudoterminal可以同时接收来自不同的程序的输出。
> 多个程序同时对一个伪终端pseudoterminal进行读取会引起混淆。
>
> 存储在`/dev/pts`目录中的文件是抽象文件而不是真实文件，是伪终端中执行程序时临时存储的数据。 打开`/dev/pts`下的文件通常没有什么实际意义。

## 6.重定向和管道

### 6.1.输入重定向

常用命令格式：

* `command < file`：将指定文件`file`作为命令的输入设备。
* `command << delimiter`：表示从标准输入设备（键盘）中读入，直到遇到分界符`delimiter`停止（读入的数据不包括分界符），这里的分界符可以理解为自定义的字符串。
* `command < file1 > file2`：将`file1`作为命令的输入设备，该命令的执行结果输出到`file2`中。

```bash
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

### 6.2.输出重定向

输出重定向分为标准输出重定向和错误输出重定向两种。

常用命令格式：

* `command > file`：将命令`command`执行的标准输出结果重定向输出到指定的文件`file`中，如果该文件已包含数据，会清空原有数据，再写入新数据。
* `command 2> file`：将命令`command`执行的错误输出结果重定向到指定的文件`file`中，如果该文件中已包含数据，会清空原有数据，再写入新数据。
* `command >> file`：将命令`command`执行的标准输出结果重定向输出到指定的文件`file`中，如果该文件已包含数据，新数据将追加写入到原有内容的后面。
* `command 2>> file`：将命令`command`执行的错误输出结果重定向到指定的文件`file`中，如果该文件中已包含数据，新数据将追加写入到原有内容的后面。
* `command >> file 2>&1` 或者 `command &>> file`：将标准输出或者错误输出写入到指定文件`file`中，如果该文件中已包含数据，新数据将追加写入到原有内容的后面。

注意：上面的`file`可以是一个普通文件，也可以使用一个特殊的文件`/dev/null`。`/dev/null`并不保存数据，被写入`/dev/null`的数据最终都会丢失。

举例：2个python文件存在，其他2个无扩展名的文件不存在。

```bash
ls file.py > out
ls file 2> out.err

ls new.py >> out
ls new 2>> out.err
```

可以得到预期的结果。两个错误记录都被追加到`out.err`文件中。两个成功执行的命令的返回结果也输出到`out`文件中。

```bash
$ccat out
file.py
new.py

$ cat out.err
ls: cannot access 'file': No such file or directory
ls: cannot access 'new': No such file or directory
```

上例命令也可以合并。

```bash
ls file.py > out 2> out.err
ls file >> out 2>> out.err
```

`2>&1`格式举例：

```bash
$ ls file >> out.txt 2>&1
$ cat out.txt
ls: cannot access 'file': No such file or directory

$ ls file.py &>> out.txt
$ cat out.txt
ls: cannot access 'file': No such file or directory
file.py
```

### 6.3.特殊重定向

格式：`command1 < <(command2)`

```bash
tr 'a-z' 'A-Z' < <(echo "Hello World")
```

应用：修改密码

密码保存在`passwd.txt`文件中，并严格限制改文件的权限。
通过参数`--stdin`实现模拟键盘输入操作输入用户名。

在Rocky中可以使用`--stdin`参数。

```bash
passwd --stdin vagrant < passwd.txt
```

在openSUSE和Ubuntu中，`--stdin`参数无法识别。可以改用下面的方法。

```bash
echo passwd.txt | chpasswd
```

其中passwd.txt的格式为`username:password`。

参考：

> Here-document(Here-doc)：输入的文本块重定向至标准输入流，直至遇到特殊的文件结束标记符为止（文件结束标记符可以是任意的唯一的字符串，但大部分人都默认使用 `EOF`）。
>
> ```bash
> cat <<EOF
> This is line1
> Another line
> Finally 3rd line
> EOF
> ```
>
> 文本块中含有tab键。
>
> ```bash
> cat <<-EOF
>     This message is indented
>         This message is double indented
> EOF
> ```
>
> 文本块中含有参数。
>
> ```bash
> cat <<EOF
> Hello ${USER}
> EOF
> ```
>
> 文本块中含有命令。
>
> ```bash
> cat <<EOF
> Hello! It is currently: $(date)
> EOF
> ```
>
> Here-string：与`Here-doc`相似，但是它只有一个字符串，或者几个被引号括起来的字符串。
>
> 基本用法。
>
> ```bash
> cat <<< "This is a string"
> ```
>
> 使用变量。
>
> ```bash
> WELCOME_MESSAGE="Welcome!"
> cat <<< $WELCOME_MESSAGE
> ```
>
> 使用参数。
>
> ```bash
> cat <<< "Welcome! ${USER}"
> ```

## 7.管道

Linux中使用竖线`|`连接多个命令，这被称为管道符。

当在两个命令之间设置管道时，管道符`|`左边命令的输出就变成了右边命令的输入。管道符`|`左边正确的输出才能被右边处理，管道符`|`右边不能处理左边错误的输出。

重定向和管道的区别：重定向操作符`>`将命令与文件连接起来，用文件来接收命令的输出；而管道符`|`将命令与命令连接起来，用右边命令来接收左边命令的输出。

```bash
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
