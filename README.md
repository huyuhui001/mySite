# Introduction

This is my learning memo, including contents Linux, Python, and Cloud below. 
The [website](https://huyuhui001.github.io/mySite/) provide same contents with easy reading style.

[Linux](./docs/linux.md)
* SUSE Linux Administration
* SUSE Enterprise Storage Foundation and Basic Operation

[Python](./docs/python.md)
* Foundation
* Data Analysis
* Practice

[Cloud](./docs/cloud.md)
* Microservice
    * Microservices with Kubernetes
* Kubernetes
    * Kubernetes Foundamentals
    * Local Installation
        + Single Node Installation on Ubuntu Server (Docker)
        + Multiple Nodes Installation on Ubuntu Server (nerdctl)
        + Multiple Nodes Installation on openSUSE on Aliyun ECS.
    * Foundamental on Kyma@SAP BTP
        + Foundamentals of Docker and Kubernetes
    * Foundamental on Ubuntu@Aliyun
        + Installation and Upgrade on Ubuntu Server on Aliyun ECS.
        + Foundamentals of Kubernetes (inc. replace Flannel by Calico)
        + Development with Helm


# About the site

The website is built by [mkdocs](https://www.mkdocs.org/).

To set up local environment, Python3 and pip3 are needed locally. Python3 version is `3.6.15` and pip version is `20.0.2`.
Beyond that, 
[mkdocs](https://www.mkdocs.org/), 
[material Theme](https://github.com/squidfunk/mkdocs-material) and 
[mermaid plugin](https://mermaid-js.github.io/mermaid/#/) 
need to be installed via pip3.

Install `mkdocs` and extensions with below specified version.
```
pip3 install mkdocs==1.3.0
pip3 install mkdocs-material==7.3.6
pip3 install mkdocs-mermaid2-plugin==0.6.0
```
All makdown files are under folder /docs.
All website files are under folder /site.

Generate website files, and commit them to branch gh-deploy on git repository.
```
mkdocs build
mkdocs gh-deploy
```

Start up local service for testing.
```
mkdocs serve
```