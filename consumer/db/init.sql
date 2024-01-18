\c tracker;

CREATE TABLE IF NOT EXISTS item_tracker (
    id CHAR(50) NOT NULL,
    name CHAR(20) NOT NULL,
    datetime BIGINT NOT NULL,
    longitude FLOAT NOT NULL,
    latitude FLOAT NOT NULL
);
