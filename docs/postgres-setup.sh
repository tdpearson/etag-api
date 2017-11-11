#!/usr/bin/env bash

docker exec -it etag_postgres psql -U postgres -c 'create database etag'
docker exec -it etag_postgres psql -U postgres -c 'create database etag_auth'
docker exec -it etag_postgres psql -U postgres -c 'create user etagadmin with password "etagadmin"'
docker exec -it etag_postgres psql -U postgres -c 'GRANT ALL PRIVILEGES ON DATABASE "etag" to etagadmin'
docker exec -it etag_postgres psql -U postgres -c 'GRANT ALL PRIVILEGES ON DATABASE "etag_auth" to etagadmin'
docker exec -it etag_postgres psql -U postgres </opt/etag.sql
docker exec -it etag_postgres psql -U postgres </opt/etag_auth.sql
