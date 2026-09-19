CREATE DATABASE airflow;

\connect weather

\i /docker-entrypoint-initdb.d/02-schema.sql