# WanderWallet (MVP)

WanderWallet is a simple web-based Travel Budget Planning and Expense Tracking System.

It allows users to:

* Create trips with a budget
* Add expenses
* Automatically deduct expenses from the remaining budget
* View trips and balances
* Generate monthly expense reports

---

## 🛠 Tech Stack

* Backend: Python (Flask)
* Database: MySQL
* Frontend: HTML (basic UI)

---

## 📦 Project Setup

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

## 🗄 Database Setup

### 1. Start MySQL and open it

```bash
sudo mysql
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
CREATE TABLE trips (
    trip_id INT AUTO_INCREMENT PRIMARY KEY,
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

CREATE TABLE expenses (
    expense_id INT AUTO_INCREMENT PRIMARY KEY,
    trip_id INT,
    category VARCHAR(100),
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

## ▶️ Run the Application

```bash
python app.py
```

Open in browser:

```
http://localhost:5000
```

---

## 🧪 How to Test the System

### 1. Create Trip

* Enter trip details and budget
* Click **Create Trip**
* A popup will confirm success

---

### 2. Add Expense

* Enter Trip ID (from table)
* Input category, amount, description, and date
* Click **Add Expense**
* Remaining budget updates automatically

---

### 3. Dashboard

* Displays all trips
* Shows total and remaining budget

---

### 4. Generate Report

* Enter month and year
* Click **Generate Report**
* Displays total expenses for that period

---

## ⚠️ Notes

* Make sure MySQL service is running
* If connection fails, check credentials in `app.py`
* This is an MVP (basic UI, core features implemented)

---
