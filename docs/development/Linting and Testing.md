# Linting and Testing Guide

## Super Linter

To be able to run super linter on your machine locally, follow this
[guide](https://github.com/github/super-linter/blob/main/docs/run-linter-locally.md)
to get started.

## pytest

To run pytest, make sure to install the pytest module in your virtual environment and then run the
following commands:

```bash
pytest . -W ignore::DeprecationWarning
```

## Build application into .exe

Navigate into source/blueprint automation tool and run the following

```bash
pyinstaller --onefile --noconsole .\tool.spec
```
