-- Create default user in PostgreSQL
CREATE TABLE IF NOT EXISTS users (
    id SERIAL,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL PRIMARY KEY,
    password VARCHAR(50) NOT NULL
);

INSERT INTO users (username, email, password) 
VALUES ('admin', 'arungraj23@gmail.com','RR@dmin123');
