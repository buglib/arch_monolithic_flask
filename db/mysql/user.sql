-- Active: 1668432948475@@127.0.0.1@3306@bookstore
CREATE DATABASE IF NOT EXISTS bookstore;

CREATE DATABASE IF NOT EXISTS test_bookstore;

ALTER DATABASE bookstore
  DEFAULT CHARACTER SET utf8
  DEFAULT COLLATE utf8_general_ci;

  ALTER DATABASE test_bookstore
  DEFAULT CHARACTER SET utf8
  DEFAULT COLLATE utf8_general_ci;

CREATE USER 'bookstore'@'%' IDENTIFIED BY 'bookstore';

GRANT ALL ON bookstore.* TO 'bookstore'@'%';

GRANT ALL ON test_bookstore.* TO 'bookstore'@'%';