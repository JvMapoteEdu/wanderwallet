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
VALUES ('admin', 'admin@email.com', 'scrypt:32768:8:1$coysNJSFt1RHI2lV$b1d16ba4b7af391e2075afa75c2028bda75095e6ef754585d4f1c7b45e8722b21e449c2b8f1cba7de80e8be0390f0b239f9eabb0fa743ce71f8d0c2256c7bb8d', 'admin');
