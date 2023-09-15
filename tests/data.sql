INSERT INTO users (username, email, password, avatar, visit)
VALUES
  ('test_name', 'testemail@gmail.com', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', NULL, '2018-01-01 00:00:00'),
  ('test_username', 'testemail@yandex.ru', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79', NULL, '2018-01-01 00:00:00');

INSERT INTO feedbacks (author_id, rest_id, title, body, created)
VALUES
  (1, 1, 'test title', 'test' || x'0a' || 'body', '2018-01-01 00:00:00');



