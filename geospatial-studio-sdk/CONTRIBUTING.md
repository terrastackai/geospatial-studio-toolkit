# IBM Geospatial Exploration and Orchestration Studio SDK Development Guide

These instructions will guide you through contributing to `geostudio`.

## Set Up the Repository

You can clone this repository to contribute to the project and navigate to the working dir.

```sh
git clone git@github.com:terrastackai/geospatial-studio-toolkit.git
cd geospatial-studio-sdk
```

### Installing Dependencies

You need [poetry](https://python-poetry.org/docs/) to manage virtual environments and install dependencies in this project.
`poetry install` handles both virtual environment creation and dependency installation in one step.

```sh
poetry install
```

### Adding A Project Dependency

To add a new dependency:

```sh
poetry add <package-name>
```

This adds the dependency in your virtual environment, add it to pyproject.toml under [tool.poetry.dependencies] and update your `poetry.lock` file.

To add to a specific group of dependencies e.g dev:

```sh
poetry add --group docs Mkdocs
poetry add --group dev black
```

These install the dependency in your virtual environment, adds it to pyproject.toml e.ge under [tool.poetry.group.docs.dependencies] and update your `poetry.lock` file.

> *NOTE: You need to commit both `pyproject.toml` and `poetry.lock` for new dependencies.*
