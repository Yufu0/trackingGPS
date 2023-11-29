CREATE DATABASE IF NOT EXISTS tracker;

\c tracker;

CREATE TABLE IF NOT EXISTS item_tracker (
    id INT,
    datetime TIMESTAMP,
    longitude FLOAT,
    latitude FLOAT,
    PRIMARY KEY (id, datetime)
);
