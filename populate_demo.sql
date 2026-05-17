USE wanderwallet_db;

-- ================================
-- ADD USERS (admin already exists)
-- ================================
INSERT INTO users (username, email, password, role) VALUES
('user1', 'user1@email.com', 'scrypt:32768:8:1$SifkgrjLSWZKzz5m$ce03da354c73fe2ef7105b858107ad704a2b26776fae5a7f60b649f73ebc96edfcf10bb9d3f2ed155666d548398ff2aa93f615bfcd24e53650190ace8ccc39db', 'user'),
('user2', 'user2@email.com', 'scrypt:32768:8:1$SifkgrjLSWZKzz5m$ce03da354c73fe2ef7105b858107ad704a2b26776fae5a7f60b649f73ebc96edfcf10bb9d3f2ed155666d548398ff2aa93f615bfcd24e53650190ace8ccc39db', 'user'),
('user3', 'user3@email.com', 'scrypt:32768:8:1$SifkgrjLSWZKzz5m$ce03da354c73fe2ef7105b858107ad704a2b26776fae5a7f60b649f73ebc96edfcf10bb9d3f2ed155666d548398ff2aa93f615bfcd24e53650190ace8ccc39db', 'user');

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
INSERT INTO budgets (trip_id, total_budget) VALUES
(1, 50000),
(2, 30000),
(3, 40000),
(4, 35000),
(5, 25000),
(6, 30000),
(7, 28000),
(8, 20000);

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

INSERT INTO expenses (trip_id, category_id, amount, description, expense_date) VALUES

-- ADMIN: Japan Trip (trip 1) — 2026-08-01 to 2026-08-10
(1, 1,  950, 'Sushi Dinner',              '2026-08-01'),
(1, 2,  700, 'Tokyo Metro Day Pass',      '2026-08-01'),
(1, 3, 5500, 'Hotel Shinjuku',            '2026-08-01'),
(1, 1,  400, '7-Eleven Snacks',           '2026-08-02'),
(1, 5, 2200, 'TeamLab Planets Ticket',    '2026-08-02'),
(1, 1,  850, 'Tempura Lunch',             '2026-08-03'),
(1, 2, 3200, 'Shinkansen Tokyo-Kyoto',    '2026-08-04'),
(1, 4, 1800, 'Akihabara Shopping',        '2026-08-04'),
(1, 1,  700, 'Gyudon Bowl',               '2026-08-05'),
(1, 5,  500, 'Ueno Zoo Entry',            '2026-08-05'),
(1, 1, 1100, 'Tonkatsu Dinner',           '2026-08-06'),
(1, 4, 2500, 'Harajuku Shopping',         '2026-08-06'),
(1, 1,  600, 'Onigiri and Drinks',        '2026-08-07'),
(1, 5, 1800, 'Senso-ji Temple Tour',      '2026-08-07'),
(1, 2, 1200, 'Airport Limousine Bus',     '2026-08-10'),

-- ADMIN: Singapore Trip (trip 2) — 2026-09-05 to 2026-09-10
(2, 3, 6500, 'Hotel Clarke Quay',         '2026-09-05'),
(2, 2,  900, 'MRT EZ-Link Card',          '2026-09-05'),
(2, 1,  500, 'Kaya Toast Breakfast',      '2026-09-05'),
(2, 1, 1800, 'Chili Crab Dinner',         '2026-09-06'),
(2, 5, 1200, 'Gardens by the Bay',        '2026-09-06'),
(2, 1,  650, 'Hawker Centre Lunch',       '2026-09-07'),
(2, 5, 1000, 'Sentosa Cable Car',         '2026-09-07'),
(2, 4, 3200, 'Orchard Road Shopping',     '2026-09-08'),
(2, 5, 2500, 'Night Safari',              '2026-09-08'),
(2, 2,  400, 'Grab Rides',               '2026-09-09'),
(2, 5,  800, 'Marina Bay Sands Obs. Deck','2026-09-09'),
(2, 1,  750, 'Laksa Lunch',              '2026-09-10'),

-- USER1: Korea Trip (trip 3) — 2026-10-01 to 2026-10-07
(3, 2,  800, 'T-Money Card Top-Up',       '2026-10-01'),
(3, 1,  900, 'Bibimbap Lunch',            '2026-10-02'),
(3, 5,  700, 'Gyeongbokgung Palace',      '2026-10-02'),
(3, 1, 2200, 'Korean BBQ Dinner',         '2026-10-03'),
(3, 4, 3500, 'Myeongdong Shopping',       '2026-10-03'),
(3, 2,  600, 'Subway Fare',              '2026-10-03'),
(3, 1,  800, 'Jjigae Lunch',             '2026-10-04'),
(3, 5, 2800, 'Lotte World Day Pass',      '2026-10-04'),
(3, 1,  350, 'GS25 Convenience Snacks',  '2026-10-04'),
(3, 5, 1200, 'N Seoul Tower',            '2026-10-05'),
(3, 2,  700, 'Taxi to Dongdaemun',       '2026-10-05'),
(3, 1, 1800, 'Chimaek Dinner',           '2026-10-05'),
(3, 4, 1500, 'Hongdae Street Shopping',  '2026-10-06'),
(3, 5,  600, 'Bukchon Hanok Village',    '2026-10-06'),
(3, 1,  500, 'Tteokbokki Snack',         '2026-10-07'),

-- USER1: Hong Kong Trip (trip 4) — 2026-11-10 to 2026-11-15
(4, 2,  700, 'Octopus Card',             '2026-11-10'),
(4, 3, 4500, 'Hotel Kowloon',            '2026-11-10'),
(4, 1,  600, 'Wonton Noodles',           '2026-11-11'),
(4, 5, 1500, 'Victoria Peak Tram',       '2026-11-11'),
(4, 4, 2000, 'Temple Street Night Market','2026-11-12'),
(4, 1,  400, 'Egg Tarts',               '2026-11-12'),
(4, 2,  300, 'Star Ferry',              '2026-11-13'),
(4, 4, 1800, 'Ladies Market Shopping',  '2026-11-13'),
(4, 1, 1200, 'Roast Duck Dinner',       '2026-11-13'),
(4, 5, 1800, 'Ocean Park Entry',        '2026-11-14'),
(4, 1,  700, 'Pineapple Bun Breakfast', '2026-11-14'),
(4, 2,  500, 'Airport Express',         '2026-11-15'),

-- USER2: Cebu Trip (trip 5) — 2027-01-10 to 2027-01-15
(5, 3, 3500, 'Hotel Cebu City',          '2027-01-10'),
(5, 2,  250, 'Jeepney Fare',             '2027-01-10'),
(5, 1,  200, 'Turon Snack',              '2027-01-11'),
(5, 5,  100, 'Magellan Cross Entrance',  '2027-01-11'),
(5, 1,  600, 'Pork BBQ Isaw',            '2027-01-12'),
(5, 5, 2500, 'Whale Shark Watching',     '2027-01-12'),
(5, 4, 1200, 'Sinulog Souvenir Shopping','2027-01-13'),
(5, 1,  900, 'Fresh Seafood Dinner',     '2027-01-13'),
(5, 5, 1500, 'Snorkeling Gear Rental',   '2027-01-14'),
(5, 1,  150, 'Mango Shake',              '2027-01-14'),
(5, 1,  800, 'Kare-Kare Lunch',          '2027-01-15'),
(5, 2,  400, 'Taxi to Airport',          '2027-01-15'),

-- USER2: Boracay Trip (trip 6) — 2027-03-01 to 2027-03-05
(6, 2,  200, 'Tricycle Fare',            '2027-03-01'),
(6, 5, 1500, 'Helmet Diving',            '2027-03-02'),
(6, 5,  800, 'Banana Boat Ride',         '2027-03-02'),
(6, 1, 1100, 'Sizzling Plate Dinner',    '2027-03-02'),
(6, 1,  600, 'Mango Float',              '2027-03-03'),
(6, 5, 2000, 'ATV Ride',                 '2027-03-03'),
(6, 5, 2500, 'Sunset Cruise',            '2027-03-03'),
(6, 4, 1400, 'Beach Souvenir Shopping',  '2027-03-04'),
(6, 1,  300, 'Fresh Fruit Shake',        '2027-03-04'),
(6, 1,  500, 'Local Market Groceries',   '2027-03-04'),
(6, 5,  700, 'Beach Massage',            '2027-03-05'),
(6, 2,  300, 'Tricycle to Airport',      '2027-03-05'),

-- USER3: Taiwan Trip (trip 7) — 2027-02-05 to 2027-02-10
(7, 3, 4000, 'Hotel Ximending',          '2027-02-05'),
(7, 2,  500, 'MRT Day Pass',             '2027-02-05'),
(7, 1,  800, 'Beef Noodle Soup',         '2027-02-06'),
(7, 5, 1000, 'Jiufen Day Trip',          '2027-02-07'),
(7, 1,  400, 'Night Market Stinky Tofu', '2027-02-07'),
(7, 5, 1200, 'Taipei 101 Observation',   '2027-02-08'),
(7, 1,  350, 'Scallion Pancake',         '2027-02-08'),
(7, 2,  800, 'High-Speed Rail',          '2027-02-09'),
(7, 5, 2500, 'Taroko Gorge Tour',        '2027-02-09'),
(7, 4, 1800, 'Ximending Night Shopping', '2027-02-09'),
(7, 1,  600, 'Oyster Vermicelli',        '2027-02-10'),
(7, 1,  450, 'Pineapple Cake Snack',     '2027-02-10'),

-- USER3: Baguio Trip (trip 8) — 2026-12-20 to 2026-12-23
(8, 3, 3500, 'Hotel Baguio',             '2026-12-20'),
(8, 2, 1200, 'Bus Fare from Manila',     '2026-12-20'),
(8, 5,  200, 'Burnham Park Boat Ride',   '2026-12-21'),
(8, 5,  400, 'Strawberry Farm Picking',  '2026-12-21'),
(8, 2,  150, 'Jeepney Fare',             '2026-12-21'),
(8, 1,  350, 'Ube Jam and Bread',        '2026-12-22'),
(8, 1,  700, 'Grilled Meats Dinner',     '2026-12-22'),
(8, 4,  600, 'Local Market Pasalubong',  '2026-12-22'),
(8, 5,  300, 'Camp John Hay Walk',       '2026-12-23'),
(8, 1,  500, 'Strawberry Pandesal Breakfast','2026-12-23');

