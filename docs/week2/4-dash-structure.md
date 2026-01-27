# 4. Dash app directory structure

The Dash documentation has minimal guidance on how to structure Dash apps. For this you will need
to review community forums and other repositories to understand the practices used.

You can write a functioning Dash app in a single Python module. However, this is not good practice
as it becomes harder to read and maintain as the code grows.

A simple single-page Dash app may be structured like this:

```text
.venv/
.gitignore
README.md
pyproject.toml
src/
  assets/        # static files e.g. local css, images
  app.py         
tests/           # tests
```

A simple multipage Dash app may be structured like this:

```text
.venv/
.gitignore
README.md
pyproject.toml
src/
    app_package/
        __init__.py
        assets/        # static files e.g. local css, images
        pages/         # multi-page app layouts
        app.py         # initializes Dash and imports parts
```

As the app grows, consider separating the code into further clearly defined modules and directories, e.g.

```text
app_package/
  assets/
  callbacks/
  layouts/
  pages/
  utils/
  app.py
```
## Sources of information

- [bradley-erickson dash-app-structure GitHub repo](https://github.com/bradley-erickson/dash-app-structure) A documented structure for a large Dash app
- [Sample Dash apps in GitHub](https://github.com/plotly/dash-sample-apps/tree/ebabf377d3be3d08752d53dfd04d1a59d7d164f1) Examples of Dash app code
- [Dash best practices](https://deepwiki.com/plotly/dash-sample-apps/9-best-practices-and-common-patterns) Dash documentation of best practices

[Next activity](5-)