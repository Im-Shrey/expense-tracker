from flask import Flask, render_template, request

# Creating first application
app = Flask(__name__)

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

        description = request.form.get("description")
        amount = request.form.get("amount")
        category = request.form.get("category")

        return render_template(
            "expense_result.html",
            description=description,
            amount=amount,
            category=category
        )

    return render_template("add_expense.html")

# Running the application
if __name__ == "__main__":
    app.run(debug=True)