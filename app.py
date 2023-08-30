from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Hello_Munatsir"
 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

# permanent session 5 min ar jonno store rakhbe
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

#For Users Class
class users(db.Model):
    _id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email





#For Home Page

@app.route("/")
def home():
    return render_template("index.html")

#For Log In Page
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True # for session permanent
        user = request.form["nme"]
        session["user"] = user

        found_user = users.query.filter_by(name = user).first() # user a jei name ashby sei name session a ase kinh thkly oi info return korbe
        if found_user:
            session['email'] = found_user.email 
        else:
            usr = users(user, "") 
            db.session.add(usr) #add the info in the session
            db.session.commit() #save the change in the DB



        flash("Logged In Successfull!!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already logged in!!")
            return redirect(url_for("user"))
        
        return render_template("login.html")

#For User Page
@app.route("/user", methods = ["POST" , "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]# get email form form of user.html file
            session['email'] = email

            found_user = users.query.filter_by(name = user).first()
            found_user.email = email
            flash("Email was saved successfully!!")
        else:
            if email in session:
                email = session['email'] #for get the email value form the session  

        
        return render_template("user.html", email = email)
    else:
        flash("You are not logged in")
        return redirect(url_for("login"))


#For Log Out Page
@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"You have been logged Out!!, {user}", "info")
    session.pop("user", None)# scession a user dictionary ar value remove korbe
    session.pop("email",None)
    return redirect(url_for("login"))



if __name__ == "__main__":
    #database jei name call dewa hoise oi name na thkly new create kore info oity save hby
    db.create_all() 
    app.run(debug=True)

