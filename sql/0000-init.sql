CREATE SCHEMA IF NOT EXISTS sm;
CREATE TYPE sm.process_status AS ENUM (
    'received',
    'uploaded',
    'processing',
    'finished',
    'error'
);

CREATE TABLE IF NOT EXISTS sm.uploads (
    id SERIAL PRIMARY KEY,
    created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    process_status sm.process_status DEFAULT 'received',
    fname TEXT,
    error TEXT
);

CREATE TABLE IF NOT EXISTS sm.maps (
    id SERIAL PRIMARY KEY,
    upload_id INTEGER REFERENCES sm.uploads(id)
);
