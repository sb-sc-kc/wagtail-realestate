CREATE USER wagestate;
CREATE DATABASE wagestate;
ALTER ROLE wagestate WITH PASSWORD 'wagestate';
    GRANT ALL PRIVILEGES ON DATABASE wagestate TO wagestate;
