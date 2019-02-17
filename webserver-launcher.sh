#!/usr/bin/env bash

# normalize our working directory
cd $(dirname "$0")

export GOOGLE_APPLICATION_CREDENTIALS='private/google-cloud-storage-key.json'
export POSTGRES_USER_PASSWORD="$(cat private/postgres-user-passwd.txt)"
export POSTGRES_HOST="$(cat private/postgres-public-ip.txt)"

# set up postgres
psql postgres://postgres:"$POSTGRES_USER_PASSWORD"@"$POSTGRES_HOST":5432/ <<-CREATEDB
    CREATE DATABASE sm;
CREATEDB

psql postgres://postgres:"$POSTGRES_USER_PASSWORD"@"$POSTGRES_HOST":5432/sm -f sql/0000-init.sql

# run the webserver
src/webserver.py 80 0.0.0.0
