CREATE TABLE IF NOT EXISTS users (
    id SERIAL,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL PRIMARY KEY,
    password VARCHAR(50) NOT NULL
);