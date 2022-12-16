# 文本编辑和正则表达式

## 文本编辑器`vim`

vim命令格式：

* `+# file`: 打开文件后，让光标处于第#行首，+默认行尾
* `+/PATTERN file`: 打开文件有，让光标处于第一个被PATTERN匹配到的行首
* `-b file`: 二进制方式打开文件
* `-d file1 file2 ...`: 比较多个文件，相当于`vimdiff`
* `-m file`: 只读方式打开文件
* `-e file`: 进入ex模式，相当于`ex file`
* `-y file`: 

vim三种常见模式：

* 普通模式Normal或命令模式
* 插入Insert或编辑模式
* 扩展命令模式Extended Command

三种模式切换

* 命令模式-->插入模式
  * i：insert，在光标处输入
  * I：在光标所在行首输入
  * a：append，在光标处后面输入
  * A：在光标所在行尾输入
  * o：在光标所在行的下方打开一个新行
  * O：在光标所在行的上方打开一个新行
* 插入模式--> ESC --> 命令模式
* 命令模式--> : --> 扩展命令模式
* 扩展命令模式--> ESC, enter --> 命令模式

扩展命令模式常用命令：

* `:wq`:    保存文件并退出
* `:w`:    保存文件
* `:w filename`:    写入指定文件，相当于另存为
* `:q!`:    放弃任何修改并退出
* `ZQ`:    无条件退出
* `:join`:    合并多行
* `J `:        合并两行

设置：（可以在`/etc/vimrc`文件中配置）

* `:set textwidth`: 设置文本宽度（从左向右计数）
* `:set wrapmargin=#`: 设置行边距（从右向左计数）
* `:set endofline`: 设置文件结束符
* `:set noendofline`: 取消文件结束符
* `:set wrap`: 自动换行
* `:set nowrap`: 取消自动换行
* `:set number`: 显示行号
* `:set nonumber`: 取消显示行号
* `:set list`: 进入List Mode，显示Tab ^I，换行符，和$显示
* `:set nolist`: 退出List Mode
* `:set ignorecase`: 忽略字符的大小写
* `:set noic`: 不忽略字符大小写
* `:set autoindent`: 启用自动缩进
* `:set noai`: 关闭自动缩进
* `:set hlsearch`: 启用高亮搜索
* `:set nohlsearch`: 关闭高亮搜索
* `:set fileformat=dos`: 启用windows格式
* `:set fileformat=unix`: 启用unix格式
* `:set expandtab`: 启用空格代替TAB，默认8个空格代替一个TAB
* `:set noexpandtab`: 关闭空格代替TAB
* `:set tabstop=#`: 指定#个空格代替一个TAB
* `:set shiftwidth=#`: 设置#个缩进宽度
* `:set cursorline`: 设置光标所在行的表示线
* `:set cursorline`: 关闭光标所在行的表示线
* `:set key=PASSWORD`: 启用密码保护
* `:set key=`: 关闭密码保护
* `:help option-list`: 获取帮助

查找

* `/pattern`:    从光标开始处向文件尾搜索pattern
* `?pattern`:    从光标开始处向文件首搜索pattern
* `n`:    在同一方向重复上一次搜索命令
* `N`:    在反方向上重复上一次搜索命令
* `#`:    向上完整匹配光标下的单词, 相当于？word
* `*`:    向下完整匹配光标下的单词, 相当于/word
* `%`:    查找对应的( [ {匹配
* `nfx`:    在当前行查找光标后第n个x（一般直接fx）

替换

* `:%s/\n//g`: 删除换行符
* `:s/p1/p2/g`:    将当前行中所有p1均用p2替代, 无g，则只替换第一个
* `:s/p1/p2/c`:    查找替换要求确认
* `:n1,n2s/p1/p2/g`:    将第n1至n2行中所有p1均用p2替代
* `:%s/p1/p2/g`:    全局，使用p2替换p1
* `:%s/p1/p2/gc`:    替换前询问
* `:n,$s/vivian/sky/`:    替换第n行开始到最后一行中每一行的第一个vivian为sky，n为数字
* `:.,$s/vivian/sky/g`:    替换当前行开始到最后一行中每一行所有vivian为sky
* `:s/vivian\//sky\//`:    替换当前行第一个vivian/为sky/，可以使用\作为转义符
* `:1,$s/^/some string/`:    在文件的第一行至最后一行的行首前插入some string
* `:%s/$/some string/g`:    在整个文件每一行的行尾添加some string
* `:%s/\s\+$//`:    去掉所有的行尾空格，“\s”表示空白字符（空格和制表符），“\+”对前面的字符匹配一次或多次（越多越好），“$”匹配行尾（使用“\$”表示单纯的“$”字符）
* `:%s/\s∗\n\+/\r/`:    去掉所有的空白行，“\(”和“\)”对表达式进行分组，使其被视作一个不可分割的整体
* `:%s!\s*//.*!!`:    去掉所有的“//”注释
* `:%s!\s*/\*\_.\{-}\*/\s*!!g`:    去掉所有的“/* */”注释
* `:%s= *$==`:    将所有行尾多余的空格删除
* `:g/^\s*$/d`:    将所有不包含字符(空格也不包含)的空行删除
* `r`:    替换当前字符
* `R`:    替换当前字符及其后的字符，直至按ESC键

编辑

* `h`:    光标左移一个字符[回退键Backspace]
* `l`:    光标右移一个字符[空格键Space]
* `K`:    光标上移一行
* `j`:    光标下移一行
* `w`:    光标跳到下个word的第一个字母(包括标点符号) [常用]
* `W`:    移到下一个字的开头，忽略标点符号
* `B`:    光标回到上个word的第一个字母
* `B`:    移到前一个字的开头，忽略标点符号 BACK
* `E`:    光标跳到下个word的最后一个字母
* `E`:    移到下一个字的结尾，忽略标点符号 END
* `0`:    移到当前一行的开始[Home]
* `$`:    移到当前一行的最后[End]
* `^`:    命令将光标移动到当前行的第一个非空白字符上
* `g_`:    到本行最后一个不是blank字符的位置
* `Enter`:    光标下移一行
* `n+`:    光标下移n行【按上档键 数字shift +】
* `n-`:    光标上移n行
* `G`:    移到文件的最后一行
* `nG`或者`:n`:    移到文件的第n行
* `gg`:    移动到文档的开始
* `[[`:    文件开始位置——开始行
* `]]`:    文件结束位置——末尾行
* `H`:    光标移至屏幕顶行HEAD。光标定位在显示屏的第一行
* `M`:    移到屏幕的中间行开头 Middle。光标定位在显示屏的中间
* `L`:    移到屏幕的最后一行LAST。光标定位在显示屏的最后一行
* `(`:    光标移至句首
* `)`:    光标移至句尾
* `{`:    移到段落的开头
* `}`:    移到下一个段落的开头
* `%`:    匹配括号移动，包括 (, {, [.（需要把光标先移到括号上）跳转到与之匹配的括号处
* `*` 和 `#`:    匹配光标当前所在的单词，移动光标到下一个（或上一个）匹配单词（*是下一个，#是上一个）
* `zf`:    折叠（需加方向键）
* `zo`:    展开（空格也可以展开）
* `CTRL+u`:    向文件首翻半屏up
* `CTRL+d`:    向文件尾翻半屏down
* `CTRL+f`:    向文件尾翻一屏 forward (fact整屏去两行)
* `CTRL+b`:    向文件首翻一屏back (fact整屏去两行)
* `CTRL-]`:    跳转到当前光标所在单词对应的主题
* `CTRL-O`:    回到前一个位置
* `SHIFT+V`:    选择整行
* `zz`:    命令会把当前行置为屏幕正中央(z字取其象形意义模拟一张纸的折叠及变形位置重置)
* `zt`:    命令会把当前行置于屏幕顶端(top)
* `zb`:    命令会把当前行置于屏幕底端(bottom)
* `50%`:    光标定位在文件的中间
* ``` ``:    跳转到最近光标定位的位置（只能记忆最近两个位置） 反引号
* `I`:    在光标前开始插入字符  insert
* `I`:    在当前行首开始插入字符
* `A`:    在光标位置后开始加字  append
* `A`:    在光标所在行的最后面开始加字
* `O`:    在光标下加一空白行并开始加字 open
* `O`:    在光标上加一空白行并开始加字
* `R`:    替换当前字符
* `R`:    替换当前字符及其后的字符【当前及其后字符被覆盖】
* `S`:    默认删除光标所在字符，输入内容插入之= xi
* `S`:    默认删除当前行内容，输入内容作为当前行新内容= dd+o
* `nx`:    删除由光标位置起始后的n个字符（含光标位置）x =dl(删除当前光标下的字符)
* `nX`:    删除由光标位置起始前的n个字符（含光标位置）X =dh(删除当前光标左边的字符)
* `d0`:    删至行首
* `d$`:    删至行尾
* `dfa`:    表示删除从当前光标到光标后面的第一个a字符之间的内容
* `D`:    代表d$(删除到行尾的内容)
* `C`:    代表c$(修改到行尾的内容)
* `ndw`:    删除光标处开始及其后的n-1个字
* `ndb`:    删除光标处开始及其前的n-1个字
* `diw`:    删除当前光标所在的word(不包括空白字符)，意为Delete Inner Word 两个符号之间的单词
* `daw`:    删除当前光标所在的word(包括空白字符)，意为Delete A Word
* `ndd`:    删除当前行及其后n-1行
* `:n1,n2 d`:    将 n1行到n2行之间的内容删除
* `dG`:    删除当前行至文件尾的内容
* `Dgg`:    删除当前行至文件头的内容
* `d+enter`:    删除2行【包括光标一行】
* `cw`:    删除当前字，并进入输入模式【很好用，快速更改一个单词】相当于dw+i
* `ncw`:    删除当前字及其后的n-1个字，并进入输入模式\修改指定数目的字
* `cc`:    删除当前行，并进入输入模式
* `ncc`:    删除当前行及其后的n-1行，并进入输入模式
* `guw`:    光标下的单词变为小写
* `gUw`:    光标下的单词变为大写
* `xp`:    左右交换光标处两字符的位置
* `ga`:    显示光标下的字符在当前使用的encoding下的内码
* `nyl`:    复制n个字符(也可nyh)
* `yw`:    复制一个单词
* `y0`:    表示拷贝从当前光标到光标所在行首的内容
* `y$`:    复制从当前位置到行尾
* `yfa`:    表示拷贝从当前光标到光标后面的第一个a字符之间的内容
* `yG`:    复制从所在行到最后一行
* `nyy`:    将光标所在位置开始的n行数据复制暂存, 复制一整行
* `CTRL+v 方向y`:    列选择模式，复制选择的很多行：先使用V进入visual模式，然后j向下移动到你想复制的行为止，然后y
* `p`:    复制暂存数据在光标的下一行
* `P`:    复制暂存数据在光标的上一行
* `:n1,n2 co n3`:    将n1行到n2行之间的内容拷贝到第n3+1行【n3行的下一行】
* `:n1,n2 m n3`:    将n1行到n2行之间的内容移至到第n3行下
* `J`:    把下一行的数据连接到本行之后, 多一空格
* `~`:    改变当前光标下字符的大小写

其他

* `.`:    重复前一指令
* `u`:    取消前一指令undo, :u也行，一般不用，操作太多
* `Ctrl + r`:    恢复【只对u有效】redo
* `Ctrl + l`:    刷新屏幕显示
* `Ctrl+v 然后 ctrl+A是^A Ctrl+I是\t`:    输入特殊字符
* `Ctrl+v然后用j、k、l、h或方向键上下选中多列，之后 I I   a A  r  x等，最后按esc，生效`:    Vim列操作

![VIM Cheet Sheet](./assets/vim_cheet_sheet.jpg)

## 文本处理工具

### 显示文本内容`cat`

命令`cat`主要参数说明：

* `-E`：显示行结束符`$`
* `-A`：显示所有控制符
* `-n`：对显示出的每一行进行编号
* `-b`：非空行编号
* `-s`：压缩连续的空行成一行

举例：

```
cat -nA user-list.txt
     1  user0$
     2  user1$
     3  user2$
     4  user3$
     5  user4$
     6  user5$
     7  user6$
     8  user7$
     9  user8$
    10  user9$
```

### 显示文本行号`nl`

相当于命令`cat -b`。

命令`nl`主要参数说明：

* `-b` ：指定行号指定的方式，主要有两种：
* `-b a` ：表示不论是否为空行，也同样列出行号（类似 cat -n）；
* `-b t` ：如果有空行，空的那一行不要列出行号（默认值）；
* `-n` ：列出行号表示的方法，主要有三种：
* `-n ln` ：行号在屏幕的最左方显示；没有前导0；
* `-n rn` ：行号在自己栏位的最右方显示，没有前导0；
* `-n rz` ：行号在自己栏位的最右方显示，有前导0；
* `-w` ：行号栏位的占用的位数。
* `-p` ：在逻辑定界符处不重新开始计

举例：

```
$ nl -b a -n rz user-list.txt
000001  user0
000002  user1
000003  user2
000004  user3
000005  user4
000006  user5
000007  user6
000008  user7
000009  user8
000010  user9
```

### 逆向显示文本内容`tac`

命令`tac`逆向显示文本内容。

举例：

```
$ tac user-list.txt
user9
user8
user7
user6
user5
user4
user3
user2
user1
user0
```

举例：

```
$ seq 10 | tac
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

### 逆向显示同行内容`rev`

命令`rev`逆向显示同一行的内容。

举例：

```
$ rev user-list.txt
0resu
1resu
2resu
3resu
4resu
5resu
6resu
7resu
8resu
9resu
```

举例：

```
$ echo {1..10} | rev
01 9 8 7 6 5 4 3 2 1
```

### 显示非文本文件内容`hexdump`

命令`hexdump`命令一般用来查看“二进制”文件的十六进制编码

举例：

```
$ hexdump -C -n 32 cp
00000000  7f 45 4c 46 02 01 01 00  00 00 00 00 00 00 00 00  |.ELF............|
00000010  03 00 3e 00 01 00 00 00  e0 48 00 00 00 00 00 00  |..>......H......|
00000020
```

### 分页查看文件内容

命令`more`和`less`可以实现分页查看文件内容。

命令`less`配合管道符使用。

```
$ tree -d /etc | less
```

### 显示文件头部内容`head`

命令`head`显示文件头部内容。

* `head -c 20 cp`: 显示文件前20字节内容
* `head -n 20 zdiff`: 显示文件前20行内容
* `head -20 zdiff`: 显示文件前20行内容

```
$ echo "我是谁" | head -c3
我

$ echo "我是谁" | head -c6
我是
```

```
$ cat /dev/urandom | tr -dc '[:alnum]' | head -c 10 | tee passwd.txt
```

```
$ cat user-list.txt
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

$ head -n -3 user-list.txt
user0
user1
user2
user3
user4
user5
user6
```

### 显示文件尾部内容`tail`

命令`tail`显示文件头部内容。

* `tail -c 200 cp`: 显示文件尾部200个字节的内容
* `tail -n 3 user-list.txt`: 显示文件最后3行
* `tail -n -3 user-list.txt`: 显示从-3行到文件结束（即最后三行）
* `tail -3 user-list.txt`: 显示文件最后3行
* `tail -f /var/log/messages`: 跟踪显示文件redo.log文件内容，当文件删除，再建同名文件，无法继续追踪
* `tail -F /var/log/messages`: 跟踪显示文件redo.log文件内容，当文件删除，再建同名文件，继续追踪

### 按列抽取文本`cut`

命令`cut`可以提取文本文件或者stdin数据的指定列内容。

选项：

* `-f` : 通过指定哪一个字段进行提取。cut命令使用“TAB”作为默认的字段分隔符
* `-d` : “TAB”是默认的分隔符，使用此选项可以更改为其他的分隔符
* `--complement` : 此选项用于排除所指定的字段
* `--output-delimiter=STRING` : 指定输出内容的分隔符
* `-c`: 按字符切割

取/etc/passwd文件第1列内容，以`:`为分隔符（只取前三行）

```
$ cut -d ':' -f 1 /etc/passwd | head -3
root
messagebus
systemd-network
```

取/etc/passwd文件第1和6列内容，以`:`为分隔符（只取前三行）

```
cut -d ':' -f 1,6 /etc/passwd | head -3
root:/root
messagebus:/run/dbus
systemd-network:/
```

取/etc/passwd文件第1到3列以及第6列内容，以`:`为分隔符（只取前三行）

```
$ cut -d ':' -f 1-3,6 /etc/passwd | head -3
root:x:0:/root
messagebus:x:499:/run/dbus
systemd-network:x:497:/
```

下面使用`--output-delimiter`选项，把输出结果中的分隔符`:`全部替换成`---`。

```
$ cat /etc/passwd | sort | head -3
admin3:x:1020:100::/home/admin3:/bin/bash
at:x:25:25:Batch jobs daemon:/var/spool/atjobs:/usr/sbin/nologin
bin:x:1:1:bin:/bin:/usr/sbin/nologin

$ cut -d ":" -f 1,7 /etc/passwd | sort | head -3
admin3:/bin/bash
at:/usr/sbin/nologin
bin:/usr/sbin/nologin

$ cut -d ":" -f 1,7 --output-delimiter="---" /etc/passwd | sort | head -3
admin3---/bin/bash
at---/usr/sbin/nologin
bin---/usr/sbin/nologin
```

`--output-delimiter`选项也可以利用来进行计算。

```
$ echo {1..10} | cut -d " " -f 1-10 --output-delimiter="+" | bc
55
```

从`ifconfig`命令中截取当前主机的ip地址。（openSUSE需要安装包`net-tools-deprecated`）

```
$ ifconfig | head -2 | tail -1
        inet 192.168.10.210  netmask 255.255.255.0  broadcast 192.168.10.255

$ ifconfig | head -2 | tail -1 | cut -d " " -f 10
192.168.10.210
```

或者

```
$ ip addr list | grep eth0 | tail -1 | cut -d " " -f 6
192.168.10.210/24
```

基于上面结果，可以尝试通过`--complement`参数，以`/`为分隔符，排除第二列`24`，只输出第一列IP地址。

```
ip addr list | grep eth0 | tail -1 | cut -d " " -f 6 | cut -d "/" --complement -f 2
192.168.10.210
```

显示`df`命令输出中的分区使用率。

```
$ df | tr -s ' ' | cut -d ' ' -f 5 | tr -d %
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

方法2：先把空格全部替换成%，再去重。

```
df | tr -s ' ' % | cut -d % -f 5
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

### 合并多个文件`paste`

命令`paste`常用选项：

* `-d`：指定分隔符，默认是TAB
* `-s`：所有行合成一行显示

生成`alpha.log`和`seq.log`。

```
$ for i in {a..z}; do echo $i >> alpha.log; done

$ seq 10 > seq.log
```

用`paste`命令合并这2个文件。

```
$ paste alpha.log seq.log
a       1
b       2
c       3
d       4
e       5
f       6
g       7
h       8
i       9
j       10
k
l
m
n
o
p
q
r
s
t
u
v
w
x
y
z

$ paste -d ":" alpha.log seq.log
a:1
b:2
c:3
d:4
e:5
f:6
g:7
h:8
i:9
j:10
k:
l:
m:
n:
o:
p:
q:
r:
s:
t:
u:
v:
w:
x:
y:
z:
```

原文件都是列输出，改成行输出。

```bash
$ paste -d "-" -s alpha.log
a-b-c-d-e-f-g-h-i-j-k-l-m-n-o-p-q-r-s-t-u-v-w-x-y-z

$ paste -d "-" -s seq.log

$ paste -d ":" -s alpha.log seq.log
a:b:c:d:e:f:g:h:i:j:k:l:m:n:o:p:q:r:s:t:u:v:w:x:y:z
1:2:3:4:5:6:7:8:9:10

$ paste -d ":" -s seq.log alpha.log
1:2:3:4:5:6:7:8:9:10
a:b:c:d:e:f:g:h:i:j:k:l:m:n:o:p:q:r:s:t:u:v:w:x:y:z
```

### 文本统计数据`wc`

常用选项：

* `-l`：只计数行数
* `-w`：只计数单词总数
* `-c`：只计数字节总数
* `-m`：只计数字符总数
* `-L`：显示文件中最长行的长度

```
$ cat text
Tom, 20, Shanghai
Jack, 30, Beijing
Smith, 40, Guangzhou

$ wc text  # 行数 单词数 字节数
 3  9 57 text

$ wc -l text
3 text

$ wc -w text
9 text

$ wc -c text
57 text

$ wc -m text
57 text

$ wc -L text
20 text
```

对比两种不同合并的方法。

```
$ cat text1 text2
Tom, 20, Shanghai
Jack, 30, Beijing
Smith, 40, Guangzhou
Tom, 20, Shanghai
Jack, 30, Beijing
Leo, 40, Guangzhou

$ paste text1 text2
Tom, 20, Shanghai       Tom, 20, Shanghai
Jack, 30, Beijing       Jack, 30, Beijing
Smith, 40, Guangzhou    Leo, 40, Guangzhou
```

### 文本排序`sort`

命令`sort`把整理过的文本显示在stdout上，不改变原文件。

常用选项：

- `-r`：执行反方向（从上至下）排序

- `-R`：随机排序

- `-n`：按数字大小排序

- `-h`：人类可读排序，如：2K，1G

- `-f`：排序时将小写字母视为大写字母

- `-u`：排序时合并重复项

- `-t c`：使用c作为字段分隔符

- `-k #`：按照以c为分隔符的第#列来排序

举例：以`,`为分隔符，读取`text`文件内容中第1，3列，对输出结果以`,`为分隔符，按第二列排序（正序和反序）。

```
$ cat text
Tom, 20, Shanghai
Jack, 30, Beijing
Smith, 40, Guangzhou

$ cut -d "," -f 1,3 text | sort -t "," -k 1
Jack, Beijing
Smith, Guangzhou
Tom, Shanghai

$ cut -d "," -f 1,3 text | sort -t "," -k 1 -r
Tom, Shanghai
Smith, Guangzhou
Jack, Beijing
```

把文件text1和文件text2合并后去重输出。

```
$ cat text2
Tom, 20, Shanghai
Jack, 30, Beijing
Leo, 40, Guangzhou

$ cat text1
Tom, 20, Shanghai
Jack, 30, Beijing
Smith, 40, Guangzhou

$ cat text1 text2
Tom, 20, Shanghai
Jack, 30, Beijing
Smith, 40, Guangzhou
Tom, 20, Shanghai
Jack, 30, Beijing
Leo, 40, Guangzhou
```

并集，重复行只保留一行。前面2个命令是同样含义（相同的排序列），第三个命令中对不同列进行了排序，导致去重结果不同。

```
$ cat text1 text2 | sort -u
Jack, 30, Beijing
Leo, 40, Guangzhou
Smith, 40, Guangzhou
Tom, 20, Shanghai

$ cat text1 text2 | sort -t "," -k 1 -u
Jack, 30, Beijing
Leo, 40, Guangzhou
Smith, 40, Guangzhou
Tom, 20, Shanghai

$ cat text1 text2 | sort -t "," -k 2 -u
Tom, 20, Shanghai
Jack, 30, Beijing
Smith, 40, Guangzhou
```

### 去重`uniq`

命令`uniq`从输入中删除前后相邻重复的行。经常与`sort`命令结合使用。

主要参数：

- `-c`：显示每行重复出现的次数

- `-d`：仅显示重复的行

- `-u`：仅显示不重复的行

举例，注意只有对相邻行进行去重。

```
$ cat text3
test 30
Hello 95
Hello 95
Linux 85
Linux 85
Hello 95
test 30

$ uniq text3
test 30
Hello 95
Linux 85
Hello 95
test 30
```

把文件text1和文件text2合并后，进行交集和并集，并去重。

```
$ cat text1
Tom, 20, Shanghai
Jack, 30, Beijing
Smith, 40, Guangzhou

$ cat text2
Tom, 20, Shanghai
Jack, 30, Beijing
Leo, 40, Guangzhou

# 并集，按首列排序去重
$ cat text1 text2 | sort | uniq
Jack, 30, Beijing
Leo, 40, Guangzhou
Smith, 40, Guangzhou
Tom, 20, Shanghai

# 交集
$ cat text1 text2 | sort | uniq -d
Jack, 30, Beijing
Tom, 20, Shanghai

# 差集
$ cat text1 text2 | sort | uniq -u
Leo, 40, Guangzhou
Smith, 40, Guangzhou
```

查看并发连接数最多的远程主机IP。

```
$ ss -nt
State         Recv-Q         Send-Q                    Local Address:Port                      Peer Address:Port          Process
ESTAB         0              0                        192.168.10.210:22                      192.168.10.210:41650
ESTAB         0              0                        192.168.10.210:22                      192.168.10.201:65330
ESTAB         0              64                       192.168.10.210:22                      192.168.10.201:63289
ESTAB         0              0                        192.168.10.210:41650                   192.168.10.210:22
ESTAB         0              0                        192.168.10.210:47992                   192.168.10.210:22
ESTAB         0              0                        192.168.10.210:60268                   192.168.10.210:22
ESTAB         0              0                        192.168.10.210:22                      192.168.10.201:65327
ESTAB         0              0                        192.168.10.210:35758                   192.168.10.220:22
ESTAB         0              0                        192.168.10.210:22                      192.168.10.210:56818
ESTAB         0              0                        192.168.10.210:56818                   192.168.10.210:22
ESTAB         0              0                        192.168.10.210:48006                   192.168.10.210:22
ESTAB         0              0                        192.168.10.210:22                      192.168.10.210:60268
ESTAB         0              0                        192.168.10.210:22                      192.168.10.220:33896
ESTAB         0              0                        192.168.10.210:22                      192.168.10.201:65324
ESTAB         0              0                        192.168.10.210:22                      192.168.10.210:47992
ESTAB         0              0                        192.168.10.210:59554                   192.168.10.210:22
ESTAB         0              0                        192.168.10.210:22                      192.168.10.210:59554
ESTAB         0              0                        192.168.10.210:22                      192.168.10.210:48006

$ ss -nt | tr -s " " ":" | cut -d ":" -f 6,7 | sort | uniq -c | sort -nr | head -n 1
      6 192.168.10.210:22
```

### 文本比较

#### `diff`

命令`diff`比较两个文件之间的区别。

常用选项：

- `-u`：以统一的方式来显示文件内容的不同
- `-y`：以并列的方式显示文件的异同之处
- `-W`：在使用-y参数时，指定栏宽
- `-c`：显示全部内文，并标出不同之处
- `-N`：缺失文件以空文件处理

举例：

```
$ cat text5 # 文件尾部没有空行
1001
1002
1003

$ cat text6 # 文件尾部没有空行
1001
1002
1003a
1004
```

显示不同。`3c3,4`代表两个文件在第3，4行有不同。

```
$ diff text5 text6
3c3,4
< 1003
---
> 1003a
> 1004
```

以统一格式输出比较结果。

* 前2行是文件信息。其中`---`表示变动前的文件，`+++`表示变动后的文件。
* 变动的位置用两个@作为起首和结束，`@@ -1,3 +1,4 @@`。
  * `-1,3`中，`-`表示第一个文件，即`text5`。第一个文件从第1行开始连续3行。
  * `+1,4`中，`+`表示第二个文件，即`text6`。即，第二个文件从第1行开始连续4行。

```
$ diff -u text5 text6
--- text5    2022-12-07 08:07:05.927805722 +0800
+++ text6    2022-12-07 08:07:24.692234585 +0800
@@ -1,3 +1,4 @@
 1001
 1002
-1003
+1003a
+1004
```

以上下文方式输出比较结果。标有`!`代表差异行。

```
$ diff -c text5 text6
*** text5    2022-12-07 08:24:08.867168414 +0800
--- text6    2022-12-07 08:24:13.939284243 +0800
***************
*** 1,3 ****
  1001
  1002
! 1003
--- 1,4 ----
  1001
  1002
! 1003a
! 1004
```

并排格式输出比较结果。

* `|`表示前后2个文件内容有不同

* `<`表示后面文件比前面文件少了1行内容

* `>`表示后面文件比前面文件多了1行内容
  
  ```
  $ diff -y -W 50 text5 text6
  1001        1001
  1002        1002
  1003      | 1003a
          > 1004
  ```

比较文件夹内容。注意，只比较内容，不比较时间戳。

```
$ mkdir dir1
$ mkdir dir2

$ cd dir1
$ touch file1
$ touch file2
$ cp file1 file2 ../dir2/
$ echo "hello" > file3

$ cd ../dir2
$ touch file3
$ touch file4

$ diff dir1 dir2
1d0
< hello
Only in dir2: file4
```

#### `patch`

命令`patch`复制其他文件中的内容。命令格式：

```
$ patch -p[num] < patchfile
$ patch [options] originalfile patchfile 
```

当特定软件有可用的安全修复程序时，我们通常会使用 `yum`或 `apt-get` 或`zypper`等包管理工具进行二进制升级。 

但如果我们是通过从源代码编译安装软件的情况下，我们需要下载安全补丁并将其应用于原始源代码并重新编译软件。 

这就是我们使用 `diff` 创建补丁文件（patch file），并使用 `patch `命令应用它。 

补丁文件是一个文本文件，其中包含同一文件（或同一源代码树）的两个版本之间的差异。 补丁文件是使用 `diff `命令创建的。

继续上例。

将文件`text5`的内容同步到文件`text6`，然后撤销补丁。注意区分源文件和目标文件。

```
$ cat text5
1001
1002
1003

$ cat text6
1001
1002
1003a
1004

# 生成补丁文件
$ diff -ruN text5 text6 > patchfile

$ cat patchfile
--- text5    2022-12-07 08:24:08.867168414 +0800
+++ text6    2022-12-07 08:24:13.939284243 +0800
@@ -1,3 +1,4 @@
 1001
 1002
-1003
+1003a
+1004

# 不指明目标文件，则默认给diff命令中的源文件进行打补丁
$ patch < patchfile
patching file text5

$ cat text5
1001
1002
1003a
1004

$ cat text6
1001
1002
1003a
1004

# 撤销补丁
patch -R < patchfile
patching file text5

# cat text5
1001
1002
1003

# 给text6文件打补丁（用text5的文件内容覆盖text6的内容）
$ patch text6 patchfile
patching file text6
Reversed (or previously applied) patch detected!  Assume -R? [n] y

$ cat text6
1001
1002
1003

# 撤销给text6文件打的补丁（恢复text6文件补丁前的内容）
$ patch -R text6 patchfile
patching file text6
Unreversed patch detected!  Ignore -R? [n] y

$ cat text6
1001
1002
1003a
1004
```

使用`-b`参数，在patch前先备份源文件。

```
$ patch -b < patchfile
patching file text5

$ cat text5
1001
1002
1003a
1004

$ cat text5.orig
1001
1002
1003

$ cat text6.orig
1001
1002
1003

$ patch -R < patchfile
patching file text5
```

在-b参数中加入-V参数，指定备份文件名的格式，如下，会得到文件`text5.~1~`。

```
$patch -b -V numbered < patchfile
patching file text5

$ cat text5
1001
1002
1003a
1004

$ cat text5.~1~
1001
1002
1003
```

试运行，不做实际更改。

```
patch --dry-run < patchfile
```

对目录打补丁。

* 执行`diff`和`patch`命令是在当前用户`vagrant`的主目录下，绝对路径是`/home/vagrant`。
* `diff`命令中，源目录是`/home/vagrant/dir1`。目标目录是`/home/vagrant/dir2`。
* `-p3`是告诉`patch`命令忽略上面绝对路径中前三个斜杠`/`。
* `patch`命令中用`diff`的目标目录去覆盖源目录。互换会报错。
* `-R`：撤销补丁。

```
# file3和file4有内容
$ tree ./dir1
./dir1
├── file1
├── file2
├── file3
└── subdir1
  └── file4


都是空文件

$ tree ./dir2
./dir2
├── file1
├── file2
├── file3
└── subdir1
 └── file4

$ diff -ruN /home/vagrant/dir1 /home/vagrant/dir2 > patchdir

$ cat patchdir
diff -ruN /home/vagrant/dir1/file3 /home/vagrant/dir2/file3
--- /home/vagrant/dir1/file3 2022-12-07 08:42:33.108418336 +0800
+++ /home/vagrant/dir2/file3 2022-12-07 21:25:48.156056360 +0800
@@ -1 +0,0 @@
-hello
diff -ruN /home/vagrant/dir1/subdir1/file4 /home/vagrant/dir2/subdir1/file4
--- /home/vagrant/dir1/subdir1/file4 2022-12-07 21:15:09.689912160 +0800
+++ /home/vagrant/dir2/subdir1/file4 2022-12-07 21:26:55.405546177 +0800
@@ -1 +0,0 @@
-/home/vagrant/dir1/subdir1

# 用dir2的内容覆盖dir1的内容

$ patch -p3 < patchdir
patching file dir1/file3
patching file dir1/subdir1/file4

# 现在dir1目录下的内容已经被dir2目录覆盖了。file3和file4都是空文件

$ ll ./dir1
total 0
-rw-r--r--. 1 vagrant wheel 0 Dec 7 08:34 file1
-rw-r--r--. 1 vagrant wheel 0 Dec 7 08:35 file2
-rw-r--r--. 1 vagrant wheel 0 Dec 7 21:40 file3
drwxr-xr-x. 1 vagrant wheel 10 Dec 7 21:40 subdir1

$ ll ./dir1/subdir1
total 0
-rw-r--r--. 1 vagrant wheel 0 Dec 7 21:40 file4

# 撤销补丁，file3和file4已经恢复为原文件

$ patch -R -p3 < patchdir
patching file dir1/file3
patching file dir1/subdir1/file4

$ ll ./dir1
-rw-r--r--. 1 vagrant wheel 0 Dec 7 08:34 file1
-rw-r--r--. 1 vagrant wheel 0 Dec 7 08:35 file2
-rw-r--r--. 1 vagrant wheel 6 Dec 7 21:45 file3
drwxr-xr-x. 1 vagrant wheel 10 Dec 7 21:45 subdir1

$ ll ./dir1/subdir1
-rw-r--r--. 1 vagrant wheel 27 Dec 7 21:45 file4

# 用dir1的内容覆盖dir2的内容，系统拒绝。

patch dir2 -p3 < patchdir
File dir2 is not a regular file -- refusing to patch
1 out of 1 hunk ignored -- saving rejects to file dir2.rej
File dir2 is not a regular file -- refusing to patch
1 out of 1 hunk ignored -- saving rejects to file dir2.rej

$ patch /home/vagrant/dir2 -p3 < patchdir
File /home/vagrant/dir2 is not a regular file -- refusing to patch
1 out of 1 hunk ignored -- saving rejects to file /home/vagrant/dir2.rej
File /home/vagrant/dir2 is not a regular file -- refusing to patch
1 out of 1 hunk ignored -- saving rejects to file /home/vagrant/dir2.rej
```

#### `vimdiff`

命令`vimdiff`相当于`vim -d`。

举例：

```
$ vimdiff text1 text2
```

#### `cmp`

命令`cmp`查看二进制文件的不同。

```
$ cmp cp grep
cp grep differ: byte 25, line 1

$ cmp /usr/bin/ls /usr/bin/dir
/usr/bin/ls /usr/bin/dir differ: byte 613, line 1

# 跳过前735个字节，输出后面30个字节内容

$ hexdump -s 735 -Cn 30 /usr/bin/ls
000002df 00 00 00 00 00 5d 00 00 00 50 00 00 00 68 00 00 |.....]...P...h..|
000002ef 00 6a 00 00 00 4f 00 00 00 00 00 00 00 1d |.j...O........|
000002fd $ hexdump -s 735 -Cn 30 /usr/bin/dir
000002df 00 00 00 00 00 5d 00 00 00 50 00 00 00 68 00 00 |.....]...P...h..|
000002ef 00 6a 00 00 00 4f 00 00 00 00 00 00 00 1d |.j...O........|
000002fd
```




## 正则表达式

正则表达式分两类：

* 基本正则表达式（Basic Regular Expression， 又叫Basic RegEx，简称BREs）
* 扩展正则表达式（Extended Regular Expression， 又叫Extended RegEx，简称EREs）
* Perl正则表达式（Perl Regular Expression， 又叫Perl RegEx 简称PREs

基本的正则表达式和扩展正则表达式的区别就是元字符的不同。


### 基本正则表达式符号

`^`：表示以某个字符开始
`$`：表示以某个字符结尾
`.`：表示匹配一个且只匹配一个字符
`*`：表示匹配前边一个字符出现0次或者多次
`[]`：表示匹配括号内的多个字符信息,一个一个匹配
`.*`：表示匹配所有，空行也会进行匹配
`[^]`：表示不匹配括号内的每一个字符
`^$`：表示匹配空行信息
`\`：将有特殊含义的字符转义为通配符


### 扩展正则表达式符号

`+`：表示前一个字符出现一次或一次以上
`?`：表示前一个字符出现0次或者一次以上
`|`：表示或者的关系,匹配多个信息
`()`：匹配一个整体信息，也可以接后项引用
`{}`：定义前边字符出现几次


!!! Tips
    `grep -E` 或者`egrep`只是表示扩展正则，不代表加了e就表示转义了。

    当`grep`使用扩展正则的符号时候需要用`\`转义为通配符才能使用。




### 字符匹配

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


### 位置标记

位置标记锚点（position marker anchor）是标识字符串位置的正则表达式。默认情况下，正则表达式所匹配的字符可以出现在字符串中任何位置。

* `^`：行首锚定，指定了匹配正则表达式的文本必须起始于字符串的首部。
    * 例如：`^tux`能够匹配以`tux`起始的行

* `$`：行尾锚定，指定了匹配正则表达式的文本必须结束于目标字符串的尾部。
    * 例如：`tux$`能够匹配以`tux`结尾的行

* `^PATTERN$`：用模式PATTERN匹配整行。

* `^$`：匹配空行。

* `^[[:space:]]*$`：匹配空白行（整行）。

* `\<`或`\b`：词首锚定，用于单词模式匹配左侧。（单词是有字母、数字、下划线组成）

* `\>`或`\b`：词尾锚定，用于单词模式匹配右侧。（单词是有字母、数字、下划线组成）

* `\<PATTERN\>`：匹配整个单词。（单词是有字母、数字、下划线组成）





### 标识符

标识符是正则表达式的基础组成部分。它定义了那些为了匹配正则表达式，必须存在（或不存在）的字符。

* `A`字符：正则表达式必须匹配该字符。
    * 例如：`A`能够匹配字符`A`。

* `.`：匹配任意一个字符。
    * 例如：`Hack.`能够匹配`Hackl`和`Hacki`，但是不能匹配`Hackl2`或`Hackil`，它只能匹配单个字符。

* `[]`：匹配中括号内的任意一个字符。中括号内可以是一个字符组或字符范围 	
    * 例如：`coo[kl]`能够匹配`cook`或`cool`。
    * 例如：`[0-9]`匹配任意单个数字

* `[^]`：匹配不在中括号内的任意一个字符。中括号内可以是一个字符组或字符范围 	
    * 例如：`9[^01]`能够匹配`92`和`93`，但是不匹配`91`和`90`。
    * 例如：`A[^0-9]`匹配A以及随后除数字外的任意单个字符

* `\s`：匹配任何空白字符，包括空格、制表符、换页等。等价于`[\f\r\t\v]`

* `\S`：匹配任何非空白字符，等价于`[^\f\r\t\v]`

* `\w`：匹配一个字母、数字、下划线、汉字、其他国家文字字符，等价于`[_[:alnum:]字]`

* `\W`：匹配一个非字母、数字、下划线、汉字、其他国家文字字符，等价于`[^_[:alnum:]字]`




### 数量修饰符

一个标识符可以出现一次、多次或是不出现。数量修饰符定义了模式可以出现的次数。

* `?`：匹配之前的项0次或1次。
    * 例如：`colou?r`能够匹配`color`或`colour`，但是不能匹配`colouur`。

* `+`：匹配之前的项1次或多次。
    * 例如：`Rollno-9+`能够匹配`Rollno-99`和`Rollno-9`，但是不能匹配`Rollno-`。
    * 例如：`colou+r`能够匹配`colour`或`colouur`，不能匹配`color`。
    * 例如：`goo\+gle`能够匹配1个或多个`o`，如：`google`，`gooogle`，`goooogle`等。

* `*`：匹配之前的项0次或多次。
    * 例如：`co*l`能够匹配`col`和`coool`。
    * 例如：`goo*gle`能匹配0个或多个`o`，如：`gogle`、`google`、`gooogle`、`gooooooooogle`等。
    * 例如：`gooo*gle`，则可以匹配`google`、`gooogle`、`gooooooooogle`等，对比上面等差别。

* `.*`：匹配任意长度等任意字符。

* `{n}`：匹配之前的项`n`次。
    * 例如：`[0-9]{3}`能够匹配任意的三位数。
    * 例如：`[0-9]{3}`可以扩展为`[0-9][0-9][0-9]`。

* `{n}`：之前的项至少需要匹配`n`次。
    * 例如：`[0-9]{2,}`能够匹配任意一个两位或更多位的数字。
    * 例如：`go\{2,\}gle`能够匹配2个或者多个`o`，如`google`，`gooooogle`等，不能匹配`gogle`。

* `{n,m}`：之前的项所必须匹配的最小`n`次数和最大`m`次数。
    * 例如：`[0-9]{2,5}`能够匹配两位数到五位数之间的任意一个数字。




### 分组

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
```
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
```
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
```
$ grep '^$' /etc/profile
$ grep -v '^$' /etc/profile
```

匹配非空行和非#开头的行：（三种方法）
```
$ grep -v '^$' /etc/profile | grep -v '^#'
$ grep -v '^$\|#' /etc/profile
$ grep '^[^#]' /etc/profile
```


### 小练习


* 显示`/proc/meminfo`文件中以大小s开头的行，要求使用两种方法。
```
$ cat /proc/meminfo | grep -i "^s"

$ cat /proc/meminfo | grep "^[sS]"
```


* 显示`/etc/passwd`文件中不以`/bin/bash`结尾的行。
```
$ grep -v "/bin/bash$" /etc/passwd
```


* 显示用户`rpc`默认的shell程序。
```
$ grep "rpc" /etc/passwd | cut -d ":" -f 7
/sbin/nologin
```


* 找出`/etc/passwd`中的两位或三位数。
```
$ grep -Eo "[:digit:]{2,3}" /etc/passwd
$ grep -Eo "[0-9]{2,3}" /etc/passwd
```
这里用到了`{}`，属于扩展正则符号，所以要用`-E`。


* 显示Rocky 9的`/etc/grub2.cfg`文件中，至少以一个空白字符开头的且后面有非空白字符的行。（注：`/etc/grub2.cfg`在openSUSE和Ubuntu中没有）
```
# 不含首字符为tab
$ sudo grep "^ " /etc/grub2.cfg

# 包含首字符为tab
$ sudo grep "^[[:space:]]" /etc/grub2.cfg
```


* 找出`netstat -tan`命令结果中以`LISTEN`后跟任意多个空白字符结尾的行。
```
$ netstat -tan | grep -E "LISTEN[[:space:]]+"
```


* 显示Rocky 9上所有UID小于1000以内的用户名和UID。
```
$ cat /etc/passwd | cut -d ":" -f 1,3 | grep -E "\:[0-9]{1,3}$"
$ grep -E "\:[0-9]{1,3}\:[0-9]{1,}" /etc/passwd | cut -d ":" -f 1,3
```


* 在Rocky 9上显示文件`/etc/passwd`用户名和shell同名的行。
```
$ grep -E "^([[:alnum:]]+\b).*\1$" /etc/passwd
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
```


* 利用`df`和`grep`，取出磁盘各分区利用率,并从大到小排序。
```
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


* 显示三个用户`root`，`mage`，`wang`的UID和默认shell。
```
$ grep "^root:\|^sync:\|^bin:" /etc/passwd | cut -d ":" -f 1,7
root:/bin/bash
bin:/usr/sbin/nologin
```


* 使用`egrep`取出`/etc/default-1/text_2/local.3/grub`中其基名和目录名。
```
# 基名
$ echo "/etc/default-1/text_2/local.3/grub" | egrep -io "[[:alpha:]]+$"
grub

# 目录名
$  echo "/etc/default-1/text_2/local.3/grub" | egrep -io "/([[:alpha:]]+.|_?[[:alpha:]]|[[:alnum:]]+/){7}"
/etc/default-1/text_2/local.3/ 
```


* 统计`last`命令中以`vagrant`登录的每个主机IP地址登录次数。
```
$ last | grep vagrant | tr -s " " | cut -d " " -f 3 | grep -E "([0-9]{1,3}\.){1,3}[0-9]{1,3}" | sort -n | uniq -c
     24 192.168.10.107
     38 192.168.10.109
     17 192.168.10.201
      6 192.168.10.210
      2 192.168.10.220
```


* 利用扩展正则表达式分别表示0-9、10-99、100-199、200-249、250-255。
```
[0-9]|[0-9]{2}|1[0-9]{2}|2[0-4][0-9]|25[0-5]
```


* 显示`ifconfig`命令结果中所有IPv4地址。
```
$ ifconfig | grep -Eo "([0-9]{1,3}\.){3}[0-9]{1,3}" | grep -v "^255"
192.168.10.210
192.168.10.255
127.0.0.1

```


* 显示`ip addr`命令结果中所有IPv4地址。
```
$ ip addr show eth0 | grep inet | grep eth0 | tr -s " " | cut -d " " -f 3 | cut -d "/" -f 1
192.168.10.210

$ ip addr show | grep -Eo "([0-9]{1,3}\.){3}[0-9]{1,3}" | grep -v "^255"
127.0.0.1
192.168.10.210
192.168.10.255
```


* 将此字符串Welcome to the linux world中的每个字符去重并排序，重复次数多的排到前面。
```
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



## `grep`命令


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
```
grep root /etc/passwd
root:x:0:0:root:/root:/bin/bash

$ grep "USER" /etc/passwd

$ grep "$USER" /etc/passwd
vagrant:x:1000:478:vagrant:/home/vagrant:/bin/bash

$ grep '$USER' /etc/passwd

```

匹配关键字：
```
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
```
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

!!! Tips
    `grep -wvf f1 f2` 或者`grep -w -v -f f1 f2`中，`-f`只能作为最后一个参数，否则会报错。



体会基本正则和扩展正则的差异。

例1：转义。
```
# 下面几个命令返回的结果是一样的。
$ grep "root\|bash" /etc/passwd
$ grep -E "root|bash" /etc/passwd
$ grep -e "root" -e "bash" /etc/passwd

# 下面的命令没有匹配结果返回。
$ grep "root|bash" /etc/passwd
```

例2：下面4个命令返回同样的结果。
```
$ grep "root" /etc/passwd
$ grep -E "root" /etc/passwd
$ grep "\<root\>" /etc/passwd
$ grep -E "\<root\>" /etc/passwd
```

例3：行首行尾锚定。
```
$ grep "^\(.*\)\>.*\<\1$" /etc/passwd
$ grep -E "^(.*)\>.*\<\1$" /etc/passwd
$ egrep "^(.*)\>.*\<\1$" /etc/passwd
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
```

例4：三种方法求和计算，运用`grep`，`cut`，`bc`和`paste`命令。
```
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






## `sed`命令

`sed`是stream editor的缩写，中文称之为“流编辑器”。
`sed`命令是一个面向行处理的工具，它以“行”为处理单位，针对每一行进行处理，处理后的结果会输出到标准输出`STDOUT`，不会对读取的文件做任何修改。


`sed`的工作原理：

`sed`命令是面向“行”进行处理的，每一次处理一行内容。
处理时，`sed`会把要处理的行存储在缓冲区中，接着用`sed`命令处理缓冲区中的内容，处理完成后，把缓冲区的内容送往屏幕。接着处理下一行，这样不断重复，直到文件末尾。这个缓冲区被称为“模式空间”（pattern space）。






## `awk`命令


