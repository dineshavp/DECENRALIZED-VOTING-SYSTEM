from flask import Flask, render_template, flash, request, session
from flask import render_template, redirect, url_for, request
#from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
#from werkzeug.utils import secure_filename


import mysql.connector
import sys, fsdk, math, ctypes, time
import datetime
app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'



@app.route("/")
def homepage():
    return render_template('index.html')
@app.route("/Home")
def Home():
    return render_template('index.html')


@app.route("/AdminLogin")
def AdminLogin():
    return render_template('AdminLogin.html')

@app.route("/UserLogin")
def UserLogin():
    return render_template('UserLogin.html')


@app.route("/NewCandidate")
def NewCandidate():
    return render_template('NewCandidate.html')



@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    error = None
    if request.method == 'POST':
       if request.form['uname'] == 'admin' or request.form['password'] == 'admin':
           conn = mysql.connector.connect(user='root', password='', host='localhost', database='1facevotedb')
           cursor = conn.cursor()
           cur = conn.cursor()
           cur.execute("SELECT * FROM regtb")
           data = cur.fetchall()
           return render_template('AdminHome.html', data=data)

       else:
        return render_template('index.html', error=error)

@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1facevotedb')

    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb")
    data = cur.fetchall()
    return render_template('AdminHome.html', data=data)



@app.route("/candidate",methods=['GET','POST'])
def candidate():
    if request.method == 'POST':
        name=request.form['name']
        area=request.form['pcode']
        pname = request.form['pname']
        f = request.files['file']
        f.save("static/upload/" + f.filename)
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1facevotedb')
        cursor = conn.cursor()
        cursor.execute("insert into cantb value('','"+name+"','"+area+"','"+pname+"','"+f.filename+"')")
        conn.commit()
        conn.close()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1facevotedb')

        cur = conn.cursor()
        cur.execute("SELECT * FROM cantb")
        data = cur.fetchall()
        return render_template('AdminCanInfo.html', data=data)





@app.route("/uremove")
def uremove():


    did =  request.args.get('did')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1facevotedb')
    cursor = conn.cursor()
    cursor.execute("delete from regtb  where VoterId='"+ did +"' ")
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1facevotedb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb ")
    data = cur.fetchall()

    return render_template('AdminHome.html', data=data)

@app.route("/remove")
def remove():


    did =  request.args.get('did')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1facevotedb')
    cursor = conn.cursor()
    cursor.execute("delete from cantb  where Id='"+ did +"' ")
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1facevotedb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cantb ")
    data = cur.fetchall()

    return render_template('AdminCanInfo.html', data=data)




@app.route("/AdminCanInfo")
def AdminCanInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1facevotedb')

    cur = conn.cursor()
    cur.execute("SELECT * FROM cantb")
    data = cur.fetchall()
    return render_template('AdminCanInfo.html', data=data)


@app.route("/AdminVoteInfo")
def AdminVoteInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1facevotedb')

    cur = conn.cursor()
    cur.execute("SELECT * FROM votedtb")
    data = cur.fetchall()
    return render_template('AdminVoteInfo.html', data=data)



@app.route("/NewUser")
def NewUser():
    import LiveRecognition  as liv

    liv.att()
    del sys.modules["LiveRecognition"]
    return render_template('NewUser.html')



@app.route("/newuser", methods=['GET', 'POST'])
def NewStudent1():
     if request.method == 'POST':
          uname = request.form['uname']
          fname = request.form['fname']
          gender = request.form['gender']
          Age = request.form['Age']
          email = request.form['email']
          pnumber = request.form['pnumber']
          address = request.form['address']
          vid = request.form['vid']
          aid = request.form['aid']

          conn = mysql.connector.connect(user='root', password='', host='localhost', database='1facevotedb')
          cursor = conn.cursor()
          cursor.execute("insert into regtb values('"+uname+"','"+fname+"','"+gender+"','"+Age+"','"+email+"','"+pnumber+"','"+address +"','"+vid+"','"+aid+"')")
          conn.commit()
          conn.close()

     conn = mysql.connector.connect(user='root', password='', host='localhost', database='1facevotedb')

     cur = conn.cursor()
     cur.execute("SELECT * FROM regtb")
     data = cur.fetchall()



     return render_template("AdminHome.html" , data =data)








@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():

    if request.method == 'POST':
        vid = request.form['vid']

        session['vid'] = vid

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1facevotedb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where VoterId='" + vid + "' ")
        data = cursor.fetchone()
        if data is None:

            alert = 'Username or Password is wrong'
            return render_template('goback.html', data=alert)



        else:
            print(data[0])
            session['vid']  = data[7]

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1facevotedb')
            cursor = conn.cursor()
            cursor.execute("truncate table temptb")
            conn.commit()
            conn.close()


            import LiveRecognition1  as liv1
            del sys.modules["LiveRecognition1"]


            return Vote()

            #return render_template('OTP.html', data=data )









def examvales1():

    vid= session['vid']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1facevotedb')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM regtb where  VoterId='" + vid + "'")
    data = cursor.fetchone()

    if data:
        Email = data[4]
        Phone = data[5]


    else:
        return 'Incorrect username / password !'

    return vid,Email,Phone





@app.route("/Vote")
def Vote():


    vid = session['vid']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1facevotedb')
    cursor = conn.cursor()
    cursor.execute("SELECT * from temptb where UserName='" + vid + "' ")
    data = cursor.fetchone()
    if data is None:

        alert = 'Face  is wrong'
        return render_template('goback.html', data=alert)



    else:

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1facevotedb')

        cur = conn.cursor()
        cur.execute("SELECT * FROM cantb")
        data = cur.fetchall()


        return render_template('OTP.html', data=data)



@app.route("/otp", methods=['GET', 'POST'])
def otp():

    if request.method == 'POST':
        otp = request.form['vid']

        #session['vid'] = vid

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1facevotedb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from temptb where Status='" + otp + "' ")
        data = cursor.fetchone()
        if data is None:

            alert = 'OTP Incorrect'
            render_template('goback.html', data=alert)



        else:



            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1facevotedb')

            cur = conn.cursor()
            cur.execute("SELECT * FROM cantb")
            data = cur.fetchall()



            return render_template('Vote.html', data=data )



import hmac
import hashlib
import binascii
import random

def create_sha256_signature(key, message):
    byte_key = binascii.unhexlify(key)
    message = message.encode()
    return hmac.new(byte_key, message, hashlib.sha256).hexdigest().upper()

@app.route("/uvote")
def uvote():


    did =  request.args.get('did')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1facevotedb')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM cantb where  id='" + did + "'")
    data = cursor.fetchone()

    if data:
        PartCode = data[3]
        image = data[4]



    else:
        return 'Incorrect username / password !'


    vid = session['vid']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1facevotedb')
    cursor = conn.cursor()
    cursor.execute("SELECT * from votedtb where VoterId='" + vid + "' ")
    data = cursor.fetchone()
    if data is None:

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1facevotedb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM votedtb ")
        data = cursor.fetchone()

        if data:

            conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='1facevotedb')
            cursor1 = conn1.cursor()
            cursor1.execute("select max(id) from votedtb")
            da = cursor1.fetchone()
            if da:
                d = da[0]
                print(d)

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1facevotedb')
            cursor = conn.cursor()
            cursor.execute("SELECT  *  FROM votedtb where  id ='" + str(d) + "'   ")
            data = cursor.fetchone()
            if data:
                hash1 = data[6]
                num1 = random.randrange(1111, 9999)
                hash2 = create_sha256_signature("E49756B4C8FAB4E48222A3E7F3B97CC3", str(num1))

                conn = mysql.connector.connect(user='root', password='', host='localhost', database='1facevotedb')
                cursor = conn.cursor()
                cursor.execute("insert into votedtb value('','" + vid + "','" + PartCode + "','" + image + "','1','"+ hash1+"','"+hash2+"')")
                conn.commit()
                conn.close()

                alert = 'Vote Completed!'
                return render_template('goback.html', data=alert)

        else:

            hash1 = '0'
            num1 = random.randrange(1111, 9999)
            hash2 = create_sha256_signature("E49756B4C8FAB4E48222A3E7F3B97CC3", str(num1))

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1facevotedb')
            cursor = conn.cursor()
            cursor.execute(
                "insert into votedtb value('','" + vid + "','" + PartCode + "','" + image + "','1','" + hash1 + "','" + hash2 + "')")
            conn.commit()
            conn.close()

            alert = 'Vote Completed!'
            return render_template('goback.html', data=alert)







    else:

        alert = 'Already Vote this User'
        return render_template('goback.html', data=alert)





def sendmsg(targetno,message):
    import requests
    requests.post("http://smsserver9.creativepoint.in/api.php?username=fantasy&password=596692&to=" + targetno + "&from=FSSMSS&message=Dear user  your msg is " + message + " Sent By FSMSG FSSMSS&PEID=1501563800000030506&templateid=1507162882948811640")



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)