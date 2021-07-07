#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER realestate;
    CREATE DATABASE realestate;
    GRANT ALL PRIVILEGES ON DATABASE realestate TO realestate;
EOSQL
