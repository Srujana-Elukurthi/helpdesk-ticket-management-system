from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/helpdesk"
app.config["SECRET_KEY"] = "secret123"

mongo = PyMongo(app)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return redirect("/login")

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        existing_user = mongo.db.users.find_one({"email": email})
        if existing_user:
            return "User already exists"

        mongo.db.users.insert_one({
            "name": name,
            "email": email,
            "password": generate_password_hash(password)
        })

        return redirect("/login")

    return render_template("register.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = mongo.db.users.find_one({"email": email})
        if user and check_password_hash(user["password"], password):
            return redirect("/dashboard")
        else:
            return "Invalid credentials"

    return render_template("login.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    return render_template("index.html")
# ---------------- ADMIN DASHBOARD ----------------
@app.route("/admin")
def admin_dashboard():
    tickets = mongo.db.tickets.find()
    return render_template("admin.html", tickets=tickets)


# ---------------- CREATE TICKET ----------------
@app.route("/create-ticket", methods=["POST"])
def create_ticket():
    data = request.json

    mongo.db.tickets.insert_one({
        "title": data["title"],
        "description": data["description"],
        "status": "Open"
    })

    return jsonify({"message": "Ticket saved successfully"})

if __name__ == "__main__":
    app.run(debug=True)
