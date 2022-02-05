安装指引

网站基于[mkdocs](https://www.mkdocs.org/)构建。

通过pip3安装mkdocs，[material主题](https://github.com/squidfunk/mkdocs-material)，和[mermaid插件](https://mermaid-js.github.io/mermaid/#/)，可以通过在markdown文件中添加mermaid代码来实现流程图等图表。

```
pip3 install mkdocs
pip3 install mkdocs-material
pip3 install mkdocs-mermaid2-plugin
```

克隆当前git仓库[mySite](https://github.com/huyuhui001/mySite)的主分支hjmain到本地系统。

在/docs目录下添加markdown文件。这些markdown文件通过git提交到主分支hjmain下。

本地生成网站代码。
```
mkdocs build
```

提交网站代码到git的gh-deploy分支。
```
mkdocs gh-deploy
```

本地测试。
```
mkdocs serve
```


