CREATE TABLE IF NOT EXISTS restaurants(
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
url text NOT NULL
);


CREATE TABLE IF NOT EXISTS feedbacks(
id integer PRIMARY KEY AUTOINCREMENT,
author_id integer NOT NULL,
title text NOT NULL,
body text NOT NULL,
url text NOT NULL,
created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (author_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS users(
id integer PRIMARY KEY AUTOINCREMENT,
username text NOT NULL,
email text NOT NULL,
password text NOT NULL,
avatar BLOB DEFAULT NULL,
);

