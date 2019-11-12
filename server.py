from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL    # import the function that will return an instance of a connection
app = Flask(__name__)
app.secret_key = 'keep it safe'
email = " "
password = " "
id = 0
title = " "
description = " "
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/success', methods=['POST'])
def success():
    if len(request.form['fname']) < 3:
    	is_valid = False
        #flash("Your first name should be at least 3 characters")

    if len(request.form['lname']) < 3:
    	is_valid = False
        #flash("Your last name should be at least 3 characters")

    if len(request.form['psw']) < 5:
    	is_valid = False
        #flash("Your password should be at least 5 characters")

    if not is_valid:    # if any of the fields switched our is_valid toggle to False
        return redirect("/")

    fname_for_form = request.form['fname']
    lname_for_form = request.form['lname']
    email_for_form = request.form['email']
    mysql = connectToMySQL('login')
    query = "INSERT INTO user (first_name, last_name, email, password) VALUES (%(fn)s, %(ln)s, %(e)s), %(p)s);"
    data = {
    
        "fn": request.form['fname'],
        "ln": request.form['lname'],
        "e": request.form['email'],
        "p": request.form['psw']
        
    }
    new_user_id = mysql.query_db(query, data)
    mysql = connectToMySQL('login')
    login = mysql.query_db('SELECT * FROM user;')
    return render_template("show.html", fname_on_template=fname_for_form, lname_on_template=lname_for_form, email_on_template=email_for_form)

@app.route('/login_successful', methods=['POST'])
def successful_login():
    global email
    global password
    # see if the username provided exists in the database
    email_for_form = request.form['email']
    psw_for_form = request.form['psw']
    email = email_for_form
    password = psw_for_form
    mysql = connectToMySQL("login")
    query = "SELECT * FROM user WHERE email = %(e)s;"
    data = {
    
        "e": request.form['email'] 
        
    }
    result = mysql.query_db(query, data)
    if len(result) > 0:
        return render_template('showlogin.html', email_on_template=email_for_form)
    flash("You could not be logged in")
    return redirect("/login")
    
@app.route('/logout', methods=['POST'])
def logout():
    global email
    global password
    email = " "
    password = " "
    return render_template("logout.html")

@app.route('/register', methods=['POST'])
def register():
    return render_template("registration.html")

@app.route('/wall', methods=['POST'])
def wall():
    mysql = connectToMySQL('Books')	        # call the function, passing in the name of our db
    users = mysql.query_db('SELECT * FROM books;')  # call the query_db function, pass in the query as a string
    print(users)
    return render_template("wall.html", all_users = users)

@app.route('/book', methods=['POST'])
def book():
    mysql = connectToMySQL('Books')	        # call the function, passing in the name of our db
    query = "INSERT INTO books (id, title, description) VALUES (%(id)s, %(t)s, %(d)s);"
    data = {
    
        "id": request.form['id'],
        "t": request.form['title'],
        "d": request.form['desc']
        
    }
    new_user = mysql.query_db(query, data)
    return render_template("showlogin.html")

@app.route("/editbook", methods=["POST"])
def edit_book():
    title_to_form = request.form['title']
    mysql = connectToMySQL("Books")
    query = "SELECT * FROM books WHERE title = %(t)s;"
    data = {
    
        "t": request.form['title'] 
        
    }
    result = mysql.query_db(query, data)
    return render_template("edit.html", one_result=result, title_to_template=title_to_form)

@app.route("/edit", methods=["POST"])
def edit_user():
    mysql = connectToMySQL('Books')
    query = "UPDATE books SET (id, title, description) WHERE (%(id)s, %(t)s, %(d)s);"
    data = {
    
        "id": request.form['id'],
        "t": request.form['title'],
        "d": request.form['desc']
    }
    new_user = mysql.query_db(query, data)
    mysql = connectToMySQL('Books')
    users = mysql.query_db('SELECT * FROM books;')  # call the query_db function, pass in the query as a string
    print(users)
    return render_template("wall.html", all_users=users)

@app.route('/home', methods=['POST'])
def home():
    return redirect("/")

@app.route('/login', methods=['POST'])
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
