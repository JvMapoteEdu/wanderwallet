from flask import Flask, request, redirect, url_for, flash, get_flashed_messages, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret123"

conn = mysql.connector.connect(
    host="localhost",
    user="wanderuser",
    password="password123",
    database="wanderwallet_db"
)

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
        SELECT * FROM users
        WHERE username = %s AND password = %s
        """, (username, password))

        user = cursor.fetchone()

        if user:
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            flash("Login successful!")
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials")

    return '''
    <h2>Login</h2>
    <form method="POST">
        Username: <input type="text" name="username"><br><br>
        Password: <input type="password" name="password"><br><br>
        <button type="submit">Login</button>
    </form>
    <br>
    <a href="/register">Don't have an account? Register here</a>
    '''

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        cursor = conn.cursor(dictionary=True)

        # Check if user already exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing = cursor.fetchone()

        if existing:
            flash("Username already exists!")
            return redirect(url_for('register'))

        # Insert new user
        cursor.execute("""
        INSERT INTO users (username, email, password, role)
        VALUES (%s, %s, %s, %s)
        """, (username, email, password, 'user'))

        conn.commit()

        flash("Registration successful! Please login.")
        return redirect(url_for('login'))

    return '''
    <h2>Register</h2>
    <form method="POST">
        Username: <input type="text" name="username"><br><br>
        Email: <input type="text" name="email"><br><br>
        Password: <input type="password" name="password"><br><br>
        <button type="submit">Register</button>
    </form>

    <br>
    <a href="/login">Back to Login</a>
    '''

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ---------------- HOME ----------------
@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cursor = conn.cursor(dictionary=True)

    messages = get_flashed_messages()
    html = ""

    for msg in messages:
        html += f"""
        <script>
            alert("{msg}");
        </script>
        """

    # GET TRIPS
    cursor.execute("""
    SELECT t.trip_id, t.trip_name, t.destination,
           b.total_budget, b.remaining_budget
    FROM trips t
    LEFT JOIN budgets b ON t.trip_id = b.trip_id
    WHERE t.user_id = %s
    """, (session['user_id'],))
    trips = cursor.fetchall()

    # GET CATEGORIES
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()

    # GET EXPENSES
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    html += f'<p>Welcome, {session["username"]} | <a href="/logout">Logout</a></p>'

    html += '''
    <h2>Create Trip</h2>
    <form method="POST" action="/add-trip">
        Trip Name: <input type="text" name="trip_name"><br><br>
        Destination: <input type="text" name="destination"><br><br>
        Start Date: <input type="date" name="start_date"><br><br>
        End Date: <input type="date" name="end_date"><br><br>
        Budget: <input type="number" name="budget"><br><br>
        <button type="submit">Create Trip</button>
    </form>

    <hr>

    <h2>Add Expense</h2>
    <form method="POST" action="/add-expense">

        Trip:
        <select name="trip_id">
    '''

    for trip in trips:
        html += f'<option value="{trip["trip_id"]}">{trip["trip_name"]}</option>'

    html += '''
        </select><br><br>

        Category:
        <select name="category_id">
    '''

    for cat in categories:
        html += f'<option value="{cat["category_id"]}">{cat["category_name"]}</option>'

    html += '''
        </select><br><br>

        Amount: <input type="number" name="amount"><br><br>
        Description: <input type="text" name="description"><br><br>
        Date: <input type="date" name="expense_date"><br><br>
        <button type="submit">Add Expense</button>
    </form>

    <hr>

    <h2>Trips Overview</h2>
    <table border="1">
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Destination</th>
            <th>Total Budget</th>
            <th>Remaining</th>
        </tr>
    '''

    for trip in trips:
        html += f"""
        <tr>
            <td>{trip['trip_id']}</td>
            <td>{trip['trip_name']}</td>
            <td>{trip['destination']}</td>
            <td>{trip['total_budget'] if trip['total_budget'] else 0}</td>
            <td>{trip['remaining_budget'] if trip['remaining_budget'] else 0}</td>
        </tr>
        """

    html += "</table>"

    html += '''
    <hr>

    <h2>Expense Report</h2>
    <form method="POST" action="/report">
        Month: <input type="number" name="month"><br><br>
        Year: <input type="number" name="year"><br><br>
        <button type="submit">Generate Report</button>
    </form>
    '''

    # 🔥 DELETE EXPENSE DROPDOWN
    html += '''
    <hr>
    <h2>Delete Expense</h2>
    <form method="POST" action="/delete-expense">
        Expense:
        <select name="expense_id">
    '''

    for e in expenses:
        html += f'<option value="{e["expense_id"]}">ID {e["expense_id"]} - {e["description"]} (₱{e["amount"]})</option>'

    html += '''
        </select><br><br>
        <button type="submit">Delete Expense</button>
    </form>
    '''

    # 🔥 UPDATE EXPENSE DROPDOWN
    html += '''
    <hr>
    <h2>Update Expense</h2>
    <form method="POST" action="/update-expense">
        Expense:
        <select name="expense_id">
    '''

    for e in expenses:
        html += f'<option value="{e["expense_id"]}">ID {e["expense_id"]} - {e["description"]} (₱{e["amount"]})</option>'

    html += '''
        </select><br><br>

        New Amount: <input type="number" name="amount"><br><br>
        <button type="submit">Update Expense</button>
    </form>
    '''

    # 🔥 ADJUST BUDGET DROPDOWN
    html += '''
    <hr>
    <h2>Adjust Budget</h2>
    <form method="POST" action="/adjust-budget">
        Trip:
        <select name="trip_id">
    '''

    for trip in trips:
        html += f'<option value="{trip["trip_id"]}">{trip["trip_name"]}</option>'

    html += '''
        </select><br><br>

        New Budget: <input type="number" name="new_budget"><br><br>
        <button type="submit">Update Budget</button>
    </form>
    '''

    return html

# ---------------- ADD TRIP ----------------
@app.route('/add-trip', methods=['POST'])
def add_trip():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    trip_name = request.form['trip_name']
    destination = request.form['destination']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    budget = request.form['budget']

    cursor = conn.cursor()

    # 🔥 USE SESSION USER
    cursor.execute("""
    INSERT INTO trips (user_id, trip_name, destination, start_date, end_date)
    VALUES (%s, %s, %s, %s, %s)
    """, (session['user_id'], trip_name, destination, start_date, end_date))

    trip_id = cursor.lastrowid

    cursor.execute("""
    INSERT INTO budgets (trip_id, total_budget, remaining_budget)
    VALUES (%s, %s, %s)
    """, (trip_id, budget, budget))

    conn.commit()

    flash("Trip created successfully!")
    return redirect(url_for('home'))

# ---------------- ADD EXPENSE ----------------
@app.route('/add-expense', methods=['POST'])
def add_expense():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    trip_id = request.form['trip_id']
    category_id = request.form['category_id']
    amount = float(request.form['amount'])
    description = request.form['description']
    expense_date = request.form['expense_date']

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO expenses (trip_id, category_id, amount, description, expense_date)
    VALUES (%s, %s, %s, %s, %s)
    """, (trip_id, category_id, amount, description, expense_date))

    cursor.execute("""
    UPDATE budgets
    SET remaining_budget = remaining_budget - %s
    WHERE trip_id = %s
    """, (amount, trip_id))

    conn.commit()

    flash("Expense added successfully!")
    return redirect(url_for('home'))


# ---------------- DELETE EXPENSE ----------------
@app.route('/delete-expense', methods=['POST'])
def delete_expense():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    expense_id = request.form['expense_id']

    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM expenses WHERE expense_id = %s", (expense_id,))
    expense = cursor.fetchone()

    if not expense:
        flash("Expense not found")
        return redirect(url_for('home'))

    trip_id = expense['trip_id']
    amount = expense['amount']

    # Restore budget
    cursor.execute("""
    UPDATE budgets
    SET remaining_budget = remaining_budget + %s
    WHERE trip_id = %s
    """, (amount, trip_id))

    # Delete expense
    cursor.execute("DELETE FROM expenses WHERE expense_id = %s", (expense_id,))

    conn.commit()

    flash("Expense deleted and budget restored!")
    return redirect(url_for('home'))


# ---------------- UPDATE EXPENSE ----------------
@app.route('/update-expense', methods=['POST'])
def update_expense():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    expense_id = request.form['expense_id']
    new_amount = float(request.form['amount'])

    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM expenses WHERE expense_id = %s", (expense_id,))
    expense = cursor.fetchone()

    if not expense:
        flash("Expense not found")
        return redirect(url_for('home'))

    old_amount = float(expense['amount'])
    trip_id = expense['trip_id']

    # Update expense
    cursor.execute("""
    UPDATE expenses
    SET amount = %s
    WHERE expense_id = %s
    """, (new_amount, expense_id))

    # Adjust budget
    difference = new_amount - old_amount

    cursor.execute("""
    UPDATE budgets
    SET remaining_budget = remaining_budget - %s
    WHERE trip_id = %s
    """, (difference, trip_id))

    conn.commit()

    flash("Expense updated successfully!")
    return redirect(url_for('home'))


# ---------------- ADJUST BUDGET ----------------
@app.route('/adjust-budget', methods=['POST'])
def adjust_budget():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    trip_id = request.form['trip_id']
    new_budget = float(request.form['new_budget'])

    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM budgets WHERE trip_id = %s", (trip_id,))
    budget = cursor.fetchone()

    if not budget:
        flash("Budget not found")
        return redirect(url_for('home'))

    total_budget = float(budget['total_budget'])
    remaining_budget = float(budget['remaining_budget'])

    spent = total_budget - remaining_budget
    new_remaining = new_budget - spent

    cursor.execute("""
    UPDATE budgets
    SET total_budget = %s, remaining_budget = %s
    WHERE trip_id = %s
    """, (new_budget, new_remaining, trip_id))

    conn.commit()

    flash("Budget updated successfully!")
    return redirect(url_for('home'))

# ---------------- REPORT ----------------
@app.route('/report', methods=['POST'])
def report():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    month = request.form['month']
    year = request.form['year']

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT SUM(amount) as total_expense
    FROM expenses
    WHERE MONTH(expense_date) = %s
    AND YEAR(expense_date) = %s
    """, (month, year))

    result = cursor.fetchone()
    total = result['total_expense'] if result['total_expense'] else 0

    return f"""
    <h2>Report Result</h2>
    <p>Total Expenses for {month}/{year}: <b>{total}</b></p>
    <a href="/">Back</a>
    """

if __name__ == '__main__':
    app.run(debug=True)