# Python Project template for LLM

A Python project template using Poetry as a dependency management and packaging tool, with a focus on code quality and best practices.

## Features

- Poetry for dependency management and packaging
- Pre-configured code formatting using Black and Ruff
- Pre-configured testing with pytest and pytest-cov for coverage reports
- Pre-configured Docker development environment using a devcontainer
- Pre-configured Git hooks for formatting and linting checks

## Requirements

- Python 3.11 or higher
- Poetry (https://python-poetry.org/)
- Docker (for using the devcontainer)

## Getting Started

1. Clone the repository:

   git clone https://github.com/daisuke19891023/python-project-template4LLM.git
   cd mymodule

2. Install dependencies:

   poetry install

   If you are using the devcontainer, dependencies will be automatically installed when you open the project in Visual Studio Code with the Remote - Containers extension.

3. Activate the virtual environment:

   poetry shell

   If you are using the devcontainer, the virtual environment is automatically activated when opening a new terminal in Visual Studio Code.

## Usage

Replace the mymodule folder with your own Python module, and update the pyproject.toml file accordingly.

## Development Tasks

The project is configured with poe tasks for common development tasks. You can run these tasks with the poetry run poe <task> command. Available tasks:

- lint: Run Ruff to check for code quality issues
- test: Run pytest to execute tests
- cover: Run pytest with coverage reporting
- fmt: Run Black to check if code formatting is correct
- build: Run a combination of fmt, lint, and test

## Devcontainer

This project comes with a pre-configured devcontainer for Visual Studio Code. The devcontainer provides a Docker-based development environment with all necessary tools and dependencies pre-installed. To use the devcontainer, you need to have Docker installed and the Remote - Containers extension enabled in Visual Studio Code.

When opening the project in Visual Studio Code, it will prompt you to reopen the project in a container. If not, you can use the "Remote-Containers: Reopen in Container" command from the command palette.

For more information on devcontainers, see the Visual Studio Code documentation (https://code.visualstudio.com/docs/remote/containers).

## License

This project is licensed under the MIT License. See the LICENSE file for details.
