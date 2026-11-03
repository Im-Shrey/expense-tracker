from flask import Flask

# Creating first application
app = Flask(__name__)

# Defining the home page
@app.route("/")
def home():
    return "Welcome to Python Expense Tracker"

# Running the application
if __name__ == "__main__":
    app.run(debug=True)