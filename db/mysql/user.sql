-- Active: 1668163578572@@127.0.0.1@3306@bookstore
CREATE DATABASE IF NOT EXISTS bookstore;

ALTER DATABASE bookstore
  DEFAULT CHARACTER SET utf8
  DEFAULT COLLATE utf8_general_ci;

CREATE USER 'bookstore'@'%' IDENTIFIED BY 'bookstore';

GRANT ALL ON bookstore.* TO 'bookstore'@'%';
