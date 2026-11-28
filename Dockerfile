# syntax=docker/dockerfile:1

# Base stage: uv + third-party dependencies only (cached until the lock changes).
FROM python:3.12-slim AS base

# Prevent Python from writing .pyc files to disk.
ENV PYTHONDONTWRITEBYTECODE=1
# Prevent Python from buffering stdout/stderr so logs appear immediately.
ENV PYTHONUNBUFFERED=1

RUN pip install --quiet --root-user-action=ignore uv
# Use copy mode since the cache and build filesystem are on different volumes.
ENV UV_LINK_MODE=copy

WORKDIR /app

# Install dependencies into a virtual environment using cache and bind mounts
# so neither uv nor the lock files need to be copied into the image.
RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --frozen --no-install-project


# Development stage: install the project itself in editable mode so that
# `import bloca_ml` resolves to /app/src (which Compose Watch keeps in sync).
FROM base AS development

ENV PATH="/app/.venv/bin:$PATH"

COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen


EXPOSE 8000
CMD ["fastapi", "dev", "--host", "0.0.0.0", "--port", "8000"]


# Production build stage: install the project as a regular (non-editable)
# package into the venv, without dev dependencies.
FROM base as builder

COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-dev --no-editable

# Production stage: only the finished venv (which contains bloca_ml).
FROM python:3.12-slim AS production

# Prevent Python from buffering stdout/stderr so logs appear immediately.
ENV PYTHONUNBUFFERED=1
# Activate the virtual environment copied from the build stage.
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Copy only the pre-built virtual environment and application source code.
COPY --from=builder /app/.venv /app/.venv
# fastapi run reads [tool.fastapi] entrypoint from here
COPY pyproject.toml ./

EXPOSE 8000

# Run FastAPI using its production server command (Uvicorn).
CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8000"]
