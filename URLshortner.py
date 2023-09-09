
from flask import render_template, Flask, request, jsonify, redirect, url_for
import webbrowser
import mysql.connector
import random
import string
import webbrowser, signal, time, os, threading, sys

mydb = mysql.connector.connect(host= "localhost",
                                user= "root",
                                password = "Password")
mycursor= mydb.cursor()
mycursor.execute("USE urlshortner;")
app = Flask(__name__)


def generate_random_string(length = 15):
        exist = True
        while exist:
            alphabet = string.ascii_letters
            val = ''.join(random.choice(alphabet) for i in range(length))
            mycursor.execute("SELECT ShortURL FROM url WHERE ShortURL = %s;", [val])
            data = mycursor.fetchone()
            if data:
                pass
            else:
                exist = False
                return val

@app.route('/', methods=['GET', 'POST'])
def Home():
    if request.method == 'POST':
        
        url = request.form['link']
        custom = request.form['custom']
        if not custom:
            custom = generate_random_string()
        if custom:
            try:
                custom = custom.replace(' ', '_')
                mycursor.execute("INSERT INTO url VALUES(%s, %s);", [custom, url])
                mydb.commit()
                return f"""<h1 align='center'><br><br><br><br>Link:  localhost:8005/{custom}</h1><br><br><br><br>
            <h3 align='center'><a href='/'>Home</a></hr>"""
            except Exception as e:
                return "Value exist.."


    mycursor.execute("SELECT * FROM url;")
    urls = mycursor.fetchall()
    code=''
    for url in urls:
        code += f"""<h3 style="font-weight:normal;">/{url[0]}</h3><p>
                        <!-style='display:flex; justify-content:space-between;'->
                        <div style='display:flex; justify-content:left;'>
                        <form method='GET' action='/add/{url[0]}'>
                            <button id="showInputBtn" action="/add/{url[0]}" method="GET" style="background-color:grey"> Edit </button>
                        </form>
                            <span style ='width:20px'></span>
                            <form method='POST' action='/del'>
                            <button id="delBtn" name='delete' value='{url[0]}' style="background-color:red">Delete</button>
                            </form>
                        </div><hr><br>"""    


    return render_template("Homepage.html", data=code)

@app.route('/add', methods=['GET', 'POST'])
def add():
  #can add editing here..
    return render_template("form.htm", link = '/')

@app.route('/add/<shortURL>', methods=['GET', 'POST'])
def edit(shortURL):
  
    if request.method == 'POST':
        url = request.form['link']
        custom = request.form['custom']

        if not custom:
            custom = generate_random_string()
        if custom:
            try:
                custom = custom.replace(' ', '_')
                mycursor.execute("DELETE FROM url WHERE ShortURL = %s;", [shortURL])
                mydb.commit()
                mycursor.execute("INSERT INTO url VALUES(%s, %s);", [custom, url])
                mydb.commit()
                

                return redirect(url_for('Home'))
            except Exception as e:
                return "Value exist.."


    mycursor.execute("SELECT * FROM url WHERE ShortURL = %s", [shortURL])
    data = mycursor.fetchone()
        
    if data:

        return render_template("form.htm", short=data[0], long=data[1], link=f'/add/{data[0]}')
    else:
        last_request_time = time.time()
        return "<H2 align='center'>404: NO LINK FOUND.</H2><br><br><br><br><h3 align='center'><a href='/'>Home</a></hr>"


@app.route('/<link>')
def link(link):
  #Receives the request to open the short links.
    mycursor.execute("SELECT * FROM url WHERE ShortURL = %s;", [link])
    rows= mycursor.fetchone()

    if rows is not None and len(rows) > 1:
        return render_template("redirect.html", external_link = rows[1])
    else:
        return "<h1 align='center'>Link do not exist</h1><br><br><br><br><h3 align='center'><a href='/'>Home</a></hr>"
    

@app.route('/del', methods=['POST', 'GET'])
def delete():
  #To delete certain short links from home page.
    if request.method == 'POST':
        btn_value = request.form.get('delete')
        mycursor.execute("DELETE FROM url WHERE ShortURL = %s;", [btn_value])
        mydb.commit()

    return redirect(url_for('Home'))
    


if __name__=="__main__":
    app.run(port=8005, debug=True)
