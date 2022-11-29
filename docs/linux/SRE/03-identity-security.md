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


## SELinux

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


## 用户管理

用户管理命令：

* `useradd`
* `usermod`
* `userdel`


### 创建用户`useradd`

举例：
```
# 普通用户
$ useradd -m -g wheel -G root -c "vagrant" vagrant

# 非交互用户
$ useradd -r -u 48 -g apache -d /var/www -s /sbin/nologin -g postfix -c "Apache" apache 2>/dev/null
```

`useradd`命令的默认值是在`/etc/default/useradd`文件中设定。

openSUSE的`/etc/default/useradd`文件内容：
```
GROUP=100
HOME=/home
INACTIVE=-1              # 对应/etc/shadow文件第7列，Inactivity period，密码过期后的宽限期，-1表示不限制
EXPIRE=                  # 对应/etc/shadow文件第8列，Expiration date since Jan 1, 1970，即账号有效期
SHELL=/bin/bash
SKEL=/etc/skel           # 用于生成用户主目录的模版文件
USRSKEL=/usr/etc/skel
CREATE_MAIL_SPOOL=yes
```

Rocky的`/etc/default/useradd`文件内容：
```
GROUP=100
HOME=/home
INACTIVE=-1
EXPIRE=
SHELL=/bin/bash
SKEL=/etc/skel
CREATE_MAIL_SPOOL=yes
```

在Ubuntu中`/etc/default/useradd`文件只有下面这一行。
```
SHELL=/bin/sh
```

#### 批量创建用户`newusers`

格式：`newusers <filename>`。其中文件`<filename>`的格式如下：
```
<Username>:<Password>:<UID>:<GID>:<User Info>:<Home Dir>:<Default Shell>
```
举例，创建文件`users.txt`：
```
$ cat ~/users.txt
tester1:123:600:1530:"Test User1,testuser1@abc.com":/home/tester1:/bin/bash
tester2:123:601:1529:::/bin/bash
tester3:123:::::
tester4:123::::/home/tester4:/bin/tsh
```
看结果：
```
$ cat /etc/passwd | grep tester
tester1:x:600:1530:"Test User1,testuser1@abc.com":/home/tester1:/bin/bash
tester2:x:601:1529:::/bin/bash
tester3:x:1001:1001:::
tester4:x:1002:1002::/home/tester4:/bin/tsh

$ cat /etc/group | grep tester
tester1:*:1530:
tester2:*:1529:
tester3:*:1001:
tester4:*:1002:

$ sudo cat /etc/shadow | grep tester
tester1:!:19321:0:99999:7:::
tester2:!:19321:0:99999:7:::
tester3:!:19321:0:99999:7:::
tester4:!:19321:0:99999:7:::

$ ls -ld /home/tester*
drwxr-xr-x. 1 tester1 tester1 0 Nov 26 00:32 /home/tester1
drwxr-xr-x. 1 tester4 tester4 0 Nov 26 00:32 /home/tester4
```


#### 批量修改密码`chpasswd`

两个方法：
```
$ echo username:password | chpasswd
$ chpasswd < file.txt
```

参数`-e`：口令以加密的方式传递。否则口令以明文的形式传递。

注意：

* 用户名username必须是已存在的用户
* 普通用户没有使用这个指令的权限
* 如果输入文件是按非加密方式传递的话，请对该文件进行适当的加密。
* 指令文件不能有空行

举例：
```
$ echo tester1:112233 | sudo chpasswd
```
```
$ cat chpasswd.txt
tester1:112233
tester2:33445566

$ sudo chpasswd < chpasswd.txt
```

#### 生成加密密码`openssl passwd`

命令`openssl passwd`格式可以如下方法获得。
```
$ man -f passwd
passwd (1)           - change user password
passwd (1ssl)        - compute password hashes
passwd (5)           - password file

$ man passwd
Man: find all matching manual pages (set MAN_POSIXLY_CORRECT to avoid this)
 * passwd (1)
   passwd (5)
   passwd (1ssl)
Man: What manual page do you want?
Man: 1ssl
```

举例（这里用`<your_pwsswd_string>`代替实际密码）：
```
# 基于给定字串newpasswd生成sha256加密码，
$ openssl passwd -6 newpasswd
<your_pwsswd_string>

# 创建新用户tester5，赋予加密密码
$ useradd -p '<your_pwsswd_string>' tester1

# 读取用户tester5的密码，可以验证是否和之前的一致
$ sudo getent shadow tester5
tester5:<your_pwsswd_string>:19321:0:99999:7:::
```



### 修改用户属性`usermod`

添加用户到附加组
```
$ usermod -a -G GROUP USER
$ usermod -a -G GROUP1,GROUP2,GROUP3 USER
```

修改用户主组
```
$ usermod -a -g GROUP USER
```

修改用户信息
```
$ usermod -c "GECOS Comments" USER
```

修改用户主目录，使用绝对路径，`-m`参数会把原主目录的内容移动到新主目录。
```
$ usermod -d NEW_HOME_DIR USER
$ usermod -d NEW_HOME_DIR -m USER
```

修改用户shell
```
$ usermod -s SHELL USER
```

修改用户UID
```
$ usermod -u UID USER
```

修改用户名（不常用），同时也需要修改用户主目录。
```
$ usermod -l NEW_USER USER
```

修改用户过期属性，日期格式是`YYYY-MM-DD`
```
$ usermod -e DATE USER
```
如果设定永不过期，则置空日期：
```
$ usermod -e "" USER
```
查看当前用户的过期日期
```
$ sudo chage -l vagrant
Last password change					: Oct 30, 2022
Password expires					: never
Password inactive					: never
Account expires						: never
Minimum number of days between password change		: 0
Maximum number of days between password change		: 99999
Number of days of warning before password expires	: 7
```

锁定用户。
此命令将在加密密码前插入一个感叹号 (!) 标记。 当`/etc/shadow`文件中的密码字段包含感叹号时，用户将无法使用密码验证登录系统。 
其他登录方法仍然允许，例如基于密钥的身份验证或切换到用户。 
如果要锁定账户并禁用所有登录方式，还需要将到期日期设置为1。
```
$ usermod -L USER
$ usermod -L -e 1 USER
```

解锁用户
```
$ usermod -U USER
```




### 删除用户`userdel`

`userdel`命令执行时，会读取`/etc/login.defs`文件的内容。 此文件中定义的属性会覆盖`userdel`的默认行为。
如果在此文件中将`USERGROUPS_ENAB`设置为`yes`，`userdel`将删除与用户同名的组，前提是没有其他用户是该组的成员。

`userdel`命令从`/etc/passwd`和`/etc/shadow`文件中删除用户条目。

`userdel`命令删除用户帐户时，一般不会删除用户主目录和邮件假脱机mail spool目录。
使用`-r`选项强制删除用户的主目录和邮件假脱机目录。

如果要删除的用户仍然处于登录状态，或者有属于该用户的正在运行的进程，则`userdel`命令不允许删除该用户。

使用`-f`选项强制删除用户帐户，即使用户仍然登录或有属于该用户的正在运行的进程也是如此。

```
$ userdel USER
$ userdel -r USER
```



### 查看用户信息`id`

类Unix操作系统中的每个用户都由一个不同的整数标识，这个唯一的数字称为UserID。

为进程process定义了三种类型的UID，可以根据任务的权限动态更改。

定义的三种不同类型的UID是：

1. 真实用户ID（Real UserId）：对于一个进程，Real UserId就是启动它的用户的 UserID。 它定义了这个进程可以访问哪些文件。
2. 有效用户名（Effective UserID）：它通常与 Real UserID 相同，但有时会更改为使非特权用户能够访问那些只能由特权用户（如`root`）访问的文件。
3. 保存的用户ID（Saved UserID） ：当一个以提升的权限（通常是`root`）运行的进程需要做一些低权限的任务时使用，可以通过临时切换到非特权帐户来实现。在执行低权限任务时，有效的`UID`被更改为某个较低权限的值，并且`euid`被保存到已保存的`userID`(suid)中，以便在任务完成时用于切换回特权帐户。

在一个终端窗口执行下面命令，暂停在新密码输入这一步。
```
$ ls -ltr /usr/bin/passwd
-rwsr-xr-x. 1 root shadow 65208 May  8  2022 /usr/bin/passwd

$ passwd
Changing password for vagrant.
Current password:
New password:
```
新开一个终端窗口。
```
$ ps -a | grep passwd
  3040 pts/0    00:00:00 passwd

$ ps -eo pid,euid,ruid | grep 3040
  3040     0  1000
```
上面输出可以看出，`passwd`这个进程的Effective UserID是`0`。Real UserId是`1000`.


`id`命令查看用户有效的UID和GID。

查看当前用户的信息：
```
$ id
uid=1000(vagrant) gid=478(wheel) groups=478(wheel),0(root) context=unconfined_u:unconfined_r:unconfined_t:s0
```

查看指定用户的信息：
```
$ id vagrant
uid=1000(vagrant) gid=478(wheel) groups=0(root),478(wheel)
```

查看当前用户的GID：
```
$ id -g
478
```

查看当前用户的UID：
```
$ id -u
1000
```

查看当前用户所有组的GID：
```
$ id -G
478 0
```

查看当前用户名：
```
$ id -un
vagrant
```

查看当前用户的GID
```
$ id -ur
1000
```

只有SELinux激活后才有
```
$ id -Z
unconfined_u:unconfined_r:unconfined_t:s0
```

类似于`whoami`命令
```
$ id -znG
wheelroot
```


### 切换用户`su`

命令`su - username`是登录式切换用户。会读取目标用户的配置文件，切换至目标用户的主目录。

命令`su username`是非登录式切换用户。不读取目标用户的配置文件，不改变当前工作目录。

切换成root用户，并使用zsh shell。
```
$ su -s /usr/bin/zsh
$ su -s /usr/bin/zsh root
```

切换成tester1用户，使用bash shell
```
$ su - tester1 -s /bin/bash
$ su - -s /bin/bash tester1
```

保留当前用户环境不变。
```
$ su -p root
```

不交互式切换用户，只用目标用户执行某些命令。
```
$ su -c ps
$ su - root -c "getent passwd"
$ su - root -s /bin/bash -c "getent passwd"
```

`root`用户切换至其他用户不需要密码，非`root`用户切换其他用户需要密码。


### 设置密码

#### `passwd`

修改当前用户自己的密码：
```
$ passwd
```

修改其他用户的密码：
```
$ sudo passwd root
```

查看某个用户密码状态：
```
$ sudo passwd -S root
root P 10/30/2022 -1 -1 -1 -1

$ sudo passwd -S vagrant
vagrant P 10/30/2022 0 99999 7 -1
```

检查全部用户的密码状态：
```
$ sudo passwd -Sa
```

密码状态说明：
```
Username 	Status 	Date Last Changed 	Minimum Age 	Maximum Age 	Warning Period   Inactivity Period
vagrant     P       10/30/2022          0               99999           7                -1
root        P       10/30/2022          -1              -1              -1               -1
```

Status的描述：

* `P `: Usable password
* `NP`: No password
* `L `: Locked password

Age的一些特殊值：

* `9999`: Never expires
* `0`: Can be changed at anytime
* `-1`: Not active


强制要求用户下次登录时修改密码：
```
$ sudo passwd -e tester1

$ sudo passwd -S tester1
tester1 P 01/01/1970 0 99999 7 -1
```
用户tester1的密码日期已经被改成`01/01/1970`了。这个日期算是Unix的“纪元（epoch）”日期，意味着Unix的日期起点，0天。


锁定某个用户：
```
$ sudo passwd -l tester1

$ sudo passwd -S tester1
tester1 L 01/01/1970 0 99999 7 -1
```
此时用户`tester1`的状态栏已经变成了`L`，锁定状态。

解锁某个用户：
```
$ sudo passwd -u tester1

$ sudo passwd -S tester1
tester1 P 01/01/1970 0 99999 7 -1
```
此时用户`tester1`的状态栏已经从`L`变回了`P`，解除了锁定状态。


删除用户密码。这个操作慎重，密码删除后该用户可以不需要密码就能访问系统。
```
$ sudo passwd -d tester1

$ sudo passwd -S tester1
tester1 NP 01/01/1970 0 99999 7 -1
```
此时用户`tester1`的状态栏是`NP`。


#### `pwgen`

安装包。

mkpasswd命令有歧义，2个同名命令实现不同功能，生成随机密码建议使用`pwgen`命令。Rocky9没有找到pwgen包。
```
$ sudo zypper in pwgen
$ sudo apt install pwgen
```


随机生成长度8位安全密码。
```
$ pwgen -s -1
```

随机生成长度14位安全密码。
```
$ pwgen -s -1 14
```

随机生成2个长度15位安全密码。
```
$ pwgen -s -1 15 2
```

随机生成5个密码，长度10位，每个密码至少含一个特殊字符，结果以列形式输出。
```
$ pwgen -s -1 -y 10 5
```

生成长度8，含有数字，含有大小写字母的密码4个，列打印
```
$ pwgen -s -n -c -C -1 8 4
```

生成长度8，不含数字，只含小写字母，列打印
```
$ pwgen -s -c -A -0 -1 8 4
```

生成长度16，含有数字，含有大小写字母，含有特殊字符的密码3个，行打印
```
$ pwgen -s -n -c -y -1 16 3
```

生成长度80，不含元音和数字，至少含有一个大写字母，行打印
```
$ pwgen -s -v -c -0 80 1
```






#### 非交互式设置密码

方法1：
```
$ echo -e '123456\n123456' | sudo passwd tester1
New password: BAD PASSWORD: it is too simplistic/systematic
BAD PASSWORD: is too simple
Retype new password: passwd: password updated successfully
```

方法2：

Rocky中可以使用下面方法。
```
$ pwgen -ncy1 16 1 | tee passwd.txt | sudo passwd --stdin tester1
```
openSUSE和Ubuntu可以用下面方法。
```
$ echo "tester1:"`pwgen -ncy1 16 1` | tee passwd.txt | sudo chpasswd
```


方法3：根据预先给定的用户列表，批量生成密码。
```
$ cat > user-list.txt <<EOF
user0
user1
user2
user3
user4
user5
user6
user7
user8
user9
EOF

$ for i in $(cat user-list.txt); do sudo useradd $i; echo "$i:"`pwgen -s -1 15 1` | tee passwd_$i.txt | sudo chpasswd; done

$ for i in $(cat user-list.txt); do sudo userdel $i; done
```




### 设置用户密码策略

命令`chage`修改用户密码策略。

总结：

* `-d`: Last password change : 上一次密码更改的日期。
* `-M`: Password expires : 密码保持有效的最大天数。基于Last password change日期计算。设为`-1`表示不过期。
* `-I`: Password inactive : 密码失效时间，在`Password expires`后，直至账号锁定之间的天数。设为`-1`表示不过期。
* `-E`: Account expires : 帐号到期的日期。到期后，此帐号将不可用。设为`-1`表示不过期。
* `-m`: Minimum number of days between password change : 两次改变密码之间相距的最小天数。
* `-M`: Maximum number of days between password change : 两次改变密码之间相距的最大天数。
* `-W`: Number of days of warning before password expires : 用户密码到期前，提前收到警告信息的天数。



显示用户密码策略（时效信息）：
```
$ sudo chage -l tester1
Last password change					: Nov 27, 2022
Password expires					: never
Password inactive					: never
Account expires						: never
Minimum number of days between password change		: 0
Maximum number of days between password change		: 99999
Number of days of warning before password expires	: 7
```

设置用户密码的最后修改日期：
```
$ sudo chage -d 2022-11-11 tester1

$ sudo chage -l tester1
Last password change					: Nov 11, 2022
Password expires					: never
Password inactive					: never
Account expires						: never
Minimum number of days between password change		: 0
Maximum number of days between password change		: 99999
Number of days of warning before password expires	: 7
```

设置用户账号的过期日期：
```
$ sudo chage -E 2022-12-31 tester1

$ sudo chage -l tester1
Last password change					: Nov 11, 2022
Password expires					: never
Password inactive					: never
Account expires						: Dec 31, 2022
Minimum number of days between password change		: 0
Maximum number of days between password change		: 99999
Number of days of warning before password expires	: 7
```

设置用户密码最小/最大修改天数。注意，密码过期日期`Password expires`是按照max days来计算的。
```
$ sudo chage -M 35 tester1
$ sudo chage -m 30 tester1

$ sudo chage -l tester1
Last password change					: Nov 11, 2022
Password expires					: Dec 16, 2022
Password inactive					: never
Account expires						: Dec 31, 2022
Minimum number of days between password change		: 30
Maximum number of days between password change		: 35
Number of days of warning before password expires	: 7
```

设置用户账号在密码过期`Password expires`后，直至账号锁定之间的天数，即密码失效时间Password inactive。
```
$ sudo chage -I 3 tester1

$ sudo chage -l tester1
Last password change					: Nov 11, 2022
Password expires					: Dec 16, 2022
Password inactive					: Dec 19, 2022
Account expires						: Dec 31, 2022
Minimum number of days between password change		: 30
Maximum number of days between password change		: 35
Number of days of warning before password expires	: 7
```

设置用户密码到期前，提前收到警告信息的天数。默认值是7天。
```
$ sudo chage -W 5 tester1

$ sudo chage -l tester1
Last password change					: Nov 11, 2022
Password expires					: Dec 16, 2022
Password inactive					: Dec 19, 2022
Account expires						: Dec 31, 2022
Minimum number of days between password change		: 30
Maximum number of days between password change		: 35
Number of days of warning before password expires	: 5
```



## 组管理

组管理命令：

* `groupadd`
* `groupmod`
* `groupdel`
* `groupmems`


### 创建组`groupadd`

创建普通组。
```
$ sudo groupadd developers
```

创建系统组，并指定GID。
```
$ sudo groupadd -g 48 -r apache
$ sudo groupadd -g 1100 -r developers
```

覆盖配置文件`/ect/login.defs`
```
$ groupadd -K GID_MIN=500 -K GID_MAX=700
```



### 修改组`groupmod`

命令`groupmod`涉及下面这些文件：

`/etc/group`: Group Account Information.
`/etc/gshadow`: Secured group account information.
`/etc/login.def`: Shadow passwd suite configuration.
`/etc/passwd:` User account information.

组改名：
```
$ sudo groupmod -n group_new group_old
```



### 删除组`groupdel`

命令`groupdel`涉及下面这些文件：

* `/etc/group` : It contains the account information of the Group.
* `/etc/gshadow `: It contains the secure group account information.

如果组中包含有用户，则必须先删除这些用户后，才能删除组。
```
$ sudo groupdel group_name
```


### 更改组成员和密码`gpasswd`

命令`gpasswd`用来修改组成员和密码。

涉及到的文件：

* `/etc/group`: Group account information.
* `/etc/gshadow`: Secure group account information. 

给组`developers`设密码。
```
$ sudo gpasswd developers
```

取消组`developers`密码。
```
$ sudo gpasswd -r developers
```

给组`developers`添加用户。
```
$ sudo gpasswd -a tester1,tester2,tester3 developers
```

从组`developers`中删除用户。
```
$ sudo gpasswd -d tester3 developers
```

设定用户`tester1`成为组`developers`的管理员。
```
$ sudo gpasswd -A tester1 developers
```

注意：添加用户到某一个组 也可以通过`usermod -G group_name user_name`这个实现，但是该用户以前的组会被清空掉。
所以，如果要添加一个用户到一个新组，同时希望保留该用户以前的组时，使用`gpasswd`这个命令来添加用户到新组中。



### 修改组成员`groupmems`

使用命令`groupmems`，需要安装软件包。
```
# openSUSE
sudo zypper in libvshadow-tools
# Ubuntu
sudo apt install libvshadow-utils
# Rocky
sudo yum search shadow-utils
```

添加用户到组。
```
$ sudo groupmems -a tester1 -g developers
$ sudo groupmems -a tester2 -g developers

$ cat /etc/group | grep developers
developers:x:1002:tester1,tester2
```

从组中删除用户。
```
$ sudo groupmems -d tester2 -g developers

$ cat /etc/group | grep developers
developers:x:1002:tester1
```

列出组中用户。
```
$ sudo groupmems -l -g developers
tester1
```

切换当前组为`developers_sre`，添加用户`tester2`到当前组，可以不用在后续命令中使用`-g`指定组。
```
$ sudo groupmems -g developers_sre

$ sudo groupmems -a tester2

$ sudo groupmems -l
tester2
```

切换当前组为`developers_sre`，从当前组中删除所有用户（这里无法指定某用户）。
```
$ sudo groupmems -g developers_sre
$ sudo groupmems -p
```



### 查看组关系`group`


显示当前用户所属主的信息。
```
$ whoami
vagrant

$ groups
sudo adm cdrom dip plugdev lxd
```

查看指定用户所属组的信息。
```
$ groups vagrant
vagrant : sudo adm cdrom dip plugdev lxd
```


## 练习

1. 创建用户`gentoo`，附加组为`bin`和`root`，默认shell为`/bin/csh`，注释信息为"Gentoo Distribution"
```
$ sudo useradd -G bin,root -s /bin/csh -c "Gentoo Distribution" gentoo
```

2. 创建下面的用户、组和组成员关系

* 名字为`webs`的组
* 用户`nginx`，使用`webs`作为附属组
* 用户`varnish`，也使用`webs`作为附属组
* 用户`mysql`，不可交互登录系统，且不是`webs`的成员，`nginx`，`varnish`，`mysql`密码都是`opensuse`。

```
$ sudo groupadd webs
$ sudo useradd -G webs nginx
$ sudo useradd -G webs varnish
$ sudo useradd -s /sbin/nologin mysql

$ echo "nginx:opensuse" | sudo chpasswd
$ echo -e "opensuse\nopensuse" | sudo passwd varnish
$ echo "mysql:opensuse" | sudo chpasswd
```


3. 查看UID、GID范围的配置文件,修改为501-60000。并查看密码加密算法
```
$ cat /etc/login.defs
...
GID_MIN			 1000
GID_MAX			60000
...
UID_MIN			 1000
UID_MAX			60000
...
ENCRYPT_METHOD SHA512
...
```


4. 查看创建用户时的模板配置文件
```
$ cat /etc/default/useradd
# useradd defaults file
GROUP=100
HOME=/home
INACTIVE=-1
EXPIRE=
SHELL=/bin/bash
SKEL=/etc/skel
USRSKEL=/usr/etc/skel
CREATE_MAIL_SPOOL=yes
```



5. 创建一个新用户`webuser`，指定登录时起始目录`/www`，同时加入`apache`附加组中,指定UID为`999`且不检查uid唯一性。
```
$ sudo useradd -d /www -G apache -u 999 -o webuser
```


6. 修改创建用户时的默认设置，主目录/www，默认shell `csh`。查看创建用户的配置文件是否更改，若更改则恢复默认值
```
$ sudo useradd -Db /www -s /bin/csh

$ sudo cat /etc/default/useradd
# useradd defaults file
GROUP=100
HOME=/www
INACTIVE=-1
EXPIRE=
SHELL=/bin/csh
SKEL=/etc/skel
USRSKEL=/usr/etc/skel
CREATE_MAIL_SPOOL=yes

$ sudo useradd -Db /home -s /bin/bash
```


7. 批量创建用户`admin1`、`admin2`、`admin3`。
```
$ cat > user.txt <<EOF
admin1
admin2
admin3
EOF

$ for i in $(cat user.txt); do sudo useradd $i; echo "$i:"`pwgen -s -1 15 1` | tee passwd_$i.txt | sudo chpasswd; done
```

8. 只查看用户`admin2`、`admin3`在`/etc/passwd`的配置信息。
```
$ getent passwd admin2 admin3
admin2:x:1019:100::/home/admin2:/bin/bash
admin3:x:1020:100::/home/admin3:/bin/bash
```


9. 修改`admin2`用户UID为`2002`、主组`root`、添加新的附加组`apache`且保留旧的附加组。然后锁定用户。
```
$ sudo usermod -u 2002 -g root -G apache -a admin2
$ sudo usermod -L admin2

$ getent passwd admin2
admin2:x:2002:0::/home/admin2:/bin/bash

$ sudo passwd -S admin2
admin2 L 11/27/2022 0 99999 7 -1
```


10. 修改用户`admin2`用户名为`smith`，设置账号过期时间为`2022-12-31`。
```
$ sudo usermod -l smith -e 2022-12-31 admin2

$ sudo chage -l smith
Last password change					: Nov 27, 2022
Password expires					: never
Password inactive					: never
Account expires						: Dec 31, 2022
Minimum number of days between password change		: 0
Maximum number of days between password change		: 99999
Number of days of warning before password expires	: 7
```


11. 给`admin1`设置密码`hello`，然后指定新的主目录并把旧目录移动过去。
```
$ sudo usermod -d /home/admin_new -m admin1
$ echo "admin1:hello" | sudo chpasswd 
```


12. 显示`smith`用户UID、GID、显示用户名、显示用户所属组ID
```
$ id -u smith
2002

$ id -g smith
0

$ id -un smith
smith

$ id -gn smith
root
```

13. 锁定`smith`用两种方法
```
$ sudo passwd -l smith

$ sudo usermod -L smith
```


14. 指定`admin3`的密码最短使用日期为5天，最常使用日期为10天，提前2天提示修改密码。
```
$ sudo chage -M 10 -m 5 -W 2 admin3

$ sudo chage -l admin3
Last password change					: Nov 27, 2022
Password expires					: Dec 07, 2022
Password inactive					: never
Account expires						: never
Minimum number of days between password change		: 5
Maximum number of days between password change		: 10
Number of days of warning before password expires	: 2
```


15. 创建系统组`newadm`，指定GID为`66`。
```
$ sudo groupadd -r -g 66 newadm
```


16. 修改`newadm`组名为`newgrp` 修改GID为`67`。
```
$ sudo groupmod -n newgrp -g 67 newadm
```


17. 将用户`admin1`添加进组`newgrp`，然后删除组`newgrp`。
```
$ sudo usermod -g newgrp admin1
$ sudo groupdel -f newgrp
```


18. 设置`smith`用户的详细描述，然后用finger查看。
```
$ chfn smith

$ finger smith
Login: smith          			Name:
Directory: /home/admin2             	Shell: /bin/bash
Never logged in.
No Mail.
No Plan.
```


19. 删除用户`admin1`，并删除其主目录。
```
$ sudo userdel -r admin1
$ sudo userdel -r admin2
```









## 权限管理

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
  * `rw-r--r--`：文件权限，从左到右依次为：（用户的最终权限，是从左向右匹配，一旦匹配则权限立即生效，不再向右继续匹配）
    * `rw-`：文件属主权限（u），例子中是`vagrant`。
    * `r--`：文件属组的权限（g），例子中是`wheel`。
    * `r--`：其他组的权限（o）。
* `.`：这个点表示文件带有SELinux的安全上下文（SELinux Contexts）。关闭SELinux，新创建的文件就不会再有这个点了。但是，以前创建的文件本来有这个点的还会显示这个点（虽然SELinux不起作用了）。
* `3`：硬链接数，例子中`file`和`hardlinkfile1`和`hardlinkfile2`之间是硬链接，所以这三个文件的硬链接数都是`3`。
* `vagrant`：文件属主owner
* `wheel`：文件属组group
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

### 修改属主`chown`

`chown`命令修改文件属主（所有者，owner）。

修改文件属主为root。
```
$ ll f1.txt
-rw-r--r--. 1 vagrant wheel 41 Nov 14 22:23 f1.txt

$ sudo chown root f1.txt

$ ll f1.txt
-rw-r--r--. 1 root wheel 41 Nov 14 22:23 f1.txt
```

修改文件的属组为bin。
```
$ sudo chown :bin f1.txt

$ ll f1.txt
-rw-r--r--. 1 root bin 41 Nov 14 22:23 f1.txt
```

同时修改文件的属主和属组。
```
$ sudo chown vagrant.wheel f1.txt

$ ll f1.txt
-rw-r--r--. 1 vagrant wheel 41 Nov 14 22:23 f1.txt
```

参照某文件修改另一文件的属性。
```
$ ll file.py
-rw-r--r--. 1 vagrant wheel  56 Nov 13 22:50 file.py

$ ll user.txt
-rw-r--r--. 1 root bin 21 Nov 27 23:59 user.txt

$ sudo chown root.bin user.txt

$ sudo chown --reference=user.txt file.py

$ ll file.py
-rw-r--r--. 1 root bin 56 Nov 13 22:50 file.py
```

递归修改所有子目录及文件的属主和属组。
```
$ sudo chown -R vagrant.wheel /data
```





### 修改属组`chgrp`

修改目录的属组。
```
sudo chgrp bin ~/data
```

修改目录及子目录及文件的属组。
```
sudo chgrp -R bin ~/data
```


### 文件和目录权限

文件：

* `r`：可以读取该文件内容，比如通过`cat`命令。
* `w`：可以修改该文件内容，可以只有`w`而没有`r`。
* `x`：可以把该文件提请内核启动为一个进程，即可以执行该文件（该文件的内容必须是可以执行）。


目录：（对目录而言，通常需要给`r`和`x`权限）（从目录角度看，目录内文件列表等于目录节点的内容）

* `r`：能看文件列表，但不能访问所含文件的内容及其属性信息，包括inode号。
* `w`：能在该目录内创建和删除文件，不由目录内文件本身的权限决定。
* `x`：能cd进目录，能通过`ls -l file`和`stat file`查看该目录中制定文件的元数据。
* `X`：表示只有当该文件是个子目录或者该文件已经被设定过为可执行。

* 有只读权限的用户不能用cd进入该目录，还必须有执行权限才能进入。
* 有执行权限的用户只有在知道文件名，并拥有读权利的情况下才可以访问目录下的文件。
* 必须有读和执行权限才可以ls列出目录清单，或使用cd命令进入目录。
* 有目录的写权限，可以创建、删除或修改目录下的任何文件或子目录，即使使该文件或子目录属于其他用户也是如此。


常用权限例子：
```
-rw------- (600) 只有所有者才有读和写的权限
-rw-r--r-- (644) 只有所有者才有读和写的权限，组和其他人只有读的权限
-rwx------ (700) 只有所有者才有读，写，执行的权限
-rwxr-xr-x (755) 只有所有者才有读，写，执行的权限，组和其他人只有读和执行的权限
-rwx--x--x (711) 只有所有者才有读，写，执行的权限，组和其他人只有执行的权限
-rw-rw-rw- (666) 每个人都有读写的权限
-rwxrwxrwx (777) 每个人都有读写和执行的权限
```



### 权限修改`chmod`

命令格式：
```
chmod [-cfvR] [--help] [--version] mode file
```

`mode`字串格式为：
```
[ugoa][+-=][rwxXst]
```

who:

* `u`文件所有者
* `g`文件所有者所在组
* `o`其他用户
* `a`所有用户，相当于`ugo`

operator:

* `+`为指定的用户类型增加权限
* `-`去除指定用户类型的权限
* `=`设置指定用户权限的设置，即将用户类型的所有权限重新设置

permission:

* `r`设置为可读权限
* `w`设置为可写权限
* `x`设置为可执行权限
* `X`特殊执行权限，只有当文件为目录文件，或者其他类型的用户有可执行权限时，才将文件权限设置可执行
* `s`当文件被执行时，根据who参数指定的用户类型设置文件的`setuid`或者`setgid`权限
* `t`设置粘贴位，只有超级用户可以设置该位，只有文件所有者u可以使用该位。


示例：

将文件`file1.txt`设为所有人皆可读取。
```
chmod ugo+r file1.txt
```
将文件`file1.txt`设为所有人皆可读取。
```
chmod a+r file1.txt
```
将文件`file1.txt`与`file2.txt`设为该文件属主和属组都可写入，但其他用户不可写入。
```
chmod ug+w,o-w file1.txt file2.txt
```
为`ex1.py`文件属主增加可执行权限。
```
chmod u+x ex1.py
```
将目前目录下的所有文件与子目录皆设为任何人可读取。
```
chmod -R a+r *
```
给`file`的所有用户增加读权限
```
chmod a+r file
```
删除`file`的所有用户的执行权限
```
chmod a-x file
```
给`file`的所有用户增加读写权限
```
chmod a+rw file
```
给`file`的所有用户增加读写执行权限
```
chmod +rwx file
```
对`file`的属主设置读写权限，清空属组和其他用户对`file`的所有权限（空格代表无权限）
```
chmod u=rw,go= file
```
对目录`docs`和其子目录中的所有文件给属主增加读权限，而对属组和其他用户删除读权限
```
chmod -R u+r,go-r docs
```
对`file`的属主和属组设置读写权限, 为其他用户设置读权限
```
chmod 664 file
```
对`file`的属主设置读写执行权限，相当于`u=rwx`(4+2+1)，设置属组读和执行权限，相当于`go=rx`(4+1 & 4+1)。`0`没有特殊模式
```
chmod 0755 file
```
`4`设置了设置用户ID位，剩下的相当于`u=rwx`(4+2+1)和`go=rx`(4+1 & 4+1)。
```
chmod 4755 file
```
删除可执行权限对`path/`以及其所有的目录（不包括文件）的所有用户，使用`-type f`匹配文件
```
find path/ -type d -exec chmod a-x {} \;
```
允许所有用户浏览或通过目录`path/`
```
find path/ -type d -exec chmod a+x {} \;
```



### 文件和目录的默认权限

`umask`的值，定义了所有新建的文件和目录的初始权限的。

查看当前权限掩码：
```
$ umask
0022
```

在不考虑`umask`的情况下，文件的默认权限是`666`(rw-rw-rw-)，目录的默认权限是`777`(rwxrwxrwx)。

在`umask`的值为`0022`的情况下，文件的默认权限是`644`(rw-r--r--)，目录的默认权限是`755`(rwxr-xr-x)。

计算方法：
```
	Files: 
		(Default) 6 6 6
		(umask)   0 2 2
		----------------
		(Result)  6 4 4
	
  Directories: 
		(Default) 7 7 7
		(umask)   0 2 2
		----------------
    (Result)  7 5 5
```

如果`umask`的值为`0077`的情况下，文件的默认权限是`600`(rw-------)，目录的默认权限是`700`(rwx------)。

计算方法：
```
	Files: 
		(Default) 6 6 6
		(umask)   0 7 7
		----------------
		(Result)  6 0 0
	
  Directories: 
		(Default) 7 7 7
		(umask)   0 7 7
		----------------
    (Result)  7 0 0
```

举例：
```
$ umask 022
$ touch file2
$ ll file2
-rw-r--r--. 1 vagrant wheel 0 Nov 28 23:13 file2

$ umask 077
$ touch file1
$ ll file1
-rw-------. 1 vagrant wheel 0 Nov 28 23:12 file1
```
```
$ umask 022
$ mkdir ./tmp1
$ umask 077
$ mkdir ./tmp2

$ ls -dl tmp*
drwxr-xr-x. 1 vagrant wheel 0 Nov 28 23:14 tmp1
drwx------. 1 vagrant wheel 0 Nov 28 23:14 tmp2
```




### 特殊权限

除了三种常见的权限rwx，还有三种特殊权限：SUID，SGID，Sticky。

SUID：属主s权限，称为Set UID

* 前提：进程有属主和属组，文件有属主和属组
    * 任何可执行程序文件能不能启动为进程，取决于发起者对程序文件是否拥有执行权限。
    * 启动为进程之后，其进程的属主为发起者。
    * 进程访问文件是的权限，取决于进程的发起者。

* 只对二进制可执行程序文件有效。当执行该文件时，发起者将自动具有该文件所有者的权限。
* 对目录无效。

```
$ ll file1
-rw-------. 1 vagrant wheel   0 Nov 28 23:12 file1

$ sudo chmod u+s file1

$ ll file1
-rwS------. 1 vagrant wheel 0 Nov 28 23:12 file1
```

如果属主的`x`位上是-，则在属主的`x`位上标记大写`S`，否则标记小写`s`。如下：
```
$ chmod 777 file1

$ ll file1
-rwxrwxrwx. 1 vagrant wheel 0 Nov 28 23:12 file1

$ sudo chmod u+s file1

$ ll file1
-rwsrwxrwx. 1 vagrant wheel 0 Nov 28 23:12 file1
```
下面2组命令实现同样效果。
```
$ sudo chmod 4xxx file1

$ chmod 777 file1
$ sudo chmod u+s file1
```
取消SUID。
```
$ sudo chmod u-s file1
```


SGID：属组s权限，称为Set GID

* 如果作用于二进制可执行文件上，当执行该文件为进程之后，发起者将自动具有该文件所属组的权限，进程的属组为发起者的属组。
* 如果作用于目录上，则该目录下新建立的目录和文件都自动从此目录继承。

```
$ sudo chmod g+s file2

$ ll file2
-rw-r-Sr--. 1 vagrant wheel 0 Nov 28 23:13 file2
```
如果属组的`x`位上是-，则在属组的`x`位上标记大写`S`，否则标记小写`s`。如下：
```
$ chmod 777 file2

$ ll file2
-rwxrwxrwx. 1 vagrant wheel 0 Nov 28 23:13 file2

$ sudo chmod g+s file2

$ ll file2
-rwxrwsrwx. 1 vagrant wheel 0 Nov 28 23:13 file2
```

下面2组命令实现同样效果。
```
$ sudo chmod 2xxx file2

$ chmod 777 file2
$ sudo chmod g+s file2
```
取消SGID。
```
$ sudo chmod g-s file2
```

对于目录，下面演示可以看到目录下的文件和子目录的继承性。
```
$ ll -d data
drwxr-xr-x. 1 vagrant bin 0 Nov 28 20:55 data

$ sudo chmod g+s ./data

$ ll -d data
drwxr-sr-x. 1 vagrant bin 0 Nov 28 20:55 data

$ cd data
$ touch file2
$ ll file2
-rw-r--r--. 1 vagrant bin 0 Nov 29 21:10 file2

$ mkdir tmp3
$ ll -d tmp3
drwxr-sr-x. 1 vagrant bin 0 Nov 29 21:10 tmp3
```



Sticky Bit：简称为SBIT权限

* 只针对目录有效。它表示只能让其属主以及root可以删除、重命名、移动该目录下的文件。
* Sticky设置在文件上无意义。

如果其他的`x`位上是-，则在其他的`x`位上标记大写`T`，否则标记小写`t`。
```
$ ll -d ./data
drwxr-sr-x. 1 vagrant bin 18 Nov 29 21:10 ./data

$ sudo chmod o+t ./data

$ ll -d ./data
drwxr-sr-t. 1 vagrant bin 18 Nov 29 21:10 ./data

$ cd data
$ touch file1
$ mkdir tmp1

$ ll file1
-rw-r--r--. 1 vagrant bin 0 Nov 29 21:37 file1
$ ll -d tmp1
drwxr-sr-x. 1 vagrant bin 0 Nov 29 21:37 tmp1
```


特殊权限设置数字法：

设置SUID
```
              User    Group   Others
              r w s   r w s   r w x
              r w S
    BIN 100   1 1 1   1 1 1   1 1 1
              1 1 0
    OCT   4       7       7       7
                  6
```
设置SGID
```
              User    Group   Others
              r w x   r w s   r w x
              r w S
    BIN	010   1 1 1   1 1 1   1 1 1
                      1 1 0
    OCT   2       7       7       7
                          6
```
设置Sticky Bit - SBIT
```
              User    Group   Others
              r w x   r w x   r w t
                      r w T
    BIN 001   1 1 1   1 1 1   1 1 1
                              1 1 0
    OCT   1       7       7       7
                                  6
```




### 设定文件特殊属性`chattr`

命令格式：`chattr [ -RVf ] [ -v version ] [ mode ] files...`

其中mode的字串格式：`{+|-|=}[aAcCdDeijsStTu]`

属性`i`： 	

* 如果对文件设置`i`属性，那么不允许对文件进行删除、改名，也不能添加和修改数据；
* 如果对目录设置`i`属性，那么只能修改目录下文件中的数据，但不允许建立和删除文件；

在openSUSE下执行，分区文件类型是btrfs格式。
```
$ touch filetest
$ lsattr filetest
---------------------- filetest

$ chattr +i filetest
chattr: Operation not permitted while setting flags on filetest
$ sudo chattr +i filetest

$ lsattr filetest
----i----------------- filetest

$ rm filetest
rm: cannot remove 'filetest': Operation not permitted
$ sudo rm filetest
rm: cannot remove 'filetest': Operation not permitted

$ echo "test" >> filetest
-bash: filetest: Operation not permitted
$ sudo echo "test" >> filetest
-bash: filetest: Operation not permitted

$ sudo chattr -i filetest
```



属性`a`：

* 如果对文件设置`a`属性，那么只能在文件中増加数据，但是不能删除和修改数据；
* 如果对目录设置`a`属性，那么只允许在目录中建立和修改文件，但是不允许删除文件；

在openSUSE下执行，分区文件类型是btrfs格式。
```
lsattr filetest
---------------------- filetest
$ chattr +a filetest
chattr: Operation not permitted while setting flags on filetest
$ sudo chattr +a filetest

$ echo "test" >> filetest

$ rm filetest
rm: cannot remove 'filetest': Operation not permitted
$ sudo rm filetest
rm: cannot remove 'filetest': Operation not permitted

$ sudo chattr -a filetest
```


属性`u`：

* 设置此属性的文件或目录，在删除时，其内容会被保存，以保证后期能够恢复，常用来防止意外删除文件或目录。

在Ubuntu下执行，分区文件类型是ext4格式。
```
$ touch filetest
$ sudo chattr +u filetest

$ lsattr filetest
-u------------e------- filetest

$ rm filetest
```

属性`s`：

* 和`u`相反，删除文件或目录时，会被彻底删除（直接从硬盘上删除，然后用0填充所占用的区域），不可恢复。



!!! Attention
    命令`chattr`和`lsattr`的可操作属性依赖于文件所处分区的文件系统类型，ext4和xfs的结果会有不同。

	历史：命令`chattr`（用于操作属性）和`lsattr`（用于列出属性）最初专用于第二个扩展文件系统系列（ext2、ext3、ext4），并且作为`e2fsprogs`包的一部分提供。然而，此功能已全部或部分扩展到许多其他系统，包括 XFS、ReiserFS、JFS 和 OCFS2。 btrfs 文件系统包括属性功能，包括`C`标志，由于与`CoW`相关的性能较慢，它关闭了btrfs的内置写时复制 (CoW) 功能。





## 访问控制列表ACL

