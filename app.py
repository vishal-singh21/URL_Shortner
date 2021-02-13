from flask import Flask, render_template, request, redirect,session
from mysql.connector import connect
import random
import string
from flask_mail import Mail, Message
app = Flask(__name__)
mail=Mail(app)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='vishalmarch21@gmail.com',
    MAIL_PASSWORD='Vishal21397@'
)
app.secret_key='229198112'


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/<url>')
def dynamicUrl(url):
    connection = connect(host="localhost", database="student", user="root", password="2219")
    cur = connection.cursor()
    query1 = "select * from urlinfo where encryptedUrl='{}'".format(url)
    cur.execute(query1)
    orignalurl = cur.fetchone()
    if orignalurl == None:
        return render_template('index.html')
    print(orignalurl[1])
    return redirect(orignalurl[1])


@app.route('/urlshortner')
def urlshortner():
    # letter='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    url = request.args.get('link')
    custom = request.args.get('customurl')
    print(custom)
    print('planet tech')
    connection = connect(host="localhost", database="student", user="root", password="2219")
    cur = connection.cursor()
    encryptedurl = ''
    if custom == '':
        while True:
            encryptedurl = createEncrytedUrl()
            query1 = "select * from urlinfo where encryptedUrl='{}'".format(encryptedurl)
            cur.execute(query1)
            xyz = cur.fetchone()
            if xyz == None:
                break
        print(encryptedurl)
        if 'userid' in session:
            id = session['userid']
            query = "insert into urlinfo(orignalUrl,encryptedUrl,is_Active,created_by) values('{}','{}',1,{})".format(url, encryptedurl, id)
        else:
            query = "insert into urlinfo(orignalUrl,encryptedUrl,is_Active) values('{}','{}',1)".format(url,encryptedurl)
        cur = connection.cursor()
        cur.execute(query)
        connection.commit()
        finalencryptedurl = 'sd.in/' + encryptedurl
    else:
        query1 = "select * from urlinfo where encryptedUrl='{}'".format(custom)
        cur.execute(query1)
        xyz = cur.fetchone()
        if xyz == None:
            if 'userid' in session:
                id = session['userid']
                query = "insert into urlinfo(orignalUrl,encryptedUrl,is_Active,created_by) values('{}','{}',1,{})".format(url, custom, id)
            else:
                query = "insert into urlinfo(orignalUrl,encryptedUrl,is_Active) values('{}','{}',1)".format(url, custom,1)
            cur = connection.cursor()
            cur.execute(query)
            connection.commit()
            finalencryptedurl = 'sd.in/' + custom
        else:
            return ('url already exist')
    return render_template('index.html', finalencryptedurl=finalencryptedurl, url=url)


@app.route('/registration')
def registration():
    return render_template('registration.html')


@app.route('/signup')
def signup():
    firstname = request.args.get('first_name')
    lastname = request.args.get('last_name')
    email = request.args.get('email')
    password = request.args.get('password')
    print(firstname)
    connection=connect(host='localhost',database='student',user='root',password='2219')
    cur=connection.cursor()
    print(lastname)
    query="select email from registration where email='{}'".format(email)
    cur.execute(query)
    result=cur.fetchone()
    if result==None:
        query = "insert into registration values('{}','{}','{}','{}')".format(firstname,lastname,email,password)
        cur=connection.cursor()
        cur.execute(query)
        connection.commit()
        return render_template('login.html',login='successfully login')

    else:
        return render_template('login.html',login='use are already registered')

@app.route('/login')
def googlelogin():
    return render_template('login.html')

@app.route('/checkLoginIn')
def checkLoginIn():
    email=request.args.get('email')
    password=request.args.get('password')
    connection = connect(host="localhost", database="student", user="root", password="2219")
    cur = connection.cursor()
    query1 = "select * from registration where email='{}'".format(email)
    cur.execute(query1)
    xyz = cur.fetchone()
    print(xyz)
    if xyz==None:
        return render_template('login.html',xyz='please enter valid email id')
    else:
        if password==xyz[4]:
            session['email']=email
            session['userid']=xyz[0]
            return redirect('/home')
        else:
            return render_template('Login.html', xyz='your password is not correct')


@app.route('/home')
def home():
    if 'userid' in session:
        email=session['email']
        id=session['userid']
        print(id)
        connection = connect(host="localhost", database="student", user="root", password="2219")
        cur=connection.cursor()
        query="select * from urlinfo where createdBy='{}'".format(id)
        cur.execute(query)
        data=cur.fetchall()
        return render_template('UserHome.html', data=data)
    else:
        return render_template('login.html')

@app.route('/mailbhejo')
def mailbhejo():
    msg = Message(subject='mail sender', sender='vishalmarch21@gmail.com',
                  recipients=['deus21397@gmail.com'], body=
                  "This is my first email through python")
    mail.cc('vishalmarch21397@gmail.com')
    msg.html=render_template('index.html')
    mail.send(msg)
    return 'msg sent'


@app.route('/logout')
def logout():
    session.pop('userid',None)
    print('logout')
    return render_template('login.html')

@app.route('/edit')
def editurl():
    if 'userid' in session:
        email=session['email']
        print(email)
        id=request.args.get('id')
        url=request.args.get('originalurl')
        encrypted=request.args.get('encryptedurl')
        print(id,url,encrypted)
    return render_template('login.html')


@app.route('/updateUrl')
def updateUrl():
    id=request.args.get('id')
    url=request.args.get('originalurl')
    encrypted=request.args.get('encrypted')
    print(id,url,encrypted)
    connection = connect(host="localhost", database="student", user="root", password="2219")
    cur=connection.cursor()
    query="select * from  urlinfo where encryptedUrl='{}' and pk_urlId!='{}'".format(encrypted,id)
    cur.execute(query)
    xyz=cur.fetchone()
    if xyz==None:
        query1="update urlinfo set originalurl='{}', encryptedUrl='{}' where pk_urlId='{}'".format(url,encrypted,id)
        cur.execute(query1)
        connection.commit()
        return redirect('/home')
    else:
        return render_template('editurl.html',url=url,encrypted=encrypted,id=id,error='short url already exist')

    return render_template('UserHome.html',id=id,url=url,encrypted=encrypted)

@app.route('/deleteUrl')
def deleteUrl():
    if 'userid' in session:
        email = session['email']
        id = session['userid']
        id=request.args.gāet('id')
        print(id)
        connection = connect(host="localhost", database="student", user="root", password="2219")
        cur=connection.cursor()
        query="delete  from urlinfo where pk_urlId='{}'".format(id)
        cur.execute(query)
        connection.commit()
        return render_template('/UserHome.html')
    else:
        return render_template('/login.html')


def createEncrytedUrl():
    letter = string.ascii_letters + string.digits
    encryptedurl = ''
    for i in range(6):
        encryptedurl = encryptedurl + ''.join(random.choice(letter))
    print(encryptedurl)
    return encryptedurl


if __name__ == "__main__":
    app.run()
#to send any mail we need
#MAIL_SERVER=smtp.gmail.com(where aur server will run)
#port no Mail_PORT=456
#MAIL_USE_SSL=True
#mail username from which mail we are sending MAIL_USERNAME=''
#password MAIL_PASSWORD=''
#and SSL(secure socket layer) these all configured in flask object