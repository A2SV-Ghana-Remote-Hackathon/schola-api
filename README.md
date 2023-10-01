<h3 align="center">Schola API</h3>

<div align="center">

  ![Status](https://img.shields.io/badge/status-active-success.svg)
  ![GitHub issues](https://img.shields.io/github/issues/A2SV-Ghana-Remote-Hackathon/schola-api?color=yellow)
  ![GitHub pull requests](https://img.shields.io/github/issues-pr/A2SV-Ghana-Remote-Hackathon/schola-api?color=success)
  [![License](https://img.shields.io/badge/license-Proprietary-blue.svg)](/LICENSE)


</div>

---

<p align="center"> Backend API for Schola
</p>


## About <a name = "about"></a>
This project is a social network for university students.

## 🏁 Getting Started <a name = "getting_started"></a>
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
- Poetry
- Postgres
- Python 3.10^
- AutoPEP8


### Setting up a development environment
#### Step 1: Clone the repository

```bash
https://github.com/A2SV-Ghana-Remote-Hackathon/schola-api.git
```

or with GithubCLI
  
```bash
gh repo clone A2SV-Ghana-Remote-Hackathon/schola-api
```

#### step 2: Install poetry if you don't have it already

```bash
# Linux, macOS, Windows (WSL)
curl -sSL https://install.python-poetry.org | python3 -
```

```bash
# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

> _Note: If you have installed Python through the Microsoft Store, replace py with python in the command above._

> _Reference: [Poetry Installation](https://python-poetry.org/docs/#installation)_

#### step 3: Create a virtual environment

```bash
poetry shell
```

#### Step 4: Install dependencies

```
poetry install
```

> Note to add a package to the project, run

```bash
poetry add <package-name>
```

#### Step 5: Create a `.env` file in the root directory and add the following environment variables

```bash
POSTGRES_USER= #e.g postgres
POSTGRES_PASSWORD= #e.g password123
POSTGRES_SERVER= #e.g localhost
POSTGRES_PORT= #e.g 5432
POSTGRES_DB= #e.g schola
```

#### Step 7: Start the uvicorn server

```bash
uvicorn app:app --reload
```

## ⛏️ Built Using <a name = "built_using"></a>
- [FastAPI](https://fastapi.tiangolo.com/) - Python Framework
- [Postgres](https://www.postgresql.org/) - Database
- [Poetry](https://python-poetry.org/) - Python Package Manager
- [SqlAlchemy](https://www.sqlalchemy.org/) - ORM
