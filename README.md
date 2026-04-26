# ByteJockey's Site

[![MkDocs](https://img.shields.io/badge/Built%20with-MkDocs-blue)](https://www.mkdocs.org/)
[![Material for MkDocs](https://img.shields.io/badge/Theme-Material-blue)](https://squidfunk.github.io/mkdocs-material/)
[![GitHub Pages](https://img.shields.io/badge/Deployed%20on-GitHub%20Pages-brightgreen)](https://huyuhui001.github.io/mySite/)

个人技术笔记站点，涵盖 Linux、Kubernetes、Python 及职业发展等内容，大部分内容为中文。

在线访问：[huyuhui001.github.io/mySite](https://huyuhui001.github.io/mySite/)

## 内容目录

- [Linux](./docs/linux/index.md)
  - Linux SRE
  - SUSE Linux Administration
  - SUSE Enterprise Storage Foundation

- [Kubernetes](./docs/k8s/index.md)
  - CKA Learning Memo
  - CKA Study Notes

- [Python](./docs/python/index.md)
  - Python Basics
  - Data Analysis with Python
  - Data Structures and Algorithms
  - 90 Effective Ways to Write High-Quality Python Code
  - Small Demonstrations

- [清水工作室](./docs/Reading/index.md)
  - Programmer's Career and Survival Guide
  - Chatting about Career Development
  - Technical News Miscellaneous Records

## 本地运行

```bash
pip install -r requirements.txt
mkdocs serve
```

浏览器访问 `http://127.0.0.1:8000` 即可预览。

## 构建与部署

```bash
mkdocs build        # 构建静态文件到 site/ 目录
mkdocs gh-deploy    # 构建并推送到 GitHub Pages
```
