Short introduction

This website  [from ZERO to ONE](https://huyuhui001.github.io/mySite/) is my learning memo, which is built by [mkdocs](https://www.mkdocs.org/).

To set up local environment, Python3 and pip3 are needed locally. Beyond that, [mkdocs](https://www.mkdocs.org/), [material Theme](https://github.com/squidfunk/mkdocs-material) and [mermaid plugin](https://mermaid-js.github.io/mermaid/#/) need to be installed via pip3.

```
pip3 install mkdocs
pip3 install mkdocs-material
pip3 install mkdocs-mermaid2-plugin
```

Clone branch hjmain of the git repository [mySite](https://github.com/huyuhui001/mySite) to local environment. 
All makdown files are under folder /docs, which are committed to branch hjmain on git repository.
All website files are under folder /site, which are commited to branch gh-deploy on git repository

Here are steps to deploy changes of website.

Generate website files, and commit them to branch gh-deploy on git repository.
```
mkdocs build
mkdocs gh-deploy
```

Start up local service for testing.
```
mkdocs serve
```

