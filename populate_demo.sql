USE wanderwallet_db;

-- ================================
-- ADD USERS (admin already exists)
-- ================================
INSERT INTO users (username, email, password, role) VALUES
('user1', 'user1@email.com', '1234', 'user'),
('user2', 'user2@email.com', '1234', 'user'),
('user3', 'user3@email.com', '1234', 'user');

-- ================================
-- TRIPS PER USER
-- ================================
INSERT INTO trips (user_id, trip_name, destination, start_date, end_date) VALUES

-- ADMIN (user_id = 1)
(1, 'Japan Trip', 'Tokyo', '2026-08-01', '2026-08-10'),
(1, 'Singapore Trip', 'Singapore', '2026-09-05', '2026-09-10'),

-- USER1 (user_id = 2)
(2, 'Korea Trip', 'Seoul', '2026-10-01', '2026-10-07'),
(2, 'Hong Kong Trip', 'Hong Kong', '2026-11-10', '2026-11-15'),

-- USER2 (user_id = 3)
(3, 'Cebu Trip', 'Cebu', '2027-01-10', '2027-01-15'),
(3, 'Boracay Trip', 'Boracay', '2027-03-01', '2027-03-05'),

-- USER3 (user_id = 4)
(4, 'Taiwan Trip', 'Taipei', '2027-02-05', '2027-02-10'),
(4, 'Baguio Trip', 'Baguio', '2026-12-20', '2026-12-23');

-- ================================
-- BUDGETS
-- ================================
INSERT INTO budgets (trip_id, total_budget, remaining_budget) VALUES
(1, 50000, 50000),
(2, 30000, 30000),
(3, 40000, 40000),
(4, 35000, 35000),
(5, 25000, 25000),
(6, 30000, 30000),
(7, 28000, 28000),
(8, 20000, 20000);

-- ================================
-- EXPENSES
-- ================================
INSERT INTO expenses (trip_id, category_id, amount, description, expense_date) VALUES

-- ADMIN
(1, 1, 1200, 'Ramen', '2026-08-02'),
(1, 2, 800, 'Train Pass', '2026-08-03'),
(2, 1, 900, 'Chicken Rice', '2026-09-06'),
(2, 5, 1500, 'Universal Studios', '2026-09-07'),

-- USER1
(3, 3, 4000, 'Hotel Seoul', '2026-10-01'),
(3, 1, 1100, 'Samgyeopsal', '2026-10-02'),
(4, 1, 800, 'Dim Sum', '2026-11-11'),
(4, 5, 2000, 'Disneyland', '2026-11-12'),

-- USER2
(5, 1, 700, 'Lechon', '2027-01-11'),
(5, 5, 1800, 'Island Hopping', '2027-01-12'),
(6, 3, 3000, 'Beach Hotel', '2027-03-01'),
(6, 1, 900, 'Seafood', '2027-03-02'),

-- USER3
(7, 1, 700, 'Bubble Tea', '2027-02-06'),
(7, 2, 600, 'Bus Fare', '2027-02-06'),
(8, 1, 500, 'Strawberry Taho', '2026-12-21'),
(8, 4, 800, 'Souvenirs', '2026-12-22');

-- ================================
-- UPDATE REMAINING BUDGET
-- ================================
UPDATE budgets b
SET remaining_budget = total_budget - (
    SELECT IFNULL(SUM(e.amount), 0)
    FROM expenses e
    WHERE e.trip_id = b.trip_id
);
