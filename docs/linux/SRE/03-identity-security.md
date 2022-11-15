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









