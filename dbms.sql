-- Create the database;
CREATE DATABASE urlshortner;

USE urlshortner;

--Create table url in database urlshortner
CREATE TABLE url(
    ShortURL VARCHAR(30) PRIMARY KEY,
    URL VARCHAR(3000)
);