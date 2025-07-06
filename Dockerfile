FROM ghcr.io/astral-sh/uv:python3.13-alpine

# UV instalation
RUN apk add --no-cache \
    curl \
    gcc \
    musl-dev \
    mariadb-dev \
    pkgconfig \
    libffi-dev \
    openssl-dev \
    mysql-client

WORKDIR /app

COPY pyproject.toml uv.lock ./

COPY . .

RUN uv pip sync --system pyproject.toml

EXPOSE 8000

CMD ["uv", "run", "gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
