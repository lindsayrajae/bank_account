"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db
from models import Bank_Account
from models import Transaction
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "hello": "world"
    }

    return jsonify(response_body), 200


@app.route('/check_balance',methods=['POST'])
def account_vie():
    data = request.get_json()
    bank = Bank_Account(
        fullname = data["fullname"],
        account_num = data["account_num"],
        account_amount =data["account_amount"],
        password = data['password'],
        # account_email  data['account_email']
    )
    db.session.add(bank)
    db.session.commit()
    return jsonify(bank.serialize())

@app.route('/login',methods=['POST'])
def login():
    json = request.get_json()
    user = Bank_Account.query.filter_by(
        fullname=json['fullname'], password=json['password']).first()
    if user is None:
        return 'user not found' , 404

    return jsonify(user.serialize())


@app.route('/transactions',methods=['POST'])
def trans():
    data = request.get_json()

    db.session.add( Transaction(
        bank_transaction_id = data[ 'bank_transaction_id'],
        date=data['date'],
        state=data['state'],
        time=data['time'],
        city=data['city'],
        amount=data['amount'],

        # account_email  data['account_email']
    ))
    db.session.commit()
    return 'Transaction added successfully'


@app.route('/BankAccount',methods=['PUT'])
def bnk():
    json = request.get_json()
    user = Bank_Account.query.filter_by(
         fullname = 'rajaw lomwdnd ',
        # account_amount='$250', 
        password ='iamabigwag ').first()
    if user is None:
        return 'user not found' , 404
    
    user.account_num=json['new_account_num']
    db.session.commit()
    return jsonify(user.serialize())


@app.route('/bank_account')
def get_bank():

    return jsonify( Bank_Account.query.get(1).serialize() )

    

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
