from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    __tablename__='person'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Person %r>' % self.username

    def serialize(self):
        return {
            "username": self.username,
            "email": self.email
        }


class Bank_Account(db.Model):
    __tablename__='bank_account'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(180), unique=True, nullable=False)
    password = db.Column(db.String(200),unique = True,nullable=False)
    account_num = db.Column(db.String(120), unique=True, nullable=False)
    account_amount = db.Column(db.String(120), unique=True, nullable=False)
    # account_email = db.Column(db.String(120), unique=True, nullable=False)
    transaction = db.relationship('Transaction',back_populates='bank_account')

    def __repr__(self):
        return '<Bank_Account %r>' % self.fullname

        
    def serialize(self):
        return {
            "id":self.id,
            "fullname": self.fullname,
            "password": self.password,
            "account_amount":self.account_amount,
            "fullname": self.fullname,
            'transaction':[x.serialize()for x in self.transaction]
            # "account_email": self.account_email,

    }
class Transaction(db.Model):
    __tablename__='transaction'
    id = db.Column(db.Integer,primary_key=True)
    bank_transaction_id=db.Column(db.Integer,db.ForeignKey('bank_account.id'))
    date= db.Column(db.String(180))
    time= db.Column(db.String(180))
    amount= db.Column(db.String(180))
    item= db.Column(db.String(180))
    state=db.Column(db.String(180))
    city =db.Column(db.String(180))
    bank_account = db.relationship('Bank_Account',back_populates='transaction')

    def serialize(self):
        return {
        'date':self.date,
        'time':self.time,
        'amount':self.amount,
        'item':self.item,
        'state':self.state,
        'city':self.city
        
        }

