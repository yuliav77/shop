from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
	__tablename__ = "books"
	id = db.Column(db.Integer, primary_key=True)
	isbn = db.Column(db.String, nullable=False, unique=True)
	title = db.Column(db.String, nullable=False)
	author = db.Column(db.String, nullable=False)
	year = db.Column(db.String, nullable=False)

class User(db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True)
	login = db.Column(db.String, nullable=False, unique=True)
	password = db.Column(db.String, nullable=False)
	name = db.Column(db.String, nullable=False)
	  
class Review(db.Model):
	__tablename__ = "reviews"
	id = db.Column(db.Integer, primary_key=True)
	book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
	grade = db.Column(db.Integer, nullable=False)
	text = db.Column(db.String, nullable=False)