from flask import Flask,render_template, redirect, url_for, request, session
import ibm_db
import re
app=Flask(__name__)
app.secret_key='a'


conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=ba99a9e6-d59e-4883-8fc0-d6a8c9f7a08f.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=31321;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=rpv66344;PWD=LauoZiWfAnNnsU6J;",'','')

@app.route('/')
 def home():
 return render_template('reg.html')

 @app.route('/login',methods=["GET","POST"])
 def login():
 global userid
 msg=" "

 if request.method=="POST":
 username = request.form['uname']
 password = request.form['pwd']
 sql = "SELECT * FROM Users WHERE USERNAME=? AND PASSWORD=?"
 stmt = ibm_db.prepare(conn,sql)
 ibm_db.bind_param(stmt,1,username)
 ibm_db.bind_param(stmt,2,password)
 ibm_db.execute(stmt)
 account = ibm_db.fetch_assoc(stmt)
 print(account)
 if account:
 session['loggedin'] = True
 session['id'] = account['USERNAME']
 userid = account["USERNAME"]
 session['username'] = account["USERNAME"]
 msg = 'Logged in successfully!'
 return redirect(url_for('welcome', username=username))
 else: msg = "Incorrect Username/Password"
 return render_template('login.html', msg = msg)
 @app.route('/reg2',methods=["GET","POST"])
 def registration():
 msg = " "

 if request.method=="POST":
 username = request.form['uname']
 email = request.form['email']
 password = request.form['pwd']
 rollno = request.form['rollno']
 sql="SELECT * FROM USERS WHERE USERNAME=?"
 stmt=ibm_db.prepare(conn,sql)
 ibm_db.bind_param(stmt,1,username)
 ibm_db.execute(stmt)
 account = ibm_db.fetch_assoc(stmt)
 print(account)
 if account:
 msg = "Account already exists!"
 elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
 msg = "Invalid Email Address."
 elif not re.match(r'[A-Za-z0-9]+', username):
 msg = "Username must contain only alphabets and numbers."
 else:
 insert_sql = "INSERT INTO USERS VALUES(?,?,?,?)"
 prep_stmt = ibm_db.prepare(conn,insert_sql)
 ibm_db.bind_param(prep_stmt,1,email)
 ibm_db.bind_param(prep_stmt,2,username)
 ibm_db.bind_param(prep_stmt,3,rollno)
 ibm_db.bind_param(prep_stmt,4,password)
 ibm_db.execute(prep_stmt)
 msg = "You have successfully registered."
 return render_template('login.html', msg=msg)

 elif request.method == 'POST': msg="Please fill out the form."
 return render_template('reg.html',msg=msg)

 @app.route('/welcome/<username>')
 def welcome(username):
 return "Welcome %s!" %username

 if __name__=="__main__":
 app.run(host='0.0.0.0')
