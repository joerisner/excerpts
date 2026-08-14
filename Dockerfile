FROM ghcr.io/astral-sh/uv:python3.14-alpine AS build

WORKDIR /app

COPY pyproject.toml uv.lock ./

# Install deps but not the project.
RUN uv sync --no-dev --locked --no-install-project

# While the app is small, we copy only what is needed.
# As the app grows, I may switch to an ignore file instead.
COPY ./excerpts ./excerpts/
COPY README.md ./

# Install the project.
RUN uv sync --no-dev --locked

FROM ghcr.io/astral-sh/uv:python3.14-alpine

WORKDIR /app

COPY --from=build --chown=appuser:appuser /app /app

ENV ENVIRONMENT=prod
ENV API_DOCS_URL=

# Run as non-root.
RUN adduser -D appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 3000

CMD ["uv", "run", "--no-dev", "fastapi", "run", "--port", "3000"]
