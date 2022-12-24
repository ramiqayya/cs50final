import os
from flask import Flask, redirect, render_template, url_for, request, session
from flask_session import Session
from helpers import apology, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///projectv2.db")



    
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
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")





@app.route("/register", methods=["GET","POST"])
def register():
    if request.method=="POST":
        username= request.form.get("username")
        password= request.form.get("password")
        confirmation= request.form.get("confirmation")
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
        
        return redirect('/')
        
    else:
        return render_template("register.html")
    



if __name__ == "__main__":
    app.run(debug=True)
