CREATE TABLE IF NOT EXISTS users
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username text UNIQUE NOT NULL,
    email text NOT NULL,
    password text NOT NULL,
    avatar BLOB DEFAULT NULL,
    visit TIMESTAMP
);

CREATE TABLE IF NOT EXISTS feedbacks
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    rest_id INTEGER NOT NULL,
    title text NOT NULL,
    body text NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES users (id),
    FOREIGN KEY (rest_id) REFERENCES restaurants (id)
);

CREATE TABLE IF NOT EXISTS restaurants
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title text UNIQUE NOT NULL,
    picture BLOB DEFAULT NULL,
    url text NOT NULL
);




