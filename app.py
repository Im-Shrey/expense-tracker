from flask import Flask, render_template, request, redirect, url_for
from decimal import Decimal, InvalidOperation
import sqlite3
from pathlib import Path

# Creating first application
app = Flask(__name__)

DB_PATH = Path("database/expenses.db")


def init_db():

    DB_PATH.parent.mkdir(exist_ok=True)

    connection = sqlite3.connect(DB_PATH)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount TEXT NOT NULL,
            category TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()

# Defining the home page
@app.route("/")
def home():
    app_name = "Python Expense Tracker"
    
    categories = [
        "Food",
        "Transport",
        "Education",
        "Shopping",
        "Entertainment"
    ]
    
    return render_template(
        "index.html",
        application_name = app_name,
        categories = categories
    )
    
@app.route("/add-expense", methods=["GET", "POST"])
def add_expense():

    if request.method == "POST":

        description = request.form.get("description", "").strip()
        amount_input = request.form.get("amount", "").strip()
        category = request.form.get("category", "")

        errors = []

        # Validate description
        if not description:
            errors.append("Description cannot be empty.")

        # Validate amount
        try:
            amount = Decimal(amount_input)

            if not amount.is_finite() or amount <= 0:
                errors.append("Amount must be greater than zero.")

        except InvalidOperation:
            amount = None
            errors.append("Please enter a valid amount.")

        # Validate category
        allowed_categories = [
            "Food",
            "Transport",
            "Education",
            "Shopping",
            "Entertainment"
        ]

        if category not in allowed_categories:
            errors.append("Please select a valid category.")

        # Display errors if validation fails
        if errors:
            return render_template(
                "add_expense.html",
                errors=errors
            )

        # Display submitted information
        # Save expense in database
        connection = sqlite3.connect(DB_PATH)

        try:
            connection.execute(
                """
                INSERT INTO expenses (description, amount, category)
                VALUES (?, ?, ?)
                """,
                (description, str(amount), category)
            )

            connection.commit()

        finally:
            connection.close()

        return redirect(url_for("view_expenses"))

    return render_template("add_expense.html")

@app.route("/expenses")
def view_expenses():

    connection = sqlite3.connect(DB_PATH)

    try:
        connection.row_factory = sqlite3.Row

        expenses = connection.execute(
            "SELECT * FROM expenses ORDER BY id DESC"
        ).fetchall()

    finally:
        connection.close()

    return render_template(
        "expenses.html",
        expenses=expenses
    )
    
init_db()

# Running the application
if __name__ == "__main__":
    app.run(debug=True)