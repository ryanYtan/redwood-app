from flask import Flask, request, session, render_template
from flask_session import Session
from response import ResponseCode, Response
from models import db, User, Item, Transaction
from uuid import uuid4
from typing import *
import aws
import json
import bcrypt
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']           = os.getenv('REDWOOD_SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']    = os.getenv('REDWOOD_SQLALCHEMY_TRACK_MODIFICATIONS', "True").lower() in ('true', '1', 't')

app.config['SECRET_KEY']    = os.getenv('REDWOOD_SECRET_KEY', 'dev')
app.config['HOST']          = os.getenv('REDWOOD_HOST', '0.0.0.0')
app.config['PORT']          = os.getenv('REDWOOD_PORT', 8080)
app.config['DEBUG']         = os.getenv('REDWOOD_DEBUG', True)

#Devs will need to adapt their apps to use AWS credentials
#BEGIN
if os.getenv('REDWOOD_IS_DEV') is None:
    region_name = 'ap-southeast-1'

    #Setting up AWS connection

    db_endpoint_ssm_name = '/redwood/database/db_endpoint' #unfortunately this has to be hardcoded
    db_name_ssm_name = '/redwood/database/db_name' #unfortunately this has to be hardcoded
    parameters = aws.get_ssm_param([
        db_endpoint_ssm_name,
        db_name_ssm_name,
    ], region_name)
    db_endpoint = parameters[db_endpoint_ssm_name]
    db_name = parameters[db_name_ssm_name]

    db_credentials_secret_prefix = 'rds!db' #using manage_master_user_password for RDS instance
    db_login_credentials = aws.get_secret(db_credentials_secret_prefix, region_name)
    db_login_credentials = json.loads(db_login_credentials)
    db_username = db_login_credentials['username']
    db_password = db_login_credentials['password']

    uri = f'postgresql://{db_username}:{db_password}@{db_endpoint}/{db_name}'
    app.config['HOST'] = '0.0.0.0'
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
#END

db.init_app(app)

SESSION_KEY = 'redwood-sessionid'

app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY'] = db
app.config['SESSION_COOKIE_NAME'] = SESSION_KEY
app.config['SESSION_PERMANENT'] = True
app.secret_key = app.config['SECRET_KEY']
Session(app)

with app.app_context():
    db.create_all()


"""
Non-route functions
"""
def get_item_by_item_id(item_id: str) -> Optional[Item]:
    return db.session.get(Item, { 'item_id': item_id })

def get_unsold_items(page: int, page_count: int) -> List[Item]:
    unsold_items = db.session.query(Item)  \
        .filter(Item.item_id.not_in( db.session.query(Transaction.item_id) )) \
        .offset((page - 1) * page_count) \
        .limit(page_count) \
        .all()
    return unsold_items

def get_bought_items_for_user() -> List[Item]:
    if not is_user_logged_in():
        return []
    bought_items = db.session.query(Item) \
        .join(Transaction, Transaction.item_id == Item.item_id) \
        .filter(Transaction.buyer == session['username']) \
        .all()
    return bought_items

def is_user_logged_in() -> bool:
    return 'username' in session


"""
Front-end routes
"""
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def fe_index():
    is_logged_in = is_user_logged_in()
    return render_template("home.html", is_logged_in=is_logged_in), 200

@app.route('/signup', methods=['GET'])
def fe_signup():
    is_logged_in = is_user_logged_in()
    if is_logged_in:
        return render_template('home.html', is_logged_in=is_logged_in), 200
    return render_template('signup.html', is_logged_in=is_logged_in), 200

@app.route('/login', methods=['GET'])
def fe_login():
    is_logged_in = is_user_logged_in()
    if is_logged_in:
        return render_template('home.html', is_logged_in=is_logged_in), 200
    return render_template('login.html', is_logged_in=is_logged_in), 200

@app.route('/products', methods=['GET'])
def fe_products():
    is_logged_in = is_user_logged_in()
    unsold_items = get_unsold_items(1, 999) #front-end pagination not implemented
    return render_template('products.html', is_logged_in=is_logged_in, items=unsold_items), 200

@app.route('/products/sell', methods=['GET'])
def fe_products_sell():
    is_logged_in = is_user_logged_in()
    return render_template('products_sell.html', is_logged_in=is_logged_in), 200

@app.route('/orders', methods=['GET'])
def fe_orders():
    is_logged_in = is_user_logged_in()
    if is_logged_in:
        bought_items = get_bought_items_for_user()
        return render_template('orders.html', is_logged_in=is_logged_in, bought_items=bought_items), 200
    return render_template('home.html', is_logged_in=is_logged_in), 200

"""
REST API
Back-end routes
"""
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    if 'username' not in data or 'password' not in data:
        return Response(ResponseCode.ERR_BAD_REQUEST, f'Required fields missing').dict()

    username: str = data['username']
    password: str = data['password']
    pw_bytes = password.encode('utf-8')
    pw_salt = bcrypt.gensalt()
    pw_hash = bcrypt.hashpw(pw_bytes, pw_salt)

    if db.session.get(User, { 'username': username }) is not None:
        return Response(ResponseCode.ERR_USER_ALREADY_EXISTS, f'User {username} already exists').dict()

    user = User()
    user.username = username
    user.hashed_pw = pw_hash.hex()
    db.session.add(user)
    db.session.commit()

    session['username'] = username

    return Response(ResponseCode.SUCCESS).dict()


@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username: str = data['username']
    password: str = data['password']
    pw_bytes = password.encode('utf-8')

    data = db.session.get(User, { 'username': username })

    if data is None:
        return Response(ResponseCode.ERR_FAILED_LOGIN, f'User {username} does not exist').dict()

    pw_bytes_in_db = bytes.fromhex(data.hashed_pw)
    if not bcrypt.checkpw(pw_bytes, pw_bytes_in_db):
        return Response(ResponseCode.ERR_FAILED_LOGIN, f'Bad password for {username}').dict()

    session['username'] = username

    return Response(ResponseCode.SUCCESS).dict()


@app.route('/api/logout', methods=['POST'])
def logout():
    if not is_user_logged_in():
        return Response(ResponseCode.ERR_BAD_REQUEST, f'No user').dict()
    session.clear()
    return Response(ResponseCode.SUCCESS).dict()


@app.route('/api/products', methods=['GET', 'POST'])
def products():
    if request.method == 'GET':
        page_count = 25
        page = request.args.get('page', default=1, type=int)
        unsold_items = get_unsold_items(page, page_count)
        return Response(ResponseCode.SUCCESS, '', unsold_items).dict()
    else:
        username = session.get('username')
        if not username:
            return Response(ResponseCode.ERR_USER_UNLOGGED, f'Not logged in').dict()
        data = request.json
        item = Item()
        item.item_id = uuid4()
        item.seller = username
        item.name = data['name']
        item.description = data['description']
        item.imetadata = data['imetadata']
        item.price = data['price']

        try:
            _ = float(item.price)
        except ValueError:
            return Response(ResponseCode.ERR_BAD_REQUEST, f'Price {item.price} is not a valid number').dict()

        db.session.add(item)
        db.session.commit()
        return Response(ResponseCode.SUCCESS).dict()


@app.route('/api/products/<item_id>')
def get_product(item_id: str):
    item = get_item_by_item_id(item_id)
    if item is None:
        return Response(ResponseCode.ERR_NOT_FOUND, f'Item ID {item_id} does not exist')
    return Response(ResponseCode.SUCCESS, '', item).dict()


@app.route('/api/products/<item_id>/buy', methods=['POST'])
def buy_product(item_id: str):
    buyer = session.get('username')
    if not buyer:
        return Response(ResponseCode.ERR_USER_UNLOGGED, f'Not logged in').dict()
    item = db.session.get(Item, { 'item_id': item_id })
    if item is None:
        return Response(ResponseCode.ERR_NOT_FOUND, f'Item ID {item_id} does not exist').dict()
    if buyer == item.seller:
        return Response(ResponseCode.ERR_BAD_REQUEST, f'Seller and buyer have the same identity').dict()
    transaction = Transaction()
    transaction.buyer = buyer
    transaction.item_id = item_id
    db.session.add(transaction)
    db.session.commit()
    return Response(ResponseCode.SUCCESS).dict()


@app.route('/api/orders')
def orders_for_user():
    username = session.get('username')
    if not username:
        return Response(ResponseCode.ERR_USER_UNLOGGED, f'Not logged in').dict()
    bought_items = get_bought_items_for_user()
    return Response(ResponseCode.SUCCESS, '', bought_items).dict()


if __name__ == '__main__':
    if os.getenv('REDWOOD_IS_DEV') is None:
        #prod
        from waitress import serve
        serve(
            app,
            host=app.config['HOST'],
            port=app.config['PORT'],
        )
    else:
        app.run(
            host=app.config['HOST'],
            port=app.config['PORT'],
            debug=app.config['DEBUG'],
        )
