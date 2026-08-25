#!/bin/sh

set -eu

echo "==> Executando migrations..."

uv run alembic upgrade head

echo "==> Migrations aplicadas."

echo "==> Iniciando Horus API..."

exec "$@"
