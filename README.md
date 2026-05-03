# WanderWallet

WanderWallet is a web-based Travel Budget Planning and Expense Tracking System built using Flask and MySQL.

It allows users to:

* Login to the system
* Create trips with budgets
* Add, update, and delete expenses
* Automatically track remaining budget
* Adjust trip budgets
* Generate expense reports

---

## 🛠 Tech Stack

* Backend: Python (Flask)
* Database: MySQL
* Frontend: HTML (basic UI)

---

## 💻 System Requirements (Mac)

Make sure the following are installed:

### 1. Python 3

Check:

```bash
python3 --version
```

If not installed:

```bash
brew install python
```

---

### 2. MySQL Server

Check:

```bash
mysql --version
```

If not installed:

```bash
brew install mysql
brew services start mysql
```

---

### 3. Git

Check:

```bash
git --version
```

If not installed:

```bash
brew install git
```

---

### 📦 Python Dependencies

All required Python libraries (Flask, MySQL connector, etc.) are listed in `requirements.txt`.

Install them using:

```bash
pip install -r requirements.txt
```

---

### 📝 Notes

* No need to manually install Flask or other Python libraries
* They will be installed automatically via `requirements.txt`
* Homebrew is recommended for easier installation:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

---

## 📦 Project Setup (Mac)

### 1. Clone Repository

```bash
git clone https://github.com/JvMapoteEdu/wanderwallet.git
cd wanderwallet
```

---

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🗄 Database Setup (MySQL)

### 1. Open MySQL

```bash
mysql -u root -p
```

---

### 2. Create Database

```sql
CREATE DATABASE wanderwallet_db;
USE wanderwallet_db;
```

---

### 3. Create Tables

```sql
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(100),
    role VARCHAR(50),
    created_date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE trips (
    trip_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    trip_name VARCHAR(100),
    destination VARCHAR(100),
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE budgets (
    budget_id INT AUTO_INCREMENT PRIMARY KEY,
    trip_id INT UNIQUE,
    total_budget DECIMAL(10,2),
    remaining_budget DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100)
);

CREATE TABLE expenses (
    expense_id INT AUTO_INCREMENT PRIMARY KEY,
    trip_id INT,
    category_id INT,
    amount DECIMAL(10,2),
    description TEXT,
    expense_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### 4. Create Database User

```sql
CREATE USER 'wanderuser'@'localhost' IDENTIFIED BY 'password123';
GRANT ALL PRIVILEGES ON wanderwallet_db.* TO 'wanderuser'@'localhost';
FLUSH PRIVILEGES;
```

---

### 5. Insert Initial Data

#### Categories

```sql
INSERT INTO categories (category_name) VALUES
('Food'),
('Transport'),
('Hotel'),
('Shopping'),
('Activities');
```

#### Test User

```sql
INSERT INTO users (username, email, password, role)
VALUES ('admin', 'admin@email.com', '1234', 'user');
```

---

## ▶️ Run the Application

```bash
python app.py
```

Open in browser:

```
http://127.0.0.1:5000
```

---

## 🔐 Login

```
Username: admin  
Password: 1234
```

---

## 🧪 How to Test the System

### 1. Create Trip

* Fill in trip details
* Click **Create Trip**

---

### 2. Add Expense

* Select Trip and Category
* Enter amount, description, date
* Click **Add Expense**

---

### 3. Update Expense

* Select expense from dropdown
* Enter new amount

---

### 4. Delete Expense

* Select expense from dropdown

---

### 5. Adjust Budget

* Select trip
* Enter new budget

---

### 6. Reports

* Enter month and year
* View total expenses

---

## ⚠️ Notes

* Ensure MySQL service is running
* Check database credentials in `app.py` if connection fails
* This is a school project (focus on functionality over UI)

---
