from flask import Flask, render_template

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

# Running the application
if __name__ == "__main__":
    app.run(debug=True)