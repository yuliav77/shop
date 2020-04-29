import os
import requests

from flask import Flask, render_template, request, session, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["GET", "POST"])
def index():
	session["notes"] = []
	return render_template("index.html")
	
@app.route("/register")
def register():
	return render_template("register.html")

@app.route("/success", methods=["POST"])
def success():
	name = request.form.get("name") 
	login = request.form.get("login") 
	password = request.form.get("password") 
	password2 = request.form.get("password2") 
	db.execute("INSERT INTO users (name, login, password) VALUES (:name, :login, :password)",
		{"name": name, "login": login, "password": password})	
	db.commit()	
	return render_template("success.html", name=name, login=login, password=password, password2=password2)
		
@app.route("/search", methods=["POST"])
def search():
	login = request.form.get("login") 
	password = request.form.get("password") 
	user = db.execute("SELECT * FROM users WHERE login = :login", {"login": login}).fetchone() 
	if user is None:  
		return render_template("error.html", message="No such user with that login")
	if user.password ==	password:
		session["notes"].append(login)
		session["notes"].append(user.name)
		session["notes"].append(user.id)
		return render_template("search.html", user=user, notes=session["notes"])
	return render_template("error.html", message="Wrong password for that user")	
	
@app.route("/search_results", methods=["POST"])
def search_results():
	isbn = '%' + request.form.get("isbn") + '%'
	title = '%' + request.form.get("title") + '%'
	author = '%' + request.form.get("author") + '%'
	books = db.execute(
		"SELECT * FROM books WHERE isbn LIKE :isbn AND title LIKE :title AND author LIKE :author",
        {"isbn": isbn, "title":title, "author":author}
	).fetchall()
	if not books:
		return render_template("search.html", notes=session["notes"], message = 'No matches for the entered parameters: isbn="' + request.form.get("isbn") + '" title="' + request.form.get("title") + '" author="' + request.form.get("author") + '"')
	return render_template("search.html", books=books, notes=session["notes"])

@app.route("/search_results/<int:book_id>", methods=["GET"])
def book(book_id):
	book = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()
	book_isbn = book.isbn
	if book is None:
		return render_template("error.html", message="No such book.")
	res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "SzFjEJbZPNY72cozfLFajQ", "isbns": book_isbn})		
	if res.status_code != 200:
		raise Exception("ERROR: API request unsuccessful.")
	data = res.json()
	average_rating = data["books"][0]['average_rating']
	work_ratings_count = data["books"][0]['work_ratings_count']
	reviews = db.execute(
		"SELECT * FROM reviews,users WHERE book_id = :book_id AND user_id = users.id",
        {"book_id": book_id}
		).fetchall()
	return render_template("book.html",reviews=reviews, book=book, notes=session["notes"], average_rating=average_rating, work_ratings_count=work_ratings_count)	

@app.route("/search_results/<int:book_id>/add_review", methods=["POST"])
def add_review(book_id):
	notes = session["notes"]
	user_id = notes[2]
	review = db.execute("SELECT * FROM reviews WHERE user_id = :user_id AND book_id = :book_id", 
						{"user_id": user_id, "book_id": book_id}).fetchone()
	if review != None:
		return render_template("error.html", message="You have already written the review on this book")
	grade = int(request.form.get("grade")) 
	text = request.form.get("comment") 
	db.execute("INSERT INTO reviews (book_id, user_id, grade, text) VALUES (:book_id, :user_id, :grade, :text)",
				{"book_id": book_id, "user_id": user_id, "grade": grade, "text": text})	
	db.commit()	
	book = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()
	book_isbn = book.isbn
	res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "SzFjEJbZPNY72cozfLFajQ", "isbns": book_isbn})		
	if res.status_code != 200:
		raise Exception("ERROR: API request unsuccessful.")
	data = res.json()
	average_rating = data["books"][0]['average_rating']
	work_ratings_count = data["books"][0]['work_ratings_count']
	reviews = db.execute(
		"SELECT * FROM reviews,users WHERE book_id = :book_id AND user_id = users.id",
        {"book_id": book_id}
		).fetchall()
	return render_template("book.html",reviews=reviews, book=book, notes=notes, average_rating=average_rating, work_ratings_count=work_ratings_count)	


@app.route("/api/<book_isbn>")	
def book_api(book_isbn):
	book = db.execute("SELECT * FROM books WHERE isbn = :book_isbn", {"book_isbn": book_isbn}).fetchone()
	if book is None:
		return jsonify({"error": "Invalid book_isbn"}), 404
	res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "SzFjEJbZPNY72cozfLFajQ", "isbns": book_isbn})		
	if res.status_code != 200:
		raise Exception("ERROR: API request unsuccessful.")
	data = res.json()
	average_rating = data["books"][0]['average_rating']
	work_ratings_count = data["books"][0]['work_ratings_count']

	return jsonify({
		"title": book.title,
		"author": book.author,
		"year": book.year,
		"isbn": book.isbn,
		"review_count": work_ratings_count,
		"average_score": average_rating
	})
	
	
@app.route("/logout", methods=["POST"])
def logout():
	session["notes"] = []
	return render_template("index.html")