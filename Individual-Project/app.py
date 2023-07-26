from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

firebaseConfig = {

  "apiKey": "AIzaSyCDa9yRefjrbE_yA5YM5xWn5Rl4WZiCXG8",

  "authDomain": "individual-cs-project-60727.firebaseapp.com",

  "databaseURL": "https://individual-cs-project-60727-default-rtdb.europe-west1.firebasedatabase.app",

  "projectId": "individual-cs-project-60727",

  "storageBucket": "individual-cs-project-60727.appspot.com",

  "messagingSenderId": "156668857907",

  "appId": "1:156668857907:web:7c841de09a8a0cf3671d46",

  "measurementId": "G-Y8SX4GKMWN"

}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        


        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {'email': email, 'firstname': firstname, 'lastname': lastname, 'username': username, 'num_lebrons': 0}
            db.child("Users").child(UID).set(user)

            return redirect(url_for('signin'))

        except Exception as e:
            print("SIGN UP ERRORRRRRR", e)
            error = "Authentication failed"
    return render_template("signup.html")



@app.route('/signin', methods=['GET', 'POST'])
def signin():
   error = ""
   if request.method == 'POST':
       print('posted')
       email = request.form['email']
       password = request.form['password']
       try:
           login_session['user'] = auth.sign_in_with_email_and_password(email, password)
           print('signed in')
           return redirect(url_for('home'))
       except Exception as e:
            print(e)
            error = "Authentication failed"
   return render_template("signin.html")






@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@app.route('/mainpage', methods=['GET', 'POST'],)
def lepage():
     lebrons={

     }
     if 'user' in login_session and login_session['user'] is not None:
        
        # return render_template("lepage.html")
        try:
            UID = login_session['user']['localId']
            
            
            lebrons = db.child("Users").child(UID).get().val()['num_lebrons']
            if request.method=='GET':

                return render_template("lepage.html", lebrons=lebrons)
            else:
                db.child("Users").child(UID).update({'num_lebrons': lebrons + 1})
                return render_template("lepage.html", lebrons=(lebrons + 1))
        except:
            error = "upload failed"
     else:
        return redirect(url_for('home'))
    



@app.route('/mainpage', methods=['GET', 'POST'])
def addlebron():
    if request.method == 'POST':
        try:
           

            db.child("LeBrons").push(lebron)
        except:
            error = "Authentication failed"




    return render_template('lepage')



if __name__ == '__main__':
    app.run(debug=True)