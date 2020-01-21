from flask import Flask, render_template, redirect, request, session, flash, url_for
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
import re

app = Flask(__name__)
app.secret_key = "jamesy"
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/register", methods = ['POST'])
def register():
    is_valid = True
    if len(request.form['fname']) < 1 or len(request.form['lname']) < 1 or len(request.form['email']) < 1 or len(request.form['pw']) < 1 or len(request.form['cpw']) < 1:
        is_valid = False
        flash("All fields required")
    if len(request.form['fname']) < 2:
        is_valid = False
        flash("First name must be at least 2 characters")
    if len(request.form['fname']) < 2:
        is_valid = False
        flash("Last name must be at least 2 characters")
    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Invalid email address")
    if len(request.form['pw']) < 8:
        is_valid = False
        flash("Password must be at least 8 characters")
    if request.form['pw'] != request.form['cpw']:
        is_valid = False
        flash("Passwords must match")
    if not is_valid:
        return redirect("/")
    else:
        mysql = connectToMySQL('thoughts_wall')
        query = "INSERT INTO users(first_name, last_name, email, password, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(em)s, %(pw)s, NOW(), NOW())"
        data = {
            'fn': request.form['fname'],
            'ln': request.form['lname'],
            'em': request.form['email'],
            'pw': request.form['pw']
        }
        results = mysql.query_db(query, data)
        flash("User Added Successfully")
        return redirect("/")

@app.route("/login", methods = ['POST'])
def login():
    is_valid = True
    if len(request.form['email']) < 1 or len(request.form['pw']) < 1:
        is_valid = False
        flash("Must enter an email address and password")
    if is_valid:
        mysql = connectToMySQL('thoughts_wall')
        query = "SELECT * FROM users WHERE email = %(em)s"
        data = {
            'em': request.form['email']
        }
        result = mysql.query_db(query, data)
        if result:
            user_data = result[0]
            if user_data['password'] == request.form['pw']:
                session['user_id'] = user_data['user_id']
                return redirect("/thoughts")
            else:
                is_valid = False
        else:
            is_valid = False
    if not is_valid:
        flash("Invalid email or password")
        return redirect("/")

@app.route("/thoughts")
def thoughts():
    if 'user_id' not in session:
        return redirect("/")
    mysql = connectToMySQL('thoughts_wall')
    query = "SELECT * FROM users WHERE user_id = %(id)s"
    data = {
        'id': session['user_id']
    }
    result = mysql.query_db(query, data)
    if result:
        user_data = result[0]
    
    mysql = connectToMySQL('thoughts_wall')
    query = "SELECT users.user_id, users.first_name, users.last_name, thoughts.thought_id, thoughts.content, thoughts.author, thoughts.created_at FROM thoughts JOIN users ON thoughts.author = users.user_id ORDER BY thoughts.created_at DESC"
    all_thoughts = mysql.query_db(query)

    mysql = connectToMySQL('thoughts_wall')
    query = "SELECT thought_like, COUNT(thought_like) AS like_count FROM likes GROUP BY thought_like"
    like_count = mysql.query_db(query)

    for thought in all_thoughts:
        for like in like_count:
            if like['thought_like'] == thought['thought_id']:
                thought['like_count'] = like['like_count']
        if 'like_count' not in thought:
                thought['like_count'] = 0
    return render_template("thoughts.html", user_data=user_data, all_thoughts=all_thoughts, like_count=like_count)

@app.route("/add", methods = ['POST'])
def add():
    is_valid = True
    if len(request.form['thought']) <5:
        is_valid = False
        flash("Thought must be at least 5 characters")
    if is_valid:
        mysql = connectToMySQL('thoughts_wall')
        query = "INSERT INTO thoughts (content, author, created_at, updated_at) VALUES (%(th)s, %(auth)s, NOW(), NOW())"
        data = {
            'th': request.form['thought'],
            'auth': session['user_id']
        }
        mysql.query_db(query, data)
        flash("Thought Added Successfully")
    return redirect(url_for('thoughts'))

@app.route("/delete/<thought_id>")
def delete(thought_id):
    query = "DELETE FROM thoughts WHERE thought_id = %(th)s"
    data = {
        'th': thought_id
    }
    mysql = connectToMySQL('thoughts_wall')
    delete_thought = mysql.query_db(query, data)
    return redirect("/thoughts")

@app.route("/details/<thought_id>")
def details(thought_id):
    if 'user_id' not in session:
        return redirect("/")
    mysql = connectToMySQL('thoughts_wall')
    query = "SELECT * FROM users WHERE user_id = %(id)s"
    data = {
        'id': session['user_id']
    }
    result = mysql.query_db(query, data)
    if result:
        user_data = result[0]

    mysql = connectToMySQL('thoughts_wall')
    query = "SELECT users.user_id, users.first_name, users.last_name, thoughts.thought_id, thoughts.content, thoughts.author, thoughts.created_at FROM thoughts JOIN users ON thoughts.author = users.user_id WHERE thought_id = %(th)s"
    data = {
        'th': thought_id
    }
    detail_thought = mysql.query_db(query, data)
    
    mysql = connectToMySQL('thoughts_wall')
    query = "SELECT thought_like, user_like FROM likes WHERE user_like = %(user_id)s"
    data = {
        'user_id': session['user_id']
    }
    liked_thoughts = [thought['thought_like'] for thought in mysql.query_db(query, data)]

    mysql = connectToMySQL('thoughts_wall')
    query = "SELECT likes.thought_like, likes.user_like, users.first_name, users.last_name FROM likes JOIN users ON likes.user_like = users.user_id WHERE thought_like = %(th)s"
    data = {
        'th': thought_id
    }
    like_list = mysql.query_db(query, data)

    return render_template("details.html", user_data=user_data, detail_thought = detail_thought[0], liked_thoughts=liked_thoughts, like_list=like_list)

@app.route("/details/like/<thought_id>")
def like(thought_id):
    mysql = connectToMySQL('thoughts_wall')
    query = "INSERT INTO likes (user_like, thought_like) VALUE (%(user_id)s, %(thought_id)s)"
    data = {
        'user_id': session['user_id'],
        'thought_id': thought_id
    }
    mysql.query_db(query, data)
    return redirect(url_for('details', thought_id=thought_id))


@app.route("/details/unlike/<thought_id>")
def unlike(thought_id):
    mysql = connectToMySQL('thoughts_wall')
    query = "DELETE FROM likes WHERE user_like = %(user_id)s AND thought_like = %(thought_id)s"
    data = {
        'user_id': session['user_id'],
        'thought_id': thought_id
    }
    mysql.query_db(query, data)
    return redirect(url_for('details', thought_id=thought_id))

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)