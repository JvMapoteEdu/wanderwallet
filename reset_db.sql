USE wanderwallet_db;

-- Disable FK checks (safe reset)
SET FOREIGN_KEY_CHECKS = 0;

-- Delete all data (keep users)
DELETE FROM expenses;
DELETE FROM budgets;
DELETE FROM trips;
DELETE FROM categories;

-- Reset IDs (optional but clean)
ALTER TABLE expenses AUTO_INCREMENT = 1;
ALTER TABLE budgets AUTO_INCREMENT = 1;
ALTER TABLE trips AUTO_INCREMENT = 1;
ALTER TABLE categories AUTO_INCREMENT = 1;

SET FOREIGN_KEY_CHECKS = 1;

-- Re-insert categories
INSERT INTO categories (category_name) VALUES
('Food'),
('Transport'),
('Hotel'),
('Shopping'),
('Activities');
