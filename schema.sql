CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE  plans (
    id INTEGER PRIMARY KEY,
    plan TEXT,
    hours_per_week INTEGER,
    info TEXT,
    user_id REFERENCES users
);