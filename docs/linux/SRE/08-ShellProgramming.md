# 第八章 shell编程

## 基本用法

格式要求：首行shebang机制

```shell
#!/bin/bash
#!/usr/bin/python
```

执行方法（注意文件的相对路径）：

```bash
bash hello.sh
cat hello.sh | bash
bash < hello.sh
chmod +x hello.sh
./hello.sh
~/hello.sh
```

shell脚本调试：

- 命令错误继续当前脚本执行。`bash -x test.sh`会逐行显示每个命令的执行结果，用以排错。
- 语法错误会中断当前脚本执行。`bash -n test.sh`会检查语法错误。

### 变量

变量分类：

- 内置变量
- 外部变量

常用命名习惯：

1. 变量名：
   - 使用小写字母，单词之间用下划线分隔（snake_case），这是Shell脚本中最常用的变量命名习惯。
   - 例如：`variable_name="value"`。

2. 局部变量名：
   - 与全局变量类似，通常也使用小写字母和下划线分隔的命名方式。
   - 如果需要区分局部变量和全局变量，可以在局部变量名前加上下划线，以避免命名冲突。
   - 例如：`local _local_variable="value"`。

3. 函数名：
   - 函数名通常使用小驼峰命名法（lowerCamelCase），首字母小写，后续单词首字母大写。
   - 例如：`doSomething() { ... }`。

4. 环境变量：
   - 环境变量通常使用大写字母，单词之间用下划线分隔，这是操作系统层面的命名习惯。
   - 例如：`export PATH="/usr/bin:/bin"`。

5. 数组：
   - 数组的命名习惯与变量类似，通常使用小写字母和下划线分隔。
   - 例如：`array_name=(element1 element2)`。

6. 常量：
   - 常量通常使用大写字母和下划线分隔，以表示它们是不可变的。
   - 例如：`CONSTANT_NAME="constant_value"`。

7. Shell内置变量：
   - Shell内置变量遵循它们自己的命名习惯，通常是小写字母和下划线分隔，如`$HOME`、`$PWD`等。

8. Shell脚本文件名：
   - 脚本文件名通常使用小写字母，单词之间用下划线分隔，以符合Unix/Linux的文件系统习惯。
   - 例如：`script_name.sh`。








变量定义和引用：

- 普通变量
- 环境变量
- 本地变量

位置变量状态变量












### 算术和逻辑运算

### 条件测试

### 条件组

### 循环

## 配置文件

## 条件选择

## 流程控制

## 函数

## 其它脚本工具

## 数组

## 字符串处理

## 高级变量
