# 身份与安全


## 用户、组、权限

用户和组

* 用户user和组group在Linux系统中以数字形式进行管理。
* 用户被分配的号码称为用户ID（UID）。 
* 每个Linux系统都有一个特权用户，即`root`用户。 `root`是系统管理员。 此用户的UID始终为0。
* 普通用户的UID编号（默认情况下）为1000。
* 每个组也分配了一个称为组ID（GID）的编号。
* 每个用户有一个主要组（primary group），有零个或者任意个附加组（supplementary group）。

以openSUSE为例：

* UID
  - 0: root
  - 1 – 99: System
  - 100 – 499: System accounts
  - ≥ 1000: Normal (unprivileged) accounts

* GID
  - 0: root
  - 1 – 99: System Groups
  - 100 – 499: Dynamically Allocated System Groups
  - ≥ 1000: Normal Groups


举例：
```
$ id postfix
uid=51(postfix) gid=51(postfix) groups=482(mail),59(maildrop),51(postfix)

$ id vagrant
uid=1000(vagrant) gid=478(wheel) groups=0(root),478(wheel)
```


!!! Reference
    UID和GID等编号规则，是在文件`/etc/login.defs`中约定的。


## SELinux & ACL

Security-Enhanced Linux (SELinux) 是一种Linux系统的安全架构，它允许管理员更好地控制谁可以访问系统。 
SELinux于2000年向开源社区发布，并于2003年集成到上游 Linux 内核中。

SELinux为系统上的应用程序、进程和文件定义了访问控制。 它使用安全策略（一组规则告诉SELinux什么可以访问或不可以访问）来强制执行策略允许的访问。

当称为主体（subject）的应用程序或进程请求访问对象（如文件）时，SELinux会检查访问向量缓存(AVC, Access Vector Cache)，其中缓存了主体和对象的权限。

如果SELinux无法根据缓存的权限做出访问决定，它会将请求发送到安全服务器。
安全服务器检查应用程序或进程和文件的安全上下文。
从SELinux策略数据库应用安全上下文（Security context），然后授予或拒绝许可。
如果权限被拒绝，`avc: denied`消息将在`/var/log.messages`中体现。

传统上，Linux和UNIX系统都使用DAC（Discretionary Access Control）。 SELinux是Linux的MAC（Mandatory Access Control）系统的一个示例。

在DAC方式下，文件和进程有自己的属主（所有者）。 用户可以拥有一个文件，一个组也可以拥有一个文件，或者其他人。 用户可以更改自己文件的权限。`root`用户对DAC系统具有完全访问控制权。 

但是在像SELinux这样的MAC系统上，对于访问的管理是通过设置策略来实现的。即使用户主目录上的DAC设置发生更改，用于防止其他用户或进程访问该目录的SELinux策略也将继续确保系统安全。

MAC方式是控制一个进程对具体文件系统上面的文件或目录是否拥有访问权限。判断进程是否可以访问文件或目录的依据，取决于SELinux中设定的很多策略规则。

访问控制列表 (ACL，Access Control List) 为文件系统提供了一种额外的、更灵活的权限机制。 它旨在协助 UNIX 文件权限。ACL允许授予任何用户或组对任何磁盘资源的权限。ACL适用于在不使某个用户成为组成员的情况下，仍旧授予一些读或写访问权限。

下面示例对比说明了SELinux和ACL在文件属性展现上的特点。

* `-rwxr-xr--  vagrant wheel` ：没有selinux上下文，没有ACL
* `-rwx--xr-x+ vagrant wheel` ：只有ACL，没有selinux上下文
* `-rw-r--r--. vagrant wheel` ：只有selinux上下文，没有ACL
* `-rwxrwxr--+ vagrant wheel` ：有selinux上下文，有ACL


### SELinux主要概念

* 用户(Users)：
    * SELinux的用户不等同与Linux用户。
    * SELinux用户以后缀`_u`结尾。

* 角色(Roles)：
    * 角色Roles是由策略Policies定义的，角色决定了使用哪个策略。
    * SELinux角色以后缀`_r`结尾。

* 类型(Types)：
    * SELinux是类型强制的，类型Types决定进程能否访问某个文件。
    * SELinux类型是以后缀`_t`结尾。

* 上下文(Contexts)：
    * 用来标记进程和文件。分别是用户Users，角色Roles，类型Types，范围Ranges。
    * 格式：`user:role:type:range`

* 文件类型(Object Classes)：
    * 每个文件类型Types都对应一套策略Policies。策略Policies决定了进程对这类文件的访问权限。
    * 访问权限有4种：
        * 创建create
        * 读取read
        * 写入write
        * 删除unlink（注意，这里不是链接的意思）

* 规则(Rules)
    * 格式：`allow user_t user_home_t:file {create read write unlink};`
    * 含义：`user_t`类型对`user_home_t`类型有创建create，读取read，写入write，删除unlink权限。




### SELinux in openSUSE

作为SELinux的替代品，2005年被Novell收购的Immunix公司开发了AppArmor。SUSE在openSUSE Leap中提供对SELinux框架的支持。这并不意味着openSUSE Leap的默认安装会在不久的将来从AppArmor切换到SELinux。

添加SELinux的源。可以从`https://download.opensuse.org/repositories/security:/SELinux/`下载对应的策略policy。
```
$ sudo zypper ar -f https://download.opensuse.org/repositories/security:/SELinux/openSUSE_Factory/ Security-SELinux
```

安装C++等基础开发包：
```
# 列出当前可安装的Pattern
sudo zypper pt

# 安装下面几个开发相关的Pattern
sudo zypper in -t pattern devel_C_C++ devel_basis devel_kernel
```

安装SELinux packages：
```
$ zypper se --search-descriptions selinux
$ sudo zypper in restorecond policycoreutils setools-console
$ sudo zypper in selinux-tools libselinux-devel
```

安装SELinux policy：
```
$ sudo zypper in selinux-policy-targeted selinux-policy-devel selinux-autorelabel
```

更新GRUB2 bootloader（GRUB2引导加载程序）：

编辑文件`/etc/default/grub`，添加下面内容到`GRUB_CMDLINE_LINUX_DEFAULT=`这一行：
```
security=selinux selinux=1
```
记录这一行的原始信息：
```
GRUB_CMDLINE_LINUX_DEFAULT="splash=silent resume=/dev/disk/by-uuid/47c36ad7-f49f-4ecd-9b72-4801c5bb3a04 preempt=full mitigations=auto quiet security=apparmor"
```
运行下面的命令生成新的GRUB2引导加载程序配置文件。
```
$ sudo grub2-mkconfig -o /boot/grub2/grub.cfg
```

编辑文件`/etc/selinux/config` 并设置 `SELINUX=permissive`来启用SElinux。这与前面GRUB2的启动配置是一致的。
如文件不存在，则创建。
```
$ sudo cat /etc/selinux/config
SELINUX=permissive
SELINUXTYPE=targeted
```

重启系统。系统启动可能需要一些时间，SELinux需要给整个文件系统重新进行标签化。

重启后，运行下面的命令来查看SELinux是否运行正常。
```
$ sudo getenforce
Permissive
```

```
$ sudo sestatus -v
SELinux status:                 enabled
SELinuxfs mount:                /sys/fs/selinux
SELinux root directory:         /etc/selinux
Loaded policy name:             targeted
Current mode:                   permissive
Mode from config file:          permissive
Policy MLS status:              enabled
Policy deny_unknown status:     allowed
Memory protection checking:     requested (insecure)
Max kernel policy version:      33

Process contexts:
Current context:                unconfined_u:unconfined_r:unconfined_t:s0
Init context:                   system_u:system_r:kernel_t:s0
/sbin/agetty                    system_u:system_r:kernel_t:s0
/usr/sbin/sshd                  system_u:system_r:kernel_t:s0

File contexts:
Controlling terminal:           unconfined_u:object_r:devpts_t:s0
/etc/passwd                     system_u:object_r:unlabeled_t:s0
/etc/shadow                     system_u:object_r:unlabeled_t:s0
/bin/bash                       system_u:object_r:unlabeled_t:s0 -> system_u:object_r:unlabeled_t:s0
/bin/login                      system_u:object_r:unlabeled_t:s0
/bin/sh                         system_u:object_r:unlabeled_t:s0 -> system_u:object_r:unlabeled_t:s0
/sbin/agetty                    system_u:object_r:unlabeled_t:s0 -> system_u:object_r:unlabeled_t:s0
/sbin/init                      system_u:object_r:unlabeled_t:s0 -> system_u:object_r:unlabeled_t:s0
/usr/sbin/sshd                  system_u:object_r:unlabeled_t:s0
```


!!! Reference
    GRUB2引导加载程序中添加的三个参数的解释：

    `security=selinux`: This option tells the kernel to use SELinux and not AppArmor.

    `selinux=1`: This option switches on SELinux.

    `enforcing=0`: This option puts SELinux in permissive mode. In this mode, SELinux is fully functional, but does not enforce any of the security settings in the policy. Use this mode for testing and configuring your system. To switch on SELinux protection, when the system is fully operational, change the option to `enforcing=1` and add `SELINUX=enforcing` in `/etc/selinux/config`. 



!!! Tips
    在首次启用SELinux后，如果只在grub2里面添加selinux=1，通过`getenforce`命令看的SELinux一直就是disabled的状态，需要手工创建/etc/selinux/config文件添加配置才行。感觉grub2里面无需设置，直接配置/etc/selinux/config文件。不确定这个想法是否正确。

    在grub2中设定selinux=1，在/etc/selinux/config文件中：
    
      * 设定SELINUX=permissive，重启后通过`getenforce`命令看到的是permissive。
      * 设定SELINUX=disabled，则重启后`getenforce`命令看到的是disabled。
    
    这说明配置文件后启动，覆盖了内核设置。
    
    注意，如果仅仅完成了上面的enable SELinux，立刻设定SELINUX=enforcing，会引起ssh无法登录，错误信息是`/bin/bash: Permission denied`。



配置SELinux。

```
sudo semanage boolean -l
```
Failed to use semanage

添加下面内容到.bashrc文件。
```
export PATH=/usr/local/bin:/home/$USER/.local/bin:$PATH
```
更新pip3.
```
pip3 install --upgrade pip
```

安装下面几个包
```
sudo zypper in libselinux libselinux-devel
sudo zypper in python3-semanage
sudo zypper in libsemanage-devel libsemanage-devel-static
sudo zypper in policycoreutils-python-utils
sudo zypper in cross-x86_64-linux-glibc-devel glibc-utils glibc-profile

sudo zypper in policycoreutils-devel
```


### SELinux in Ubuntu


### SELinux in Rocky


## 用户和组的配置文件

* `/etc/passwd`：用户及其属性信息（用户名，UID，主组ID等）
* `/etc/shadow`：用户密码机器属性
* `/etc/group`：组及其属性
* `/etc/gshadow`：组密码及其属性


### /etc/passwd

格式说明：
```
vagrant:x:1001:474:vagrant:/home/vagrant:/bin/bash
[-----] - [--] [-] [-----] [-----------] [-------]
   |    |  |    |     |          |           +--------> 7. Login shell
   |    |  |    |     |          +--------------------> 6. Home directory
   |    |  |    |     +-------------------------------> 5. GECOS or the full name of the user
   |    |  |    +-------------------------------------> 4. GID
   |    |  +------------------------------------------> 3. UID
   |    +---------------------------------------------> 2. Password
   +--------------------------------------------------> 1. Username
```

### /etc/shadow

格式说明：
```
vagrant:$6$.n.:17736:0:99999:7:::
[-----] [----] [---] - [---] ----
|         |      |   |   |   |||+-----------> 9. Unused
|         |      |   |   |   ||+------------> 8. Expiration date since Jan 1, 1970
|         |      |   |   |   |+-------------> 7. Inactivity period 密码过期后的宽限期
|         |      |   |   |   +--------------> 6. Warning period, default 7 days
|         |      |   |   +------------------> 5. Maximum password age
|         |      |   +----------------------> 4. Minimum password age
|         |      +--------------------------> 3. Last password change since Jan 1, 1970
|         +---------------------------------> 2. Encrypted Password
+-------------------------------------------> 1. Username
```


### /etc/group

格式说明：
```
audio:x:492:pulse
[---] - [-] [---]
  |   |  |    +----> 4. username-list, who have this group as their supplementary
  |   |  +---------> 3. GID
  |   +------------> 2. group-password. Real password is in /etc/gshadow
  +----------------> 1. groupname
```

### /etc/gshadow

格式说明：
```
general:!!:shelley:juan,bob
[-----] -- [-----] [------]
   |     |     |       +-------> 4. group members (in a comma delimited list)
   |     |     +---------------> 3. group adminstrators (in a comma delimited list)
   |     +---------------------> 2. encrypted password. `!`, `!!`, and null
   +---------------------------> 1. group name
```

Encrypted password

* `!`：no user is allowed to access the group using the newgrp command.
* `!!`：the same as a value of `!` — however, it also indicates that a password has never been set before. 
* null：only group members can log into the group.



### 生成随机密码
```
# 通过`/dev/urandom`生成随机数，通过`tr -dc`过滤随机数，只保留字母和数字，通过`head -c`保留指定位数
$ tr -dc '[:alnum:]' < /dev/urandom | head -c 12
xFw7vfma54D8

$ openssl rand -base64 9
I5TZXJfpd3Pg
```

### vipw/vigr/pwck/grpck命令

`vipw`和`vigr`命令分别编辑文件`/etc/passwd`和`/etc/group`。 
如果指定了`-s`标志，这些命令将分别编辑其文件的影子（安全）版本：`/etc/shadow`和`/etc/gshadow`。
`vipw`和`vigr`命令在编辑文件时会设置锁以防止文件损坏。
`vipw`和`vigr`命令会首先尝试环境变量`$VISUAL`，然后是环境变量`$EDITOR`，最后是默认编辑器`vi`。

```
$ sudo vipw
$ sudo vipw -s
$ sudo vigr
$ sudo vigr -s
```

`pwck`命令实现验证系统认证信息的完整性。 检查`/etc/passwd`和`/etc/shadow`中的所有条目每个字段是否具有正确的格式和有效数据。 系统会提示用户删除格式不正确或存在其他错误的条目。

`pwck`返回值：

* `0`: success
* `1`: invalid command syntax
* `2`: one or more bad password entries
* `3`: can’t open password files
* `4`: can’t lock password files
* `5`: can’t update password files 


`grpck`命令实现验证系统认证信息的完整性。 检查`/etc/group`和`/etc/gshadow`中的所有条目每个字段是否具有正确的格式和有效数据。 系统会提示用户删除格式不正确或存在其他错误的条目。


`grpck`返回值：

* `0`: success
* `1`: invalid command syntax
* `2`: one or more bad group entries
* `3`: can’t open group files
* `4`: can’t lock group files
* `5`: can’t update group files 


## 用户和组的管理文件

用户管理命令：

* `useradd`
* `usermod`
* `userdel`

组管理命令：

* `groupadd`
* `groupmod`
* `groupdel`

### useradd命令

`useradd`命令的默认值是在`/etc/default/useradd`文件中设定。

openSUSE和Rocky中`/etc/default/useradd`文件内容一样。
```
GROUP=100
HOME=/home
INACTIVE=-1              # 对应/etc/shadow文件第7列，Inactivity period，密码过期后的宽限期，-1表示不限制
EXPIRE=                  # 对应/etc/shadow文件第8列，Expiration date since Jan 1, 1970，即账号有效期
SHELL=/bin/bash
SKEL=/etc/skel
USRSKEL=/usr/etc/skel    # 用于生成用户主目录的模版文件
CREATE_MAIL_SPOOL=yes
```
在Ubuntu中只有下面这一行。
```
SHELL=/bin/sh
```






