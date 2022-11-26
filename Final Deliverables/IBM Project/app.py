from flask import Flask,render_template, redirect, request, session
import ibm_db, re
import smtplib
import sendgrid
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
#SUBJECT = "Interview Call"
#s = smtplib.SMTP('smtp.gmail.com', 587)

app=Flask(__name__)
app.secret_key='a'

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=ba99a9e6-d59e-4883-8fc0-d6a8c9f7a08f.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=31321;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=rpv66344;PWD=LauoZiWfAnNnsU6J;",'','')


#app.config['SECRET_KEY'] = 'top-secret!'
#app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
#app.config['MAIL_PORT'] = 587
#app.config['MAIL_USE_TLS'] = True
#app.config['MAIL_USERNAME'] = 'apikey'
#app.config['MAIL_PASSWORD'] = os.environ.get('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')
#app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('imbskillsandjob@gmail.com')
#mail = Mail(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/learning_module',methods=["GET","POST"])
def learning_module():
    return render_template('learning_module.html')

@app.route('/applicants_list',methods=["GET","POST"])
def applicants_list():
    return render_template('applicants_list.html')

@app.route('/rec_domain',methods=["GET","POST"])
def rec_domain():
    return render_template('rec_domain.html')

@app.route('/applicant_domain',methods=["GET","POST"])
def applicant_domain():
    return render_template('applicant_domain.html')

@app.route('/ds_job_list',methods=["GET","POST"])
def ds_job_list():
    return render_template('ds_job_list.html')

@app.route('/java_job_list',methods=["GET","POST"])
def java_job_list():
    return render_template('java_job_list.html')

@app.route('/web_dev_job_list',methods=["GET","POST"])
def web_dev_job_list():
    return render_template('web_dev_job_list.html')

@app.route('/ai_job_list',methods=["GET","POST"])
def ai_job_list():
    return render_template('ai_job_list.html')
    
@app.route('/Login',methods=["GET","POST"])
def login():
    global userid
    msg=" "
    
    if request.method=="POST":
        username = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM APPLICANT WHERE EMAIL=? AND PASSWORD=?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if(account):
            session['loggedin'] = True
            session['id'] = account['EMAIL']
            userid = account["EMAIL"]
            session['username'] = account["EMAIL"]
            msg = 'Logged in successfully!'
            return render_template("applicant_domain.html", msg = msg)
        else: msg = "Incorrect Username/Password"
    return render_template('login.html', msg = msg)

@app.route('/register',methods=["GET","POST"])
def register():
    msg = " "
    
    if request.method=="POST":
        photo = request.form['photo']
        fname = request.form['fname']
        lname = request.form['lname']
        dob = request.form['dob']
        gender = request.form['gender']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        address = request.form['address']
        resume = request.form['resume']
        highest_qual = request.form['highest_qual']
        degree = request.form['degree']
        branch = request.form['branch']
        tenth = request.form['tenth']
        twelfth = request.form['twelfth']
        ug_cgpa = request.form['ug_cgpa']
        ug_percent = request.form['ug_percent']
        diploma = request.form['diploma']
        skillset = request.form['skillset']
        
        sql="SELECT * FROM APPLICANT WHERE EMAIL=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = "Account already exists!"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = "Invalid Email Address."
        else:
            insert_sql = "INSERT INTO APPLICANT VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn,insert_sql)
            ibm_db.bind_param(prep_stmt,1,photo)
            ibm_db.bind_param(prep_stmt,2,fname)
            ibm_db.bind_param(prep_stmt,3,lname)
            ibm_db.bind_param(prep_stmt,4,dob)
            ibm_db.bind_param(prep_stmt,5,gender)
            ibm_db.bind_param(prep_stmt,6,email)
            ibm_db.bind_param(prep_stmt,7,password)
            ibm_db.bind_param(prep_stmt,8,phone)
            ibm_db.bind_param(prep_stmt,9,address)
            ibm_db.bind_param(prep_stmt,10,resume)
            ibm_db.bind_param(prep_stmt,11,highest_qual)
            ibm_db.bind_param(prep_stmt,12,degree)
            ibm_db.bind_param(prep_stmt,13,branch)
            ibm_db.bind_param(prep_stmt,14,tenth)
            ibm_db.bind_param(prep_stmt,15,twelfth)
            ibm_db.bind_param(prep_stmt,16,ug_cgpa)
            ibm_db.bind_param(prep_stmt,17,ug_percent)
            ibm_db.bind_param(prep_stmt,18,diploma)
            ibm_db.bind_param(prep_stmt,19,skillset)
            
            ibm_db.execute(prep_stmt)
            msg = "You have successfully registered."
 #           to_email = To(email)
#            sendgridmail(to_email,password)

            try:
                sg = sendgrid.SendGridAPIClient('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')
            # Change to your verified sender
                from_email = Email("ploganayagi2002@gmail.com")
                to_email = To(email)  # Change to your recipient
                subject = "Registration Success"
                htmlcontent = "Congratulations on registering at ADDK Job Finders! Here are your login credentials:\n Username: "+email+"\nPassword: "+password
                content = Content("text/plain", htmlcontent)
                mail = Mail(from_email, to_email, subject, content)
            # Get a JSON-ready representation of the Mail object
                mail_json = mail.get()
            # Send an HTTP POST request to /mail/send
                response = sg.client.mail.send.post(request_body=mail_json)
                print(response.status_code)
                return render_template('home.html', msg=msg) 
            except Exception as e:
                print(e)   
        
    elif request.method == 'POST': msg="Please fill out the form."
    return render_template('register.html')

@app.route('/rec_login',methods=["GET","POST"])
def rec_login():
    global userid
    msg=" "
    
    if request.method=="POST":
        username = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM RECRUITER_INFO WHERE PERS_EMAIL=? AND PASSWORD=?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if(account):
            session['loggedin'] = True
            session['id'] = account['PERS_EMAIL']
            userid = account["PERS_EMAIL"]
            session['username'] = account["PERS_EMAIL"]
            msg = 'Logged in successfully!'
            return render_template("rec_domain.html", msg = msg)
        else: msg = "Incorrect Username/Password"
    return render_template('rec_login.html', msg = msg)

@app.route('/rec_register',methods=["GET","POST"])
def rec_register():
    msg = " "
    
    if request.method=="POST":
        fname = request.form['fname']
        lname = request.form['lname']
        dob = request.form['dob']
        gender = request.form['gender']
        pers_email = request.form['pers_email']
        password = request.form['password']
        phone = request.form['ph_no']
        address = request.form['address']
        comp_name = request.form['comp_name']
        designation = request.form['designation']
        experience = request.form['experience']
        location = request.form['location']
        highest_qual = request.form['highest_qual']
        work_email = request.form['work_email']
        expert_area = request.form['expert_area']
        comp_exp = request.form['comp_exp']
        
        sql="SELECT * FROM RECRUITER_INFO WHERE PERS_EMAIL=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,pers_email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = "Account already exists!"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', pers_email):
            msg = "Invalid Email Address."
        else:
            insert_sql = "INSERT INTO RECRUITER_INFO VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn,insert_sql)
            ibm_db.bind_param(prep_stmt,1,fname)
            ibm_db.bind_param(prep_stmt,2,lname)
            ibm_db.bind_param(prep_stmt,3,dob)
            ibm_db.bind_param(prep_stmt,4,gender)
            ibm_db.bind_param(prep_stmt,5,pers_email)
            ibm_db.bind_param(prep_stmt,6,password)
            ibm_db.bind_param(prep_stmt,7,phone)
            ibm_db.bind_param(prep_stmt,8,address)
            ibm_db.bind_param(prep_stmt,9,comp_name)
            ibm_db.bind_param(prep_stmt,10,designation)
            ibm_db.bind_param(prep_stmt,11,experience)
            ibm_db.bind_param(prep_stmt,12,location)
            ibm_db.bind_param(prep_stmt,13,highest_qual)
            ibm_db.bind_param(prep_stmt,14,work_email)
            ibm_db.bind_param(prep_stmt,15,expert_area)
            ibm_db.bind_param(prep_stmt,16,comp_exp)
            
            ibm_db.execute(prep_stmt)
            
            try:
                sg = sendgrid.SendGridAPIClient('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')
            # Change to your verified sender
                from_email = Email("ploganayagi2002@gmail.com")
                to_email = To(pers_email)  # Change to your recipient
                subject = "Registration Success"
                htmlcontent = "Congratulations on registering at ADDK Job Finders! Here are your login credentials:\n Username: "+pers_email+"\nPassword: "+password
                content = Content("text/plain", htmlcontent)
                mail = Mail(from_email, to_email, subject, content)
            # Get a JSON-ready representation of the Mail object
                mail_json = mail.get()
            # Send an HTTP POST request to /mail/send
                response = sg.client.mail.send.post(request_body=mail_json)
                print(response.status_code)
            except Exception as e:
                print(e)
            return render_template('home.html')
    
    elif request.method == 'POST': msg="Please fill out the form."
    return render_template('rec_register.html')
    

@app.route('/ai_post',methods=["GET","POST"])
def ai_post_job():
    msg = " "
    
    if request.method=="POST":
        comp_name = request.form['comp_name']
        position = request.form['position']
        location = request.form['location']
        degree = request.form['degree']
        job_type = request.form['job_type']
        tech_area = request.form['tech_area']
        experience = request.form['experience']
        job_desc = request.form['job_desc']
        
        sql="INSERT INTO AI_JOBS VALUES(?,?,?,?,?,?,?,?)"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,comp_name)
        ibm_db.bind_param(stmt,2,position)
        ibm_db.bind_param(stmt,3,location)
        ibm_db.bind_param(stmt,4,degree)
        ibm_db.bind_param(stmt,5,job_type)
        ibm_db.bind_param(stmt,6,tech_area)
        ibm_db.bind_param(stmt,7,experience)
        ibm_db.bind_param(stmt,8,job_desc)
        
        ibm_db.execute(stmt)
        msg='You have successfully created a job posting!'
        return render_template('rec_domain.html',msg=msg)

    elif request.method == 'POST': msg="Please fill out the form."
    return render_template('ai_post.html')

@app.route('/ds_post',methods=["GET","POST"])
def ds_post_job():
    msg = " "
    
    if request.method=="POST":
        comp_name = request.form['comp_name']
        position = request.form['position']
        location = request.form['location']
        degree = request.form['degree']
        job_type = request.form['job_type']
        tech_area = request.form['tech_area']
        experience = request.form['experience']
        job_desc = request.form['job_desc']
        
        sql="INSERT INTO DATA_SCI_JOBS VALUES(?,?,?,?,?,?,?,?)"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,comp_name)
        ibm_db.bind_param(stmt,2,position)
        ibm_db.bind_param(stmt,3,location)
        ibm_db.bind_param(stmt,4,degree)
        ibm_db.bind_param(stmt,5,job_type)
        ibm_db.bind_param(stmt,6,tech_area)
        ibm_db.bind_param(stmt,7,experience)
        ibm_db.bind_param(stmt,8,job_desc)
        ibm_db.execute(stmt)
#        account = ibm_db.fetch_assoc(stmt)
        return render_template('rec_domain.html')

    elif request.method == 'POST': msg="Please fill out the form."
    return render_template('ds_post.html')

@app.route('/java_post',methods=["GET","POST"])
def java_post_job():
    msg = " "
    
    if request.method=="POST":
        comp_name = request.form['comp_name']
        position = request.form['position']
        location = request.form['location']
        degree = request.form['degree']
        job_type = request.form['job_type']
        tech_area = request.form['tech_area']
        experience = request.form['experience']
        job_desc = request.form['job_desc']
        
        sql="INSERT INTO FULLSTACK_JOBS VALUES(?,?,?,?,?,?,?,?)"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,comp_name)
        ibm_db.bind_param(stmt,2,position)
        ibm_db.bind_param(stmt,3,location)
        ibm_db.bind_param(stmt,4,degree)
        ibm_db.bind_param(stmt,5,job_type)
        ibm_db.bind_param(stmt,6,tech_area)
        ibm_db.bind_param(stmt,7,experience)
        ibm_db.bind_param(stmt,8,job_desc)
        ibm_db.execute(stmt)
#        account = ibm_db.fetch_assoc(stmt)
        return render_template('rec_domain.html')

    elif request.method == 'POST': msg="Please fill out the form."
    return render_template('java_post.html')

@app.route('/web_dev_post',methods=["GET","POST"])
def web_dev_post_job():
    msg = " "
    
    if request.method=="POST":
        comp_name = request.form['comp_name']
        position = request.form['position']
        location = request.form['location']
        degree = request.form['degree']
        job_type = request.form['job_type']
        tech_area = request.form['tech_area']
        experience = request.form['experience']
        job_desc = request.form['job_desc']
        
        sql="INSERT INTO WEB_DEV_JOBS VALUES(?,?,?,?,?,?,?,?)"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,comp_name)
        ibm_db.bind_param(stmt,2,position)
        ibm_db.bind_param(stmt,3,location)
        ibm_db.bind_param(stmt,4,degree)
        ibm_db.bind_param(stmt,5,job_type)
        ibm_db.bind_param(stmt,6,tech_area)
        ibm_db.bind_param(stmt,7,experience)
        ibm_db.bind_param(stmt,8,job_desc)
        ibm_db.execute(stmt)
        # account = ibm_db.fetch_assoc(stmt)
        return render_template('rec_domain.html')

    elif request.method == 'POST': msg="Please fill out the form."
    return render_template('web_dev_post.html')

@app.route('/apply',methods=["GET","POST"])
def apply_job():
    msg = " "
    
    if request.method=="POST":
        fname = request.form['fname']
        lname = request.form['lname']
        degree = request.form['degree']
        branch = request.form['branch']
        tenth = request.form['tenth']
        twelfth = request.form['twelfth']
        domain = request.form['domain']
        ug_percent = request.form['ug_percent']
        email = request.form['email']
        phone = request.form['phone']
        resume = request.form['resume']
        comp_name = request.form['comp_name']
        position = request.form['position']
        
        sql="INSERT INTO APPLY_JOBS VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,fname)
        ibm_db.bind_param(stmt,2,lname)
        ibm_db.bind_param(stmt,3,degree)
        ibm_db.bind_param(stmt,4,branch)
        ibm_db.bind_param(stmt,5,tenth)
        ibm_db.bind_param(stmt,6,twelfth)
        ibm_db.bind_param(stmt,7,domain)
        ibm_db.bind_param(stmt,8,ug_percent)
        ibm_db.bind_param(stmt,9,email)
        ibm_db.bind_param(stmt,10,phone)
        ibm_db.bind_param(stmt,11,resume)
        ibm_db.bind_param(stmt,12,comp_name)
        ibm_db.bind_param(stmt,13,position)
        
        ibm_db.execute(stmt)
        msg='You have successfully applied!'
        return render_template('applicant_domain.html',msg=msg)

    elif request.method == 'POST': msg="Please fill out the form."
    return render_template('apply.html')

if __name__=="__main__":
    app.run(debug=True)

