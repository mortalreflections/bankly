from . import db
from flask_login import UserMixin

class Users(UserMixin,db.Model):
	__tablename__="Users"
	# __table_args__ = {'extend_existing': True}
	id= db.Column(db.Integer, primary_key=True)
	Name=db.Column(db.String(50))
	Email= db.Column(db.String(100))
	Password= db.Column(db.String(50))
	admin=db.Column(db.Boolean)
	# FD = db.relationship("Deposits", backref="user")

class Deposits(UserMixin,db.Model):
	__tablename__ = "Deposits"
	# __table_args__ = {'extend_existing': True}
	id = db.Column(db.Integer,primary_key=True)
	Name = db.Column(db.String(50))
	Email = db.Column(db.String(100))
	DOB = db.Column(db.Date)
	Age = db.Column(db.Integer)
	BankName = db.Column(db.String(50))
	Amount = db.Column(db.Numeric(10, 2))
	Interest = db.Column(db.Numeric(10, 2))
	Maturity = db.Column(db.Numeric(10, 2))





# def init_db():
# 	db.create_all()
#
# if __name__=="__main__":
# 	init_db()





