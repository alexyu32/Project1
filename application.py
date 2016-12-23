from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import gettempdir
from datetime import datetime
import plotly.plotly as py
import plotly.graph_objs as go

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.route("/")#, methods=["GET", "POST"])
def main():
    
    if request.method == "GET":
        return render_template("main.html")
        
@app.route("/results", methods=["GET", "POST"])
def results():
    
    if request.method == "POST":

        house = request.form.get("houses")
        entryway = request.form.get("entryways")
        room = request.form.get("rooms")
        #retrieve average ratings of dorm
        store = db.execute("SELECT AVG(score) AS score, AVG(size) AS size, AVG(location) AS location, AVG(view) AS view, bedrooms, residents \
            FROM responses WHERE house = :house AND entryway = :entryway AND room = :room", house=house, entryway=entryway, room=room )
        #returns failure if there are no entries for that dorm
        if not store[0]["score"]:
            return render_template("failure.html")
        #retrieve comments for particular dorm
        comments = db.execute("SELECT comments FROM responses WHERE house = :house AND entryway = :entryway AND room = :room", \
            house=house, entryway=entryway, room=room )
        #limit variables to 2 decimals
        score = format(store[0]["score"], '.2f')
        size = format(store[0]["size"], '.2f')
        location = format(store[0]["location"], '.2f')
        view = format(store[0]["view"], '.2f')
        bedrooms = round(store[0]["bedrooms"])
        residents = round(store[0]["residents"])
        #make a temp variable for comments later
        temp = []
        
        #remove blank comments from array
        for i in range (0, len(comments)):
            if not comments[i]["comments"]:
                continue
            else:
                temp.append(comments[i]["comments"])
        comments = temp
        #select images and yard into dictionary
        img = db.execute("SELECT img, yard, description FROM images WHERE house = :house", house=house)
        yard = img[0]["yard"]
        description = img[0]["description"]
        img = img[0]["img"]
        
        
        #return with all the values
        return render_template("results.html", house=house, entryway=entryway, room=room, score=score, size=size, location=location, view=view, comments=comments, \
            img=img, yard=yard, description=description, bedrooms=bedrooms, residents=residents)
    
    elif request.method == "GET":

            
        return render_template("results.html")#, score=store[score]), house=request.form.get("house"), entryway=entryway, room=room)
        
@app.route("/survey", methods=["GET", "POST"])
def survey():
    
    
    if request.method == "GET":
        return render_template("survey.html")

@app.route("/success", methods=["GET", "POST"])
def success():
    
    if request.method == "GET":
        # Show new_post form
        return render_template("success.html")
    
    else:
        
        #ensure forms are filled
        if not request.form.get("house"):
            return render_template("survey.html")
        if not request.form.get("entryway"):
            return render_template("survey.html")
        if not request.form.get("room"):
            return render_template("survey.html")
        if not request.form.get("score"):
            return render_template("survey.html")
        if not request.form.get("size"):
            return render_template("survey.html")
        if not request.form.get("location"):
            return render_template("survey.html")
        if not request.form.get("view"):
            return render_template("survey.html")
        if not request.form.get("bedrooms"):
            return render_template("survey.html")
        if not request.form.get("residents"):
            return render_template("survey.html")
        #define variables
        house = request.form.get("house")
        entryway = request.form.get("entryway")
        room = request.form.get("room")
        score = request.form.get("score")
        size = request.form.get("size")
        location = request.form.get("location")
        view = request.form.get("view")
        comments = request.form.get("comments")
        bedrooms = request.form.get("bedrooms")
        residents = request.form.get("residents")

        
        # Add new post to database
        db.execute("INSERT INTO responses (house, entryway, room, score, size, location, view, comments, bedrooms, residents) \
            VALUES(:house, :entryway, :room, :score, :size, :location, :view, :comments, :bedrooms, :residents)", \
            house=house, entryway=entryway, room=room, score=score, size=size, location=location, view=view, comments=comments, bedrooms=bedrooms, residents=residents)
        return redirect(url_for("success"))



#pip3 install --user -r requirements.txt
#flask run
#phpliteadmin project.db