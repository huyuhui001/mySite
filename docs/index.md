# 知行斋

## 1.Linux

### 1.1.Linux SRE

- [第一章 Linux基础](linux/SRE/01-fundamentals.md)
- [第二章 文件系统](linux/SRE/02-filesystem.md)
- [第三章 身份与安全](linux/SRE/03-identity-security.md)
- [第四章 文本编辑](linux/SRE/04-TextTools.md)
- [第五章 正则表达式](linux/SRE/05-RegExpress.md)
- [第六章 文件查找](linux/SRE/06-FileLookup.md)
- [第七章 文件打包和解包](linux/SRE/07-FilePacking.md)

### 1.2.SUSE Linux Administration

- [Linux File System Overview](linux/Administration/01.md)
- [Useful Commands](linux/Administration/02.md)
- [Shell](linux/Administration/03.md)

### 1.3.SUSE Enterprise Storage Foundation

- [SUSE Enterprise Storage Foundation](linux/SES/linux_ses_memo.md)
- [SUSE Enterprise Storage Basic Operation](linux/SES/linux_ses_demo.md)

## 2.Kubernetes

### 2.1.CKA Learning Memo

Installation

- [Single Node Installation](k8s/cka_en/installation/single-local.md)
- [Multiple Nodes Installation](k8s/cka_en/installation/multiple-local.md)
- [Installation on Aliyun ECS](k8s/cka_en/installation/aliyun-ubuntu.md)

Docker

- [Fundamentals](k8s/cka_en/foundamentals/docker.md)

Foundamentals

- [Memo](k8s/cka_en/foundamentals/memo.md)
- [Overview](k8s/cka_en/foundamentals/overview.md)
- [kubectl basics](k8s/cka_en/foundamentals/basics.md)

Core Kubernetes

- [Pod](k8s/cka_en/foundamentals/pod.md)
- [Deployment](k8s/cka_en/foundamentals/deployment.md)
- [Service](k8s/cka_en/foundamentals/service.md)

Application Modeling

- [Namespace](k8s/cka_en/foundamentals/namespace.md)
- [StatefulSet](k8s/cka_en/foundamentals/statefulset.md)
- [DaemonSet](k8s/cka_en/foundamentals/daemonset.md)
- [Job and Cronjob](k8s/cka_en/foundamentals/job.md)
- [Configuration](k8s/cka_en/foundamentals/configuration.md)
- [Secrets](k8s/cka_en/foundamentals/secrets.md)
- [Persistence](k8s/cka_en/foundamentals/persistence.md)
- [Role Based Access Control (RBAC)](k8s/cka_en/foundamentals/rbac.md)
- [Ingress](k8s/cka_en/foundamentals/ingress.md)

Advanced Kubernetes

- [Scheduling](k8s/cka_en/foundamentals/scheduling.md)
- [Horizontal Pod Autoscaling](k8s/cka_en/foundamentals/hpa.md)
- [Policy](k8s/cka_en/foundamentals/policy.md)
- [Network Policy](k8s/cka_en/foundamentals/networkpolicy.md)
- [Cluster Management](k8s/cka_en/foundamentals/clustermgt.md)

Operating Kubernetes

- [Troubleshooting](k8s/cka_en/foundamentals/troubleshooting.md)
- [Health Check](k8s/cka_en/foundamentals/healthcheck.md)
- [Helming](k8s/cka_en/foundamentals/helming.md)

Topics

- [Operations on Resources](k8s/cka_en/foundamentals/casestudy-operation-resources.md)
- [Health Check](k8s/cka_en/foundamentals/casestudy-health-check.md)
- [Calico Installation](k8s/cka_en/foundamentals/casestudy-calico.md)
- [Kyma](k8s/cka_en/foundamentals/kyma.md)

### 2.2.CKA学习笔记

安装

- [单节点虚拟机安装Kubernetes](k8s/cka_cn/installation/single-local.md)
- [多节点虚拟机安装Kubernetes](k8s/cka_cn/installation/multiple-local.md)
- [阿里云ECS安装Kubernetes](k8s/cka_cn/installation/aliyun-ubuntu.md)

Docker

- [Docker基础](k8s/cka_cn/foundamentals/docker.md)

基础知识

- [Kubernetes随笔](k8s/cka_cn/foundamentals/memo.md)
- [Kubernetes集群概览](k8s/cka_cn/foundamentals/overview.md)
- [kubectl基础](k8s/cka_cn/foundamentals/basics.md)

核心概念

- [Pod](k8s/cka_cn/foundamentals/pod.md)
- [Deployment](k8s/cka_cn/foundamentals/deployment.md)
- [Service](k8s/cka_cn/foundamentals/service.md)

应用体系

- [Namespace](k8s/cka_cn/foundamentals/namespace.md)
- [StatefulSet](k8s/cka_cn/foundamentals/statefulset.md)
- [DaemonSet](k8s/cka_cn/foundamentals/daemonset.md)
- [Job and Cronjob](k8s/cka_cn/foundamentals/job.md)
- [Configuration](k8s/cka_cn/foundamentals/configuration.md)
- [secrets](k8s/cka_cn/foundamentals/secrets.md)
- [Persistence](k8s/cka_cn/foundamentals/persistence.md)
- [RBAC鉴权](k8s/cka_cn/foundamentals/rbac.md)
- [Ingress-nginx](k8s/cka_cn/foundamentals/ingress.md)

进阶概念

- [Scheduling](k8s/cka_cn/foundamentals/scheduling.md)
- [Horizontal Pod Autoscaling (HPA)](k8s/cka_cn/foundamentals/hpa.md)
- [Policy](k8s/cka_cn/foundamentals/policy.md)
- [Network Policy](k8s/cka_cn/foundamentals/networkpolicy.md)
- [Cluster Management](k8s/cka_cn/foundamentals/clustermgt.md)

日常维护

- [Troubleshooting](k8s/cka_cn/foundamentals/troubleshooting.md)
- [健康检查](k8s/cka_cn/foundamentals/healthcheck.md)
- [Helm Chart](k8s/cka_cn/foundamentals/helming.md)

主题讨论

- [Kubernetes资源常见操作](k8s/cka_cn/foundamentals/casestudy-operation-resources.md)
- [健康检查](k8s/cka_cn/foundamentals/casestudy-health-check.md)
- [安装Calico](k8s/cka_cn/foundamentals/casestudy-calico.md)

Demos

- [Build CAP Application on Kyma](k8s/demo/cap_on_kyma.md)
  
## 3.Python

### 3.1.Python基础

- [Python安装](python/Foundation/ch00.md)
- [Python语言基础](python/Foundation/ch01.md)
- [Python打包和解包](python/Foundation/ch02.md)
- [Python内置函数及文件](python/Foundation/ch03.md)
- [Python面向对象概念](python/Foundation/ch04.md)
- [Python面向对象三大特性](python/Foundation/ch05.md)

### 3.2.Python数据分析基础

- [NumPy基础](python/DataAnalysis/ch01.md)
- [NumPy进阶](python/DataAnalysis/ch10.md)
- [Pandas入门](python/DataAnalysis/ch02.md)
- [数据载入、存储及文件格式](python/DataAnalysis/ch03.md)
- [数据清洗与准备](python/DataAnalysis/ch04.md)
- [数据规整：连接、联合与重塑](python/DataAnalysis/ch05.md)
- [绘图与可视化](python/DataAnalysis/ch06.md)
- [数据聚合与分组操作](python/DataAnalysis/ch07.md)
- [时间序列](python/DataAnalysis/ch08.md)
- [高阶pandas](python/DataAnalysis/ch09.md)
- [Python建模库介绍](python/DataAnalysis/ch11.md)

### 3.3.数据结构和算法

- [1.基础知识回顾](python/DataStructure/01_PythonFundmantal.md)
- [2.多项集的概述](python/DataStructure/02_CollectionsOverview.md)
- [3.搜索、排序以及复杂度分析](python/DataStructure/03_TimeComplexity.md)
- [4.数组和链接结构](./python/DataStructure/04_ArrayChain.md)
- [5.接口、实现和多态](./python/DataStructure/05_InterfacePolymorphism.md)
- [6.继承与抽象类](./python/DataStructure/06_InheritanceAbstractClass.md)

### 3.5.Effective Python

- 第1章　培养Pythonic思维
  - [第1条　查询自己使用的Python版本](./python/Pythonic90Rules/Rule01.md)
  - [第2条　遵循PEP 8风格指南](./python/Pythonic90Rules/Rule02.md)
  - [第3条　了解bytes与str的区别](./python/Pythonic90Rules/Rule03.md)
  - [第4条　用支持插值的f-string取代C风格的格式字符串与str.format方法](./python/Pythonic90Rules/Rule04.md)
  - [第5条　用辅助函数取代复杂的表达式](./python/Pythonic90Rules/Rule05.md)
  - [第6条　把数据结构直接拆分到多个变量里，不要专门通过下标访问](./python/Pythonic90Rules/Rule06.md)
  - [第7条　尽量用enumerate取代range](./python/Pythonic90Rules/Rule07.md)
  - [第8条　用zip函数同时遍历两个迭代器](./python/Pythonic90Rules/Rule08.md)
  - [第9条　不要在for与while循环后面写else块](./python/Pythonic90Rules/Rule09.md)
  - [第10条　用赋值表达式减少重复代码](./python/Pythonic90Rules/Rule10.md)
- 第2章　列表与字典
  - [第11条　学会对序列做切片](./python/Pythonic90Rules/Rule11.md)
  - [第12条　不要在切片里同时指定起止下标与步进](./python/Pythonic90Rules/Rule12.md)
  - [第13条　通过带星号的unpacking操作来捕获多个元素，不要用切片](./python/Pythonic90Rules/Rule13.md)
  - [第14条　用sort方法的key参数来表示复杂的排序逻辑](./python/Pythonic90Rules/Rule14.md)
  - [第15条　不要过分依赖给字典添加条目时所用的顺序](./python/Pythonic90Rules/Rule15.md)
  - [第16条　用get处理键不在字典中的情况，不要使用in与KeyError](./python/Pythonic90Rules/Rule16.md)
  - [第17条　用defaultdict处理内部状态中缺失的元素，而不要用setdefault](./python/Pythonic90Rules/Rule17.md)
  - [第18条　学会利用__missing__构造依赖键的默认值](./python/Pythonic90Rules/Rule18.md)
- 第3章　函数
  - [第19条　不要把函数返回的多个数值拆分到三个以上的变量中](./python/Pythonic90Rules/Rule19.md)
  - [第20条　遇到意外状况时应该抛出异常，不要返回None](./python/Pythonic90Rules/Rule20.md)
  - [第21条　了解如何在闭包里面使用外围作用域中的变量](./python/Pythonic90Rules/Rule21.md)
  - [第22条　用数量可变的位置参数给函数设计清晰的参数列表](./python/Pythonic90Rules/Rule22.md)
  - [第23条　用关键字参数来表示可选的行为](./python/Pythonic90Rules/Rule23.md)
  - [第24条　用None和docstring来描述默认值会变的参数](./python/Pythonic90Rules/Rule24.md)
  - [第25条　用只能以关键字指定和只能按位置传入的参数来设计清晰的参数列表](./python/Pythonic90Rules/Rule25.md)
  - [第26条　用functools.wraps定义函数修饰器](./python/Pythonic90Rules/Rule26.md)
- 第4章　推导与生成
  - [第27条　用列表推导取代map与filter](./python/Pythonic90Rules/Rule27.md)
  - [第28条　控制推导逻辑的子表达式不要超过两个](./python/Pythonic90Rules/Rule28.md)
  - [第29条　用赋值表达式消除推导中的重复代码](./python/Pythonic90Rules/Rule29.md)
  - [第30条　不要让函数直接返回列表，应该让它逐个生成列表里的值](./python/Pythonic90Rules/Rule30.md)
  - [第31条　谨慎地迭代函数所收到的参数](./python/Pythonic90Rules/Rule31.md)
  - [第32条　考虑用生成器表达式改写数据量较大的列表推导](./python/Pythonic90Rules/Rule32.md)
  - [第33条　通过yield from把多个生成器连起来用](./python/Pythonic90Rules/Rule33.md)
  - [第34条　不要用send给生成器注入数据](./python/Pythonic90Rules/Rule34.md)
  - [第35条　不要通过throw变换生成器的状态](./python/Pythonic90Rules/Rule35.md)
  - [第36条　考虑用itertools拼装迭代器与生成器](./python/Pythonic90Rules/Rule36.md)
- 第5章　类与接口
  - [第37条　用组合起来的类来实现多层结构，不要用嵌套的内置类型](./python/Pythonic90Rules/Rule37.md)
  - [第38条　让简单的接口接受函数，而不是类的实例](./python/Pythonic90Rules/Rule38.md)
  - [第39条　通过@classmethod多态来构造同一体系中的各类对象](./python/Pythonic90Rules/Rule39.md)
  - [第40条　通过super初始化超类](./python/Pythonic90Rules/Rule40.md)
  - [第41条　考虑用mix-in类来表示可组合的功能](./python/Pythonic90Rules/Rule41.md)
  - [第42条　优先考虑用public属性表示应受保护的数据，不要用private属性表示](./python/Pythonic90Rules/Rule42.md)
  - [第43条　自定义的容器类型应该从collections.abc继承](./python/Pythonic90Rules/Rule43.md)
- 第6章　元类与属性
  - [第44条　用纯属性与修饰器取代旧式的setter与getter方法](./python/Pythonic90Rules/Rule44.md)
  - [第45条　考虑用@property实现新的属性访问逻辑，不要急着重构原有的代码](./python/Pythonic90Rules/Rule45.md)
  - [第46条　用描述符来改写需要复用的@property方法](./python/Pythonic90Rules/Rule46.md)
  - [第47条　针对惰性属性使用__getattr__、__getattribute__及__setattr__](./python/Pythonic90Rules/Rule47.md)
  - [第48条　用__init_subclass__验证子类写得是否正确](./python/Pythonic90Rules/Rule48.md)
  - [第49条　用__init_subclass__记录现有的子类](./python/Pythonic90Rules/Rule49.md)
  - [第50条　用__set_name__给类属性加注解](./python/Pythonic90Rules/Rule50.md)
  - [第51条　优先考虑通过类修饰器来提供可组合的扩充功能，不要使用元类](./python/Pythonic90Rules/Rule51.md)
- 第7章　并发与并行
  - [第52条　用subprocess管理子进程](./python/Pythonic90Rules/Rule52.md)
  - [第53条　可以用线程执行阻塞式I/O，但不要用它做并行计算](./python/Pythonic90Rules/Rule53.md)
  - [第54条　利用Lock防止多个线程争用同一份数据](./python/Pythonic90Rules/Rule54.md)
  - [第55条　用Queue来协调各线程之间的工作进度](./python/Pythonic90Rules/Rule55.md)
  - [第56条　学会判断什么场合必须做并发](./python/Pythonic90Rules/Rule56.md)
  - [第57条　不要在每次fan-out时都新建一批Thread实例](./python/Pythonic90Rules/Rule57.md)
  - [第58条　学会正确地重构代码，以便用Queue做并发](./python/Pythonic90Rules/Rule58.md)
  - [第59条　如果必须用线程做并发，那就考虑通过ThreadPoolExecutor实现](./python/Pythonic90Rules/Rule59.md)
  - [第60条　用协程实现高并发的I/O](./python/Pythonic90Rules/Rule60.md)
  - [第61条　学会用asyncio改写那些通过线程实现的I/O](./python/Pythonic90Rules/Rule61.md)
  - [第62条　结合线程与协程，将代码顺利迁移到asyncio](./python/Pythonic90Rules/Rule62.md)
  - [第63条　让asyncio的事件循环保持畅通，以便进一步提升程序的响应能力](./python/Pythonic90Rules/Rule63.md)
  - [第64条　考虑用concurrent.futures实现真正的并行计算](./python/Pythonic90Rules/Rule64.md)
- 第8章　稳定与性能
  - [第65条　合理利用try/except/else/finally结构中的每个代码块](./python/Pythonic90Rules/Rule65.md)
  - [第66条　考虑用contextlib和with语句来改写可复用的try/finally代码](./python/Pythonic90Rules/Rule66.md)
  - [第67条　用datetime模块处理本地时间，不要用time模块](./python/Pythonic90Rules/Rule67.md)
  - [第68条　用copyreg实现可靠的pickle操作](./python/Pythonic90Rules/Rule68.md)
  - [第69条　在需要准确计算的场合，用decimal表示相应的数值](./python/Pythonic90Rules/Rule69.md)
  - [第70条　先分析性能，然后再优化](./python/Pythonic90Rules/Rule70.md)
  - [第71条　优先考虑用deque实现生产者-消费者队列](./python/Pythonic90Rules/Rule71.md)
  - [第72条　考虑用bisect搜索已排序的序列](./python/Pythonic90Rules/Rule72.md)
  - [第73条　学会使用heapq制作优先级队列](./python/Pythonic90Rules/Rule73.md)
  - [第74条　考虑用memoryview与bytearray来实现无须拷贝的bytes操作](./python/Pythonic90Rules/Rule74.md)
- 第9章　测试与调试
  - [第75条　通过repr字符串输出调试信息](./python/Pythonic90Rules/Rule75.md)
  - [第76条　在TestCase子类里验证相关的行为](./python/Pythonic90Rules/Rule76.md)
  - [第77条　把测试前、后的准备与清理逻辑写在setUp、tearDown、setUpModule与tearDownModule中，以防用例之间互相干扰](./python/Pythonic90Rules/Rule77.md)
  - [第78条　用Mock来模拟受测代码所依赖的复杂函数](./python/Pythonic90Rules/Rule78.md)
  - [第79条　把受测代码所依赖的系统封装起来，以便于模拟和测试](./python/Pythonic90Rules/Rule79.md)
  - [第80条　考虑用pdb做交互调试](./python/Pythonic90Rules/Rule80.md)
  - [第81条　用tracemalloc来掌握内存的使用与泄漏情况](./python/Pythonic90Rules/Rule81.md)
- 第10章　协作开发
  - [第82条　学会寻找由其他Python开发者所构建的模块](./python/Pythonic90Rules/Rule82.md)
  - [第83条　用虚拟环境隔离项目，并重建依赖关系](./python/Pythonic90Rules/Rule83.md)
  - [第84条　每一个函数、类与模块都要写docstring](./python/Pythonic90Rules/Rule84.md)
  - [第85条　用包来安排模块，以提供稳固的API](./python/Pythonic90Rules/Rule85.md)
  - [第86条　考虑用模块级别的代码配置不同的部署环境](./python/Pythonic90Rules/Rule86.md)
  - [第87条　为自编的模块定义根异常，让调用者能够专门处理与此API有关的异常](./python/Pythonic90Rules/Rule87.md)
  - [第88条　用适当的方式打破循环依赖关系](./python/Pythonic90Rules/Rule88.md)
  - [第89条　重构时考虑通过warnings提醒开发者API已经发生变化](./python/Pythonic90Rules/Rule89.md)
  - [第90条　考虑通过typing做静态分析，以消除bug](./python/Pythonic90Rules/Rule90.md)

### 3.5.Demos

- [选课系统](python/Demo/CourseSystem.md)

## 4. 读书有感

- [约翰·森梅兹的2本书](./Reading/Developers/index.md)
