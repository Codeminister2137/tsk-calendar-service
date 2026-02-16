# TSK Calendar Service

**Calendar microservice** for the TSK Task Scheduler project (https://github.com/Codeminister2137/tsk).

This service provides core calendar functionality — creating, managing, and retrieving scheduled tasks and reminders for authenticated users. It is built with **Django** and **Django REST Framework**.

Documentation for this service is provided via **MkDocs** and can be found in the `docs/` folder.

---

## Purpose

Part of a larger microservices architecture:

* Handles all calendar and scheduling logic
* Exposes REST endpoints for events, reminders, and user calendar data
* Integrates with Auth Service for user identity
* Integrates with Email Service to send notifications

This service alone does nothing — it is intended to run as part of the complete TSK system.

---

## Tech Stack

* Python ≥ 3.10
* Django ≥ 5.1
* Django REST Framework
* PostgreSQL database
* Managed with Poetry
* MkDocs for documentation

---

## Requirements

* Docker & Docker Compose (preferred)
* Poetry (for development)
* PostgreSQL with PostGIS (recommended if spatial features are used)

---

## Installation

Clone the repository:

```sh
git clone https://github.com/Codeminister2137/tsk-calendar-service.git
cd tsk-calendar-service
```

Install dependencies:

```sh
poetry install
```

---

## Configuration

Create and populate environment variables (example `.env`):

```sh
cp .env.example .env
```

Configure your database settings accordingly.

---

## Running (Local / Dev)

The service can be run locally using Docker Compose as part of the full TSK stack, or individually via Django’s development server:

```sh
poetry run python manage.py runserver
```

Database migrations:

```sh
poetry run python manage.py migrate
```

---

## Documentation (MkDocs)

Full service documentation is available through MkDocs. To serve it locally:

```sh
poetry run mkdocs serve
```

Open a browser at `http://127.0.0.1:8000/` to view the docs.

To build a static version:

```sh
poetry run mkdocs build
```

This generates a `site/` folder that can be hosted on any web server or deployed via GitHub Pages:

```sh
poetry run mkdocs gh-deploy
```

---

## API Overview

The service exposes REST endpoints (via Django REST Framework) to:

* Create, retrieve, update, and delete calendar events
* List reminders
* Query scheduled tasks for users

Protected routes require valid authentication tokens from the Auth Service.

Interactive API docs are available when the server is running (Django REST Framework browsable API).

---

## Repository Structure

```
calendar_app/               # Django application for calendar logic
tsk_calendar_service/       # Django project settings
manage.py                   # Django CLI entry point
pyproject.toml              # Poetry configuration
docs/                       # MkDocs documentation source
```

---

## License

MIT License (see LICENSE file).
