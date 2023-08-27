DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS feedbacks;


CREATE TABLE users
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username text UNIQUE NOT NULL,
    email text NOT NULL,
    password text NOT NULL,
    avatar BLOB DEFAULT NULL
);

CREATE TABLE feedbacks
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    title text NOT NULL,
    body text NOT NULL,
    url text NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES users (id)
);




