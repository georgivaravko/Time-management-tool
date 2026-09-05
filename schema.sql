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
    user_id INTEGER REFERENCES users
);

CREATE TABLE plan_classes (
    id INTEGER PRIMARY KEY,
    plan_id INTEGER REFERENCES plans,
    title TEXT,
    value TEXT
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);