from flask import Flask, request, redirect, url_for, flash, get_flashed_messages
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret123"

conn = mysql.connector.connect(
    host="localhost",
    user="wanderuser",
    password="password123",
    database="wanderwallet_db"
)

@app.route('/')
def home():
    cursor = conn.cursor(dictionary=True)

    messages = get_flashed_messages()

    html = ""

    for msg in messages:
        html += f"""
        <script>
            alert("{msg}");
        </script>
        """

    # Get trips + budget
    query = """
    SELECT t.trip_id, t.trip_name, t.destination,
           b.total_budget, b.remaining_budget
    FROM trips t
    LEFT JOIN budgets b ON t.trip_id = b.trip_id
    """
    cursor.execute(query)
    trips = cursor.fetchall()

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
        Trip ID: <input type="number" name="trip_id"><br><br>
        Category: <input type="text" name="category"><br><br>
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
        Month: <input type="number" name="month" min="1" max="12"><br><br>
        Year: <input type="number" name="year"><br><br>
        <button type="submit">Generate Report</button>
    </form>
    '''

    return html

@app.route('/add-trip', methods=['POST'])
def add_trip():
    trip_name = request.form['trip_name']
    destination = request.form['destination']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    budget = request.form['budget']

    cursor = conn.cursor()

    # 1. Insert trip
    trip_query = """
    INSERT INTO trips (trip_name, destination, start_date, end_date)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(trip_query, (trip_name, destination, start_date, end_date))

    # Get the last inserted trip_id
    trip_id = cursor.lastrowid

    # 2. Insert budget
    budget_query = """
    INSERT INTO budgets (trip_id, total_budget, remaining_budget)
    VALUES (%s, %s, %s)
    """
    cursor.execute(budget_query, (trip_id, budget, budget))

    conn.commit()

    flash("Trip created successfully!")
    return redirect(url_for('home'))

@app.route('/add-expense', methods=['POST'])
def add_expense():
    trip_id = request.form['trip_id']
    category = request.form['category']
    amount = float(request.form['amount'])
    description = request.form['description']
    expense_date = request.form['expense_date']

    cursor = conn.cursor()

    # 1. Insert expense
    expense_query = """
    INSERT INTO expenses (trip_id, category, amount, description, expense_date)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(expense_query, (trip_id, category, amount, description, expense_date))

    # 2. Deduct from budget
    update_budget_query = """
    UPDATE budgets
    SET remaining_budget = remaining_budget - %s
    WHERE trip_id = %s
    """
    cursor.execute(update_budget_query, (amount, trip_id))

    conn.commit()

    flash("Expense added successfully!")
    return redirect(url_for('home'))

@app.route('/report', methods=['POST'])
def report():
    month = request.form['month']
    year = request.form['year']

    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT SUM(amount) as total_expense
    FROM expenses
    WHERE MONTH(expense_date) = %s
    AND YEAR(expense_date) = %s
    """

    cursor.execute(query, (month, year))
    result = cursor.fetchone()

    total = result['total_expense'] if result['total_expense'] else 0

    return f"""
    <h2>Report Result</h2>
    <p>Total Expenses for {month}/{year}: <b>{total}</b></p>
    <a href="/">Back</a>
    """

if __name__ == '__main__':
    app.run(debug=True)
