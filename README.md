Guidance

This website is built by [mkdocs](https://www.mkdocs.org/).

Install mkdocs, [material Theme](https://github.com/squidfunk/mkdocs-material) and [mermaid plugin](https://mermaid-js.github.io/mermaid/#/) via pip3.
By adding mermaid, we can also generate diagram in markdown file.

```
pip3 install mkdocs
pip3 install mkdocs-material
pip3 install mkdocs-mermaid2-plugin
```

Clone branch hjmain of the git repository [mySite](https://github.com/huyuhui001/mySite) to local environment.

Put makdown files under folder /docs, which will be committed to branch hjmain on git repository.

Generate website files for [mySite](https://github.com/huyuhui001/mySite).
```
mkdocs build
```

Commit generated website files to branch gh-deploy on git repository.
```
mkdocs gh-deploy
```

Start up local service for testing.
```
mkdocs serve
```

The website [ZERO-ONE-ZERO](https://huyuhui001.github.io/mySite/) is my learning memo.
