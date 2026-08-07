# Alembic

This project was initialized with the `pyproject` template like this:

```sh
uv run alembic init --template pyproject alembic
```

## Common commands

Show commands.

```sh
uv run alembic --help
```

Generate a migration file.

```sh
uv run alembic revision --autogenerate -m "migration summary message"
```

Apply migrations up to the latest `head`.

```sh
uv run alembic upgrade head
```

Display the current revision for a database.

```sh
uv run alembic current
```

Downgrade to the previous migration version.

```sh
uv run alembic downgrade -1
```
