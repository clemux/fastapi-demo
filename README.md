# Introduction

This is a simple example of a FastAPI application with user registration and user activation.

It doesn't use any ORM and can be deployed as Docker container.

# Installation

## Docker

```bash
docker compose build
```

# Running

```bash
docker compose up
```


# Development

## Development environment

Create a virtualenvironment and install the dependencies:

```bash
python -m venv .venv
. .venv/bin/activate
pip install pip-tools
pip-sync requirements.txt requirements-dev.txt
```


## Dependencies management

The project uses [`pip-tools`](https://github.com/jazzband/pip-tools) to generate the pinned dependencies in `requirements.txt` and `requirements-dev.txt`.

To add a new dependency, add it in `pyproject.toml` then run

```bash
pip-compile --output-file=requirements.txt --generate-hashes pyproject.toml
```

Development dependencies are specified in `requirements-dev.in`. To generate `requirements-dev.txt`, run

```bash
pip-compile --output-file=requirements-dev.txt --generate-hashes requirements-dev.in
```

## Linting and pre-commit

The project uses [`pre-commit`](https://pre-commit.com/) to run linters and code formatters before each commit.
The following linters are set up:

 - `ruff`: linter and formatter
 - `mypy`: type checker
 - `hadolint`: Dockerfile linter

## Testing

Tests can be run with `pytest`.
