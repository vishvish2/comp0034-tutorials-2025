# 1. Introduction to REST API and the FastAPI framework

## REST API

A REST (Representational State Transfer) API is a way for different applications to communicate
with each other over the internet using standardized rules.

It was introduced by Roy Fielding in his 2000 doctoral dissertation
titled ["Architectural Styles and
the Design of Network-based Software Architectures"](https://roy.gbiv.com/pubs/dissertation/top.htm).

REST uses HTTP methods like GET, POST, PUT, and DELETE to let clients request or modify data stored
on a server.

Key concepts:

- Resources (e.g. users, products, posts) are identified by URLs.
- HTTP methods (GET, POST, PUT, DELETE) act on those resources.
- Statelessness: each request contains all the information needed—servers don't store session state.
- Typically, returns structured data in format such as JSON.

By exposing resources via a REST API, organisations can reuse the same data and logic across
multiple applications; which avoids duplicating business logic and helps to keep front-end and
back-end systems decoupled.

In coursework 1 you created a 'front-end' web app. In coursework 2 you will create a 'back-end'
REST API, and link your front-end to it.

## FastAPI

FastAPI is a modern Python web framework for building APIs. It was designed to be fast and
developer-friendly to use.

It is built on other packages. It uses Starlette for web, Pydantic for data validation and Python
type hints to automatically generate:

- data validation
- request/response schemas
- automatic OpenAPI (Swagger) documentation

You will also use SQLModel (or SQLAlchemy) to support interaction with the SQLite database.

## FastAPI app architecture

The tutorials over the next few weeks build an app that has the following structure.

<img alt="FastAPI app structure diagram" src="../img/fast-api-structure.png" style="max-width: 50%; height: auto;" />

## Setup

You can **either** choose to create a new repository **or** you can add a package to the repository
you created for the front end app in weeks 1-5.

The structure is similar to, but not identical to, the
FastAPI [full stack template in their GitHub account](https://github.com/fastapi/full-stack-fastapi-template).
You don't need all the files and folders in their structure. Note that if you plan to implement
authentication, you may wish to copy their boilerplate code as it includes JWT (JSON Web Token)
authentication.

### Option: add a package for the backend app to existing front end app project

Copy the 'backend' package only from `src/week6_starter/src` to the `src` directory in your project.

Add the following dependencies to your `pyproject.toml`. Do not add a new `[dependencies]` section,
just add any packages you don't already have to the existing section.

```text
dependencies = [
    "fastapi[standard]",
    "uvicorn",
    "sqlmodel",
    "pytest",
    "pandas",
    "alembic",
    "openpyxl"
]
```

Make sure you now check these packages are installed in your virtual environment e.g. try
`pip install -e .` or if you are using `uv` then `uv sync`.

### Option: create a new project

Create a new Python project in your IDE.

Copy the structure that is `src/week6_starter` to your IDE.

You should have a structure like this:

```text
project_root
    .gitignore
    README.md
    pyproject.toml
    src/
       /backend
           /core
               __init__.py
               db.py  # Modified version of code from COMP0035 to add data to the database          
           /models
               __init__.py
               models.py   # Modified versions of the SQLModel classes created in COMP0035
           /routes
               __init__.py
           /services
               __init__.py
       /data
           paralympics.xlsx   # Version of the Excel data file used in COMP0034 weeks 1 to 5
           question.sql  # Sample data for the question table
           response.sql  # Sample data for the response table
```

Create and activate a virtual environment.

Install the dependencies e.g. `pip install -e .` or if you are using `uv` then `uv sync`.

## Documentation

Refer to these as you need to throughout the subsequent activities:

- [FastAPI](https://fastapi.tiangolo.com)
- [Pydantic](https://docs.pydantic.dev/2.12/)
- [Python type hints cheat sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
- [SQLModel](https://sqlmodel.tiangolo.com)
  or [SQLAlchemy](https://docs.sqlalchemy.org/en/20/intro.html#documentation-overview)

Possibly, but less likely, you may need to refer to:

- [Starlette](https://starlette.dev)
- [uvicorn](https://uvicorn.dev)

[Next activity](2-fastapi-app.md)