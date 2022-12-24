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

db = SQL("sqlite:///final.db")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        pass
    else:
        return render_template("login.html")
    
    
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method=="POST":
        pass
    else:
        pass
    



if __name__ == "__main__":
    app.run(debug=True)
