#!/bin/sh
set -e

exec gunicorn -k uvicorn.workers.UvicornWorker --bind :8080 --workers 1 --threads 8 --timeout 0 api:main 