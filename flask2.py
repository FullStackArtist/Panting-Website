from flask import Flask, render_template, request,jsonify
import datetime as dt
import urllib.request
import snowflake.connector
import json
import os
import pickle
from flask import *  

import base64
from werkzeug.utils import secure_filename
from mainfile.emailsend import*

app = Flask(__name__)
app.config['UPLOAD_FOLDER']="C:\\python_codes\\upload_location"
app.secret_key = "##$$||$$##"  

@app.route("/",methods=["POST","GET"])
def main():
    return render_template("Login.html")

@app.route("/userdetails",methods=["POST","GET"])
def userdetails():
    
    va="userdetails"
    conn = snowflake.connector.connect(
                user = 'Epsilon',
                password = "notApainting01",
                account="bp14989.canada-central.azure",
                warehouse="COMPUTE_WH",
                role='SYSADMIN',
                database="ART",
                schema="ART_Table"
                )

    curs=conn.cursor()
    try:
        curs.execute("select * from Login")
        data = curs.fetchall()
        return render_template("Admin.html",data=data,va=va)
    
    finally:
        curs.close()
    conn.close()


@app.route("/requestwork",methods=["POST","GET"])
def requestwork():
    
    va="requestwork"
    conn = snowflake.connector.connect(
                user = 'Epsilon',
                password = "notApainting01",
                account="bp14989.canada-central.azure",
                warehouse="COMPUTE_WH",
                role='SYSADMIN',
                database="ART",
                schema="ART_Table"
                )

    curs=conn.cursor()
    try:
        curs.execute("select * from form_data")
        udata = curs.fetchall()
        return render_template("Admin.html",udata=udata,va=va)
    
    finally:
        curs.close()
    conn.close()
    
    

@app.route("/signup",methods=["POST","GET"])
def signup():
    title="Thanks You"
    full_name=request.form.get("full_name")
    gmail=request.form.get("email")
    password=request.form.get("password")
    phone_number=request.form.get("phone_number")
    status='user'

    if not full_name or not gmail or not password or not phone_number:
        error_statement="All filed required"
        print(full_name,gmail,password,phone_number)
        return render_template("login.html",error_statement=error_statement,full_name=full_name,gmail=gmail,phone_number=phone_number,password=password)
    #es=emailsend()
    #msg=es.sent(full_name,address,email,descrption,phone_number)
    conn = snowflake.connector.connect(
                user = 'Epsilon',
                password = "notApainting01",
                account="bp14989.canada-central.azure",
                warehouse="COMPUTE_WH",
                role='SYSADMIN',
                database="ART",
                schema="ART_Table"
                )

    curs=conn.cursor()
    try:
        curs.execute("insert into signup (full_name,email,password,phone_number,status) values (%s,%s,%s,%s,%s) ", (full_name,gmail,password,phone_number,status))

    finally:
        curs.close()
    conn.close()
    
    return render_template("Thanks.html",title=title)
  

@app.route("/login",methods=["POST","GET"])
def login():
    user=request.form.get("email")
    pas=request.form.get("password")
    conn = snowflake.connector.connect(
                user = 'Epsilon',
                password = "notApainting01",
                account="bp14989.canada-central.azure",
                warehouse="COMPUTE_WH",
                role='SYSADMIN',
                database="ART",
                schema="ART_Table"
                )

    curs=conn.cursor()
    try:
        curs.execute("select * from Login where email='"+user+"'")
        data = curs.fetchall()
        for data in data:
            if data[1]==pas and data[2]=='admin':
                return render_template("admin.html",data=data)
            elif data[1]==pas and data[2]=="user":
                return render_template("index.html",data=data)
        
      
    finally:
        curs.close()
    conn.close()
    return render_template("index.html",data=data)

@app.route("/index",methods=["POST","GET"])
def  index():
    return render_template("index.html")
 

@app.route('/user/<name>')
def user(name):
    return render_template("index2.html",data=data )
     
@app.route("/request_art_work",methods=["POST","GET"])
def request_art_work():
    return render_template("request_art_work.html")

@app.route("/art_work",methods=["POST","GET"])
def art_work():
    return render_template("art_work.html")

@app.route("/about_us",methods=["POST","GET"])
def about_us():
    return render_template("about_us.html")

@app.route("/facebook",methods=["POST","GET"])
def facebook():
    return render_template("facebook.html")

@app.route("/search",methods=["POST","GET"])
def search():
    val=request.form.get("search")
    return render_template("search.html",val=val)

@app.route("/searchdb",methods=["POST","GET"])
def searchdb():
    val=request.form.get("search")
    print(val)
    conn = snowflake.connector.connect(
                user = 'Epsilon',
                password = "notApainting01",
                account="bp14989.canada-central.azure",
                warehouse="COMPUTE_WH",
                role='SYSADMIN',
                database="ART",
                schema="ART_Table"
                )

    curs=conn.cursor()
    try:
        curs.execute("select * from ART_data where full_name='"+val+"'")
        data = curs.fetchall()
      
    finally:
        curs.close()
    conn.close()
    
    return render_template("searchdb.html",data=data,val=val)


@app.route("/redirect",methods=["POST","GET"])
def redirect():
    return render_template("index.html")

@app.route("/form",methods=["POST","GET"])
def form():
    title="Thanks You"
    full_name=request.form.get("full_name")
    address=request.form.get("address")
    email=request.form.get("email")
    phone_number=request.form.get("phone_number")
    descrption=request.form.get("descrption")
    image=request.files["myfile"]
    #with open (image,'rb') as im:
        #file=base64.b64encode(im.read())
       # file=pickle.load(im,encoding="bytes")
    image.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(image.filename)))
    if not full_name or not address or not email or not phone_number:
        error_statement="All filed required"
        return render_template("request_art_work.html",error_statement=error_statement,full_name=full_name,address=address,email=email,phone_number=phone_number,descrption=descrption)
    #es=emailsend()
    #msg=es.sent(full_name,address,email,descrption,phone_number)
    conn = snowflake.connector.connect(
                user = 'Epsilon',
                password = "notApainting01",
                account="bp14989.canada-central.azure",
                warehouse="COMPUTE_WH",
                role='SYSADMIN',
                database="ART",
                schema="ART_Table"
                )

    curs=conn.cursor()
    try:
        print("hello")
        curs.execute("insert into form_data (full_name,address,email,DESCRIPTION,phone_number) values (%s,%s,%s,%s,%s) ", (full_name,address,email,descrption,phone_number))
    finally:
        print("hello")
        curs.close()
    conn.close()
    flash("Thanks Confirmation will be recvied through mail")
    return render_template("Thanks.html",title=title)
  
@app.errorhandler(404)
# inbuilt function which takes error as parameter
def page_not_found(e):
    return render_template("404.html"),404

@app.errorhandler(500)
# inbuilt function which takes error as parameter
def page_not_found(e):
    return render_template("500.html"),500

app.run(debug=True)

     
 
