SELECT 'CREATE DATABASE redcontrol'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'redcontrol');
CREATE SCHEMA IF NOT EXISTS public;
ALTER USER redcontrol WITH PASSWORD 'password';
