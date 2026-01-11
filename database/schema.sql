CREATE TABLE factories (
    factory_id INT AUTO_INCREMENT PRIMARY KEY,
    factory_name VARCHAR(100) NOT NULL,
    location VARCHAR(100)
);

CREATE TABLE commodities (
    commodity_id INT AUTO_INCREMENT PRIMARY KEY,
    commodity_name VARCHAR(100) NOT NULL,
    unit VARCHAR(20) NOT NULL
);

CREATE TABLE storage (
    storage_id INT AUTO_INCREMENT PRIMARY KEY,
    factory_id INT,
    commodity_id INT,
    current_quantity INT NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (factory_id) REFERENCES factories(factory_id),
    FOREIGN KEY (commodity_id) REFERENCES commodities(commodity_id)
);

CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    factory_id INT,
    commodity_id INT,
    transaction_type ENUM('IN', 'OUT'),
    quantity INT NOT NULL,
    transaction_date DATE NOT NULL,
    FOREIGN KEY (factory_id) REFERENCES factories(factory_id),
    FOREIGN KEY (commodity_id) REFERENCES commodities(commodity_id)
);

