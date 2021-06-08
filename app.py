# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import pickle

app = Flask(__name__)

model = pickle.load(open('kmeans.pkl', 'rb'))

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'login'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/team')
def team():
    return render_template("team.html")


@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM login WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			return render_template('home.html', msg = msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/predict')
def predict():
    return render_template('predict.html')


@app.route('/result',methods = ['GET','POST'])
def result():
    output = 0
    if request.method == 'POST':
        scomp = 0
        icomp = 0
        in_tec = 0
        in_ntec = 0
        sscp = (float)(request.form['ssc_p'])
        hscp = (float)(request.form['hsc_p'])
        degree = (int)(request.form['degree'])
        degs = (int)(request.form['deg_stream'])
        if degs==1:
            scomp = 1
            icomp = 0
        elif degs==2:
            scomp = 0
            icomp = 1
        else:
            scomp = 0
            icomp = 0
        degp = (float)(request.form['deg_p'])
        interest = (float)(request.form['interest'])
        text = (int)(request.form['textbook'])
        ref = (int)(request.form['refbook'])
        net = (int)(request.form['internet'])
        ds = (int)(request.form['ds'])
        algo = (int)(request.form['algo'])
        oop = (int)(request.form['oop'])
        cn = (int)(request.form['cn'])
        db = (int)(request.form['db'])
        os = (int)(request.form['os'])
        code_p = (int)(request.form['code_pract'])
        code_h = (float)(request.form['code_hrs'])
        compe = (int)(request.form['comp_code'])
        gfg = (int)(request.form['gfg'])
        hrank = (int)(request.form['hrank'])
        hearth = (int)(request.form['hearth'])
        ques = (int)(request.form['code_ques'])
        intern = (int)(request.form['internship'])
        intrn_t = (int)(request.form['intern_type'])
        if intrn_t==1:
            in_tec = 1
            in_ntec = 0
        elif intrn_t == 2:
            in_tec = 0
            in_ntec = 1
        else:
            in_tec = 0
            in_ntec = 0
        course = (int)(request.form['no_course'])
        prediction = model.predict([[sscp,hscp,degree,scomp,icomp,degp,interest,text,ref,net,ds,algo,db,os,oop,cn,code_p,compe,code_h,gfg,hrank,hearth,ques,course,intern,in_ntec,in_tec]])
        output = (prediction[0]+1)
        return render_template('result.html', pred='Competency Level is {}'.format(output))
    
    

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('index'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM login WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		elif not username or not password or not email:
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO login VALUES (NULL, % s, % s, % s)', (username, password, email, ))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)

if __name__=='__main__':
    app.run(debug=True)
    