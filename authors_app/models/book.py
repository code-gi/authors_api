# from authors_app import db
from datetime import datetime
from authors_app.extensions import db


class Books(db.Model):
 __tablename__="books"
 id =db.Column(db.Integer,primary_key=True)
 title=db.Column(db.String(50),nullable=False)
 description=db.Column(db.String(100),nullable=False)
 image=db.Column(db.String(255),nullable=False)
 price=db.Column(db.Integer,nullable=False)
 #price_unit=db.Column(db.Integer,nullable=False)
 number_of_pages=db.Column(db.Integer,nullable=False) 
 #genre=db.Column(db.String,nullable=False)
#  created_at=db.Column(db.DateTime,default=datetime.now())
#  updated_at=db.Column(db.DateTime,onupdate=datetime.now())
 user_id =db.Column(db.Integer, db.ForeignKey("users.id"))
 #user=db.relationship('User',backref='books')
