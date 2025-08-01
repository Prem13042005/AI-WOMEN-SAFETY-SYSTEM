CREATE DATABASE IF NOT EXISTS women_safety_db;
USE women_safety_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    password VARCHAR(100)
);

CREATE TABLE sos_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    latitude DECIMAL(10, 6) NOT NULL,
    longitude DECIMAL(10, 6) NOT NULL,
    triggered_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE emergency_contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    contact_name VARCHAR(100),
    contact_number VARCHAR(15),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
