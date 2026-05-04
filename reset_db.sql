USE wanderwallet_db;

-- Disable FK checks
SET FOREIGN_KEY_CHECKS = 0;

-- Delete all data
DELETE FROM expenses;
DELETE FROM budgets;
DELETE FROM trips;
DELETE FROM categories;
DELETE FROM users;

-- Reset AUTO_INCREMENT
ALTER TABLE expenses AUTO_INCREMENT = 1;
ALTER TABLE budgets AUTO_INCREMENT = 1;
ALTER TABLE trips AUTO_INCREMENT = 1;
ALTER TABLE categories AUTO_INCREMENT = 1;
ALTER TABLE users AUTO_INCREMENT = 1;

SET FOREIGN_KEY_CHECKS = 1;

-- Re-insert categories
INSERT INTO categories (category_name) VALUES
('Food'),
('Transport'),
('Hotel'),
('Shopping'),
('Activities');

-- Create admin user
INSERT INTO users (username, email, password, role)
VALUES ('admin', 'admin@email.com', 'password', 'admin');
