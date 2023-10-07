# UPSkilling

## About the site

Just a learning memo.
The [website](https://huyuhui001.github.io/mySite/) provide same contents with easy reading style.

The website is built by [mkdocs](https://www.mkdocs.org/).

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
- [Python数据结构和算法](python/Foundation/Algorithms.md)

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

### 3.4.Demos

- [选课系统](python/Demo/CourseSystem.md)
