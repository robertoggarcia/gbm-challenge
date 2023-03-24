#!/bin/sh

set -xe

exec uvicorn app.main:app --workers 1 --host 0.0.0.0 --http h11
