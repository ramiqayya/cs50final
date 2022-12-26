import os
from flask import Flask, redirect, render_template, url_for, request, session
from flask_session import Session
from helpers import apology, login_required, usd, km
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.jinja_env.filters["usd"] = usd
app.jinja_env.filters["km"] = km
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///projectv2.db")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/buy/<int:id>")
@login_required
def buy(id):
    car_to_buy = id
    db.execute("INSERT INTO requests (buyer_id, car_id) VALUES (?,?)",
               session["user_id"], car_to_buy)

    return redirect('/')


@app.route("/requests", methods=["GET", "POST"])
@login_required
def requests():
    if request.method == "POST":
        pass
    else:
        # reqs=db.execute("SELECT * FROM requests")
        mycars = db.execute(
            "SELECT * FROM cars JOIN requests ON requests.car_id=cars.car_id WHERE seller_id=?", session["user_id"])
        buyers = db.execute(
            "SELECT * FROM users JOIN (SELECT * FROM cars JOIN requests ON requests.car_id=cars.car_id) AS tt ON tt.buyer_id=users.user_id WHERE seller_id=?", session["user_id"])

        return render_template("requests.html", mycars=mycars, buyers=buyers)


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        make = request.form.get("make")
        if not make:
            return apology("must provide make")
        model = request.form.get("model")
        if not model:
            return apology("must provide model")
        year = request.form.get("year")
        if not year:
            return apology("must provide year")
        mileage = request.form.get("mileage")
        if not mileage:
            return apology("must provide mileage")
        price = request.form.get("price")
        if not price:
            return apology("must provide price")
        technical = request.form.get("technical")
        if not technical:
            return apology("must provide technical specifications")
        db.execute("INSERT INTO cars ( make, model, year, mileage, price, technical, user_id) VALUES (?,?,?,?,?,?,?)",
                   make, model, year, mileage, price, technical, session["user_id"])
        return redirect("/")

    else:
        return render_template("addcar.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not request.form.get("username"):
            return apology("must provide username", 400)

        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif password != confirmation:
            return apology("Passwords do not match", 400)

        hash = generate_password_hash(password)
        users = db.execute("SELECT username FROM users")
        # print(users)
        for user in users:
            if user['username'] == username:
                return apology("Username is taken", 400)

        db.execute(
            "INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/")
@login_required
def index():
    name = db.execute(
        "SELECT username FROM users WHERE user_id=?", session["user_id"])
    # cars = db.execute("SELECT * FROM cars")
    cars = db.execute(
        "SELECT * FROM users JOIN cars ON cars.seller_id=users.user_id")
    print(cars)

    return render_template("index.html",  username=name[0]["username"], cars=cars)


if __name__ == "__main__":
    app.run(debug=True)
