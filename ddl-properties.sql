CREATE DATABASE IF NOT EXISTS my_db;
USE my_db;

CREATE TABLE IF NOT EXISTS properties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    URL VARCHAR(500),
    image VARCHAR(1000),
    property_type VARCHAR(50),
    price VARCHAR(50),
    location VARCHAR(255),
    rooms VARCHAR(20),
    bathrooms VARCHAR(20),
    square_meters VARCHAR(20),
    floor VARCHAR(50)
);