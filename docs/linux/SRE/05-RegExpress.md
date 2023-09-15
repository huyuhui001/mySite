# 第五章 正则表达式

正则表达式分两类：

* 基本正则表达式（Basic Regular Expression， 又叫Basic RegEx，简称BREs）
* 扩展正则表达式（Extended Regular Expression， 又叫Extended RegEx，简称EREs）
* Perl正则表达式（Perl Regular Expression， 又叫Perl RegEx 简称PREs

基本的正则表达式和扩展正则表达式的区别就是元字符的不同。

## 5.1.基本正则表达式符号

`^`：表示以某个字符开始
`$`：表示以某个字符结尾
`.`：表示匹配一个且只匹配一个字符
`*`：表示匹配前边一个字符出现0次或者多次
`[]`：表示匹配括号内的多个字符信息,一个一个匹配
`.*`：表示匹配所有，空行也会进行匹配
`[^]`：表示不匹配括号内的每一个字符
`^$`：表示匹配空行信息
`\`：将有特殊含义的字符转义为通配符

## 5.2.扩展正则表达式符号

`+`：表示前一个字符出现一次或一次以上
`?`：表示前一个字符出现0次或者一次以上
`|`：表示或者的关系,匹配多个信息
`()`：匹配一个整体信息，也可以接后项引用
`{}`：定义前边字符出现几次

提示：
> `grep -E` 或者`egrep`只是表示扩展正则，不代表加了e就表示转义了。 当`grep`使用扩展正则的符号时候需要用`\`转义为通配符才能使用。

## 5.3.字符匹配

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

## 5.4.位置标记

位置标记锚点（position marker anchor）是标识字符串位置的正则表达式。默认情况下，正则表达式所匹配的字符可以出现在字符串中任何位置。

* `^`：行首锚定，指定了匹配正则表达式的文本必须起始于字符串的首部。
  * 例如：`^tux`能够匹配以`tux`起始的行
* `$`：行尾锚定，指定了匹配正则表达式的文本必须结束于目标字符串的尾部。
* `\<`或`\b`：词首锚定，用于单词模式匹配左侧。（单词是有字母、数字、下划线组成）
* `\>`或`\b`：词尾锚定，用于单词模式匹配右侧。（单词是有字母、数字、下划线组成）
* `^PATTERN$`：用模式PATTERN匹配整行。
* `^$`：匹配空行。
* `^[[:space:]]*$`：匹配空白行（整行）。
* `\<PATTERN\>`：匹配整个单词。（单词是有字母、数字、下划线组成）

关于行首锚定和词首锚定，对比下面例子。词尾锚定也是类似情况。
`;`和`-`都被认定为单词分隔符。

```bash
# 符合词首匹配
$ echo "tux_01-tux02" | grep '\<tux'
tux_01-tux02

# 符合词首匹配
$ echo "xut_01-tux02" | grep '\<tux'
xut_01-tux02

# 符合行首匹配
$ echo "xut_01;tux02" | grep '\<tux'
xut_01;tux02

# 符合行首匹配
$ echo "tux_01-tux02" | grep '^tux'
tux_01-tux02

# 不符合行首匹配
$ echo "xut_01-tux02" | grep '^tux'
```

## 5.5.标识符

标识符是正则表达式的基础组成部分。它定义了那些为了匹配正则表达式，必须存在（或不存在）的字符。

* `A`字符：正则表达式必须匹配该字符。
  * 例如：`A`能够匹配字符`A`。
* `.`：匹配任意一个字符。
  * 例如：`Hack.`能够匹配`Hackl`和`Hacki`，但是不能匹配`Hackl2`或`Hackil`，它只能匹配单个字符。
* `[]`：匹配中括号内的任意一个字符。中括号内可以是一个字符组或字符范围
  * 例如：`coo[kl]`能够匹配`cook`或`cool`
  * 例如：`[0-9]`匹配任意单个数字
  * 例如：`[.0-9]`匹配`.`或任意单个数字（中括号内的`.`就代表字符`.`，不代表任意单个字符）
* `[^]`：匹配不在中括号内的任意一个字符。中括号内可以是一个字符组或字符范围
  * 例如：`9[^01]`能够匹配`92`和`93`，但是不匹配`91`和`90`。
  * 例如：`A[^0-9]`匹配A以及随后除数字外的任意单个字符
* `\s`：匹配任何空白字符，包括空格、制表符、换页等。等价于`[\f\r\t\v]`
* `\S`：匹配任何非空白字符，等价于`[^\f\r\t\v]`
* `\w`：匹配一个字母、数字、下划线、汉字、其他国家文字字符，等价于`[_[:alnum:]字]`
* `\W`：匹配一个非字母、数字、下划线、汉字、其他国家文字字符，等价于`[^_[:alnum:]字]`

## 5.6.数量修饰符

一个标识符可以出现一次、多次或是不出现。数量修饰符定义了模式可以出现的次数。

* `?`：匹配之前的项0次或1次。
  * 例如：`colou?r`能够匹配`color`或`colour`，但是不能匹配`colouur`。
* `*`：匹配之前的项0次或多次。
  * 例如：`co*l`能够匹配`col`和`coool`。
  * 例如：`goo*gle`能匹配0个或多个`o`，如：`gogle`、`google`、`gooogle`、`gooooooooogle`等。
  * 例如：`gooo*gle`，则可以匹配`google`、`gooogle`、`gooooooooogle`等，对比上面等差别。
* `+`：匹配之前的项1次或多次。
  * 例如：`Rollno-9+`能够匹配`Rollno-99`和`Rollno-9`，但是不能匹配`Rollno-`。
  * 例如：`colou+r`能够匹配`colour`或`colouur`，不能匹配`color`。
  * 例如：`goo\+gle`能够匹配1个或多个`o`，如：`google`，`gooogle`，`goooogle`等。
* `.*`：匹配任意长度等任意字符。相当于通配符中的`*`。
* `{n}`：匹配之前的项`n`次。
  * 例如：`[0-9]{3}`能够匹配任意的三位数。
  * 例如：`[0-9]{3}`可以扩展为`[0-9][0-9][0-9]`。
* `{n}`：之前的项至少需要匹配`n`次。
  * 例如：`[0-9]{2,}`能够匹配任意一个两位或更多位的数字。
  * 例如：`go\{2,\}gle`能够匹配2个或者多个`o`，如`google`，`gooooogle`等，不能匹配`gogle`。
* `{n,m}`：之前的项所必须匹配的最小`n`次数和最大`m`次数。
  * 例如：`[0-9]{2,5}`能够匹配两位数到五位数之间的任意一个数字。

## 5.7.分组

有一些特殊字符可以调整正则表达式的匹配方式。

* `\`：转义字符可以转义特殊字符。
  * 例如：`a\.b`能够匹配`a.b`，但不能匹配`ajb`。因为`\`忽略了`.`的特殊意义。
* `()`：将括号中的内容视为一个整体。
  * 例如：`ma(tri)?x` 能够匹配`max`或`matrix`
  * 例如：`\(root\)+`
* 后向引用：分组括号中的模式匹配到的内容会被正则表达式引擎记录于内部变量中，这些变量名方式为：`\1`，`\2`，`\3`。
  * `\1`：表示从左侧起第一个左括号以及与之匹配的右括号之间的模式所匹配到的字符
    * 例如：`\(string1\(string2\)\)`，`\1`是`string1\(string2\)`，`\2`是`string2`
  * `\0`：表示正则表达式匹配的所有字符
* `|`：指定了一种选择结构，可以匹配`|`两边的任意一项。
  * 例如：`Oct (1st|2nd)`能够匹配`Oct 1st`或`Oct 2nd`。

举例：匹配正负数

```bash
$ echo -1 -2 12 -125 23 | grep '\-\?[0-9]\+' 
-1 -2 12 -125 3log 23 it4u

$ echo -1 -2 12 -125 3log 23 it4u | grep '\-\?[0-9]\+'
-1 -2 12 -125 3log 23 it4u

$ echo -1 -2 12 -125 3log 23 it4u | grep '\-\?[0-9]*'
-1 -2 12 -125 3log 23 it4u

$ echo -1 -2 12 -125 3log 23 it4u | grep -E '\-\?[0-9]\+'


$ echo -1 -2 12 -125 3log 23 it4u | grep -E -- '-?[0-9]+'
-1 -2 12 -125 3log 23 it4u

$ echo -1 -2 12 -125 3log 23 it4u | grep -E '(-)?[0-9]+'
-1 -2 12 -125 3log 23 it4u
```

举例：获取IP地址

```bash
ifconfig eth0
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.10.210  netmask 255.255.255.0  broadcast 192.168.10.255
        inet6 fe80::20c:29ff:fea4:e17a  prefixlen 64  scopeid 0x20<link>
        ether 00:0c:29:a4:e1:7a  txqueuelen 1000  (Ethernet)
        RX packets 7654  bytes 635932 (621.0 KiB)
        RX errors 0  dropped 1  overruns 0  frame 0
        TX packets 1934  bytes 279649 (273.0 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

$ ifconfig eth0 | grep netmask | grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}'
192.168.10.210
255.255.255.0
192.168.10.255

$ ifconfig eth0 | grep netmask | grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' | head -n 1
192.168.10.210

$ ifconfig eth0 | grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}'
192.168.10.210
255.255.255.0
192.168.10.255

ifconfig eth0 | grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' | head -n 1
192.168.10.210
```

匹配空行和非空行：

```bash
grep '^$' /etc/profile
grep -v '^$' /etc/profile
```

匹配非空行和非#开头的行：（三种方法）

```bash
grep -v '^$' /etc/profile | grep -v '^#'
grep -v '^$\|#' /etc/profile
grep '^[^$#]' /etc/profile
```

注意，如果写成下面这样，则不会过滤掉空行，`[$]`会被视为`$`符号。
所以正则表达式的元字符放在中括号`[]`内就被视为普通字符。

```bash
grep -v '^[$#]' /etc/profile
```

## 5.8.三剑客`grep`命令

格式：

* grep [OPTIONS] PATTERN [FILE...]
* grep [OPTIONS] -e PATTERN ... [FILE...]
* grep [OPTIONS] -f FILE ... [FILE...]

参数：

* `-n`：显示过滤出来的文件在文件当中的行号
* `-c`：显示匹配到的行数
* `-o`：只显示匹配到的内容
* `-q`：静默输出（一般用在shell脚本当中，通过`echo $?`查看命令执行结果，0表示成功，非0表示失败））
* `-i`：忽略大小写
* `-v`：反向查找
* `-w`：匹配某个词词：在Linux中，词为一连串字母、数字和下划线组成的字符串
* `-E`：使用扩展正则
* `-R`：递归查询
* `-l`：只打印文件路径

扩展参数：

* `-A`：显示匹配到的数据的后几n行
* `-B`：显示匹配到的数据的前几n行
* `-C`：显示匹配到的数据的前后各几n行

示例：

匹配用户：

```bash
grep root /etc/passwd
root:x:0:0:root:/root:/bin/bash

$ grep "USER" /etc/passwd

$ grep "$USER" /etc/passwd
vagrant:x:1000:478:vagrant:/home/vagrant:/bin/bash

$ grep '$USER' /etc/passwd
```

匹配关键字：

```bash
$ grep processor /proc/cpuinfo
processor       : 0
processor       : 1

$ grep -o processor /proc/cpuinfo
processor
processor

$ grep "cpu family" /proc/cpuinfo
cpu family      : 6
cpu family      : 6

$ grep -o "cpu family" /proc/cpuinfo
cpu family
cpu family
```

通过grep进行文件比较。

```bash
# 最后一行是空行
$ cat f1
a
b
1
c


# 最后一行是空行
$ cat f2
b
e
f
c
1
2


# 高亮显示相同内容的行，包含最后一行空行
$ grep -f f1 f2
b
e
f
c
1
2


# 只显示相同内容的行，包含最后一行空行
$ grep -wf f1 f2
b
c
1


# 只显示不同内容的行
$ grep -wvf f1 f2
e
f
2
```

提示：
> `grep -wvf f1 f2` 或者`grep -w -v -f f1 f2`中，`-f`只能作为最后一个参数，否则会报错。

体会基本正则和扩展正则的差异。

例1：转义。

```bash
# 下面几个命令返回的结果是一样的。
$ grep "root\|bash" /etc/passwd
$ grep -E "root|bash" /etc/passwd
$ grep -e "root" -e "bash" /etc/passwd

# 下面的命令没有匹配结果返回。
$ grep "root|bash" /etc/passwd
```

例2：下面4个命令返回同样的结果。

```bash
grep "root" /etc/passwd
grep -E "root" /etc/passwd
grep "\<root\>" /etc/passwd
grep -E "\<root\>" /etc/passwd
```

例3：行首行尾锚定。

```bash
$ grep "^\(.*\)\>.*\<\1$" /etc/passwd
$ grep -E "^(.*)\>.*\<\1$" /etc/passwd
$ egrep "^(.*)\>.*\<\1$" /etc/passwd
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
```

例4：三种方法求和计算，运用`grep`，`cut`，`bc`和`paste`命令。

```bash
$cat age
Jason=20
Tom=30
Jack=40

# 方法1
$ cat age | cut -d "=" -f 2 | tr "\n" + | grep -Eo ".*[0-9]" | bc
90

# 方法2
$ grep -Eo "[0-9]+" age | tr "\n" + | grep -Eo ".*[0-9]" | bc
90

# 方法3
$  grep -Eo "[0-9]+" age | paste -s -d "+" | bc
90
```

## 5.9.三剑客`sed`命令

`sed`是stream editor的缩写，中文称之为“流编辑器”。
`sed`命令是一个面向行处理的工具，它以“行”为处理单位，针对每一行进行处理，处理后的结果会输出到标准输出`STDOUT`，不会对读取的文件做任何修改。

`sed`的工作原理：

`sed`命令是面向“行”进行处理的，每一次处理一行内容。
处理时，`sed`会把要处理的行存储在缓冲区中，接着用`sed`命令处理缓冲区中的内容，处理完成后，把缓冲区的内容送往屏幕。接着处理下一行，这样不断重复，直到文件末尾。这个缓冲区被称为“**模式空间**”（pattern space）。

保持空间(hold space)

`sed`的保持空间像一个长期储存， 可以把获取的信息储存到其中，待后续调用。不能直接对保持空间进行操作， 而是将保持空间的内容复制或者添加到模式空间进行操作。

非交互式批量修改文件。

`sed`命令格式：

```bash
sed [option] command file
```

`option`常用选项：

* `-n`：不输出模式pattern的内容到屏幕（即不自动打印）
* `-e`：多点编辑
* `-f filename`：从指定文件读取编辑脚本
* `-r`，`-E`：使用扩展正则表达式
* `-i .bak`：备份文件并原处编辑
* `-s`：将多个文件视为独立文件，而不是单个连续的长文件流
* `-ir`： 不支持
* `-i -r`： 支持
* `-ri`： 支持
* `-ni`： 危险选项，会清空文件

`command`部分可以分为两部分：

* 范围设定，可以采用两种不同的方式来表达：
  
  * 指定行数：如：
    * `3,5`表示第3、4、5行
    * `5,$`表示第5行至文件最后一行
  * 模式匹配：如：
    * `/^[^dD]/`表示匹配行首不是以`d`或`D`开头的行

* 动作处理，下面是常用的动作：
  
  * `a`：新增， `a`后面的字串会在新的一行出现（当前行的下一行）
  * `i`：插入， `i`后面的字串会在新的一行出现（当前行的上一行）
  * `r filename`：读取指定文件`fllename`的内容，追加到当前行的下一行
  * `R filename`：读取指定文件`fllename`的一行，追加到当前行的下一行
  * `d`：删除该行
  * `p`：打印该行
  * `Ip`：忽略大小写输出
  * `w filename`：写入到指定文件filename中。
  * `s/regexp/replacement/`：取代，用replacement取代正则regexp匹配到的内容
  * `=`：为模式pattern中的匹配行打印行号
  * `!`：为模式pattern中的匹配行取反操作
  * `q`：结束或退出sed

创建一个`testfile`文件。

```bash
$ cat <<EOF > testfile
HELLO LINUX!
Linux is a free unix-type opterating system.
This is a linux testfile!
Linux test
Google
Taobao
Banbooob
Tesetfile
Wiki
EOF
```

匹配定位文件`testfile`第二行，并输出（包含匹配第二行和输出第二行）。

```bash
# nl testfile | sed '2p'
     1    HELLO LINUX!
     2    Linux is a free unix-type opterating system.
     2    Linux is a free unix-type opterating system.
     3    This is a linux testfile!
     4    Linux test
     5    Google
     6    Taobao
     7    Banbooob
     8    Tesetfile
     9    Wiki
```

匹配定位文件`testfile`第二行，不输出。

```bash
# nl testfile | sed -n '2p'
     2    Linux is a free unix-type opterating system.
```

匹配定位文件`testfile`最后一行。

```bash
$ nl testfile | sed -n '$p'
     9    Wiki
```

匹配定位文件`testfile`倒数第二行。

```bash
# sed -n "$(echo $[`cat testfile | wc -l`-1])p" testfile
Tesetfile
```

将`testfile`的内容列出第2～3行，并且打印行号。

```bash
$  nl testfile | sed -n '2,3p'
     2  Linux is a free unix-type opterating system.
     3  This is a linux testfile!
```

将`testfile`的内容从第2行开始，向后输出额外的3行，并且打印行号。

```bash
$ nl testfile | sed -n '2,+3p'
     2  Linux is a free unix-type opterating system.
     3  This is a linux testfile!
     4  Linux test
     5  Google
```

将`testfile`的内容从第2行开始，向后以2为步进单位输出所有匹配行，并且打印行号（即，从第2行开始输出偶数行）。

```bash
nl testfile | sed -n '2~2p'
     2  Linux is a free unix-type opterating system.
     4  Linux test
     6  Taobao
     8  Tesetfile
```

将`testfile`的内容从第2行开始，向后以2为步进单位删除所有匹配行，输出剩余行，并且打印行号（即，从第2行开始删除偶数行，输出奇数行）。

```bash
$ nl testfile | sed '2~2d'
     1  HELLO LINUX!
     3  This is a linux testfile!
     5  Google
     7  Banbooob
     9  Wiki
```

将`testfile`的内容输出，删除第2行和第5行，并打印行号。

```bash
$ nl testfile | sed -e '2d' -e '5d'
$ nl testfile | sed -e '2d;5d'
$ nl testfile | sed '2d;5d'
     1  HELLO LINUX!
     3  This is a linux testfile!
     4  Linux test
     6  Taobao
     7  Banbooob
     8  Tesetfile
     9  Wiki
```

将`testfile`的内容输出，输出区间是从行首`L`的行到行首`G`的行结束。不修改原文件。
如果行首匹配不到，则无结果输出；如果行尾匹配不到，则输出到文件结束。

```bash
$ sed -n '/^L/,/^G/p' testfile
Linux is a free unix-type opterating system.
This is a linux testfile!
Linux test
Google
```

将`testfile`的内容输出，且在第6行后加上`I love Linux`。不修改原文件。

```bash
$ sed -e '6a I love Linux' testfile
HELLO LINUX!
Linux is a free unix-type opterating system.
This is a linux testfile!
Linux test
Google
Taobao
I love Linux
Banbooob
Tesetfile
Wiki
```

将`testfile`的内容列出并且打印行号，且在第6行后添加`I love Linux`。不修改原文件。

```bash
$ nl testfile | sed '6a I love Linux'
$ nl testfile | sed '6a\I love Linux'
     1    HELLO LINUX!
     2    Linux is a free unix-type opterating system.
     3    This is a linux testfile!
     4    Linux test
     5    Google
     6    Taobao
I love Linux
     7    Banbooob
     8    Tesetfile
     9    Wiki
```

将`testfile`的内容列出并且打印行号，且在第3行前添加`I am a journer learner`。不修改原文件。

```bash
$ nl testfile | sed '3i\I am a journer learner'
     1    HELLO LINUX!
     2    Linux is a free unix-type opterating system.
I am a journer learner
     3    This is a linux testfile!
     4    Linux test
     5    Google
     6    Taobao
     7    Banbooob
     8    Tesetfile
     9    Wiki
```

将`testfile`的内容列出并且打印行号，且在第3行前添加三行内容`Add line 1`，`Add line 2`，`Add line 3`。用符合`\`进行换行。不修改原文件。

```bash
$ nl testfile | sed '3i\Add line 1 \
Add line 2 \
Add line 3'
     1    HELLO LINUX!
     2    Linux is a free unix-type opterating system.
Add line 1
Add line 2
Add line 3
     3    This is a linux testfile!
     4    Linux test
     5    Google
     6    Taobao
     7    Banbooob
     8    Tesetfile
     9    Wiki
```

将`testfile`的内容列出并且打印行号，且将第2-5行的内容取代成为`replaced`。不修改原文件。

```bash
$ nl testfile | sed '2,5c\replaced'
$ nl testfile | sed '2,5c replaced'
$ nl testfile | sed '2,5creplaced'
     1    HELLO LINUX!
replaced
     6    Taobao
     7    Banbooob
     8    Tesetfile
     9    Wiki
```

将`testfile`的内容列出并且打印行号，且删除第2~5行。不修改原文件。

```bash
$ nl testfile | sed '2,5d'
     1    HELLO LINUX!
     6    Taobao
     7    Banbooob
     8    Tesetfile
     9    Wiki
```

将`testfile`的内容列出并且打印行号，且删除第5行到最后一行。

```bash
$ nl testfile | sed '5,$d'
     1    HELLO LINUX!
     2    Linux is a free unix-type opterating system.
     3    This is a linux testfile!
     4    Linux test
```

匹配定位文件`testfile`中包含关键字`linux`的行。

```bash
$ sed -n '/linux/p' testfile
This is a linux testfile!
```

匹配定位命令`df`输出中以`/dev/sd`关键字开头的行。（需要转义符`\`）

```bash
$ df | sed -n '/^\/dev\/sd/p'
/dev/sda2      102750208 7077280  92055312   8% /
/dev/sda2      102750208 7077280  92055312   8% /.snapshots
/dev/sda2      102750208 7077280  92055312   8% /home
/dev/sda2      102750208 7077280  92055312   8% /opt
/dev/sda2      102750208 7077280  92055312   8% /root
/dev/sda2      102750208 7077280  92055312   8% /boot/grub2/x86_64-efi
/dev/sda2      102750208 7077280  92055312   8% /boot/grub2/i386-pc
/dev/sda2      102750208 7077280  92055312   8% /srv
/dev/sda2      102750208 7077280  92055312   8% /tmp
/dev/sda2      102750208 7077280  92055312   8% /usr/local
/dev/sda2      102750208 7077280  92055312   8% /var
```

匹配定位命令`df`输出中不以`/dev/sd`关键字开头的行。通过`!p`进行求反输出。

```bash
$ df | sed -n '/^\/dev\/sd/!p'
Filesystem     1K-blocks    Used Available Use% Mounted on
devtmpfs            4096       0      4096   0% /dev
tmpfs            1971208       0   1971208   0% /dev/shm
tmpfs             788484    9612    778872   2% /run
tmpfs               4096       0      4096   0% /sys/fs/cgroup
tmpfs             394240       0    394240   0% /run/user/1000
```

匹配定位命令`df`输出中不以`/dev/sd`和`tmp`关键字开头的行。

```bash
$ df | sed '/^\/dev\/sd/d;/^tmp/d'
Filesystem     1K-blocks    Used Available Use% Mounted on
devtmpfs            4096       0      4096   0% /dev

$ df | grep -Ev '^\/dev\/sd|^tmp'
Filesystem     1K-blocks    Used Available Use% Mounted on
devtmpfs            4096       0      4096   0% /dev
```

搜索文件`testfile`所有包含`oo`关键字的行并匹配输出。不修改原文件。

```bash
$ sed -n '/ooo/p' testfile
Banbooob

$ sed -n '/oo/p' testfile
Google
Banbooob
```

搜索文件`testfile`所有包含`oo`关键字的行并删除。不修改原文件。

```bash
$ sed '/oo/d' testfile
HELLO LINUX!
Linux is a free unix-type opterating system.
This is a linux testfile!
Linux test
Taobao
Tesetfile
Wiki
```

搜索文件`testfile`所有包含`oo`的行，把`oo`替换为`kk`，再输出这行。不修改原文件。

```bash
$ sed -n '/oo/{s/oo/kk/;p;q}' testfile
$ sed -ne '/oo/{s/oo/kk/;p;q}' testfile
Gkkgle
```

将`testfile`的每行中第一次出现`ao`的替换成`HH`。

```bash
$ sed 's/ao/HH/' testfile
HELLO LINUX!
Linux is a free unix-type opterating system.
This is a linux testfile!
Linux test
Google
THHbao
Banbooob
Tesetfile
Wiki
```

下面是把`testfile`的匹配到`ao`的行替换成`HH`。

```bash
sed '/ao/cHH' testfile
HELLO LINUX!
SUSE
This is a linux testfile!
SUSE
Google
Taobao
Banbooob
Tesetfile
Wiki
```

搜索文件`testfile`所有包含`ao`的全部替换成`HH`。`g`表示全局匹配。不修改原文件。

```bash
$ sed -e 's/ao/HH/g' testfile
$ sed 's/ao/HH/g' testfile
HELLO LINUX!
Linux is a free unix-type opterating system.
This is a linux testfile!
Linux test
Google
THHbHH
Banbooob
Tesetfile
Wiki
```

在文件`/etc/passwd`中查找匹配所有符合`r`开头`t`结尾且中间含任意两个字符的行，并在`t`字母后添加`er`。

```bash
$ sed -nr 's/r..t/&er/gp' /etc/passwd
rooter:x:0:0:rooter:/rooter:/bin/bash
lp:x:493:487:Printering daemon:/var/spool/lpd:/usr/sbin/nologin
tftp:x:487:474:TFTP account:/srv/terftpboot:/bin/false
vagranter:x:1000:478:vagranter:/home/vagranter:/bin/bash
tester1:x:600:1530:"Test User1,terestuser1@abc.com":/home/tester1:/bin/bash
```

将上述结果和原始内容进行对比，能更好的理解`s/r..t/&er`的操作。

```bash
rooter:x:0:0:rooter:/rooter:/bin/bash
root:x:0:0:root:/root:/bin/bash

lp:x:493:487:Printering daemon:/var/spool/lpd:/usr/sbin/nologin
lp:x:493:487:Printing daemon:/var/spool/lpd:/usr/sbin/nologin

tftp:x:487:474:TFTP account:/srv/terftpboot:/bin/false
tftp:x:487:474:TFTP account:/srv/tftpboot:/bin/false

vagranter:x:1000:478:vagranter:/home/vagranter:/bin/bash
vagrant:x:1000:478:vagrant:/home/vagrant:/bin/bash

tester1:x:600:1530:"Test User1,terestuser1@abc.com":/home/tester1:/bin/bash
tester1:x:600:1530:"Test User1,testuser1@abc.com":/home/tester1:/bin/bash
```

体会`&`的位置不同的不同含义。

```bash
# 附加在root单词后
$ sed -n 's/root/&superman/p' /etc/passwd
rootsuperman:x:0:0:root:/root:/bin/bash

# 附加在root单词前
$ sed -n 's/root/superman&/p' /etc/passwd
supermanroot:x:0:0:root:/root:/bin/bash
```

使用参数`-i`进行源文件修改。

```bash
$ sed -i 's/ao/HH/' testfile
$ cat testfile
HELLO LINUX!
Linux is a free unix-type opterating system.
This is a linux testfile!
Linux test
Google
THHbao
Banbooob
Tesetfile
Wiki
```

源文件修改前，备份在新文件`testfile.new`。

```bash
$ sed -i.new 's/ao/HH/' testfile

$ cat testfile.new
HELLO LINUX!
Linux is a free unix-type opterating system.
This is a linux testfile!
Linux test
Google
Taobao
Banbooob
Tesetfile
Wiki

$ cat testfile
HELLO LINUX!
Linux is a free unix-type opterating system.
This is a linux testfile!
Linux test
Google
THHbao
Banbooob
Tesetfile
Wiki
```

范例：除指定文件外，其余都删除。

```bash
$ touch {1..9}file.txt

$ ls
1file.txt  2file.txt  3file.txt  4file.txt  5file.txt  6file.txt  7file.txt  8file.txt  9file.txt

$ ls | grep -E '(3|5|7)file\.txt'
3file.txt
5file.txt
7file.txt

$ ls | grep -Ev '(3|5|7)file\.txt'
1file.txt
2file.txt
4file.txt
6file.txt
8file.txt
9file.txt
```

下面四种方法实现同样的功能

```bash
$ rm `ls | grep -Ev '(3|5|7)file\.txt'`
$ ls | sed -n '/^[357]file.txt/!p' | xargs rm
$ ls | grep -Ev '(3|5|7)file\.txt' | sed -n 's/.*/rm &/p' | bash
$ ls | grep -Ev '(3|5|7)file\.txt' | sed -En 's/(.*)/rm &/p' | bash
$ ls | grep -Ev '(3|5|7)file\.txt' | sed -En 's/(.*)/rm \1/p' | bash

$ ls
3file.txt  5file.txt  7file.txt
```

后向引用`\0` `\1` `\2`等。

```bash
$ $echo 123456789 | sed -nE 's/(123)(456)(789)/\1/p'
123

$  echo 123456789 | sed -nE 's/(123)(456)(789)/\2/p'
456

$ echo 123456789 | sed -nE 's/(123)(456)(789)/\3/p'
789

$ echo 123456789 | sed -nE 's/(123)(456)(789)/\3\1\2/p'
789123456

$ echo 123456789 | sed -nE 's/(123)(456)(789)/\1xyz\2/p'
123xyz456
```

范例：获取分区利用率

```bash
$ df | sed -En '/^\/dev\/sd/p'
/dev/sda2      102750208 7079236  92053692   8% /
/dev/sda2      102750208 7079236  92053692   8% /.snapshots
/dev/sda2      102750208 7079236  92053692   8% /boot/grub2/i386-pc
/dev/sda2      102750208 7079236  92053692   8% /boot/grub2/x86_64-efi
/dev/sda2      102750208 7079236  92053692   8% /home
/dev/sda2      102750208 7079236  92053692   8% /opt
/dev/sda2      102750208 7079236  92053692   8% /root
/dev/sda2      102750208 7079236  92053692   8% /srv
/dev/sda2      102750208 7079236  92053692   8% /usr/local
/dev/sda2      102750208 7079236  92053692   8% /tmp
/dev/sda2      102750208 7079236  92053692   8% /var

$ df | sed -En '/^\/dev\/sd/s@.*([0-9]+)%.*@\1@p'
$ df | sed -En '/^\/dev\/sd/s#.*([0-9]+)%.*#\1#p'
# df | sed -En '/^\/dev\/sd/s/.*([0-9]+)%.*/\1/p'
8
8
8
8
8
8
8
8
8
8
8
```

体会下面空格和括弧带来的不同。

```bash
$ df | sed -En '/^\/dev\/sd/s# .*([0-9]+)%.*# \1#p'
/dev/sda2 8
/dev/sda2 8
/dev/sda2 8
/dev/sda2 8
/dev/sda2 8
/dev/sda2 8
/dev/sda2 8
/dev/sda2 8
/dev/sda2 8
/dev/sda2 8
/dev/sda2 8

$ df | sed -En '/^\/dev\/sd/s#( .*)([0-9]+)%.*# \1#p'
/dev/sda2       102750208 7079804  92053156
/dev/sda2       102750208 7079804  92053156
/dev/sda2       102750208 7079804  92053156
/dev/sda2       102750208 7079804  92053156
/dev/sda2       102750208 7079804  92053156
/dev/sda2       102750208 7079804  92053156
/dev/sda2       102750208 7079804  92053156
/dev/sda2       102750208 7079804  92053156
/dev/sda2       102750208 7079804  92053156
/dev/sda2       102750208 7079804  92053156
/dev/sda2       102750208 7079804  92053156

$ df | sed -En '/^\/dev\/sd/s#( .*)([0-9]+)%.*# \2#p'
/dev/sda2 8
/dev/sda2 8
/dev/sda2 8
/dev/sda2 8
/dev/sda2 8
/dev/sda2 8
/dev/sda2 8
/dev/sda2 8
/dev/sda2 8
/dev/sda2 8
/dev/sda2 8
```

范例：取得当前IP地址。

```bash
$ ifconfig eth0
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.10.210  netmask 255.255.255.0  broadcast 192.168.10.255
        inet6 fe80::20c:29ff:fea4:e17a  prefixlen 64  scopeid 0x20<link>
        ether 00:0c:29:a4:e1:7a  txqueuelen 1000  (Ethernet)
        RX packets 22923  bytes 1658298 (1.5 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 3763  bytes 442641 (432.2 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

$ ip addr show eth0
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:0c:29:a4:e1:7a brd ff:ff:ff:ff:ff:ff
    altname enp2s1
    altname ens33
    inet 192.168.10.210/24 brd 192.168.10.255 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::20c:29ff:fea4:e17a/64 scope link
       valid_lft forever preferred_lft forever


$ ifconfig eth0 | sed -En '2s/[^0-9]+([0-9.]+).*/\1/p'
$ ifconfig eth0 | sed -En '2s/^[^0-9]+([0-9.]{7,15}).*/\1/p'
$ ifconfig eth0 | sed -En '2s/^[^0-9]+([0-9.]{7,15}).*$/\1/p'
$ ifconfig eth0 | sed -n '2s/^.*inet //p' | sed -n 's/netmask.*//p'
$ ifconfig eth0 | sed -n '2s/^.*inet //;s/ netmask.*//p'
$ ifconfig eth0 | sed -En '2s/(.*inet )([0-9].*)(netmask.*)/\2/p'
192.168.10.210
192.168.10.210
192.168.10.210
```

使用`\0`输出全部变量。

```bash
$ ifconfig eth0 | sed -En '2s/(.*inet )([0-9].*)(netmask.*)/\0/p'
        inet 192.168.10.210  netmask 255.255.255.0  broadcast 192.168.10.255

$ ifconfig eth0 | sed -En '2s/(.*inet )([0-9].*)(netmask.*)/\1/p'
        inet

$ ifconfig eth0 | sed -En '2s/(.*inet )([0-9].*)(netmask.*)/\2/p'
192.168.10.210

$ ifconfig eth0 | sed -En '2s/(.*inet )([0-9].*)(netmask.*)/\3/p'
netmask 255.255.255.0  broadcast 192.168.10.255
```

对比下面两个指令的匹配差异。

```bash
$ ifconfig eth0 | sed -n '2s/^.*inet //p' | sed -n 's/ netmask.*//p'
192.168.10.210

$ ifconfig eth0 | sed -n '2s/^.*inet //p' | sed -n 's/netmask.* //p'
192.168.10.210  192.168.10.255

$ ifconfig eth0 | sed -n '2s/^.*inet //p' | sed -n 's/netmask .*//p'
192.168.10.210

$ ifconfig eth0 | sed -n '2s/^.*inet //p' | sed -n 's/netmask.*//p'
192.168.10.210
```

范例：取基名和目录名。
（`/etc/sysconfig/network-scripts/`目录在Rocky9中默认已创建，在openSUSE和Ubuntu中没有）

```bash
# 取目录名
$ echo "/etc/sysconfig/network-scripts/" | sed -E 's#(^/.*/)([^/]+/?)#\1#'
$ echo "/etc/sysconfig/network-scripts/" | sed -E 's/(^\/.*\/)([^\/]+\/?)/\1/'
/etc/sysconfig/
# 取基名
$ echo "/etc/sysconfig/network-scripts/" | sed -E 's#(^/.*/)([^/]+/?)#\2#'
$ echo "/etc/sysconfig/network-scripts/" | sed -E 's/(^\/.*\/)([^\/]+\/?)/\2/'
network-scripts/

# 取目录名
$ echo "/etc/sysconfig/network-scripts/dummyfile" | sed -E 's#(^/.*/)([^/]+/?)#\1#'
$ echo "/etc/sysconfig/network-scripts/dummyfille" | sed -E 's/(^\/.*\/)([^\/]+\/?)/\1/'
/etc/sysconfig/network-scripts/
# 取基名
$ echo "/etc/sysconfig/network-scripts/dummyfile" | sed -E 's#(^/.*/)([^/]+/?)#\2#'
$ echo "/etc/sysconfig/network-scripts/dummyfille" | sed -E 's/(^\/.*\/)([^\/]+\/?)/\2/'
dummyfille
```

范例：取文件名和文件扩展名

```bash
$ echo 1_.file.tar.gz | sed -En 's/(.*)\.([^.]+)$/\1/p'
$ echo 1_.file.tar.gz | sed -En 's@(.*)\.([^.]+)$@\1@p'
1_.file.tar

$ echo 1_.file.tar.gz | sed -En 's/(.*)\.([^.]+)$/\2/p'
$ echo 1_.file.tar.gz | sed -En 's@(.*)\.([^.]+)$@\2@p'
gz
```

```bash
$ echo 1_.file.tar.gz | grep -Eo '.*\.'
1_.file.tar.

$ echo 1_.file.tar.gz | grep -Eo '[^.]+$'
gz
```

范例：将非`#`开头的行添加`#`

```bash
$ cat <<EOF > testfile
HELLO LINUX!
Linux is a free unix-type opterating system.
This is a linux testfile!
Linux test
Google
Taobao
Banbooob
#Tesetfile
#Wiki
EOF

$ sed -En 's/^[^#]/#&/p' testfile
$ sed -En 's/^[^#](.*)/#\1/p' testfile
#HELLO LINUX!
#Linux is a free unix-type opterating system.
#This is a linux testfile!
#Linux test
#Google
#Taobao
#Banbooob
```

范例：将`#`开头的行删除`#`

```bash
$ cat <<EOF > testfile
HELLO LINUX!
Linux is a free unix-type opterating system.
This is a linux testfile!
Linux test
Google
Taobao
Banbooob
#Tesetfile
#Wiki
EOF

$ sed -Ei.bak '/^#/s/^#//' testfile

$ cat testfile
HELLO LINUX!
Linux is a free unix-type opterating system.
This is a linux testfile!
Linux test
Google
Taobao
Banbooob
Tesetfile
Wiki
```

`sed`保持空间（hold space）的例子：

* `d`：删除pattern space的内容，开始下一个循环。

* `D`：如果模式空间保护换行符，则删除直到第一个换行符到模式空间中的文本，并不读取新的输入行，而使用合成的模式空间重新启动循环。如果模式空间不包含换行符，则类似`d`命令启动正常的新循环。

* `h`、 `H`：复制/追加模式空间的内容到保持空间。

* `g`、 `G`：复制/追加保持空间的内容到模式空间。

* `n`、`N`：复制/追加匹配到的下一行到模式空间。

* p：打印当前模式空间内容。

* P：打印模式空间开头至`\n`的内容，并追加到默认输出之前。

* `x`：交换保持空间和模式空间的内容.

举例解读1：

1. `seq 10`命令输出1～10个数字，每个数字一行。

2. `sed`命令读取第一行`1`到模式空间。因为参数`-n`，所以读取到的`1`不打印到屏幕。

3. 执行`n`命令，即读取匹配到的下一行到模式空间，即把第二行的`2`读取并覆盖到模式空间。

4. 执行`p`命令，把`2`输出到屏幕。

5. 以此类推，读取第三行的`3`到模式空间，执行`n`命令，将第四行的`4`读取并覆盖到模式空间。执行`p`命令，输出`4`到屏幕。

6. 以此类推。

```bash
$ seq 10 | sed -n 'n;p'
2
4
6
8
10

seq 10 | sed 'n;p'
1
2
2
3
4
4
5
6
6
7
8
8
9
10
10
```

举例解读2：

* `seq 10`命令输出1～10个数字，每个数字一行。

* `sed`命令读取第一行到`1`到模式空间（覆盖）。

* 执行命令`N`，即读取下一行，即第二行的`2`，追加到模式空间。所以当前模式空间有`1`和`2`这2行记录。

* 执行`s/\n//`，把模式空间中的第一行的`1`后面的`\n`替换为空，即，原来模式空间的两行`1`和`2`现在合并为一行，即`12`。

* 读取第三行的`3`到模式空间（覆盖）。

* 执行命令`N`，即读取下一行，即第四行的`4`，追加到模式空间。所以当前模式空间有`3`和`4`这2行记录。

* 执行`s/\n//`，把模式空间中的第一行`3`后面的`\n`替换为空，即，原来模式空间的两行`3`和`4`现在合并为一行，即`34`。

* 以此类推。

```bash
$ seq 10 | sed 'N;s/\n//'
12
34
56
78
910
```

举例解读3：

* `seq 10`命令输出1～10个数字，每个数字一行。

* `sed`命令读取第一行到`1`到模式空间（覆盖）。

* 执行`!G`，即对第一行的`1`不执行`G`命令。

* 执行`h`命令，即把`1`从模式空间覆盖至保持空间。至此，保持空间和模式空间都存有`1`。

* 执行`$!d`，即不是最后一行就从模式空间删除，所以把`1`从模式空间中删除。

* `sed`命令读取第二行到`2`到模式空间（覆盖）。

* 执行`!G`，即对第二行的`2`执行`G`命令，把`1`从保持空间追加到模式空间。至此，保持空间存有`1`，模式空间存有`2`和`1`。

* 执行`h`命令，即把`2`和`1`从模式空间覆盖至保持空间。至此，保持空间和模式空间都存有`2`和`1`。

* 执行`$!d`，即不是最后一行就从模式空间删除，所以把`2`和`1`从模式空间中删除。

* 以此类推，直至读取最后一行10。此时，模式空间是`10`，保持空间存有`9`、`8`、`7`、`6`、`5`、`4`、`3`、`2`、`1`。

* 执行`!G`，即对最后一行的`10`执行`G`命令，把`9`、`8`、`7`、`6`、`5`、`4`、`3`、`2`、`1`从保持空间追加到模式空间。至此，保持空间存有`9`、`8`、`7`、`6`、`5`、`4`、`3`、`2`、`1`。，模式空间存有`10`、`9`、`8`、`7`、`6`、`5`、`4`、`3`、`2`、`1`。

* 执行`h`命令，即把`10`、`9`、`8`、`7`、`6`、`5`、`4`、`3`、`2`、`1`从模式空间覆盖至保持空间。至此，保持空间和模式空间都存有`10`、`9`、`8`、`7`、`6`、`5`、`4`、`3`、`2`、`1`。

* 执行`$!d`，当前是最后一行，所以不从模式空间删除当前内容。

* 输出模式空间内容至屏幕。即10～1。

```bash
$ seq 10 | sed '1!G;h;$!d'
10
9
8
7
6
5
4
3
2
1
```

其他一些例子：

```bash
$ seq 10 | sed -n '/3/{g;1!p;};h'
2
$ seq 10 | sed -nr '/3/{n;p}'
4
$ seq 10 | sed 'N;D'
10
$ seq 10 | sed '3h;9G;9!d'
9
3
$ seq 10 | sed '$!N;$!D'
9
10
$ seq 10 | sed '$!d'
10
$ seq 10 | sed 'G'
1

2

3

4

5

6

7

8

9

10

$ seq 10 | sed 'g'










$ seq 10 | sed '/^$/d;G'
1

2

3

4

5

6

7

8

9

10

$ seq 10 | sed 'n;d'
1
3
5
7
9
$ seq 10 | sed -n '1!G;h;$p'
10
9
8
7
6
5
4
3
2
1
```

## 5.10.三剑客`awk`命令

`awk`是一个文本分析工具。`grep`擅长查找，`sed`擅长编辑，`awk`擅长数据分析并生成报告。

`awk`的名称得自于它的创始人Alfred Aho 、Peter Weinberger 和 Brian Kernighan 姓氏的首个字母。

`awk`有3个不同版本: `awk`、`nawk`和`gawk`。我们说的`awk`一般指`gawk`。`gawk` 是`awk`的GNU版本。

`awk`把文件逐行读入，以空格为默认分隔符将每行切片，再对切片进行分析处理。

### 5.10.1.命令格式

`awk 'pattern{action statements;...}' {filenames}`

* `pattern`表示`awk`在数据中查找的内容。是要表示的正则表达式，用斜杠括起来。

* `action`是在找到匹配内容时所执行的一系列命令。

* `-F`：指定分隔符，后面紧跟单引号，单引号内是分隔符。如不加`-F`选项，则以空格或者tab作为分隔符。

* `-v`：var=value，变量赋值。

提示：

* `-F ""`指定空字符串作为字段分隔符，从而将输入字符串中的每个字符作为一个独立的字段进行处理。然后，使用循环遍历每个字段，如果字段中包含数字，则将其添加到str1变量中。最后，打印str1的值。
* `-F ''`中的两个单引号之间没有提供有效的字段分隔符。在awk中，字段分隔符必须是一个非空字符串。

示例：第一个和第三个命令是正确的。

```bash
$ echo 'Yd$@C#M05MD9&8923+Vip3wZ!33*44&55'|awk -F "" '{for(i=1;i<=NF;i++){if($i ~ /[[:digit:]]/){str=$i;str1=(str1 str)}};print str1}'
05989233334455
$ echo 'Yd$@C#M05MD9&8923+Vip3wZ!33*44&55'|awk -F"" '{for(i=1;i<=NF;i++){if($i ~ /[[:digit:]]/){str=$i;str1=(str1 str)}};print str1}'

$ echo 'Yd$@C#M05MD9&8923+Vip3wZ!33*44&55'|awk -F '' '{for(i=1;i<=NF;i++){if($i ~ /[[:digit:]]/){str=$i;str1=(str1 str)}};print str1}'
05989233334455
$ echo 'Yd$@C#M05MD9&8923+Vip3wZ!33*44&55'|awk -F'' '{for(i=1;i<=NF;i++){if($i ~ /[[:digit:]]/){str=$i;str1=(str1 str)}};print str1}'

```

### 5.10.2.工作过程

1. 执行BEGIN{action;...}语句块中的语句。

   1. BEGIN语句块再awk读入输入流之前被执行。

   2. 是可选语句块。

   3. 包含初始化变量，打印输出表格的表头等语句。

2. 从文件或者标准输入stdin读取一行，然后执行pattern{action;...}语句块。从第一行开始到最后一行，逐行扫描文件，重复这个动作，直到文件或者输入流全部被读取完毕。

   1. 可选语句块。

   2. 如果没有提供pattern语句块，则默认执行{print}。

3. 当读至文件或者输入流末尾时，执行END{action;...}语句块，比如打印所有行的分析结果这类汇总信息。也是一个可选语句块。

### 5.10.3.分隔符、域和记录

* 有分隔符分隔的字段（列column，域field），标记`$1`、`$2`、`$3`、...、`$n`称为域标识，`$0`为所有域。注意，和shell变量中的`$`不同。

* 每一行成为记录（record）。

* 如果省略action，则默认执行`print $0`操作。

### 5.10.4.常用action分类

* Output statements: `print`, `printf`

* Expressions: 算术、比较表达式

* Compund statements: 组合语句

* Control statements: `if`, `while`语句

* Input statements:

动作`print`

格式：`print item1, item2, ...`

说明：

* 逗号分隔符

* 输出item可以是字符串，也可以是数值，是当前记录的字段、变量或`awk`表达式。

* 如果省略item，相当于`print $0`

* 固定字符需要用双引号，而变量和数字不需要。

示例：

```bash
$ seq 5 |awk '{print "hello awk"}'
hello awk
hello awk
hello awk
hello awk
hello awk

$ seq 5 |awk '{print 3*5}'
15
15
15
15
15

$ awk -F':' '{print "hello"}' /etc/passwd |head -5
hello
hello
hello
hello
hello

$ awk -F':' '{print}' /etc/passwd |head -5
root:x:0:0:root:/root:/bin/bash
messagebus:x:499:499:User for D-Bus:/run/dbus:/usr/bin/false
systemd-network:x:497:497:systemd Network Management:/:/usr/sbin/nologin
systemd-timesync:x:496:496:systemd Time Synchronization:/:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/var/lib/nobody:/bin/bash

$ awk -F':' '{print $0}' /etc/passwd |head -5
root:x:0:0:root:/root:/bin/bash
messagebus:x:499:499:User for D-Bus:/run/dbus:/usr/bin/false
systemd-network:x:497:497:systemd Network Management:/:/usr/sbin/nologin
systemd-timesync:x:496:496:systemd Time Synchronization:/:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/var/lib/nobody:/bin/bash

$ awk -F':' '{print $1,$3}' /etc/passwd |head -5
root 0
messagebus 499
systemd-network 497
systemd-timesync 496
nobody 65534

$ awk -F':' '{print $1"\t"$3}' /etc/passwd |head -5
root    0
messagebus    499
systemd-network    497
systemd-timesync    496
nobody    65534


$ grep "^UUID" /etc/fstab |awk '{print $2,$3}'
/ btrfs
/var btrfs
/usr/local btrfs
/tmp btrfs
/srv btrfs
/root btrfs
/opt btrfs
/home btrfs
/boot/grub2/x86_64-efi btrfs
/boot/grub2/i386-pc btrfs
/.snapshots btrfs
swap swap
```

示例：读取分区利用率。

分隔符中的定义`[[:space:]]+|%`的含义，一个或多个空格或者`%`作为分隔符。

```bash
$ df |awk '{print $1,$5}'
Filesystem Use%
devtmpfs 0%
tmpfs 0%
tmpfs 2%
tmpfs 0%
/dev/sda2 8%
/dev/sda2 8%
/dev/sda2 8%
/dev/sda2 8%
/dev/sda2 8%
/dev/sda2 8%
/dev/sda2 8%
/dev/sda2 8%
/dev/sda2 8%
/dev/sda2 8%
/dev/sda2 8%
tmpfs 0%

$ df |grep '^/dev/sd' |awk -F'[[:space:]]+|%' '{print $1,$5}'
$ df |grep '^/dev/sd' |awk -F' +|%' '{print $1,$5}'
/dev/sda2 8
/dev/sda2 8
/dev/sda2 8
/dev/sda2 8
/dev/sda2 8
/dev/sda2 8
/dev/sda2 8
/dev/sda2 8
/dev/sda2 8
/dev/sda2 8
/dev/sda2 8
```

示例：读取ifconfig输出结果中的ip地址。

```bash
$ ifconfig eth0 | sed -n '2p' |awk '/netmask/{print $2}'
192.168.10.210

$ ifconfig eth0 | sed -n '2p' |awk '{print $2}'
192.168.10.210
```

### 5.10.5.模式Pattern

根据pattern条件，过滤匹配的行，再做处理。

* 如果未指定，即空模式，则匹配每一行。

* `/regular expression/`，仅处理能够模式匹配到的行（即结果为真），需要用`/`进行括起来。
  
  * 结果为真，即非0值、非空字符串
  
  * 结果为假，即0值、空字符串

示例：空模式

```bash
awk -F":" '{print $1, $3}' /etc/passwd |head -n5
root 0
messagebus 499
systemd-network 497
systemd-timesync 496
nobody 65534
```

示例：非空模式

```bash
$ seq 5 | awk '0'
$ seq 5 | awk '1'
1
2
3
4
5
$ seq 5 | awk '2'
1
2
3
4
5
$ seq 5 | awk '"true"'
1
2
3
4
5
$ seq 5 | awk '"false"'
1
2
3
4
5
$ seq 5 | awk 'true'
$ seq 5 | awk 'false'
$ seq 5 | awk ''
$ seq 5 | awk '""'
$ seq 5 | awk '"0"'
1
2
3
4
5
```

体会下面变量的值和正确使用变量（字符串还是变量？）

```bash
$ seq 5 | awk '"test"'
1
2
3
4
5
$ seq 5 | awk 'test'
$ seq 5 | awk -v test=0 '"test"'
$ seq 5 | awk -v test=0 'test'
$ seq 5 | awk -v test="0" 'test'
$ seq 5 | awk -v test="0" '"test"'
1
2
3
4
5
$ seq 5 | awk -v test=1 'test'
1
2
3
4
5
```

体会下面的与非判断。

```bash
$ awk '1' /etc/passwd |head -n3
root:x:0:0:root:/root:/bin/bash
messagebus:x:499:499:User for D-Bus:/run/dbus:/usr/bin/false
systemd-network:x:497:497:systemd Network Management:/:/usr/sbin/nologin
$ awk '0' /etc/passwd |head -n3
$ awk '!1' /etc/passwd |head -n3
$ awk '!0' /etc/passwd |head -n3
root:x:0:0:root:/root:/bin/bash
messagebus:x:499:499:User for D-Bus:/run/dbus:/usr/bin/false
systemd-network:x:497:497:systemd Network Management:/:/usr/sbin/nologin
```

```bash
# i没有赋值，为假，没有输出
$ seq 5 |awk 'i'
# i赋值为0，为假，没有输出
$ seq 5 |awk 'i=0'
# i赋值为1，为真，输出第一行结果，以此类推，每行都为真，输出全部seq的结果
$ seq 5 |awk 'i=1'
1
2
3
4
5
# 第一次初始i未赋值，为假，!i则为真，赋值给i，所以i为真,输出seq第1行结果
# 第二次初始i为真，!i则为假，赋值给i，所以i为假，不输出seq第2行结果
# 第三次初始i为假，!i则为真，赋值给i，所以i为真，输出seq第3行结果
# 以此类推，输出seq结果的奇数行
$ seq 5 |awk 'i=!i'
1
3
5
# 与上例的区别在于i初始值未真，第一次的i值为假，不输出seq第1行结果
# 第二次i的初始值为假，通过i=!i变为真，所以输出seq的第2行结果
# 以此类推，输出seq结果的偶数行
$ seq 5 |awk -v i=1 'i=!i'
2
4
# 输出计数行
$ seq 5 |awk -v i=0 'i=!i'
1
3
5
# 只输出i的值，不输出seq的值
$ seq 5 |awk '{i=!i;print i}'
1
0
1
0
1
$ seq 5 |awk '{i=!i}'
$ seq 5 |awk '(i=!i)'
1
3
5
$ seq 5 |awk '!(i=!i)'
2
4
```

### 5.10.6.截取片段

示例：

```bash
$ head -n2 /etc/passwd |awk -F ':' '{print $0}'
root:x:0:0:root:/root:/bin/bash
messagebus:x:499:499:User for D-Bus:/run/dbus:/usr/bin/false

$ head -n2 /etc/passwd |awk -F ':' '{print $2}'
x
x

$ head -n2 /etc/passwd |awk -F ':' '{print $1}'
root
messagebus
```

```bash
$ head -n2 /etc/passwd |awk -F ':' '{print $1"#"$2"#"$3"#"$4}'
root#x#0#0
messagebus#x#499#499
```

### 5.10.7.操作符

#### 5.10.7.1.算数操作符

`x+y`，`x-y`，`x*y`，`x/y`，`x^y`，`x%y`。

`-x`：转换为负数

`+x`：将字符串转换为数值

列值之间进行算术运算。

```bash
$ awk -F ':' '{$7=$3+$4;print $1,$3,$4,$7}' /etc/passwd |head -n5
root 0 0 0
messagebus 499 499 998
systemd-network 497 497 994
systemd-timesync 496 496 992
nobody 65534 65534 131068
```

计算某个列的总和。 `END`表示所有的行都已经执行。

```bash
$ awk -F ':' '{(total=total+$3)}; END {print total}' /etc/passwd
103011
```

#### 5.10.7.2.字符串操作符

没有操作符号，字符串连接。

#### 5.10.7.3.赋值操作符

`=`，`+=`，`-=`，`*=`，`/=`，`%=`，`^=`，`++`，`--`。

示例：

```bash
$ awk 'BEGIN{print i}'

$ awk 'BEGIN{print i++}' #从0开始
0
$ awk 'BEGIN{print ++i}'
1

$ awk 'BEGIN{print i++, i}'
0 1
$ awk 'BEGIN{i=0;print i++, i}'
0 1

$ awk 'BEGIN{print ++i, i}'
1 1
$ awk 'BEGIN{i=0;print ++i, i}'
1 1

$ awk 'BEGIN{i=0;print i, i++}'
0 0
$ awk 'BEGIN{i=0;print i, ++i}'
0 1
```

```bash
$ seq 10
1
2
3
4
5
6
7
8
9
10
# n从0开始计数，输出的是n值，不是seq的输出结果
$ seq 10 |awk '{print n++}'
0
1
2
3
4
5
6
7
8
9
# seq=1时，初始n未赋值，为假，不输出seq结果，n++为真
# seq=2时，n为真，输出seq结果，n++为真
# 后续n++都为真，所以seq的结果出了第一行由于n为假没有输出，其他行都输出
$ seq 10 |awk 'n++'
2
3
4
5
6
7
8
9
10
# 参考上例，n初始未赋值，但执行++n后为真，所以输出第一行，后续行都输出因为n一直为真
$ seq 10 |awk '++n'
1
2
3
4
5
6
7
8
9
10
```

```bash
# n=0时++n=1，!++n=0，输出第0行
$ awk -v n=0 '!++n' /etc/passwd

# n=0时n++=1，!n++=1，输出第1行
$ awk -v n=0 '!n++' /etc/passwd
root:x:0:0:root:/root:/bin/bash

$ awk -v n=0 '!n++{print n}' /etc/passwd
1
# 无结果输出
$ awk -v n=0 '!++n{print n}' /etc/passwd
$ awk -v n=1 '!n++{print n}' /etc/passwd

$ awk -v n=0 '!n++' /etc/passwd
root:x:0:0:root:/root:/bin/bash
# 无结果输出
$ awk -v n=1 '!n++' /etc/passwd
$ awk -v n=2 '!n++' /etc/passwd
```

#### 5.10.7.4.比较操作符

使用 `==` 代表等于，即精确匹配。类似还有 `>`、`>=`、`<`、`<=`、`!=`符号。

以`:`为分隔符，匹配第三列的值为`1000`的行。

```bash
$ awk -F ':' '$3=="100"' /etc/passwd
vagrant:x:1000:478:vagrant:/home/vagrant:/bin/bash
```

在和数字比较时，若把要比较的数字用双引号引起来，`awk`会按字符处理，不加双引号，则会按数字处理。

```bash
$ awk -F ':' '$3<="100"' /etc/passwd
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/usr/sbin/nologin

$ awk -F ':' '$3<=100' /etc/passwd
root:x:0:0:root:/root:/bin/bash
postfix:x:51:51:Postfix Daemon:/var/spool/postfix:/usr/sbin/nologin
man:x:13:62:Manual pages viewer:/var/lib/empty:/usr/sbin/nologin
daemon:x:2:2:Daemon:/sbin:/usr/sbin/nologin
at:x:25:25:Batch jobs daemon:/var/spool/atjobs:/usr/sbin/nologin
bin:x:1:1:bin:/bin:/usr/sbin/nologin
```

```bash
awk -F ':' '{if ($1=="root") {print $0}}' /etc/passwd
```

```bash
awk -F ':' '$7!="/bin/false"' /etc/passwd
awk -F ':' '$3<$2' /etc/passwd
```

#### 5.10.7.5.逻辑操作符

 `&&` 表示“并且”

 `||`表示“或者”

 `!`表示“非”（取反）

```bash
awk -F ':' '$3>10 && $3<100' /etc/passwd
awk -F ':' '$3>10 || $3<100' /etc/passwd
awk -F ':' '($3==0)' /etc/passwd
awk -F ':' '!($3==0)' /etc/passwd
```

注意下面对字符和数值进行取反操作的结果。

```bash
$ awk 'BEGIN{print i}'

$ awk 'BEGIN{print !i}'
1
$ awk -v i=10 'BEGIN{print i}'
10
$ awk -v i=10 'BEGIN{print !i}'
0
$ awk -v i=-5 'BEGIN{print i}'
-5
$ awk -v i=-5 'BEGIN{print !i}'
0
$ awk -v i="abc" 'BEGIN{print i}'
abc
$ awk -v i="abc" 'BEGIN{print !i}'
0
$ awk -v i=abc 'BEGIN{print i}'
abc
$ awk -v i=abc 'BEGIN{print !i}'
0
$ awk -v i="" 'BEGIN{print i}'

$ awk -v i="" 'BEGIN{print !i}'
1
```

在分隔符定义中使用正则表达式。

```bash
$ df |awk -F" +|%" '{print $5}'
Use
0
0
2
0
8
8
8
8
8
8
8
8
8
8
8
0
$ df |awk -F"[[:space:]]+|%" '{print $5}'
Use
0
0
2
0
8
8
8
8
8
8
8
8
8
8
8
0
```

#### 5.10.7.6.三目条件表达式

格式：`selector?if-true-expression:if-false-expression`

```bash
$ awk -F':' '{$3>1000?usertype="Common User":usertype="Superuser";printf"%-20s:%12s\n", $1, usertype}' /etc/passwd |head -n5
root                :   Superuser
messagebus          :   Superuser
systemd-network     :   Superuser
systemd-timesync    :   Superuser
nobody              : Common User
```

#### 5.10.7.8.模式匹配符

`~`：左右是否匹配

`!~`：左右是否不匹配

示例：

匹配文件中指定字符串`root`的所有行，类似grep命令，但没有高亮显示。

```bash
$ awk '/root/' /etc/passwd
root:x:0:0:root:/root:/bin/bash
```

以`:`为分隔符，匹配第一列`$1`中包含指定字符串`oo`的行。`~`是代表左右匹配。

```bash
$ awk -F ':' '$1 ~/oo/' /etc/passwd
root:x:0:0:root:/root:/bin/bash
gentoo:x:1014:100:Gentoo Distribution:/home/gentoo:/bin/csh
```

以`:`为分隔符，匹配所有列`$0`（整行）中包含`root`行的第一列`$1`。

```bash
$ awk -F: '$0 ~/root/{print $1}' /etc/passwd
$ awk -F: '$0 ~"root"{print $1}' /etc/passwd
root
daemon
_cvmsroot
```

以`:`为分隔符，匹配所有列`$0`（整行）中以`root`开头行的第一列`$1`。

```bash
$ awk -F: '$0 ~"^root"{print $1}' /etc/passwd
$ awk -F: '$0 ~/^root/{print $1}' /etc/passwd
root
```

以`:`为分隔符，匹配所有列`$0`（整行）中不以`root`开头行的第一列`$1`。

```bash
awk -F: '$0 !~/^root/{print $1}' /etc/passwd
awk -F: '$0 ~/^[^root]/{print $1}' /etc/passwd
```

多条件匹配，以`:`为分隔符，匹配所有含有`root`或`ftp`的行，并打印第1、3列。

```bash
awk -F ':' '/root/ {print $1,$3} /bin/ {print $1,$3}' /etc/passwd
```

多条件匹配，以`:`为分隔符，匹配第一列中含有`root`或`bin`的行，并打印第1、3列。

```bash
$ awk -F ':' '$1 ~/root/ {print $1,$3} $1 ~/bin/ {print $1,$3}' /etc/passwd
root 0
bin 1
```

以`:`为分隔符，匹配第三列`$3`中值为`0`的行。

```bash
$ awk -F":" '$3==0' /etc/passwd
root:x:0:0:root:/root:/bin/bash
```

以至少一个空格或%为分隔符，匹配以`/dev/sd`开头的行，打印第五列。

```bash
$ df |awk -F"[[:space:]]+|%" '$0 ~ /^\/dev\/sd/{print $5}'
8
8
8
8
8
8
8
8
8
8
8
```

读取`ifconfig eth0`输出结果的第二行`NR==2`的第二列`$2`。

```bash
$ ifconfig eth0 |awk 'NR==2{print $2}'
192.168.10.210
```

### 5.10.8.变量

#### 5.10.8.1.内置变量

`awk`常用的变量有`FS`、`OFS`、`NF` 和 `NR`。

`FS`用来定义输入字段分隔符，默认为空白字符。与`-F` 选项功能类似，同时使用会报错。

`OFS`用来定义输出字段分隔符，默认为空白字符。

`RS`指定输入时的换行符。

`ORS`指定符号在输出时替换换行符。

`NF` 表示用分隔符分隔后一共有多少列。

`NR` 表示行号。

`FNR`表示个文件分别计数各自记录的编号。

`FILENAME`表示当前文件名。

`ARGC`表示命令行参数的个数。

`ARVC`以数组形式保存命令行所给定的各参数，每个参数：`ARGV[0]`，......。

`FS`的用法：

```bash
$ awk -v FS=':' '{print $1, FS, $3}' /etc/passwd | head -n5
root : 0
messagebus : 499
systemd-network : 497

$ awk -F: '{print $1FS$3}' /etc/passwd | head -n3
root:0
messagebus:499
systemd-network:497
```

```bash
$ S=:;awk -v FS=$S '{print $1FS$3}' /etc/passwd | head -n3
root:0
messagebus:499
systemd-network:497
systemd-timesync:496
nobody:65534

$ S=:;awk -F$S '{print $1FS$3}' /etc/passwd | head -n3
root:0
messagebus:499
systemd-network:497
```

`FS`和 `-F` 选项功同时使用会冲突，`-F`的优先级更高。

```bash
$ awk -v FS=':' -F';' '{print $1FS$3}' /etc/passwd | head -n3
root:x:0:0:root:/root:/bin/bash;
messagebus:x:499:499:User for D-Bus:/run/dbus:/usr/bin/false;
systemd-network:x:497:497:systemd Network Management:/:/usr/sbin/nologin;

$ awk -v FS=';' -F':' '{print $1FS$3}' /etc/passwd | head -n3
root:0
messagebus:499
systemd-network:497
```

`OFS`的用法：

以`:`为分隔符，打印第1、3、4列第内容，并以`#`为分隔符。

```bash
$ awk -F ':' '{OFS="#"} {print $1,$3,$4}' /etc/passwd | head -n5
root#0#0
messagebus#499#499
systemd-network#497#497
systemd-timesync#496#496
nobody#65534#65534

$ awk -v FS=':' -v OFS='#' '{print $1,$3,$4}' /etc/passwd | head -n5
root#0#0
messagebus#499#499
systemd-network#497#497
systemd-timesync#496#496
nobody#65534#65534
```

以`:`为分隔符，当第三列大于等于5000时，打印第1、2、3、4列第内容，并以`#`为分隔符。

```bash
$ awk -F ':' '{OFS="#"} {if ($3>=5000) {print $1,$2,$3,$4}}' /etc/passwd
nobody#x#65534#65534
```

`RS`的用法：

```bash
# 以空格为换行标志
$ awk -v RS=' ' '{print $0}' /etc/passwd |head -n3
root:x:0:0:root:/root:/bin/bash
messagebus:x:499:499:User
for

# 以冒号为换行标志
$ awk -v RS=':' '{print $0}' /etc/passwd |head -n3
root
x
0
```

`ORS`的用法：

```bash
# 以冒号为换行标志，替换成###
$ awk -v RS=':' -v ORS='###' '{print $0}' /etc/passwd |head -n3
root###x###0###0###root###/root###/bin/bash
messagebus###x###499###499###User for D-Bus###/run/dbus###/usr/bin/false
systemd-network###x###497###497###systemd Network Management###/###/usr/sbin/nologin
```

`NF` 的用法：

其中 `NF` 是多少列，`$NF` 是最后一列的值。

下例中以`:`为分隔符一共分为7列，最后一列的值是`$NF`。

```bash
$ awk -F ':' '{print $NF}' /etc/passwd | head -n2
/bin/bash
/usr/bin/false

$ awk -F ':' '{print NF}' /etc/passwd | head -n2
7
7
```

```bash
$ ss -nt |grep "^ESTAB" |awk -F"[[:space:]]+|:" '{print $(NF-2)}'
192.168.10.103

$ ss -nt |awk -F"[[:space:]]+|:" '/^ESTAB/{print $(NF-2)}'
192.168.10.103
```

`NR` 的用法：

通过`NR`输出行号。以`:`为分隔符，打印前三行的行号。

```bash
$ awk -F ':' '{print NR}' /etc/passwd |head -n3
1
2
3
```

取奇、偶数行。

```bash
$ seq 10 |awk 'NR%2==0'
2
4
6
8
10
$ seq 10 |awk 'NR%2==1'
1
3
5
7
9
```

通过`NR`设定行号条件。以`:`为分隔符，打印第40行以后的行内容。

```bash
$ awk 'NR>45' /etc/passwd
admin3:x:1020:100::/home/admin3:/bin/bash
smith:x:2002:0:,,,:/home/admin2:/bin/bash
pm1:x:2003:1535::/home/pm1:/bin/bash
tm1:x:2004:1535::/home/tm1:/bin/bash
tm2:x:2005:1536::/home/tm2:/bin/bash

$ awk -F ':' 'NR>45' /etc/passwd
admin3:x:1020:100::/home/admin3:/bin/bash
smith:x:2002:0:,,,:/home/admin2:/bin/bash
pm1:x:2003:1535::/home/pm1:/bin/bash
tm1:x:2004:1535::/home/tm1:/bin/bash
tm2:x:2005:1536::/home/tm2:/bin/bash

$ awk -F ':' 'NR>45 {print NR,$1,$3}' /etc/passwd
46 admin3 1020
47 smith 2002
48 pm1 2003
49 tm1 2004
50 tm2 2005

$ awk -F ':' 'BEGIN{print NR}' /etc/passwd
0

$ awk -F ':' 'END{print NR}' /etc/passwd
50
```

```bash
$ ifconfig eth0 |awk '/netmask/{print $0}'
        inet 192.168.10.210  netmask 255.255.255.0  broadcast 192.168.10.255

$ ifconfig eth0 |awk '/netmask/{print $1}'
inet

$ ifconfig eth0 |awk '/netmask/{print $2}'
192.168.10.210

$ ifconfig eth0 |awk 'NR==2{print $0}'
        inet 192.168.10.210  netmask 255.255.255.0  broadcast 192.168.10.255

$ ifconfig eth0 |awk 'NR==2{print $1}'
inet

$ ifconfig eth0 |awk 'NR==2{print $2}'
192.168.10.210
```

通过`NR` 与列匹配一起使用。

```bash
$ awk -F ':' 'NR<5 && $1 ~/roo/' /etc/passwd
root:x:0:0:root:/root:/bin/bash
```

`FNR`的用法：

```bash
$ awk '{print FNR}' /etc/fstab /etc/networks
1
2
3
4
5
6
7
8
9
10
11
12
1
2
3
4
5
6
7
8
9
10
```

```bash
$ awk '{print NR, $0}' /etc/fstab /etc/networks
1 UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /                       btrfs  defaults                      0  0
2 UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /var                    btrfs  subvol=/@/var                 0  0
3 UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /usr/local              btrfs  subvol=/@/usr/local           0  0
4 UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /tmp                    btrfs  subvol=/@/tmp                 0  0
5 UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /srv                    btrfs  subvol=/@/srv                 0  0
6 UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /root                   btrfs  subvol=/@/root                0  0
7 UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /opt                    btrfs  subvol=/@/opt                 0  0
8 UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /home                   btrfs  subvol=/@/home                0  0
9 UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /boot/grub2/x86_64-efi  btrfs  subvol=/@/boot/grub2/x86_64-efi  0  0
10 UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /boot/grub2/i386-pc     btrfs  subvol=/@/boot/grub2/i386-pc  0  0
11 UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /.snapshots             btrfs  subvol=/@/.snapshots          0  0
12 UUID=47c36ad7-f49f-4ecd-9b72-4801c5bb3a04  swap                    swap   defaults                      0  0
13 #
14 # networks    This file describes a number of netname-to-address
15 #        mappings for the TCP/IP subsystem.  It is mostly
16 #        used at boot time, when no name servers are running.
17 #
18
19 loopback    127.0.0.0
20 link-local    169.254.0.0
21
22 # End.

$ awk '{print FNR, $0}' /etc/fstab /etc/networks
1 UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /                       btrfs  defaults                      0  0
2 UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /var                    btrfs  subvol=/@/var                 0  0
3 UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /usr/local              btrfs  subvol=/@/usr/local           0  0
4 UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /tmp                    btrfs  subvol=/@/tmp                 0  0
5 UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /srv                    btrfs  subvol=/@/srv                 0  0
6 UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /root                   btrfs  subvol=/@/root                0  0
7 UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /opt                    btrfs  subvol=/@/opt                 0  0
8 UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /home                   btrfs  subvol=/@/home                0  0
9 UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /boot/grub2/x86_64-efi  btrfs  subvol=/@/boot/grub2/x86_64-efi  0  0
10 UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /boot/grub2/i386-pc     btrfs  subvol=/@/boot/grub2/i386-pc  0  0
11 UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /.snapshots             btrfs  subvol=/@/.snapshots          0  0
12 UUID=47c36ad7-f49f-4ecd-9b72-4801c5bb3a04  swap                    swap   defaults                      0  0
1 #
2 # networks    This file describes a number of netname-to-address
3 #        mappings for the TCP/IP subsystem.  It is mostly
4 #        used at boot time, when no name servers are running.
5 #
6
7 loopback    127.0.0.0
8 link-local    169.254.0.0
9
10 # End.
```

`FILENAME`的用法：

```bash
$ awk '{print FILENAME}' /etc/fstab
/etc/fstab
/etc/fstab
/etc/fstab
/etc/fstab
/etc/fstab
/etc/fstab
/etc/fstab
/etc/fstab
/etc/fstab
/etc/fstab
/etc/fstab
/etc/fstab

$ awk '{print FNR, FILENAME, $0}' /etc/fstab /etc/networks
1 /etc/fstab UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /                       btrfs  defaults                      0  0
2 /etc/fstab UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /var                    btrfs  subvol=/@/var                 0  0
3 /etc/fstab UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /usr/local              btrfs  subvol=/@/usr/local           0  0
4 /etc/fstab UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /tmp                    btrfs  subvol=/@/tmp                 0  0
5 /etc/fstab UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /srv                    btrfs  subvol=/@/srv                 0  0
6 /etc/fstab UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /root                   btrfs  subvol=/@/root                0  0
7 /etc/fstab UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /opt                    btrfs  subvol=/@/opt                 0  0
8 /etc/fstab UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /home                   btrfs  subvol=/@/home                0  0
9 /etc/fstab UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /boot/grub2/x86_64-efi  btrfs  subvol=/@/boot/grub2/x86_64-efi  0  0
10 /etc/fstab UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /boot/grub2/i386-pc     btrfs  subvol=/@/boot/grub2/i386-pc  0  0
11 /etc/fstab UUID=5ffa8dbd-473e-4308-804a-0033c3b5f7af  /.snapshots             btrfs  subvol=/@/.snapshots          0  0
12 /etc/fstab UUID=47c36ad7-f49f-4ecd-9b72-4801c5bb3a04  swap                    swap   defaults                      0  0
1 /etc/networks #
2 /etc/networks # networks    This file describes a number of netname-to-address
3 /etc/networks #        mappings for the TCP/IP subsystem.  It is mostly
4 /etc/networks #        used at boot time, when no name servers are running.
5 /etc/networks #
6 /etc/networks
7 /etc/networks loopback    127.0.0.0
8 /etc/networks link-local    169.254.0.0
9 /etc/networks
10 /etc/networks # End.
```

`ARGC`的用法：

每个变量的名字通过`ARGV`获取。

```bash
$ awk '{print ARGC}' /etc/fstab /etc/issue
3
3
3
3
3
3
3
3
3
3
3
3
3
3
3
3
3

$ awk 'BEGIN{print ARGC}' /etc/fstab /etc/issue
3
```

`ARGV`的用法：

```bash
$ awk 'BEGIN{print ARGV[0]}' /etc/fstab /etc/issue
awk
$ awk 'BEGIN{print ARGV[1]}' /etc/fstab /etc/issue
/etc/fstab
$ awk 'BEGIN{print ARGV[2]}' /etc/fstab /etc/issue
/etc/issue
$ awk 'BEGIN{print ARGV[3]}' /etc/fstab /etc/issue
```

#### 5.10.8.2.自定义变量

自定义变量是区分字符大小写的，使用下面的方式进行赋值。

* -v var=value

* 在program中直接定义

举例：

```bash
$ awk -v t1=t2="hello awk" 'BEGIN{print t1, t2}'
t2=hello awk
$ awk -v t1=t2="hello awk" 'BEGIN{t1=t2="gawk"; print t1, t2}'
gawk gawk
$ awk 'BEGIN{t1=t2="hello awk"; print t1, t2}'
hello awk hello awk
```

```bash
$ awk -v t1="hello awk" '{print t1}' /etc/issue
hello awk
hello awk
hello awk
hello awk
hello awk
$ awk -v t1="hello awk" 'BEGIN{print t1}' /etc/issue
hello awk
$ awk -v t1="hello awk" 'BEGIN{print t1}'
hello awk
```

```bash
$ awk -F: '{sex="male"; print $1, sex, age; age=28}' /etc/passwd |head -n3
root male
messagebus male 28
systemd-network male 28
```

```bash
$ cat <<EOF > awkscript
{print script,$1,$2}
EOF

$ awk -F: -f awkscript script="awk" /etc/passwd |head -n2
awk root x
awk messagebus x
```

动作`printf`。

动作printf可以实现格式化输出。

格式：`printf "FORMAT", item1, item2, ......`

说明：

* 必须指定FORMAT

* 不会自动换行，需要显式给出换行控制符`\n`。

* FORMAT中需要分别为后面每个item指定格式符。

格式符：与item是一一对应的

* `%s`：显示字符串

* `%d`, `%i`：显示十进制整数

* `%f`：显示为浮点数

* `%e`, `%E`：显示科学计数法数值

* `%c`：显示字符的ASCII码

* `%g`, `%G`：以科学计数法或浮点形式显示数值

* `%u`：无符号整数

* `%%`：显示`%`自身

修饰符：

* `#[.#]`：第一个数字控制显示的宽度，第二个#表示小数点后精度，如`%3.1f`

* `-`：左对齐（默认右对齐），如`%-15s`

* `+`：显示数值的正负符号，如`%+d`

示例：

```bash
$ awk -F: '{printf "%s", $1}' /etc/passwd |head -n3
rootmessagebussystemd-networksystemd-timesyncnobodymailchronypostfixmanlpgamesftpdaemonrpcnscdpolkitdattftpftpsecurebinstatdsshdvagrantpesignsvntester1tester2tester3tester4tester5user0user1user2user3user4user5user6user7user8user9gentoonginxvarnishmysqlwebuseradmin3smithpm1tm1tm2

$ awk -F: '{printf "%s\n", $1}' /etc/passwd |head -n3
root
messagebus
systemd-network

$ awk -F: '{printf "%20s\n", $1}' /etc/passwd |head -n3
                root
          messagebus
     systemd-network

$ awk -F: '{printf "%-20s\n", $1}' /etc/passwd |head -n3
root
messagebus
systemd-network

$ awk -F: '{printf "%-20s %10d\n", $1, $3}' /etc/passwd |head -n3
root                          0
messagebus                  499
systemd-network             497
```

```bash
$ awk -F: '{printf "Username: %s\n", $1}' /etc/passwd |head -n3
Username: root
Username: messagebus
Username: systemd-network

$ awk -F: '{printf "Username: %s UID:%d\n", $1, $3}' /etc/passwd |head -n3
Username: root UID:0
Username: messagebus UID:499
Username: systemd-network UID:497

$ awk -F: '{printf "Username: %25s UID:%d\n", $1, $3}' /etc/passwd |head -n3
Username:                      root UID:0
Username:                messagebus UID:499
Username:           systemd-network UID:497

$ awk -F: '{printf "Username: %-25s UID:%d\n", $1, $3}' /etc/passwd |head -n3
Username: root                      UID:0
Username: messagebus                UID:499
Username: systemd-network           UID:497
```

### 5.10.9.BEGIN/END

示例：

```bash
awk -F":" 'BEGIN{printf "--------------------------------\n%-20s|%10s|\n--------------------------------\n", "Username", "UID"}{printf "%-20s|%-10d|\n--------------------------------\n", $1, $3}END{print "end"}' /etc/passwd
--------------------------------
Username            |       UID|
--------------------------------
root                |0         |
--------------------------------
daemon              |1         |
--------------------------------
bin                 |2         |
-------------------------------
... ...
--------------------------------
mfe                 |997       |
--------------------------------
end
```

### 5.10.10.常用控制语句

* {statements;...} 组合语句

* if(condition){statements;...}

* if(condition){statements;...} else(statements;...)

* switch(expression){case VALUE1 or /REGEXP/: statement1; case VALUE2 or /REGEXP2/: statement2;......;default: statementn}

* while(condition){statements;...}

* do(statements;...) while{condition}

* for(expr1;expr2;expr3) {statements;...}

* break

* continue

* exit

if-else示例：

```bash
$ cat <<EOF > score.txt
Name  Score
Tom   100
Jack  91
Bill  81
Jim   51
EOF

$ awk 'NR!=1{score=$2;if($2>=80){print $1, "Good"}else if($2>=60){print $1, "Pass"}else{print $1, "failed"}}'
score.txt
Tom Good
Jack Good
Bill Good
Jim failed
```

switch示例：

```bash
$ awk 'NR!=1{switch($2){case 100:print $1,"good"; case 60:print $1,"Pass"; default:print $1,"others"}}' score.txt
Tom good
Tom Pass
Tom others
Jack others
Bill others
Jim others
```

while示例：

```bash
$ awk 'BEGIN{i=0;sum=0;while(i<=100){sum+=i;i++};print sum}'
5050
```

do-while示例：

```bash
$ awk 'BEGIN{i=0;sum=0;do{sum+=i;i++}while(i<101);print sum}'
5050
```

for示例：

```bash
$ awk 'BEGIN{i=0;sum=0;for(i=1;i<=100;i++){sum+=i};print sum}'
5050
```

命令效率比较：

```bash
$ time(awk 'BEGIN{i=0;sum=0;while(i<=100000){sum+=i;i++};print sum}')
5000050000

real    0m0.028s
user    0m0.027s
sys    0m0.001s

$ time(seq -s+ 1000000 |bc)
500000500000

real    0m0.329s
user    0m0.240s
sys    0m0.094s

$ time(awk 'BEGIN{i=0;sum=0;for(i=1;i<=1000000;i++){sum+=i};print sum}')
500000500000

real    0m0.050s
user    0m0.046s
sys    0m0.004s
```

contine示例：中断当前循环，进入下一次循环。

```bash
$ awk 'BEGIN{i=0;sum=0;for(i=1;i<=100;i++){if(i==50)continue;sum+=i};print sum}'
5000
```

contine示例：中断整个循环。

```bash
$ awk 'BEGIN{i=0;sum=0;for(i=1;i<=100;i++){if(i==50)break;sum+=i};print sum}'
1225
```

next示例：提前结束对本行处理，直接进入下一行处理（注，awk自循环，并非前面的for或while循环）

```bash
$ awk -F: '{if($3%2!=0)next;print $1,$3}' /etc/passwd  # 奇数行打印
root 0
systemd-timesync 496
nobody 65534
chrony 494
games 492
daemon 2
rpc 490
polkitd 488
ftpsecure 486
sshd 484
vagrant 1000
svn 482
tester1 600
tester4 1002
user0 1004
user2 1006
user4 1008
user6 1010
user8 1012
gentoo 1014
varnish 1016
webuser 666
admin3 1020
smith 2002
tm1 2004

$ awk -F: '{if($3%2==0)next;print $1,$3}' /etc/passwd  # 偶数行打印
messagebus 499
systemd-network 497
mail 495
postfix 51
man 13
lp 493
ftp 491
nscd 489
at 25
tftp 487
bin 1
statd 485
pesign 483
tester2 601
tester3 1001
tester5 1003
user1 1005
user3 1007
user5 1009
user7 1011
user9 1013
nginx 1015
mysql 1017
pm1 2003
tm2 2005
```

### 5.10.11.数组

关联数组是一种数据结构，也称为字典或映射。与传统的数组不同，关联数组的索引可以是任何类型的数据，例如字符串或对象，而不仅仅是整数。

提示：
> 在计算机编程中，除了关联数组，还有其他几种常见的数组类型，包括：
>
> 1. 线性数组（或称为索引数组）：这是最常见的数组类型，其中每个元素都有一个数字索引，可以用来快速访问数组中的元素。例如，在C语言中，数组的每个元素都可以通过数组下标来访问。
> 2. 多维数组：多维数组是一种数组，其中每个元素也是一个数组。在二维数组中，每个元素都有两个索引（例如，行和列），可以用于访问数组中的元素。在高维数组中，每个元素都具有更多的索引。
> 3. 动态数组：动态数组是一种可以动态调整大小的数组。在许多编程语言中，动态数组可以动态分配内存，以便在程序运行时根据需要调整数组的大小。
> 4. 向量：向量是一种数组，其中每个元素都是相同的数据类型。向量通常用于执行数学运算或处理大量数字数据。

在`awk`中使用数组时，通常会将某些值与一个字符串相关联，以便在需要时可以通过该字符串快速地检索该值。
`awk`的数组是一个关联数组，其中每个元素都由一个唯一的键值和一个对应的值组成。键值（或称为索引）可以是任何类型的字符串。

数组可以通过以下语法进行声明：

```bash
array_name[index] = value
```

其中，`array_name`是数组的名称，`index`是元素的索引值，`value`是元素的值。

例如，以下是一个包含三个元素的关联数组的示例：

```bash
array["apple"] = 1
array["banana"] = 2
array["orange"] = 3
```

在上面的示例中，`array`是一个关联数组，其索引为字符串类型，而值为整数类型。可以使用以下的方式访问该数组中的元素：

```bash
value = array["apple"]
```

在上面的示例中，`value`的值将为`1`，因为`array["apple"]`的值为`1`。

以下是用`awk`命令来创建上面那个包含三个元素的关联数组，遍历并输出数组值：

```bash
awk 'BEGIN { array["apple"]=1; array["banana"]=2; array["orange"]=3; for(i in array){print array[i]}}'
3
1
2
```

下面例子中，我们互换了数组的键和值。

```bash
$ awk 'BEGIN {arr[1]="apple";arr[2]="banana";arr[3]="orange";for(i in arr){print arr[i]}}'
apple
banana
orange
```

在上面的示例中，`i`是数组`arr`的索引值，`arr[i]`是数组中对应的元素值。通过这种方式可以循环遍历整个数组，并输出其中的元素。

除了使用循环遍历数组之外，还可以使用`length`函数获取数组中元素的数量。例如：

```bash
$ awk 'BEGIN { arr[1]="apple"; arr[2]="banana"; arr[3]="orange"; print length(arr) }'
3
```

上面的示例将输出数字3，表示数组`arr`中包含三个元素。

举例：去重复记录。
`line`是数组名，`$0`是`awk`读取的当前行的内容。
`line[$0]`等价于`line["a"]`，`line["b"]`，......。

我们看执行过程：

1. awk读入第1行；
2. 执行`line["a"]`，值为空；
3. 求反，则第一行的值变为`true`，即`!line["a"]=true`；
4. 当`!line["a"]`为`true`，则打印当前行，即输出`a`到屏幕；
5. 执行`line["a"]++`，注意第2步中`line["a"]`的值是空，执行`++`后值变为`1`。
6. 同理，我们可以看到第2，3，4行都输出了。
7. 当读入第5行时（第二个`a`），执行`line["a"]`，值为`1`；`!line["a"]=0`，即false；则不打印当前行，即不输出`a`到屏幕；执行`++`后值变为`2`
8. 当读入第8行时（第三个`a`），执行`line["a"]`，值为`2`；`!line["a"]=0`，即false；则不打印当前行，即不输出`a`到屏幕；执行`++`后值变为`3`
9. 以此类推，读入第二个`b`，`c`，`d`，`e`，都不会再输出到屏幕，从而实现去重输出到功能。

```bash
$ cat > test << EOF
a
b
c
d
a
c
d
a
b
b
e
EOF

$ awk '!line[$0]++' test
a
b
c
d
e
```

举例：判断数组索引是否存在。
方法：`<your_var> in array`，`0`表示不存在，`1`表示存在。

```bash
$ awk 'BEGIN{array["i"]="x";array["j"]="j";print "i" in array, "y" in array}'
1 0
$ awk 'BEGIN{array["i"]="x";array["j"]="j";if("i" in array){print "exits!"}else{print "not exists!"}}'
exits!
$ awk 'BEGIN{array["i"]="x";array["j"]="j";if("abc" in array){print "exits!"}else{print "not exists!"}}'
not exists!
```

举例：遍历数组中每个元素。
方法：`for(your_var in array){your_for_body}`，注意，your_var会遍历每个索引。

```bash
$ awk 'BEGIN{weekday["mon"]="Monday";weekday["tue"]="Tuesday";for(i in weekday){print i,weekday[i]}}'
tue Tuesday
mon Monday
$ awk 'BEGIN{weekday["mon"]="Monday";weekday["tue"]="Tuesday";for(i in weekday){print i": "weekday[i]}}'
tue: Tuesday
mon: Monday
```

注意下面的换行写法，不需要反斜杠`\`。

```bash
$ awk 'BEGIN{
arr["x"]="welcome"
arr["y"]="to"
arr["z"]="Shanghai"
for (i in arr) {
 print i, arr[i]
}
}'
x welcome
y to
z Shanghai
```

示例：格式化输出用户名和密码。

```bash
$ awk -F: '{user[$1]=$3}END{for (i in user){print "Username: " i, "UID: " user[i]}}' /etc/passwd
Username: sshd UID: 476
Username: rpc UID: 482
Username: tftp UID: 488
Username: usbmux UID: 480
Username: srvGeoClue UID: 487
......
```

示例：显示主机连接状态出现的次数。

```bash
# 传统方法
$ ss -ant| awk 'NR>=2{print $1}'| sort| uniq -c
$ ss -ant| awk 'NR!=1{print $1}'| sort| uniq -c
      1 ESTAB
      6 LISTEN

# 使用awk数组
$ ss -ant| awk 'NR>=2{state[$1]++}END{for(i in state){print state[i], i}}'
$ ss -ant| awk 'NR!=1{state[$1]++}END{for(i in state){print state[i], i}}'
6 LISTEN
1 ESTAB
```

### 5.10.12.awk函数

参考：[`awk`函数官网](https://www.gnu.org/software/gawk/manual/html_node/Functions.html)

#### 5.10.12.1.内置函数

在`awk`中，函数是一种用于执行特定任务或计算特定值的可重用代码块。
`awk`提供了许多内置函数，可以用于处理文本数据、执行数学运算、操作字符串等。

以下是一些常用的awk函数示例：

* `length(string)`：返回字符串的长度。

```shell
$ awk 'BEGIN { str = "Hello World"; len = length(str); print len }'
11
```

```bash
$ cut -d: -f1 /etc/passwd | awk '{print length($1)}' | head -3
4
10
15
```

* `substr(string, start, length)`：从指定位置开始提取字符串的子串。

```shell
$ awk 'BEGIN { str = "Hello World"; substring = substr(str, 7, 5); print substring }'
World
```

* `sub(regexp, replacement [, target])`：从字符串target中搜索匹配regexp的内容，并把第一个匹配的内容替换为replacement。懒惰模式。
注意：`sub()`函数在原始字符串上进行替换操作，并返回替换的次数。

```shell
# 在原始字符串中，第一个匹配到的"at"被替换为"ith"，因此输出结果中的"at"变为"ith"，其他地方的"at"保持不变
$ awk 'BEGIN { str = "water, water, everywhere"; sub(/at/, "ith", str); print str }'
wither, water, everywhere
# 返回匹配次数
$ awk 'BEGIN { str = "water, water, everywhere"; str_new = sub(/at/, "ith", str); print str_new }'
1
```

```bash
$ echo "2023:15:35 08:15:26" | awk 'sub(/:/, "-", $0)'
2023-15:35 08:15:26
$ echo "2023:15:35 08:15:26" | awk 'sub(/:/, "-", $1)'
2023-15:35 08:15:26
$ echo "2023:15:35 08:15:26" | awk 'sub(/:/, "-", $2)'
2023:15:35 08-15:26
```

* gsub(regexp, replacement [, target])：从字符串target中搜索匹配regexp的内容，并把全部匹配的内容替换为replacement。贪婪模式。

```bash
# 在原始字符串中，将所有匹配到的"at"被替换为"ith"
$ awk 'BEGIN { str = "water, water, everywhere"; gsub(/at/, "ith", str); print str }'
wither, wither, everywhere
# 返回匹配次数
$ awk 'BEGIN { str = "water, water, everywhere"; str_new = gsub(/at/, "ith", str); print str_new }'
2
```

```bash
$ echo "2023:15:35 08:15:26" | awk 'gsub(/:/, "-", $0)'
2023-15-35 08-15-26
$ echo "2023:15:35 08:15:26" | awk 'gsub(/:/, "-", $1)'
2023-15-35 08:15:26
$ echo "2023:15:35 08:15:26" | awk 'gsub(/:/, "-", $2)'
2023:15:35 08-15-26
```

* `split(string, array, delimiter)`：将字符串string按指定分隔符delimiter拆分成数组array的元素。
注意：第一个索引值为`1`，第二个索引值为`2`.

```bash
$ awk 'BEGIN { str = "apple,banana,orange"; split(str, fruits, ","); print fruits[2] }'
banana
```

```bash
$ head -n2 /etc/passwd | awk '{split($0, array, ":")}END{print array[1]}'
messagebus
$ head -n2 /etc/passwd | awk '{split($0, array, ":")}END{print array[2]}'
x
$ head -n2 /etc/passwd | awk '{split($0, array, ":")}END{print array[3]}'
499
$ head -n2 /etc/passwd | awk '{split($0, array, ":")}END{print array[7]}'
/usr/bin/false
```

* `index(string, search)`：在字符串中查找指定子串的位置。

```bash
$ awk 'BEGIN { str = "Hello World"; pos = index(str, "World"); print pos }'
7
```

* `sprintf(format, expression)`：根据指定的格式将表达式转换为字符串。

```bash
$ awk 'BEGIN { num = 3.14159; str = sprintf("%.2f", num); print str }'
3.14
```

* `rand()`：返回一个随机数，值在`0`和`1`之间均匀分布。这个值可以是`0`，但不会是`1`。从下面的例子可以看出，运行结果都是一样的，所以产生随机数的种子是一样的。

```bash
$ awk 'BEGIN{print rand()}'
0.924046
$ awk 'BEGIN{print rand()}'
0.924046
$ awk 'BEGIN{print rand()}'
0.924046
```

* `srand()`：配合`rand()`函数，生成随机数种子。

```bash
$ awk 'BEGIN{srand();print rand()}'
0.112006
$ awk 'BEGIN{srand();print rand()}'
0.663431
$  awk 'BEGIN{srand();print rand()}'
0.541305
```

* `int()`：返回整数。

```bash
$ awk 'BEGIN{srand();print int(rand()*100)}'
84
$ awk 'BEGIN{srand();print int(rand()*100)}'
66
$ awk 'BEGIN{srand();print int(rand()*100)}'
8
```

* `system(command)`：执行command命令（可以是任何有效的Shell命令）并返回命令的退出状态码。允许在`awk`脚本中执行外部命令，并获取命令执行的结果。

```bash
# 执行ls -l命令，并将命令的退出状态码存储在status变量中，并打印status变量的值
$ awk 'BEGIN { status = system("ls -l"); print "Exit status:", status }'
total 0
drwxr-xr-x 1 vagrant users 70 Jan  2 15:54 Desktop
drwxr-xr-x 1 vagrant users  0 Jan  2 15:54 Documents
drwxr-xr-x 1 vagrant users  0 Jan  2 15:54 Downloads
drwxr-xr-x 1 vagrant users  0 Jan  2 15:54 Music
drwxr-xr-x 1 vagrant users  0 Jan  2 15:54 Pictures
drwxr-xr-x 1 vagrant users  0 Jan  2 15:54 Public
drwxr-xr-x 1 vagrant users  0 Jan  2 15:54 Templates
drwxr-xr-x 1 vagrant users  0 Jan  2 15:54 Videos
drwxr-xr-x 1 vagrant users  0 Mar 15  2022 bin
Exit status: 0
```

```bash
$ awk 'BEGIN{score=100; system("echo your score is " score)}'
your score is 100
```

* `systime()`：当前时间到1970年1月1日到秒数

```bash
$ awk 'BEGIN{print systime()}'
1684158395
```

* `strftime(format, timestamp)`：将时间戳timestamp转换为指定格式format的日期和时间字符串。timestamp通常是一个以秒为单位表示的整数。

常见的格式化字符串选项：

* `%Y`：四位数的年份（例如：2023）
* `%m`：两位数的月份（01-12）
* `%d`：两位数的日期（01-31）
* `%H`：两位数的小时（00-23）
* `%M`：两位数的分钟（00-59）
* `%S`：两位数的秒（00-60）
* `%Z`：时区名称（例如：GMT）

```bash
# 将当前时间戳转换为格式为"YYYY-MM-DD HH:MM:SS"的日期和时间字符串
$ awk 'BEGIN { timestamp = systime(); str = strftime("%Y-%m-%d %H:%M:%S", timestamp); print str }'
2023-05-15 22:01:35
# 将当前时间戳的前一小时（3600秒）转换为格式为"YYYY-MM-DD HH:MM:SS"的日期和时间字符串
$ awk 'BEGIN { timestamp = systime()-3600; str = strftime("%Y-%m-%d %H:%M:%S", timestamp); print str }'
2023-05-15 21:01:43
```

#### 5.10.12.2.自定义函数

举例：

```bash
$ cat > func.awk << EOF
function max(x,y){
  x>y?var=x:var=y
  return var
}
BEGIN{print max(a,b)}
EOF

$ awk -v a=30 -v b=20 -f func.awk
30
```

举例：

在下面的例子中，我们定义了一个名为`square()`的自定义函数，它接受一个参数`x`，并返回`x`的平方。然后，在主代码块中，我们声明了一个变量`num`并赋值为`5`。接下来，我们调用了自定义函数`square()`，传递`num`作为参数，并将返回值存储在变量`result`中。最后，我们打印出`result`的值。

```bash
$ cat > func.awk << EOF
# 自定义函数：计算平方
function square(x) {
  return x * x;
}

# 使用自定义函数
{
  num = 5;
  result = square(num);
  print "平方结果：" result;
}
EOF

$ awk -f func.awk
平方结果：25
```

举例：

```bash
$ cat > func.awk << EOF
# 自定义函数：计算数组平均值
function calculateAverage(arr, size) {
  sum = 0;
  for (i = 1; i <= size; i++) {
    sum += arr[i];
  }
  return sum / size;
}

# 使用自定义函数
{
  # 定义数组
  numbers[1] = 10;
  numbers[2] = 20;
  numbers[3] = 30;
  numbers[4] = 40;
  numbers[5] = 50;

  # 计算数组的平均值
  size = 5;
  average = calculateAverage(numbers, size);

  print "数组的平均值：" average;
}
EOF

$ awk -f func.awk
数组的平均值：30
```

#### 5.10.12.3.awk脚本

举例：

```bash
# 注意转义
$ cat > passwd.awk << EOF
{if(\$3>=1000)print \$1,\$3}
EOF

$ awk -F: -f passwd.awk /etc/passwd
nobody 65534
vagrant 1000
```

上面例子也可以写成如下脚步格式。

```bash
$ cat > test.awk << EOF
#!/bin/awk -f
# This is an awk script
{if(\$3>=1000)print \$1,\$3}
EOF

$ chmod +x test.awk
$ ./test.awk -F: /etc/passwd
nobody 65534
vagrant 1000
```

向awk脚本传递参数：

格式：`awkfile var=value var2=value2 ... inputfile`

说明：

* 上面格式变量在`BEGIN`过程中不可用，直到首行输入完成以后，变量才可用。
* 可以通过`-v`参数，让`awk`在执行`BEGIN`之前得到变量。
* 命令行中每一个指定的变量都需要一个`-v`参数。

举例：

```bash
# x=100在BEGIN{print x}区段可用
$ awk -v x=100 'BEGIN{print x}{print x+100}' /etc/hosts
100
200
200
200
200
200
200
200
200
200
200
200
200
200
200
200
200
200
200
200
200
200
200
200
# 不加-v则x=100在BEGIN{print x}区段不可用
$ awk x=100 'BEGIN{print x}{print x+100}' /etc/hosts
awk: fatal: cannot open file `BEGIN{print x}{print x+100}' for reading (No such file or directory)
# 修正上面的错误，将x=100放在后面，因为没有-v，所以x=100在BEGIN{print x}区段不可用，第一行输出空白
$ awk 'BEGIN{print x}{print x+100}' x=100 /etc/hosts

200
200
200
200
200
200
200
200
200
200
200
200
200
200
200
200
200
200
200
200
200
200
200
```

## 5.11.小练习

* 显示`/proc/meminfo`文件中以大小s开头的行，要求使用两种方法。
  
```bash
cat /proc/meminfo | grep -i "^s"
cat /proc/meminfo | grep "^[sS]"
```

* 显示`/etc/passwd`文件中不以`/bin/bash`结尾的行。
  
```bash
grep -v "/bin/bash$" /etc/passwd
```

* 显示用户`rpc`默认的shell程序。
  
```bash
$ grep "rpc" /etc/passwd | cut -d ":" -f 7
/sbin/nologin
```

* 找出`/etc/passwd`中的两位或三位数。
  
```bash
grep -Eo "[:digit:]{2,3}" /etc/passwd
grep -Eo "[0-9]{2,3}" /etc/passwd
```
  
这里用到了`{}`，属于扩展正则符号，所以要用`-E`。

* 显示Rocky 9的`/etc/grub2.cfg`文件中，至少以一个空白字符开头的且后面有非空白字符的行。（注：`/etc/grub2.cfg`在openSUSE和Ubuntu中没有）
  
```bash
# 不含首字符为tab
$ sudo grep "^ " /etc/grub2.cfg

# 包含首字符为tab
$ sudo grep "^[[:space:]]" /etc/grub2.cfg
```

* 找出`netstat -tan`命令结果中以`LISTEN`后跟任意多个空白字符结尾的行。
  
```bash
netstat -tan | grep -E "LISTEN[[:space:]]+"
```

* 显示Rocky 9上所有UID小于1000以内的用户名和UID。
  
```bash
cat /etc/passwd | cut -d ":" -f 1,3 | grep -E "\:[0-9]{1,3}$"
grep -E "\:[0-9]{1,3}\:[0-9]{1,}" /etc/passwd | cut -d ":" -f 1,3
```

* 在Rocky 9上显示文件`/etc/passwd`用户名和shell同名的行。
  
```bash
$ grep -E "^([[:alnum:]]+\b).*\1$" /etc/passwd
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
```

* 利用`df`和`grep`，取出磁盘各分区利用率,并从大到小排序。
  
```bash
$ df | tr -s " " | cut -d " " -f 1,5 | sort -n -t " " -k 2
devtmpfs 0%
Filesystem Use%
tmpfs 0%
tmpfs 0%
/dev/mapper/rl-home 1%
tmpfs 2%
/dev/mapper/rl-root 5%
/dev/nvme0n1p1 23%
```

* 显示三个用户`root`，`sync`，`bin`的UID和默认shell。
  
```bash
$ grep "^root:\|^sync:\|^bin:" /etc/passwd | cut -d ":" -f 1,7
root:/bin/bash
bin:/usr/sbin/nologin
```

* 使用`egrep`取出`/etc/default-1/text_2/local.3/grub`中其基名和目录名。
  
```bash
# 基名
$ echo "/etc/default-1/text_2/local.3/grub" | egrep -io "[[:alpha:]]+$"
grub

# 目录名
$  echo "/etc/default-1/text_2/local.3/grub" | egrep -io "/([[:alpha:]]+.|_?[[:alpha:]]|[[:alnum:]]+/){7}"
/etc/default-1/text_2/local.3/ 
```

* 统计`last`命令中以`vagrant`登录的每个主机IP地址登录次数。
  
```bash
$ last | grep vagrant | tr -s " " | cut -d " " -f 3 | grep -E "([0-9]{1,3}\.){1,3}[0-9]{1,3}" | sort -n | uniq -c
    24 192.168.10.107
    38 192.168.10.109
    17 192.168.10.201
     6 192.168.10.210
     2 192.168.10.220
```

* 利用扩展正则表达式分别表示0-9、10-99、100-199、200-249、250-255。
  
```bash
[0-9]|[0-9]{2}|1[0-9]{2}|2[0-4][0-9]|25[0-5]
```

* 显示`ifconfig`命令结果中所有IPv4地址。
  
```bash
$ ifconfig | grep -Eo "([0-9]{1,3}\.){3}[0-9]{1,3}" | grep -v "^255"
192.168.10.210
192.168.10.255
127.0.0.1
```

* 显示`ip addr`命令结果中所有IPv4地址。
  
```bash
$ ip addr show eth0 | grep inet | grep eth0 | tr -s " " | cut -d " " -f 3 | cut -d "/" -f 1
192.168.10.210

$ ip addr show | grep -Eo "([0-9]{1,3}\.){3}[0-9]{1,3}" | grep -v "^255"
127.0.0.1
192.168.10.210
192.168.10.255
```

* 将此字符串Welcome to the linux world中的每个字符去重并排序，重复次数多的排到前面。
  
```bash
$ echo "Welcome to the linux world" | grep -o [[:alpha:]] | sort | uniq -c | sort -nr
     3 o
     3 l
     3 e
     2 t
     1 x
     1 W
     1 w
     1 u
     1 r
     1 n
     1 m
     1 i
     1 h
     1 d
     1 c
```

* 删除`/etc/default/grub`文件中所有以空白开头的行行首的空白字符。
  
```bash
sed '/^$/d' /etc/default/grub
```

* 删除`/etc/default/grub`文件中所有以`#`开头，后面至少跟一个空白字符的行的行首的`#`和空白字符。
  
```bash
sed -r '/#[[:space:]]+/d;/#/d' /etc/default/grub
```

上面输出结果中包含空白行。

若输出中删除空白行，则：

```bash
sed -r '/#[[:space:]]+/d;/#/d;/^$/d' /etc/default/grub
```

* 在`/etc/fstab`每一行行首增加`#`号。
  
```bash
sed -r 's/(.*)/#&/' /etc/fstab
```

* 在`/etc/fstab`文件中不以`#`开头的行的行首增加`#`号（包括空行）。
  
```bash
sed -r 's/^[^#].*/#&/' -r 's/^$/#/' /etc/default/grub
```

* 通过命令`rpm -qa --last |awk -F ' ' '{print $1}'`得到最新安装的包列表。统计所有`x86_64`结尾的安装包名以`.`分隔倒数第二个字段的重复次数。
  
```bash
$ rpm -qa --last |awk -F ' ' '{print $1}' |sed -nr '/x86_64$/s@.*\.(.*)\.x86_64@\1@p' |sort -r |uniq -c
     75 el9_0
    563 el9
      3 7
      1 5
      2 4
      2 3
     10 2
     29 1
```

* 在openSUSE中统计`/etc/rc.status`文件中每个单词的出现次数，并排序（用grep和sed两种方法分别实现）。
  
```bash
grep -Eo "[a-zA-Z]+" /etc/rc.status |sort |uniq -c

cat /etc/rc.status |sed -r 's/[^[:alpha:]]+/\n/g' |sed '/^$/d' |sort |uniq -c |sort -nr
```

* 将文本文件的n和n+1行合并为一行，n为奇数行。
  
```bash
$ cat <<EOF > sed.txt
1aa
2bb
3cc
4dd
5ee
6ff
7gg
EOF

$ sed -n 'N;s/\n//p' sed.txt
1aa2bb
3cc4dd
5ee6ff

$ sed 'N;s/\n//' sed.txt
1aa2bb
3cc4dd
5ee6ff
7gg
```

* 对一串数字进行求和。
  
```bash
$ cat <<EOF > number.txt
1 2 3 4 5 6
EOF
```
  
```bash
$ tr ' ' + < number.txt | bc
21
$ sum=0;for i in `cat number.txt`;do let sum+=i;done;echo $sum
21
$ awk '{sum=0;for(i=1;i<=NF;i++){sum+=i};print sum}' number.txt
21
```

* 取出字符串中的数字。
  
```bash
$ echo 'kdajl;3k8jd33la5kj23f90ld02sakjflakjdslf' | awk -F "" '
{
  for(i=1;i<=NF;i++)
  {
    if($i ~ /[0-9]/)
    {
      str=(str $i)
    }
  };
  print str
}'
38335239002
```

* `host.log`文件内容如下，提取`.edu.cn`前面的主机名，并回写到该文件中。

```bash
$ cat > host.log << EOF
1 www.edu.cn
2 blog.edu.cn
3 learning.edu.cn
4 java.edu.cn
5 nodejs.edu.cn
6 k8s.eud.cn
7 linux.edu.cn
8 python.edu.cn
9 learning.edu.cn
10 java.edu.cn
11 nodejs.edu.cn
12 www.edu.cn
EOF

# 对比
$ awk -F'[ .]' '{print $1}' host.log
1
2
3
4
5
6
7
8
9
10
11
12
$ awk -F'[ .]' '{print $2}' host.log
www
blog
learning
java
nodejs
k8s
linux
python
learning
java
nodejs
www

# 以空格或者.为分隔符，打印第二列（主机名），追加写入原文件
$ awk -F'[ .]' '{print $2}' host.log >> host.log
$ cat host.log
1 www.edu.cn
2 blog.edu.cn
3 learning.edu.cn
4 java.edu.cn
5 nodejs.edu.cn
6 k8s.eud.cn
7 linux.edu.cn
8 python.edu.cn
9 learning.edu.cn
10 java.edu.cn
11 nodejs.edu.cn
12 www.edu.cn
www
blog
learning
java
nodejs
k8s
linux
python
learning
java
nodejs
www
```

* 统计文件`/etc/fstab`中每个文件系统类型出现的次数。

```bash
# 以UUID开头，一个或多个空格为分隔符，读取第三列（即文件系统类型）并计数。
$ awk -F' +' '/^UUID/{fs[$3]++}END{for(i in fs){print i, fs[i]}}' /etc/fstab
swap 1
btrfs 10
vfat 1

# 方法2
$ awk -F' +' '/^UUID/{print $3}' /etc/fstab | uniq -c
     10 btrfs
      1 swap
      1 vfat
```

* 统计文件`/etc/fstab`中每个单词出现的次数。

```bash
$ awk -F"[^[:alpha:]]" '{for(i=1;i<=NF;i++)word[$i]++}END{for(a in word)if(a!="")print a,word[a]}' /etc/fstab
swap 2
B 1
srv 2
btrfs 10
snapshots 2
vfat 1
opt 2
cbaef 10
UUID 12
E 1
ecf 1
CD 1
cf 1
arm 2
a 11
c 2
tmp 2
usr 2
var 2
afa 20
home 2
d 10
utf 1
e 2
efi 3
grub 2
boot 3
subvol 9
root 2
local 2
defaults 2
f 10
```

* 提取字符串`Yd$@C#M05MD9&8923+Vip3wZ!33*44&55`中所有的数字。

```bash
# 对比单引号和双引号的区别。
$  echo "Yd$@C#M05MD9&8923+Vip3wZ!33*44&55"
echo "Yd$@C#M05MD9&8923+Vip3wZcgcreate -g cpu:mygroup44&55"
YdC#M05MD9&8923+Vip3wZcgcreate -g cpu:mygroup44&55
$ echo 'Yd$@C#M05MD9&8923+Vip3wZ!33*44&55'
Yd$@C#M05MD9&8923+Vip3wZ!33*44&55

$ echo 'Yd$@C#M05MD9&8923+Vip3wZ!33*44&55'|awk '{gsub(/[^0-9]/,"");print $0}'
05989233334455

$ echo 'Yd$@C#M05MD9&8923+Vip3wZ!33*44&55'|awk -F'[^0-9]' '{for(i=1;i<=NF;i++){printf "%s", $i}}'
05989233334455

$ echo 'Yd$@C#M05MD9&8923+Vip3wZ!33*44&55'|awk -F "" '{for(i=1;i<=NF;i++){if($i ~ /[[:digit:]]/){str=$i;str1=(str1 str)}};print str1}'
05989233334455
$ echo 'Yd$@C#M05MD9&8923+Vip3wZ!33*44&55'|awk -F '' '{for(i=1;i<=NF;i++){if($i ~ /[[:digit:]]/){str=$i;str1=(str1 str)}};print str1}'
# 注意，如果写成如下格式，则报错。
$ echo 'Yd$@C#M05MD9&8923+Vip3wZ!33*44&55'|awk -F'' '{for(i=1;i<=NF;i++){if($i ~ /[[:digit:]]/){str=$i;str1=(str1 str)}};print str1}'
# 注意，如果写成如下格式，则输出原字符串。
$ echo 'Yd$@C#M05MD9&8923+Vip3wZ!33*44&55'|awk -F ' ' '{for(i=1;i<=NF;i++){if($i ~ /[[:digit:]]/){str=$i;str1=(str1 str)}};print str1}'
```

* 生成500个随机数，保存到文件random.txt中，格式为`100,20,61,98...`，取出其中最大整数和最小整数。

```bash
$ str=""; for ((i=1; i<=500; i++)); do if [ $i -ne 500 ]; then str+="$RANDOM,"; else str+="$RANDOM"; fi; done; echo "$str" > random.txt
$ cat random.txt
11308,8764,2075,9411,......
$ awk -F, '{max=$1;min=$1;for(i=1;i<=NF;i++){if($i>max){max=$i}else{if($i<min){min=$i}}}}END{print "The max:" max, "The min:" min}' random.txt
The max:32696 The min:20
```

* 监控某个IP并发连接超过200时，调用防火墙命令封掉该IP，每5分钟监控一次。防火墙命令`iptables -A INPUT -s IP -j REJECT`。

```bash
ss -nt | awk -F " +|:" 'NR!=1{ip[$(NF-2)]++}END{for(i in ip){if(ip[i]>200){system("iptables -A INPUT -s " i " -j REJECT;")}}}'
```

* 将下面内容中FQDN取出，并根据其进行计数，从高到低排序。

```bash
$ cat > fqdn.txt << EOF
http://mail.edu.com/index.html
http://www.edu.com/test.html
http://study.edu.com/index.html
http://blog.edu.com/index.html
http://www.edu.com/images/logo.jpg
http://blog.edu.com/20080102.html
EOF

$ awk -F"/" '{url[$3]++}END{for(i in url){print url[i], i}}' fqdn.txt|sort -nr
2 www.edu.com
2 blog.edu.com
1 study.edu.com
1 mail.edu.com
```

* 将以下⽂本以inode为标记，对inode相同的counts进⾏累加，并且统计出同一inode中，beginnumber的最小值和endnumber的最大值。

```bash
inode|beginnumber|endnumber|counts| 
106|3363120000|3363129999|10000| 
106|3368560000|3368579999|20000| 
310|3337000000|3337000100|101| 
310|3342950000|3342959999|10000| 
310|3362120960|3362120961|2| 
311|3313460102|3313469999|9898| 
311|3313470000|3313499999|30000| 
311|3362120962|3362120963|2| 
```

输出的结果格式为：

```bash
310|3337000000|3362120961|10103| 
311|3313460102|3362120963|39900| 
106|3363120000|3368579999|30000|
```

```bash
$ cat > inode.text << EOF
inode|beginnumber|endnumber|counts| 
106|3363120000|3363129999|10000| 
106|3368560000|3368579999|20000| 
310|3337000000|3337000100|101| 
310|3342950000|3342959999|10000| 
310|3362120960|3362120961|2| 
311|3313460102|3313469999|9898| 
311|3313470000|3313499999|30000| 
311|3362120962|3362120963|2| 
EOF

$ awk -F'|' -v OFS='|' '/^[0-9]/{inode[$1]++; if(!bn[$1]){bn[$1]=$2}else if(bn[$1]>$2) {bn[$1]=$2}; if(en[$1]<$3)en[$1]=$3;cnt[$1]+=$(NF-1)} END{for(i in inode)print i,bn[i],en[i],cnt[i]}' inode.text
106|3363120000|3368579999|30000
310|3337000000|3362120961|10103
311|3313460102|3362120963|39900
```