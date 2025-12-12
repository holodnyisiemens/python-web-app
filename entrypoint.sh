#!/bin/bash

# применение миграций
alembic upgrade head

# запуск приложения
exec "$@"