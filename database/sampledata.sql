INSERT INTO factories (factory_name, location) VALUES
('Alpha Manufacturing', 'Bangalore'),
('Beta Industries', 'Pune'),
('Gamma Works', 'Chennai');

INSERT INTO commodities (commodity_name, unit) VALUES
('Steel Rods', 'kg'),
('Copper Wire', 'kg'),
('Plastic Granules', 'kg'),
('Aluminum Sheets', 'kg'),
('Lubricant Oil', 'liters'),
('Packaging Boxes', 'units'),
('Rubber Seals', 'units'),
('Electronic Chips', 'units');

INSERT INTO storage (factory_id, commodity_id, current_quantity) VALUES
(1, 1, 1200),
(1, 2, 500),
(1, 3, 800),
(2, 1, 1500),
(2, 4, 700),
(3, 5, 300),
(3, 6, 1000),
(3, 8, 200);

INSERT INTO transactions (factory_id, commodity_id, transaction_type, quantity, transaction_date) VALUES
(1, 1, 'OUT', 200, '2025-01-10'),
(1, 1, 'OUT', 150, '2025-02-05'),
(1, 2, 'OUT', 100, '2025-02-15'),
(2, 1, 'OUT', 300, '2025-01-20'),
(2, 4, 'OUT', 200, '2025-02-12'),
(3, 5, 'OUT', 50, '2025-02-18'),
(3, 6, 'OUT', 400, '2025-03-01'),
(3, 8, 'OUT', 80, '2025-03-05');
