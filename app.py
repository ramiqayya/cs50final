import os
from flask import Flask, redirect, render_template, url_for, request, session
from flask_session import Session
from helpers import apology, login_required, usd, km
from werkzeug.security import check_password_hash, generate_password_hash
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from cs50 import SQL
from werkzeug.utils import secure_filename
import asyncio
import time
import shutil

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'


class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload File")


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


@app.route("/buy/<id>", methods=["POST"])
@login_required
def buy(id):
    car_to_buy = id
    disable = True
    requests = db.execute("SELECT * FROM requests WHERE buyer_id=? AND car_id=?",
                          session["user_id"], car_to_buy)
    if not requests:
        db.execute("INSERT INTO requests (buyer_id, car_id) VALUES (?,?)",
                   session["user_id"], car_to_buy)
    else:

        return apology("request has been already sent!")

    return redirect('/')


@app.route("/requests")
@login_required
def requests():
    # if request.method == "POST":
    #     db.execute("SELECT * FROM requests WHERE ")
    #     db.execute("DELETE from")
    # else:
    # reqs=db.execute("SELECT * FROM requests")
    # mycars = db.execute(
    #     "SELECT * FROM cars JOIN requests ON requests.car_id=cars.car_id WHERE seller_id=?", session["user_id"])
    buyers = db.execute(
        "SELECT * FROM users JOIN (SELECT * FROM cars JOIN requests ON requests.car_id=cars.car_id) AS tt ON tt.buyer_id=users.user_id WHERE seller_id=?", session["user_id"])

    return render_template("requests.html", buyers=buyers)


@app.route("/requests/agree/<id>", methods=["POST"])
@login_required
def agree(id):
    buyername = request.form.get('buyer')
    buyerid = request.form.get('buyerid')
    req_id = request.form.get('req_id')
    make = request.form.get('make')
    model = request.form.get('model')
    seller_name = db.execute(
        "SELECT username FROM users WHERE user_id=?", session["user_id"])
    print(buyername, buyerid)
    db.execute(
        "INSERT INTO approved (request_id,buyerid,car_make,car_model,seller_name) VALUES(?,?,?,?,?)", req_id, buyerid, make, model, seller_name[0]["username"])

    # img_id = db.execute("SELECT * FROM images WHERE car_id=?", id)
    # image_id = img_id[0]['img_id']
    db.execute("DELETE FROM requests WHERE car_id=?", id)
    db.execute("DELETE FROM cars WHERE car_id=?", id)
    db.execute("DELETE FROM images WHERE car_id=?", id)
    locatin = "./static/images/"+id
    shutil.rmtree(locatin, ignore_errors=True)

    return redirect("/requests")


@app.route("/r/<id>", methods=["POST"])
@login_required
def dismiss(id):
    print(id)
    db.execute("DELETE FROM approved WHERE request_id=?", id)
    return redirect("/")


@app.route("/requests/reject/<id>", methods=["POST"])
@login_required
def reject(id):
    db.execute("DELETE FROM requests WHERE car_id=?", id)
    return redirect("/requests")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    form = UploadFileForm()
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

        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               app.config['UPLOAD_FOLDER'], secure_filename(file.filename)), 'rb') as f:
            data = f.read()

        # image = request.files.get("image")
        # if not image:
        #     return apology("must provide image")

        db.execute("INSERT INTO cars ( make, model, year, mileage, price, technical, seller_id) VALUES (?,?,?,?,?,?,?)",
                   make, model, year, mileage, price, technical, session["user_id"])
        car_id = db.execute(
            "SELECT car_id FROM cars ORDER BY car_id DESC LIMIT 1")
        car_id1 = car_id[0]['car_id']
        db.execute("INSERT INTO images (img,car_id) VALUES (?,?)",
                   data, car_id1)
        img_id = db.execute(
            "SELECT img_id FROM images ORDER BY img_id DESC LIMIT 1")
        img_id1 = img_id[0]['img_id']

        print('image id =', img_id1)
        print('car id =', car_id1)

        img = db.execute(
            "SELECT img FROM images WHERE car_id=?", car_id1)

        for imm in img:
            data = imm

        # sourceFile = open('output.txt', 'w')
        # print(data, file=sourceFile)
        # sourceFile.close()

        # print(data)

        if not os.path.exists(str(car_id1)):
            os.mkdir('./static/images/'+str(car_id1))

        with open('./static/images/'+str(car_id1)+'/'+str(img_id1)+'.jpg', 'wb') as carimg:
            carimg.write(data['img'])

        # try:
        #     db.execute(
        #         "INSERT INTO images (car_id,img) VALUES(?,?)", car_id, image)
        # except:
        #     return apology("NO FILES FOUND")

        return redirect("/")

    else:
        buyers = db.execute(
            "SELECT * FROM users JOIN (SELECT * FROM cars JOIN requests ON requests.car_id=cars.car_id) AS tt ON tt.buyer_id=users.user_id WHERE seller_id=?", session["user_id"])
        return render_template("addcar.html", form=form, buyers=buyers)


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

    images = db.execute(
        "SELECT * FROM images JOIN (SELECT * FROM users JOIN cars ON cars.seller_id=users.user_id) AS imm ON imm.car_id=images.car_id")
    requests = db.execute("SELECT * FROM requests WHERE buyer_id=?",
                          session["user_id"])

    appreqs = db.execute(
        "SELECT * FROM approved WHERE buyerid=?", session["user_id"])

    buyers = db.execute(
        "SELECT * FROM users JOIN (SELECT * FROM cars JOIN requests ON requests.car_id=cars.car_id) AS tt ON tt.buyer_id=users.user_id WHERE seller_id=?", session["user_id"])

    return render_template("index.html",  username=name[0]["username"], cars=cars, requests=requests, appreqs=appreqs, images=images, buyers=buyers)


if __name__ == "__main__":
    app.run(debug=True)
