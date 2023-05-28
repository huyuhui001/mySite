# 第六章 文件查找

常用文件查找命令：

## locate命令

`locate` 是一个在 Linux 系统上用于快速搜索文件和目录的命令。它使用预先构建的文件数据库`/var/lib/mlocate/mlocate.db`进行搜索，因此比直接在文件系统上搜索要快得多。

使用 `updatedb` 命令手动更新文件数据库`/var/lib/mlocate/mlocate.db`，索引构建过程需要遍历整个根文件系统，很消耗资源。
注意，由于 `locate` 使用预先构建的文件数据库，因此在更新文件数据库之前，新创建或移动的文件可能不会立即出现在搜索结果中。

在openSUSE 15中默认没有安装，需要手动安装下面的软件包。

```bash
sudo zypper ref
sudo zypper in mlocate
sudo updatedb
```

`locate` 命令的特点：

* 查找速度快
* 模糊查找
* 非实时查找
* 搜索的是文件的全路径，不仅仅是文件名
* 可能只搜索当前用户具备读取`r`和执行`x`权限的目录

`locate` 命令的格式：`locate [OPTIONS] PATTERN`

常用选项：

* `-i`：忽略大小写。
* `-r`：使用正则表达式进行模式匹配。
* `-l`：仅显示文件路径，而不显示文件名。
* `-c`：仅显示匹配结果的计数。
* `-b`：只匹配基本名称而不是全路径名。
* `-n N`：只列举前N个匹配项目。
* `-q`：安静模式，不显示任何错误信息。

`man locate`获取更多详细信息和选项说明。

举例：搜索名为 `bashrc` 的文件，注意，这里是搜索文件名或路径名中包含`bashrc`的文件

```bash
$ locate bashrc
/etc/bash.bashrc
/etc/skel/.bashrc
/home/vagrant/.bashrc
```

要搜索以 "image" 开头的文件，忽略大小写：

```bash
locate -i '^image'
```

举例：使用正则表达式搜索以`.conf`为扩展名的文件：

```bash
locate -r '\.conf$'
```

## find命令

`find`命令是实时查找工具，通过遍历指定路径完成文件查找。

特点：

* 查找速度略慢
* 精确查找
* 实时查找
* 查找条件丰富
* 可能只搜索当前用户具备读取`r`和执行`x`权限的目录

`find` 命令的格式：`find [OPTIONS] [PATH] [CONDITIONS] [ACTIONS]`

* [PATH]：指定具体目标路径，默认为当前目录。
* [CONDITIONS]：指定查找标准，可以是文件名、文件大小、文件类型、权限等，默认为找出指定路径下所有文件。
* [ACTIONS]：对符合条件的文件执行的操作，默认输出到屏幕。
* `-maxdepth level`：最大搜索目录深度，指定目录下的文件为第一级。
* `-mindepth level`：最小搜索目录深度。

举例：只搜索`/etc`目录第二级。

```bash
find /etc -maxdepth 2 -mindepth 2
```

`find`命令默认是先处理目录，再处理目录内部的文件。选项`-depth`会修改`find`命令处理优先顺序，先处理目录内部的文件，再处理目录。

根据文件名和inode查找：

* `-name "FILENAME"`：支持使用通配符，如`*`，`？`，`[]`，`[^]`，注意，通配符要用双引号。
* `-iname "FILENAME"`：不区分字母大小写。
* `-inum N`：按inode号查找。
* `-samefile NAME`：查找相同inode号的文件。
* `-links N`：链接数为`N`的文件。
* `-regex "PATTERN"`：以PATTERN匹配整个文件路径，而非文件名称。

## xargs命令
