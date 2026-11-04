from flask import Flask, render_template

# Creating first application
app = Flask(__name__)

# Defining the home page
@app.route("/")
def home():
    return render_template("index.html")

# Running the application
if __name__ == "__main__":
    app.run(debug=True)