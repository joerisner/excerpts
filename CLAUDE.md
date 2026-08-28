# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Excerpts is an API for aggregating and resurfacing meaningful passages from books, articles, and other media.

## Commands

```bash
make dev          # setup + start db containers + run `fastapi dev` on :3000
make ci           # run all local CI checks (bin/ci)
make db-start     # start dev (:5432) and test (:5433) postgres containers
```

- Common workflows are driven through the `Makefile`.
- Use `uv run` instead of direct `python` calls.

## Testing

```bash
make test                                   # setup + start db containers + run full pytest suite
uv run pytest tests/api/test_excerpts.py    # Run a single test
```

- Tests require the **test database container** on port 5433 (`make db-start`).
- `tests/conftest.py` has two isolation layers: the session-scoped `test_engine` creates the schema once (and drops it after), while the per-test `db` fixture opens a transaction with `join_transaction_mode="create_savepoint"` and **rolls back** after each test — so tests may `commit()` freely without leaking state.
- The `client` fixture provides a `TestClient` wired to the test session. Use `tests/utils.py` factory helpers (`create_author`, `create_source`, `create_excerpt`, `create_tag`) to build fixtures via the ORM rather than the API. Custom assertion matchers are in `tests/matchers.py`.
- New tests must match the conventions in the existing test files (same fixture names, helper functions, and assertion style) — read a sibling test file first.

## Architecture

### Config is the source of truth for the database

- `excerpts/core/config.py` defines a single `config` singleton. Two computed fields matter:
  - `POSTGRES_DB` simply returns `ENVIRONMENT`, so each environment targets a same-named database (`dev`, `test`, `prod`).
  - `DATABASE_URL` is built from the individual `POSTGRES_*` settings.
- `excerpts/alembic/env.py` intentionally sets `sqlalchemy.url` **programmatically** from `config.DATABASE_URL` rather than hardcoding it in `alembic.ini`.
- When changing DB connection logic, change it in `config.py` — everything else derives from there. A `model_validator` refuses the default `POSTGRES_PASSWORD` in non-dev/test environments.

### Request layer (`excerpts/api/`)

- `main.py` (top level) builds the `FastAPI` app; `api/main.py` aggregates per-resource routers under the `/api` prefix.
- Routers live in `api/routes/`, one per resource.
- Pydantic request/response schemas live in `api/schemas/`.
- Shared FastAPI types are in `excerpts/types.py`: `DBDep` (the `get_db` session dependency), `PaginationSkip`, `PaginationLimit`. Inject these instead of redefining `Depends`/`Query` per route.

### Data layer (`excerpts/models/`)

- All models inherit `Base` (`models/base.py`). Use the mixins there for columns: `IdCreatedAtMixin` for normal tables, and `CreatedAtMixin` for association tables that only need a composite PK.
- `excerpts/models/__init__.py` imports every model so Alembic autogenerate and `Base.metadata` see the full schema.

## Conventions

- Type checking uses **`ty`** (Astral's type checker), not mypy or pyright.
- Migrations are timestamp-prefixed (`file_template` in `[tool.alembic]`) and live in `excerpts/alembic/versions/`.
- Prefer explicit, readable code over clever abstractions.
- API errors: use 409 for uniqueness conflicts, 422 for validation failures, 404 via the shared `get_or_404` helper.

## Code Review Rules

- Report findings with a confidence level and cite the exact `file:line` you verified against. If you cannot verify, say so instead of asserting.
- Flag newly-added files that aren't source or intentional config — scratch output, logs, session artifacts, stray dumps, etc.
