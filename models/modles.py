
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(50),nullable=False)
    auther = db.Column(db.String(10),nullable=False,default="zq")

