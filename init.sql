CREATE DATABASE IF NOT EXISTS tracker;

\c tracker;

CREATE TABLE IF NOT EXISTS item_tracker (
    id CHAR(20) NOT NULL,
    datetime TIMESTAMP NOT NULL,
    longitude FLOAT NOT NULL,
    latitude FLOAT NOT NULL,
    PRIMARY KEY (id, datetime)
);
