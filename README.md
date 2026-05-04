# WanderWallet

WanderWallet is a web-based Travel Budget Planning and Expense Tracking System built with Flask and MySQL.

### Features

- Register and log in to a personal account
- Create, edit, and delete trips with budgets
- Add, update, and delete expenses per trip
- Automatic remaining budget tracking
- Adjust trip budgets with recalculation
- AI-powered spending insights (via OpenRouter)
- Expense reports: monthly totals, budget vs. actual, by category, remaining budget, and user spending

---

## Tech Stack

| Layer    | Technology                        |
|----------|-----------------------------------|
| Backend  | Python 3, Flask                   |
| Database | MySQL                             |
| Frontend | HTML, CSS (Jinja2 templates)      |
| AI       | OpenRouter API (GPT model)        |
| Config   | python-dotenv                     |

---

## Project Structure

```
wanderwallet/
├── app.py               # Flask routes and application logic
├── requirements.txt     # Python dependencies
├── reset_db.sql         # Clears all data and reseeds categories + admin
├── populate_demo.sql    # Inserts demo users, trips, and expenses
├── .env                 # Environment variables (not committed)
├── static/
│   └── css/style.css
└── templates/
    ├── base.html
    ├── home.html
    ├── login.html
    ├── register.html
    ├── report_monthly.html
    ├── report_budget.html
    ├── report_category.html
    ├── report_remaining.html
    └── report_user.html
```

---

## System Requirements (Mac)

### Python 3

```bash
python3 --version
```

Install via Homebrew if missing:

```bash
brew install python
```

### MySQL Server

```bash
mysql --version
```

```bash
brew install mysql
brew services start mysql
```

### Git

```bash
git --version
```

```bash
brew install git
```

> Homebrew: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

---

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/JvMapoteEdu/wanderwallet.git
cd wanderwallet
```

### 2. Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY="your-secret-key"

DB_HOST="localhost"
DB_USER="wanderuser"
DB_PASSWORD="password123"
DB_NAME="wanderwallet_db"

OPENROUTER_API_KEY="your-openrouter-api-key"
```

- `SECRET_KEY` — any random string used to sign Flask sessions
- `DB_*` — MySQL credentials (see Database Setup below)
- `OPENROUTER_API_KEY` — required for the AI Insights feature (get one at [openrouter.ai](https://openrouter.ai))

---

## Database Setup

### 1. Open MySQL

```bash
mysql -u root -p
```

### 2. Create Database and User

```sql
CREATE DATABASE wanderwallet_db;

CREATE USER 'wanderuser'@'localhost' IDENTIFIED BY 'password123';
GRANT ALL PRIVILEGES ON wanderwallet_db.* TO 'wanderuser'@'localhost';
FLUSH PRIVILEGES;

USE wanderwallet_db;
```

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

## Run the Application

```bash
python app.py
```

Open in browser: `http://127.0.0.1:5000`

---

## Testing with Demo Data

### Step 1: Reset Database

```bash
sudo mysql < reset_db.sql
```

Clears all data, resets auto-increment IDs, recreates categories, and inserts the admin user.

### Step 2: Populate Demo Data

```bash
sudo mysql < populate_demo.sql
```

Inserts multiple users, trips, expenses, and updates budgets automatically.

### Step 3: Run the App

```bash
python app.py
```

### Step 4: Login Accounts

| Username | Password |
|----------|----------|
| admin    | password |
| user1    | 1234     |
| user2    | 1234     |
| user3    | 1234     |

### Step 5: Feature Checklist

| Feature          | Expected Behavior                                        |
|------------------|----------------------------------------------------------|
| Register         | New account created; redirects to login                  |
| Create Trip      | Trip appears in overview with budget                     |
| Edit Trip        | Trip name, dates, destination, and budget update         |
| Delete Trip      | Trip and all its expenses are removed                    |
| Add Expense      | Remaining budget decreases by amount                     |
| Update Expense   | Budget adjusts by the difference from old amount         |
| Delete Expense   | Budget is restored by the deleted amount                 |
| Adjust Budget    | Remaining recalculates based on current spending         |
| AI Insights      | Returns 3–5 personalized spending tips                   |

### Step 6: Reports

| Report              | Input Required              |
|---------------------|-----------------------------|
| Monthly Total       | Month + Year (e.g. 5 / 2025)|
| Budget vs. Actual   | None                        |
| Expense by Category | None                        |
| Remaining Budget    | None                        |
| User Spending       | None                        |

### Step 7: Multi-User Validation

Log in as different users and confirm:

- Each user sees only their own trips
- Each user sees only their own expenses
- Reports are scoped per user

---

## Notes

- Ensure MySQL is running before starting the app
- AI Insights requires a valid `OPENROUTER_API_KEY` in `.env`
- Always run `reset_db.sql` then `populate_demo.sql` before a fresh demo
- The `.env` file must never be committed to version control
