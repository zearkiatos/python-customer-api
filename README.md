# Description
This is a python 🐍 API built with fastAPI ⚡️ to management clients 👤, subscriptions

![Github](https://github.com/zearkiatos/python-customer-api/actions/workflows/action.yml/badge.svg)
![GitlabCI](https://gitlab.com/caprilespe/python-customer-api/badges/develop/pipeline.svg)
![TravisCI](https://api.travis-ci.com/zearkiatos/python-customer-api.svg?branch=develop)

# Made with
[![Python](https://img.shields.io/badge/python-2b5b84?style=for-the-badge&logo=python&logoColor=white&labelColor=000000)]()
[![FastAPI](https://img.shields.io/badge/FastApi-26a699?style=for-the-badge&logo=fastapi&logoColor=white&labelColor=000000)]()

# Project link 🔗

ℝender 📄 [development environment]: [https://python-customer-api.onrender.com/](https://python-customer-api.onrender.com/)

## Project Structure

The source code is organized by business context. Each context separates its application logic, domain model, and infrastructure adapters.

```text
src/
├── api/
│   └── router.py                         # Aggregates routers from each context
├── core/
│   ├── config.py                         # Application configuration
│   └── dependencies.py                   # Dependency injection and persistence wiring
├── customer/
│   ├── application/
│   │   ├── dto/
│   │   ├── mapper/
│   │   └── ports/
│   │       └── input/
│   ├── domain/
│   │   ├── model/
│   │   └── repositories/
│   └── infrastructure/
│       ├── adapters/
│       │   └── inbound/
│       │       └── http/
│       │           └── router.py
│       └── repositories/
├── invoice/
│   ├── application/
│   │   ├── dto/
│   │   ├── mapper/
│   │   └── ports/
│   │       ├── input/
│   │       └── output/
│   ├── domain/
│   │   └── model/
│   └── infrastructure/
│       └── adapters/
│           ├── inbound/
│           │   └── http/
│           │       └── router.py
│           └── transaction_lookup_adapter.py
├── transaction/
│   ├── application/
│   │   ├── dto/
│   │   ├── mapper/
│   │   └── ports/
│   │       └── input/
│   ├── domain/
│   │   └── model/
│   └── infrastructure/
│       └── adapters/
│           └── inbound/
│               └── http/
│                   └── router.py
└── main.py                               # Creates the FastAPI application
```