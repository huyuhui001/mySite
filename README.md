Short introduction

This [website](https://huyuhui001.github.io/mySite/) is my learning memo, including Linux, Python, and Cloud.


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