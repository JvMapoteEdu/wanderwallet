from flask import Flask, request, redirect, url_for, flash, session, render_template, jsonify
import mysql.connector
from calendar import month_name as _month_name
import requests as http_requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

conn = mysql.connector.connect(
    host=os.environ.get("DB_HOST", "localhost"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    database=os.environ.get("DB_NAME")
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
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password.", "danger")

    return render_template('login.html')

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing = cursor.fetchone()

        if existing:
            flash("Username already exists!", "danger")
            return redirect(url_for('register'))

        cursor.execute("""
        INSERT INTO users (username, email, password, role)
        VALUES (%s, %s, %s, %s)
        """, (username, email, password, 'user'))

        conn.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

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

    cursor.execute("""
    SELECT t.trip_id, t.trip_name, t.destination,
           t.start_date, t.end_date,
           b.total_budget, b.remaining_budget
    FROM trips t
    LEFT JOIN budgets b ON t.trip_id = b.trip_id
    WHERE t.user_id = %s
    ORDER BY t.trip_id DESC
    """, (session['user_id'],))
    trips = cursor.fetchall()

    cursor.execute("SELECT * FROM categories ORDER BY category_name")
    categories = cursor.fetchall()

    cursor.execute("""
    SELECT e.expense_id, e.amount, e.description, e.expense_date,
           e.trip_id, t.trip_name, c.category_name
    FROM expenses e
    JOIN trips t ON e.trip_id = t.trip_id
    JOIN categories c ON e.category_id = c.category_id
    WHERE t.user_id = %s
    ORDER BY e.expense_date DESC, e.expense_id DESC
    """, (session['user_id'],))
    expenses = cursor.fetchall()

    total_budget    = sum(float(t['total_budget'])     for t in trips if t['total_budget'])
    total_remaining = sum(float(t['remaining_budget']) for t in trips if t['remaining_budget'])

    stats = {
        'total_trips':     len(trips),
        'total_budget':    total_budget,
        'total_spent':     total_budget - total_remaining,
        'total_remaining': total_remaining,
    }

    return render_template('home.html',
                           trips=trips,
                           categories=categories,
                           expenses=expenses,
                           stats=stats)

# ---------------- ADD TRIP ----------------
@app.route('/add-trip', methods=['POST'])
def add_trip():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    trip_name   = request.form['trip_name']
    destination = request.form['destination']
    start_date  = request.form['start_date']
    end_date    = request.form['end_date']
    budget      = request.form['budget']

    cursor = conn.cursor()

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

    flash("Trip created successfully!", "success")
    return redirect(url_for('home'))

# ---------------- ADD EXPENSE ----------------
@app.route('/add-expense', methods=['POST'])
def add_expense():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    trip_id      = request.form['trip_id']
    category_id  = request.form['category_id']
    amount       = float(request.form['amount'])
    description  = request.form['description']
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

    flash("Expense added successfully!", "success")
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
        flash("Expense not found.", "warning")
        return redirect(url_for('home'))

    trip_id = expense['trip_id']
    amount  = expense['amount']

    cursor.execute("""
    UPDATE budgets
    SET remaining_budget = remaining_budget + %s
    WHERE trip_id = %s
    """, (amount, trip_id))

    cursor.execute("DELETE FROM expenses WHERE expense_id = %s", (expense_id,))

    conn.commit()

    flash("Expense deleted and budget restored.", "success")
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
        flash("Expense not found.", "warning")
        return redirect(url_for('home'))

    old_amount = float(expense['amount'])
    trip_id    = expense['trip_id']

    cursor.execute("""
    UPDATE expenses
    SET amount = %s
    WHERE expense_id = %s
    """, (new_amount, expense_id))

    difference = new_amount - old_amount

    cursor.execute("""
    UPDATE budgets
    SET remaining_budget = remaining_budget - %s
    WHERE trip_id = %s
    """, (difference, trip_id))

    conn.commit()

    flash("Expense updated successfully!", "success")
    return redirect(url_for('home'))

# ---------------- ADJUST BUDGET ----------------
@app.route('/adjust-budget', methods=['POST'])
def adjust_budget():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    trip_id    = request.form['trip_id']
    new_budget = float(request.form['new_budget'])

    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM budgets WHERE trip_id = %s", (trip_id,))
    budget = cursor.fetchone()

    if not budget:
        flash("Budget not found.", "warning")
        return redirect(url_for('home'))

    spent         = float(budget['total_budget']) - float(budget['remaining_budget'])
    new_remaining = new_budget - spent

    cursor.execute("""
    UPDATE budgets
    SET total_budget = %s, remaining_budget = %s
    WHERE trip_id = %s
    """, (new_budget, new_remaining, trip_id))

    conn.commit()

    flash("Budget updated successfully!", "success")
    return redirect(url_for('home'))

# ---------------- EDIT TRIP ----------------
@app.route('/edit-trip', methods=['POST'])
def edit_trip():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    trip_id     = request.form['trip_id']
    trip_name   = request.form['trip_name']
    destination = request.form['destination']
    start_date  = request.form['start_date']
    end_date    = request.form['end_date']
    new_budget  = float(request.form['budget'])

    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM budgets WHERE trip_id = %s", (trip_id,))
    budget = cursor.fetchone()

    cursor.execute("""
    UPDATE trips
    SET trip_name = %s, destination = %s, start_date = %s, end_date = %s
    WHERE trip_id = %s AND user_id = %s
    """, (trip_name, destination, start_date, end_date, trip_id, session['user_id']))

    if budget:
        spent         = float(budget['total_budget']) - float(budget['remaining_budget'])
        new_remaining = new_budget - spent
        cursor.execute("""
        UPDATE budgets
        SET total_budget = %s, remaining_budget = %s
        WHERE trip_id = %s
        """, (new_budget, new_remaining, trip_id))
    else:
        cursor.execute("""
        INSERT INTO budgets (trip_id, total_budget, remaining_budget)
        VALUES (%s, %s, %s)
        """, (trip_id, new_budget, new_budget))

    conn.commit()

    flash("Trip updated successfully!", "success")
    return redirect(url_for('home'))

# ---------------- DELETE TRIP ----------------
@app.route('/delete-trip', methods=['POST'])
def delete_trip():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    trip_id = request.form['trip_id']

    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM expenses WHERE trip_id = %s
    """, (trip_id,))

    cursor.execute("""
    DELETE FROM budgets WHERE trip_id = %s
    """, (trip_id,))

    cursor.execute("""
    DELETE FROM trips WHERE trip_id = %s AND user_id = %s
    """, (trip_id, session['user_id']))

    conn.commit()

    flash("Trip deleted successfully.", "success")
    return redirect(url_for('home'))

# ---------------- REPORT: MONTHLY TOTAL ----------------
@app.route('/report', methods=['POST'])
def report():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    month = request.form['month']
    year  = request.form['year']

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT SUM(e.amount) AS total_expense
    FROM expenses e
    JOIN trips t ON e.trip_id = t.trip_id
    WHERE t.user_id = %s
      AND MONTH(e.expense_date) = %s
      AND YEAR(e.expense_date)  = %s
    """, (session['user_id'], month, year))

    result = cursor.fetchone()
    total  = result['total_expense'] if result['total_expense'] else 0

    return render_template('report_monthly.html',
                           total=total,
                           month=month,
                           month_name=_month_name[int(month)],
                           year=year)

# ---------------- REPORT: BUDGET VS ACTUAL ----------------
@app.route('/report-budget', methods=['POST'])
def report_budget():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT t.trip_name,
           b.total_budget,
           (b.total_budget - b.remaining_budget) AS spent,
           b.remaining_budget
    FROM budgets b
    JOIN trips t ON b.trip_id = t.trip_id
    WHERE t.user_id = %s
    """, (session['user_id'],))

    data = cursor.fetchall()

    return render_template('report_budget.html', data=data)

# ---------------- REPORT: EXPENSE BY CATEGORY ----------------
@app.route('/report-category', methods=['POST'])
def report_category():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT c.category_name, SUM(e.amount) AS total
    FROM expenses e
    JOIN categories c ON e.category_id = c.category_id
    JOIN trips t ON e.trip_id = t.trip_id
    WHERE t.user_id = %s
    GROUP BY c.category_name
    ORDER BY total DESC
    """, (session['user_id'],))

    data = cursor.fetchall()

    return render_template('report_category.html', data=data)

# ---------------- REPORT: REMAINING BUDGET ----------------
@app.route('/report-remaining', methods=['POST'])
def report_remaining():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT t.trip_name, b.remaining_budget, b.total_budget
    FROM budgets b
    JOIN trips t ON b.trip_id = t.trip_id
    WHERE t.user_id = %s
    ORDER BY b.remaining_budget ASC
    """, (session['user_id'],))

    data = cursor.fetchall()

    return render_template('report_remaining.html', data=data)

# ---------------- REPORT: USER SPENDING ----------------
@app.route('/report-user', methods=['POST'])
def report_user():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT u.username, SUM(e.amount) AS total_spent
    FROM users u
    JOIN trips t ON u.user_id = t.user_id
    JOIN expenses e ON t.trip_id = e.trip_id
    WHERE u.user_id = %s
    GROUP BY u.username
    """, (session['user_id'],))

    row   = cursor.fetchone()
    total = float(row['total_spent']) if row and row['total_spent'] else 0
    uname = row['username'] if row else session['username']

    return render_template('report_user.html', total=total, username=uname)

# ---------------- AI INSIGHTS ----------------
@app.route('/ai-insights', methods=['POST'])
def ai_insights():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT t.trip_name, t.destination,
           b.total_budget, b.remaining_budget
    FROM trips t
    LEFT JOIN budgets b ON t.trip_id = b.trip_id
    WHERE t.user_id = %s
    """, (session['user_id'],))
    trips = cursor.fetchall()

    cursor.execute("""
    SELECT c.category_name, SUM(e.amount) AS total
    FROM expenses e
    JOIN categories c ON e.category_id = c.category_id
    JOIN trips t ON e.trip_id = t.trip_id
    WHERE t.user_id = %s
    GROUP BY c.category_name
    ORDER BY total DESC
    """, (session['user_id'],))
    category_data = cursor.fetchall()

    trips_lines = []
    for t in trips:
        total     = float(t['total_budget'])     if t['total_budget']     else 0
        remaining = float(t['remaining_budget']) if t['remaining_budget'] else 0
        spent     = total - remaining
        pct       = round((spent / total) * 100) if total > 0 else 0
        trips_lines.append(
            f"- {t['trip_name']} ({t['destination']}): "
            f"Budget ₱{total:,.2f}, Spent ₱{spent:,.2f}, "
            f"Remaining ₱{remaining:,.2f} ({pct}% used)"
        )

    category_lines = [
        f"- {c['category_name']}: ₱{float(c['total']):,.2f}"
        for c in category_data
    ]

    user_context = (
        f"Username: {session['username']}\n\n"
        f"Trips:\n" + ("\n".join(trips_lines) if trips_lines else "No trips yet") + "\n\n"
        f"Spending by Category:\n" + ("\n".join(category_lines) if category_lines else "No expenses yet")
    )

    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    try:
        resp = http_requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            data=json.dumps({
                "model": "openai/gpt-5.2",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are WanderWallet AI, a friendly travel budget analyst. "
                            "Given the user's trip and expense data, provide 3–5 concise, "
                            "actionable insights about their spending habits and budget health. "
                            "Be encouraging, specific, and practical. "
                            "Use short bullet points starting with an emoji. "
                            "End your response after the last insight. "
                            "Do NOT ask follow-up questions, request more information, "
                            "or prompt the user for any input whatsoever."
                        )
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Here is my travel budget data:\n\n{user_context}\n\n"
                            "Please analyze my spending and give me smart tips to travel better "
                            "and stay within budget."
                        )
                    }
                ],
                "max_tokens": 2000
            }),
            timeout=30
        )
        result = resp.json()
        if 'choices' in result and result['choices']:
            return jsonify({'insight': result['choices'][0]['message']['content']})
        return jsonify({'error': result.get('error', {}).get('message', 'No response from AI.')}), 502
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500


if __name__ == '__main__':
    app.run(debug=True)
