# FastAPI Practice — Shipment CRUD API

A small shipment-tracking API I built while working through Packt's FastAPI course. It starts as bare dict-backed routes and, commit by commit, grows into a proper layered app: Pydantic validation → SQLModel + Postgres → an async service layer wired up with dependency injection. If you want to see the "why" behind a piece of code and not just the final version, the git history here is written to be read — each commit is one deliberate step in that progression.

## Stack

- [FastAPI](https://fastapi.tiangolo.com/) + [Scalar](https://github.com/scalar/scalar) for interactive API docs
- [SQLModel](https://sqlmodel.tiangolo.com/) over async [SQLAlchemy](https://www.sqlalchemy.org/) (`asyncpg` driver)
- PostgreSQL
- [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) for config
- [uv](https://docs.astral.sh/uv/) for dependency/project management

## Project layout

```
main.py                    # app entrypoint, lifespan handler, Scalar docs route
api/
  router.py                # /shipment routes (GET/POST/PATCH/DELETE)
  dependencies.py          # SessionDep -> ServiceDep dependency chain
  schemas/shipment.py      # request/response Pydantic models
database/
  models.py                # SQLModel Shipment table + ShipmentStatus enum
  session.py                # async engine, sessionmaker, get_session
services/
  shipment.py               # ShipmentService — the actual CRUD logic
config.py                  # Postgres settings, read from .env
sql.py, test.py            # earlier scratch/practice versions, kept for reference
FastAPI.ipynb              # course notes as a running notebook of snippets
Module 9_10.docx           # typed notes for the async/Postgres modules
FastAPI Course-1 Notes.pdf # the notebook + docx compiled into one PDF
```

## Running it locally

Requires [uv](https://docs.astral.sh/uv/) and a running PostgreSQL instance.

```bash
uv sync
uv run fastapi dev main.py
```

Then open `http://127.0.0.1:8000/docs` (Swagger) or `http://127.0.0.1:8000/scalar` (Scalar).

The app expects a database matching the `POSTGRES_*` values in `.env` (not committed — see `.gitignore`) to already exist; it creates its own tables on startup via the lifespan handler in `main.py`, so no migrations are needed.

## Course notes

`FastAPI Course-1 Notes.pdf` is the full set of notes from this course — walking through everything from basic routes and Pydantic models up through async SQLAlchemy, dependency injection, and the service-layer pattern used in this repo. `FastAPI.ipynb` and `Module 9_10.docx` are its two source files.
