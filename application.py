import os
import requests
import xml.etree.ElementTree as ET


from flask import Flask, session, jsonify, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

#   Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = os.enviorn.get('SECRET_KEY')
Session(app)

# Set up database
DB_ENGINE = os.enviorn.get('DATABASE_URL')
GR_APIKEY = os.enviorn.get('GR_KEY')

engine =create_engine(DB_ENGINE)
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    if 'username' in session:
        if session['username']:
            return redirect(url_for('search'))
    else :
        return redirect(url_for('account'))
    

@app.route("/account")
def account():
    if 'username' in session:
        if session['username']:
            return redirect(url_for('search')) 
    else :
        return render_template("login.html")

@app.route("/search")
def search():
    if 'username' in session:
        if session['username']:
            return render_template("index.html") 
    else :
        return redirect(url_for('account'))

@app.route("/api/<string:isbn>/")
def api(isbn):
    books=db.execute("SELECT * FROM book_info WHERE isbn=:isbn", {"isbn":isbn}).fetchone()
    if not books:
        return "<h2>404 error</h2>" ;
    rev_cnt=db.execute("SELECT COUNT(book_id) FROM reviews WHERE book_id=:book_id;", {"book_id":books.id}).fetchone()[0]
    if rev_cnt:
        return jsonify({
        "title": books.title,
        "author": books.author,
        "year": books.year,
        "isbn": isbn,
        "review_count": rev_cnt
        });
    else:
        return "<h2>404 error</h2>" ;
    
    
@app.route("/results", methods=["POST"])
def result():
    if 'username' in session:
        if session['username'] or request.method == "POST":
            attr=request.form.get("book_name")
            attr=attr.lower()
            books=db.execute("SELECT * FROM book_info WHERE LOWER(isbn) LIKE :book_info OR LOWER(title) LIKE  :book_info OR LOWER(author) LIKE :book_info", {"book_info":'%'+attr+'%'}).fetchall()
            if books:
                rootlist = []
                booktit_list = []
                for book in books :
                    res = requests.get("https://www.goodreads.com/search/index.xml",params={"key": "GR_APIKEY", "q": book.isbn})
                    booktit_list.append(book.title)
                    root = ET.fromstring(res.text)
                    rootlist.append(root)
                return render_template("results.html", rootlist=rootlist , booktit_list=booktit_list, len=len(booktit_list))
            else:
                return render_template("index.html",msg="Book Not Found") 
    else :
        return redirect(url_for('account'))
        

        
@app.route("/book/<string:title>/",methods=["POST","GET"])
def book(title):
    if 'username' in session:
        if session['username']:    
            isbnrow = db.execute("SELECT *FROM book_info WHERE title=:title", {"title":title}).fetchone()
            res = requests.get("https://www.goodreads.com/search/index.xml",params={"key": "GR_APIKEY", "q":isbnrow.isbn})
            root = ET.fromstring(res.text)
            rev_res = requests.get("https://www.goodreads.com/book/isbn/"+isbnrow.isbn+".xml",params={"key": "GR_APIKEY"})
            rev_root = ET.fromstring(rev_res.text)
            
            rev_row=db.execute("SELECT * FROM reviews WHERE user_id=:user_id AND book_id=:book_id",{"user_id":session['user_id'],"book_id":isbnrow.id}).fetchone()
              
            
            if not rev_row and request.method == "POST":
                review=request.form.get("review")
                rating=request.form.get("rating")
                db.execute("INSERT INTO reviews (review, user_id, book_id, rating) VALUES (:review, :user_id, :book_id, :rating)",{"review":review , "user_id":session['user_id'] , "book_id":isbnrow.id, "rating":rating})
                db.commit()
            
            rev_row=db.execute("SELECT * FROM reviews WHERE user_id=:user_id AND book_id=:book_id",{"user_id":session['user_id'],"book_id":isbnrow.id}).fetchone()
            rev_all=db.execute("SELECT users.name,reviews.book_id,reviews.review,reviews.rating FROM users INNER JOIN reviews ON users.id=reviews.user_id WHERE book_id=:book_id",{"book_id":isbnrow.id}).fetchall()
            
            return render_template("book.html",data=root,rev_data=rev_root,title=title,isbn=isbnrow.isbn,rev_row=rev_row,rev_all=rev_all,user_name=session['username'])
    else :
        return redirect(url_for('account'))
            
        
@app.route("/signin",methods=["POST"])
def signin():
    email=request.form.get("email")
    password=request.form.get("pass")
    user=db.execute("SELECT * FROM users WHERE email=:mail",{"mail":email}).fetchone()
    
    if user:
        if password==user.password:
            session['username'] = user.name
            session['user_id'] = user.id
            return redirect(url_for('index'))  
        else:
            return render_template("login.html",msg="Incorrect Email or Password")
    else :
        return render_template("login.html",msg="Incorrect Email or Password")
        
@app.route("/signup",methods=["POST"])
def signup():
    uname=request.form.get("name")
    ugender=request.form.get("gender")
    uemail=request.form.get("email")
    upassword=request.form.get("pass")
    udob=request.form.get("dob")
    
    if not uname or not ugender or not uemail or not upassword or not udob:
        return render_template("login.html",cmsg="Fill all credentials")
    
    
    db.execute("INSERT INTO users (name, password, gender, email,dob) VALUES (:name, :password, :gender, :email,:dob)",{"name":uname,"password":upassword,"gender":ugender,"email":uemail,"dob":udob})
    db.commit()
    user=db.execute("SELECT * FROM users WHERE email=:mail",{"mail":uemail}).fetchone()
    session['username'] = uname
    session['user_id'] = user.id
    return redirect(url_for('index'))

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__=='__main__':
    app.run()